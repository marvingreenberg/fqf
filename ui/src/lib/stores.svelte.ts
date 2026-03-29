import type { ActSummary, SharedSchedule, ViewMode, MobileSortMode, ShareRef } from '$lib/types';
import { FESTIVAL_DATES, IDENTITY_STORAGE_KEY } from '$lib/types';

const SAVE_DEBOUNCE_MS = 1000;

interface StoredIdentity {
    token: string;
    name: string;
}

class AppState {
    selectedDate = $state<string>(FESTIVAL_DATES[0]);
    viewMode = $state<ViewMode>('grid');
    mobileSortMode = $state<MobileSortMode>('by-time');
    token = $state<string | null>(null);
    name = $state<string>('');
    confirmed = $state<boolean>(false);
    picks = $state<Set<string>>(new Set());
    acts = $state<ActSummary[]>([]);
    loading = $state<boolean>(false);
    sharedSchedules = $state<SharedSchedule[]>([]);

    // Query params set on page load when a ?share= link is opened
    pendingShareId = $state<string | null>(null);
    pendingShareName = $state<string | null>(null);

    // Filter state
    hiddenGenres = $state<Set<string>>(new Set());
    hiddenStages = $state<Set<string>>(new Set());
    showAll = $state<boolean>(false);

    private _saveTimeout: ReturnType<typeof setTimeout> | null = null;

    get picksArray(): string[] {
        return [...this.picks];
    }

    loadFromStorage(): void {
        if (typeof localStorage === 'undefined') return;
        const raw = localStorage.getItem(IDENTITY_STORAGE_KEY);
        if (!raw) return;
        try {
            const stored = JSON.parse(raw) as StoredIdentity;
            this.token = stored.token ?? null;
            this.name = stored.name ?? '';
        } catch {
            // Corrupt storage — ignore and start fresh
        }
    }

    saveToStorage(): void {
        if (typeof localStorage === 'undefined') return;
        if (!this.token) return;
        const stored: StoredIdentity = { token: this.token, name: this.name };
        localStorage.setItem(IDENTITY_STORAGE_KEY, JSON.stringify(stored));
    }

    async confirm(token: string, name?: string): Promise<void> {
        const { loadSchedule, loadSharedSchedule } = await import('$lib/api');
        const resp = await loadSchedule(token);
        this.token = resp.token;
        this.name = name ?? resp.name ?? '';
        this.picks = new Set(resp.picks);
        this.confirmed = true;
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
        }
        this.token = null;
        this.name = '';
        this.confirmed = false;
        this.picks = new Set();
        this.sharedSchedules = [];
    }

    togglePick(slug: string): void {
        const next = new Set(this.picks);
        if (next.has(slug)) {
            next.delete(slug);
        } else {
            next.add(slug);
        }
        this.picks = next;
        this.scheduleSave();
    }

    isPicked(slug: string): boolean {
        return this.picks.has(slug);
    }

    clearPicks(): void {
        this.picks = new Set();
    }

    scheduleSave(): void {
        if (!this.token) return;
        if (this._saveTimeout) clearTimeout(this._saveTimeout);
        this._saveTimeout = setTimeout(async () => {
            if (this.token) {
                const { savePicks } = await import('$lib/api');
                await savePicks(this.token, this.picksArray, this.name || undefined);
            }
        }, SAVE_DEBOUNCE_MS);
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

    isActVisible(act: { genre: string; stage: string }): boolean {
        if (this.showAll) return true;
        if (this.hiddenGenres.has(act.genre)) return false;
        if (this.hiddenStages.has(act.stage)) return false;
        return true;
    }
}

export const appState = new AppState();
