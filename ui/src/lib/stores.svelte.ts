import type { ActSummary, ViewMode, MobileSortMode } from '$lib/types';
import { FESTIVAL_DATES } from '$lib/types';

const SAVE_DEBOUNCE_MS = 1000;

class AppState {
    selectedDate = $state<string>(FESTIVAL_DATES[0]);
    viewMode = $state<ViewMode>('grid');
    mobileSortMode = $state<MobileSortMode>('by-time');
    token = $state<string | null>(null);
    picks = $state<Set<string>>(new Set());
    acts = $state<ActSummary[]>([]);
    loading = $state<boolean>(false);

    // Filter state (stub for Task 15)
    hiddenGenres = $state<Set<string>>(new Set());
    hiddenStages = $state<Set<string>>(new Set());
    showAll = $state<boolean>(false);

    private _saveTimeout: ReturnType<typeof setTimeout> | null = null;

    get picksArray(): string[] {
        return [...this.picks];
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
                await savePicks(this.token, this.picksArray);
            }
        }, SAVE_DEBOUNCE_MS);
    }

    // Filter methods (stub for Task 15)
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
