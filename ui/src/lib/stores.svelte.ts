import type { ActSummary, SharedSchedule, ViewMode, MobileSortMode, ShareRef } from '$lib/types';
import {
    FESTIVAL_DATES,
    FINGERPRINT_COUNTER_KEY,
    IDENTITY_STORAGE_KEY,
    PICKS_STORAGE_KEY,
    ACTS_STORAGE_PREFIX,
    STAGES_STORAGE_KEY,
    ACTS_CACHE_TTL_MS
} from '$lib/types';
import { GRID_START_HOUR, MINUTES_PER_HOUR } from '$lib/constants';
import {
    MAYBE_PREFIX,
    isPicked as _isPicked,
    isMaybe as _isMaybe,
    isSelected as _isSelected,
    togglePick as _togglePick,
    toggleMaybe as _toggleMaybe
} from '$lib/picks';

export type MapMode = 'scroll' | 'now' | 'my-schedule';
const DEFAULT_MAP_MINUTES = GRID_START_HOUR * MINUTES_PER_HOUR;

const SAVE_AFTER_CHANGES = 4;
const SAVE_DEBOUNCE_MS = 5_000;
const SAVED_FLASH_MS = 2_000;

interface StoredIdentity {
    token: string;
    name: string;
    counter: number;
}

class AppState {
    selectedDate = $state<string>(FESTIVAL_DATES[0]);
    viewMode = $state<ViewMode>('all-acts');
    mobileSortMode = $state<MobileSortMode>('by-time');
    token = $state<string | null>(null);
    name = $state<string>('');
    counter = $state<number>(0);
    ownShareId = $state<string>('');
    confirmed = $state<boolean>(false);
    picks = $state<Set<string>>(new Set());
    acts = $state<ActSummary[]>([]);
    loading = $state<boolean>(false);
    sharedSchedules = $state<SharedSchedule[]>([]);

    // Query params set on page load when a ?share= link is opened
    pendingShareId = $state<string | null>(null);
    pendingShareName = $state<string | null>(null);

    // Map view state (persists across tab switches, resets on page reload)
    mapMode = $state<MapMode>('scroll');
    mapManualMinutes = $state<number>(DEFAULT_MAP_MINUTES);
    mapShowPaths = $state<boolean>(false);

    // Filter state
    hiddenGenres = $state<Set<string>>(new Set());
    hiddenStages = $state<Set<string>>(new Set());
    showAll = $state<boolean>(false);
    showSelected = $state<boolean>(false);

    // Network / save status
    isOnline = $state<boolean>(true);
    saveError = $state<boolean>(false);
    savedFlash = $state<boolean>(false);

    private _saveTimeout: ReturnType<typeof setTimeout> | null = null;
    private _unsavedChanges = 0;
    private _savedFlashTimeout: ReturnType<typeof setTimeout> | null = null;

    get picksArray(): string[] {
        return [...this.picks];
    }

    /** Set of slugs in the maybe state (without the `?` prefix). */
    get maybes(): Set<string> {
        const result = new Set<string>();
        for (const entry of this.picks) {
            if (entry.startsWith(MAYBE_PREFIX)) result.add(entry.slice(MAYBE_PREFIX.length));
        }
        return result;
    }

    loadFromStorage(): void {
        if (typeof localStorage === 'undefined') return;
        const raw = localStorage.getItem(IDENTITY_STORAGE_KEY);
        if (raw) {
            try {
                const stored = JSON.parse(raw) as StoredIdentity;
                this.token = stored.token ?? null;
                this.name = stored.name ?? '';
                this.counter = stored.counter ?? 0;
            } catch {
                // Corrupt storage — ignore and start fresh
            }
        }
        // Counter persists independently across identity clears
        const rawCounter = localStorage.getItem(FINGERPRINT_COUNTER_KEY);
        if (rawCounter !== null) {
            const parsed = parseInt(rawCounter, 10);
            if (!isNaN(parsed)) this.counter = parsed;
        }
        // Hydrate picks from local cache (will be overwritten by API on confirm)
        const rawPicks = localStorage.getItem(PICKS_STORAGE_KEY);
        if (rawPicks) {
            try {
                const pickArr = JSON.parse(rawPicks) as string[];
                if (Array.isArray(pickArr)) this.picks = new Set(pickArr);
            } catch {
                // Corrupt — ignore
            }
        }
    }

    /** Read cached acts for a date from localStorage, or null if absent/stale. */
    loadCachedActs(date: string): ActSummary[] | null {
        if (typeof localStorage === 'undefined') return null;
        const raw = localStorage.getItem(`${ACTS_STORAGE_PREFIX}${date}`);
        if (!raw) return null;
        try {
            const entry = JSON.parse(raw) as { acts: ActSummary[]; cachedAt: number };
            if (Date.now() - entry.cachedAt > ACTS_CACHE_TTL_MS) return null;
            return entry.acts;
        } catch {
            return null;
        }
    }

    /** Write acts for a date to localStorage. */
    cacheActs(date: string, acts: ActSummary[]): void {
        if (typeof localStorage === 'undefined') return;
        try {
            localStorage.setItem(
                `${ACTS_STORAGE_PREFIX}${date}`,
                JSON.stringify({ acts, cachedAt: Date.now() })
            );
        } catch {
            // localStorage quota exceeded — ignore gracefully
        }
    }

    /** Read cached stage locations from localStorage, or null if absent. */
    loadCachedStages(): { lat: number; lng: number; name: string }[] | null {
        if (typeof localStorage === 'undefined') return null;
        const raw = localStorage.getItem(STAGES_STORAGE_KEY);
        if (!raw) return null;
        try {
            return JSON.parse(raw) as { lat: number; lng: number; name: string }[];
        } catch {
            return null;
        }
    }

    /** Write stage locations to localStorage. */
    cacheStages(stages: { lat: number; lng: number; name: string }[]): void {
        if (typeof localStorage === 'undefined') return;
        try {
            localStorage.setItem(STAGES_STORAGE_KEY, JSON.stringify(stages));
        } catch {
            // Ignore quota errors
        }
    }

    saveToStorage(): void {
        if (typeof localStorage === 'undefined') return;
        if (!this.token) return;
        const stored: StoredIdentity = {
            token: this.token,
            name: this.name,
            counter: this.counter
        };
        localStorage.setItem(IDENTITY_STORAGE_KEY, JSON.stringify(stored));
        localStorage.setItem(FINGERPRINT_COUNTER_KEY, String(this.counter));
    }

    async confirm(token: string, name?: string, counter?: number): Promise<void> {
        const { loadSchedule, loadSharedSchedule } = await import('$lib/api');
        let resp: Awaited<ReturnType<typeof loadSchedule>>;
        try {
            resp = await loadSchedule(token);
        } catch {
            // API unreachable — confirm from locally cached picks so the app is
            // still usable offline. Identity fields stay as loaded from storage.
            this.confirmed = true;
            if (counter !== undefined) this.counter = counter;
            // picks already hydrated by loadFromStorage() — nothing more to do
            return;
        }
        this.token = resp.token;
        this.name = name ?? resp.name ?? '';
        this.ownShareId = resp.share_id ?? '';
        this.picks = new Set(resp.picks);
        // Keep localStorage in sync with the authoritative server copy
        this._cachePicksLocally();
        this.confirmed = true;
        if (counter !== undefined) this.counter = counter;
        this.saveToStorage();

        // Restore persisted shared schedules from the API response
        if (resp.shares && resp.shares.length > 0) {
            const loaded = await Promise.allSettled(
                resp.shares.map(async (ref: ShareRef) => {
                    const shared = await loadSharedSchedule(ref.share_id);
                    return {
                        share_id: ref.share_id,
                        name: ref.name || shared.name,
                        picks: shared.picks,
                        acts: shared.acts
                    };
                })
            );
            this.sharedSchedules = loaded
                .filter(
                    (r): r is PromiseFulfilledResult<SharedSchedule> => r.status === 'fulfilled'
                )
                .map((r) => r.value);
        }
    }

    clearIdentity(): void {
        if (typeof localStorage !== 'undefined') {
            localStorage.removeItem(IDENTITY_STORAGE_KEY);
            // FINGERPRINT_COUNTER_KEY intentionally retained across clears
        }
        this.token = null;
        this.name = '';
        this.confirmed = false;
        this.picks = new Set();
        this.sharedSchedules = [];
    }

    togglePick(slug: string): void {
        this.picks = _togglePick(slug, this.picks);
        this.scheduleSave();
    }

    toggleMaybe(slug: string): void {
        this.picks = _toggleMaybe(slug, this.picks);
        this.scheduleSave();
    }

    isPicked(slug: string): boolean {
        return _isPicked(slug, this.picks);
    }

    isMaybe(slug: string): boolean {
        return _isMaybe(slug, this.picks);
    }

    isSelected(slug: string): boolean {
        return _isSelected(slug, this.picks);
    }

    clearPicks(): void {
        this.picks = new Set();
    }

    /** Write picks to localStorage so they survive a page reload without network. */
    private _cachePicksLocally(): void {
        if (typeof localStorage === 'undefined') return;
        localStorage.setItem(PICKS_STORAGE_KEY, JSON.stringify(this.picksArray));
    }

    private _showSavedFlash(): void {
        this.savedFlash = true;
        if (this._savedFlashTimeout) clearTimeout(this._savedFlashTimeout);
        this._savedFlashTimeout = setTimeout(() => {
            this.savedFlash = false;
        }, SAVED_FLASH_MS);
    }

    private async _flushSave(): Promise<void> {
        if (this._saveTimeout) clearTimeout(this._saveTimeout);
        this._saveTimeout = null;

        // Always write to localStorage immediately — even if the API call fails,
        // the local copy is up to date.
        this._cachePicksLocally();

        if (!this.token) return;

        try {
            const { savePicks } = await import('$lib/api');
            await savePicks(this.token, this.picksArray, this.name || undefined);
            this._unsavedChanges = 0;
            const hadError = this.saveError;
            this.saveError = false;
            if (hadError) this._showSavedFlash();
        } catch {
            // Network or server failure — keep _unsavedChanges so a retry fires
            // when the network watcher calls flushSaveIfPending().
            this.saveError = true;
        }
    }

    /**
     * Called by the network watcher when connectivity is restored.
     * Retries a pending/failed save if one is outstanding.
     */
    flushSaveIfPending(): void {
        if (this._unsavedChanges > 0 || this.saveError) {
            this._flushSave();
        }
    }

    scheduleSave(): void {
        if (!this.token) return;
        this._unsavedChanges++;
        if (this._unsavedChanges >= SAVE_AFTER_CHANGES) {
            this._flushSave();
            return;
        }
        if (this._saveTimeout) clearTimeout(this._saveTimeout);
        this._saveTimeout = setTimeout(() => this._flushSave(), SAVE_DEBOUNCE_MS);
    }

    setViewMode(mode: ViewMode): void {
        if (this._unsavedChanges > 0) {
            this._flushSave();
        }
        this.viewMode = mode;
    }

    async addSharedSchedule(schedule: SharedSchedule): Promise<void> {
        const exists = this.sharedSchedules.some((s) => s.share_id === schedule.share_id);
        if (!exists) {
            this.sharedSchedules = [...this.sharedSchedules, schedule];
        }
        if (this.token) {
            const { addShareToSchedule } = await import('$lib/api');
            await addShareToSchedule(this.token, {
                share_id: schedule.share_id,
                name: schedule.name
            });
        }
    }

    async removeSharedSchedule(shareId: string): Promise<void> {
        this.sharedSchedules = this.sharedSchedules.filter((s) => s.share_id !== shareId);
        if (this.token) {
            const { removeShareFromSchedule } = await import('$lib/api');
            await removeShareFromSchedule(this.token, shareId);
        }
    }

    toggleGenre(genre: string): void {
        const next = new Set(this.hiddenGenres);
        if (next.has(genre)) next.delete(genre);
        else next.add(genre);
        this.hiddenGenres = next;
    }

    toggleStage(stage: string): void {
        const next = new Set(this.hiddenStages);
        if (next.has(stage)) next.delete(stage);
        else next.add(stage);
        this.hiddenStages = next;
    }

    isActVisible(act: { genre: string; stage: string; slug: string }): boolean {
        if (this.showAll) return true;
        const hiddenByFilter = this.hiddenGenres.has(act.genre) || this.hiddenStages.has(act.stage);
        if (hiddenByFilter) return (this.showSelected && this.isSelected(act.slug));
        return true;
    }
}

export const appState = new AppState();
