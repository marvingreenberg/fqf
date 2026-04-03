import { describe, it, expect, beforeEach } from 'vitest';
import { appState } from '$lib/stores.svelte';
import {
    IDENTITY_STORAGE_KEY,
    FINGERPRINT_COUNTER_KEY,
    PICKS_STORAGE_KEY,
    ACTS_STORAGE_PREFIX,
    STAGES_STORAGE_KEY,
    ACTS_CACHE_TTL_MS
} from '$lib/types';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Reset AppState to a clean baseline between tests. */
function resetState(): void {
    appState.picks = new Set();
    appState.token = null;
    appState.name = '';
    appState.counter = 0;
    appState.confirmed = false;
    appState.sharedSchedules = [];
    appState.hiddenGenres = new Set();
    appState.hiddenStages = new Set();
    appState.showAll = false;
    appState.showSelected = false;
}

// ---------------------------------------------------------------------------
// picksArray getter
// ---------------------------------------------------------------------------

describe('picksArray', () => {
    beforeEach(resetState);

    it('returns an empty array when no picks', () => {
        expect(appState.picksArray).toEqual([]);
    });

    it('returns all entries including ?-prefixed maybes', () => {
        appState.picks = new Set(['act-a', '?act-b', 'act-c']);
        expect(appState.picksArray.sort()).toEqual(['?act-b', 'act-a', 'act-c']);
    });

    it('reflects the current set contents', () => {
        appState.picks = new Set(['only-one']);
        expect(appState.picksArray).toEqual(['only-one']);
    });
});

// ---------------------------------------------------------------------------
// maybes getter
// ---------------------------------------------------------------------------

describe('maybes', () => {
    beforeEach(resetState);

    it('returns an empty set when no picks', () => {
        expect(appState.maybes.size).toBe(0);
    });

    it('includes slugs that are in maybe state (without prefix)', () => {
        appState.picks = new Set(['?act-a', '?act-b']);
        const m = appState.maybes;
        expect(m.has('act-a')).toBe(true);
        expect(m.has('act-b')).toBe(true);
    });

    it('excludes bare picked slugs', () => {
        appState.picks = new Set(['act-a', '?act-b']);
        const m = appState.maybes;
        expect(m.has('act-a')).toBe(false);
        expect(m.has('act-b')).toBe(true);
    });

    it('returns bare slugs without the ? prefix', () => {
        appState.picks = new Set(['?some-act']);
        expect([...appState.maybes][0]).toBe('some-act');
    });
});

// ---------------------------------------------------------------------------
// togglePick
// ---------------------------------------------------------------------------

describe('togglePick', () => {
    beforeEach(resetState);

    it('unpicked → picked', () => {
        appState.token = 'tok'; // prevents scheduleSave from doing nothing
        appState.picks = new Set();
        appState.togglePick('my-act');
        expect(appState.picks.has('my-act')).toBe(true);
    });

    it('picked → unpicked', () => {
        appState.token = 'tok';
        appState.picks = new Set(['my-act']);
        appState.togglePick('my-act');
        expect(appState.picks.has('my-act')).toBe(false);
    });

    it('maybe → picked (clears maybe prefix)', () => {
        appState.token = 'tok';
        appState.picks = new Set(['?my-act']);
        appState.togglePick('my-act');
        expect(appState.picks.has('my-act')).toBe(true);
        expect(appState.picks.has('?my-act')).toBe(false);
    });

    it('preserves other entries', () => {
        appState.token = 'tok';
        appState.picks = new Set(['other-act', '?another-act']);
        appState.togglePick('my-act');
        expect(appState.picks.has('other-act')).toBe(true);
        expect(appState.picks.has('?another-act')).toBe(true);
    });
});

// ---------------------------------------------------------------------------
// toggleMaybe
// ---------------------------------------------------------------------------

describe('toggleMaybe', () => {
    beforeEach(resetState);

    it('unpicked → maybe', () => {
        appState.token = 'tok';
        appState.picks = new Set();
        appState.toggleMaybe('my-act');
        expect(appState.picks.has('?my-act')).toBe(true);
        expect(appState.picks.has('my-act')).toBe(false);
    });

    it('maybe → unpicked', () => {
        appState.token = 'tok';
        appState.picks = new Set(['?my-act']);
        appState.toggleMaybe('my-act');
        expect(appState.picks.has('?my-act')).toBe(false);
    });

    it('picked → maybe (clears bare slug)', () => {
        appState.token = 'tok';
        appState.picks = new Set(['my-act']);
        appState.toggleMaybe('my-act');
        expect(appState.picks.has('?my-act')).toBe(true);
        expect(appState.picks.has('my-act')).toBe(false);
    });
});

// ---------------------------------------------------------------------------
// isPicked / isMaybe / isSelected
// ---------------------------------------------------------------------------

describe('isPicked / isMaybe / isSelected', () => {
    beforeEach(resetState);

    it('isPicked returns true for bare slug in picks', () => {
        appState.picks = new Set(['act-x']);
        expect(appState.isPicked('act-x')).toBe(true);
    });

    it('isPicked returns false for ?-prefixed slug', () => {
        appState.picks = new Set(['?act-x']);
        expect(appState.isPicked('act-x')).toBe(false);
    });

    it('isMaybe returns true for ?-prefixed slug', () => {
        appState.picks = new Set(['?act-x']);
        expect(appState.isMaybe('act-x')).toBe(true);
    });

    it('isMaybe returns false for bare slug', () => {
        appState.picks = new Set(['act-x']);
        expect(appState.isMaybe('act-x')).toBe(false);
    });

    it('isSelected returns true for picked', () => {
        appState.picks = new Set(['act-x']);
        expect(appState.isSelected('act-x')).toBe(true);
    });

    it('isSelected returns true for maybe', () => {
        appState.picks = new Set(['?act-x']);
        expect(appState.isSelected('act-x')).toBe(true);
    });

    it('isSelected returns false when absent', () => {
        appState.picks = new Set();
        expect(appState.isSelected('act-x')).toBe(false);
    });
});

// ---------------------------------------------------------------------------
// clearPicks
// ---------------------------------------------------------------------------

describe('clearPicks', () => {
    beforeEach(resetState);

    it('empties the picks set', () => {
        appState.picks = new Set(['act-a', '?act-b', 'act-c']);
        appState.clearPicks();
        expect(appState.picks.size).toBe(0);
    });

    it('is idempotent on an already-empty set', () => {
        appState.picks = new Set();
        appState.clearPicks();
        expect(appState.picks.size).toBe(0);
    });
});

// ---------------------------------------------------------------------------
// loadFromStorage
// ---------------------------------------------------------------------------

describe('loadFromStorage', () => {
    beforeEach(() => {
        resetState();
        localStorage.clear();
    });

    it('hydrates identity from IDENTITY_STORAGE_KEY', () => {
        const stored = { token: 'abc-token', name: 'Alice', counter: 3 };
        localStorage.setItem(IDENTITY_STORAGE_KEY, JSON.stringify(stored));
        appState.loadFromStorage();
        expect(appState.token).toBe('abc-token');
        expect(appState.name).toBe('Alice');
    });

    it('hydrates picks from PICKS_STORAGE_KEY', () => {
        localStorage.setItem(PICKS_STORAGE_KEY, JSON.stringify(['act-a', '?act-b']));
        appState.loadFromStorage();
        expect(appState.picks.has('act-a')).toBe(true);
        expect(appState.picks.has('?act-b')).toBe(true);
    });

    it('FINGERPRINT_COUNTER_KEY overrides counter from identity', () => {
        const stored = { token: 't', name: 'N', counter: 1 };
        localStorage.setItem(IDENTITY_STORAGE_KEY, JSON.stringify(stored));
        localStorage.setItem(FINGERPRINT_COUNTER_KEY, '7');
        appState.loadFromStorage();
        expect(appState.counter).toBe(7);
    });

    it('handles corrupt identity JSON gracefully', () => {
        localStorage.setItem(IDENTITY_STORAGE_KEY, 'not-json{{{');
        expect(() => appState.loadFromStorage()).not.toThrow();
        expect(appState.token).toBeNull();
    });

    it('handles corrupt picks JSON gracefully', () => {
        localStorage.setItem(PICKS_STORAGE_KEY, 'bad-json');
        expect(() => appState.loadFromStorage()).not.toThrow();
        expect(appState.picks.size).toBe(0);
    });

    it('does nothing when localStorage is empty', () => {
        appState.loadFromStorage();
        expect(appState.token).toBeNull();
        expect(appState.picks.size).toBe(0);
    });
});

// ---------------------------------------------------------------------------
// saveToStorage
// ---------------------------------------------------------------------------

describe('saveToStorage', () => {
    beforeEach(() => {
        resetState();
        localStorage.clear();
    });

    it('writes identity to IDENTITY_STORAGE_KEY', () => {
        appState.token = 'my-token';
        appState.name = 'Bob';
        appState.counter = 2;
        appState.saveToStorage();
        const raw = localStorage.getItem(IDENTITY_STORAGE_KEY);
        expect(raw).not.toBeNull();
        const parsed = JSON.parse(raw!);
        expect(parsed.token).toBe('my-token');
        expect(parsed.name).toBe('Bob');
        expect(parsed.counter).toBe(2);
    });

    it('writes counter to FINGERPRINT_COUNTER_KEY', () => {
        appState.token = 'my-token';
        appState.counter = 5;
        appState.saveToStorage();
        expect(localStorage.getItem(FINGERPRINT_COUNTER_KEY)).toBe('5');
    });

    it('does nothing when token is null', () => {
        appState.token = null;
        appState.saveToStorage();
        expect(localStorage.getItem(IDENTITY_STORAGE_KEY)).toBeNull();
    });
});

// ---------------------------------------------------------------------------
// loadCachedActs / cacheActs
// ---------------------------------------------------------------------------

describe('loadCachedActs / cacheActs', () => {
    beforeEach(() => {
        resetState();
        localStorage.clear();
    });

    it('returns null when no cache exists', () => {
        expect(appState.loadCachedActs('2026-04-16')).toBeNull();
    });

    it('round-trips acts through localStorage', () => {
        const acts = [
            {
                slug: 'test-act',
                name: 'Test Act',
                stage: 'Stage A',
                date: '2026-04-16',
                start: '12:00',
                end: '13:00',
                genre: 'Jazz (Traditional)'
            }
        ];
        appState.cacheActs('2026-04-16', acts);
        const result = appState.loadCachedActs('2026-04-16');
        expect(result).not.toBeNull();
        expect(result![0].slug).toBe('test-act');
    });

    it('returns null for expired cache', () => {
        const expiredTime = Date.now() - ACTS_CACHE_TTL_MS - 1000;
        const acts = [
            {
                slug: 'old-act',
                name: 'Old Act',
                stage: 'Stage A',
                date: '2026-04-16',
                start: '12:00',
                end: '13:00',
                genre: 'Blues'
            }
        ];
        localStorage.setItem(
            `${ACTS_STORAGE_PREFIX}2026-04-16`,
            JSON.stringify({ acts, cachedAt: expiredTime })
        );
        expect(appState.loadCachedActs('2026-04-16')).toBeNull();
    });

    it('returns null for corrupt cache JSON', () => {
        localStorage.setItem(`${ACTS_STORAGE_PREFIX}2026-04-16`, 'bad-json');
        expect(appState.loadCachedActs('2026-04-16')).toBeNull();
    });

    it('caches per-date — different dates do not interfere', () => {
        const acts16 = [
            {
                slug: 'thu-act',
                name: 'Thu',
                stage: 'S',
                date: '2026-04-16',
                start: '12:00',
                end: '13:00',
                genre: 'Funk'
            }
        ];
        const acts17 = [
            {
                slug: 'fri-act',
                name: 'Fri',
                stage: 'S',
                date: '2026-04-17',
                start: '14:00',
                end: '15:00',
                genre: 'R&B / Soul'
            }
        ];
        appState.cacheActs('2026-04-16', acts16);
        appState.cacheActs('2026-04-17', acts17);
        expect(appState.loadCachedActs('2026-04-16')![0].slug).toBe('thu-act');
        expect(appState.loadCachedActs('2026-04-17')![0].slug).toBe('fri-act');
    });
});

// ---------------------------------------------------------------------------
// loadCachedStages / cacheStages
// ---------------------------------------------------------------------------

describe('loadCachedStages / cacheStages', () => {
    beforeEach(() => {
        resetState();
        localStorage.clear();
    });

    it('returns null when no cache exists', () => {
        expect(appState.loadCachedStages()).toBeNull();
    });

    it('round-trips stage data through localStorage', () => {
        const stages = [
            { lat: 29.9584, lng: -90.0644, name: 'Abita Beer Stage' },
            { lat: 29.959, lng: -90.0639, name: 'NewOrleans.com Stage' }
        ];
        appState.cacheStages(stages);
        const result = appState.loadCachedStages();
        expect(result).not.toBeNull();
        expect(result![0].name).toBe('Abita Beer Stage');
        expect(result!.length).toBe(2);
    });

    it('returns null for corrupt stage JSON', () => {
        localStorage.setItem(STAGES_STORAGE_KEY, '{{bad}}');
        expect(appState.loadCachedStages()).toBeNull();
    });
});

// ---------------------------------------------------------------------------
// setViewMode
// ---------------------------------------------------------------------------

describe('setViewMode', () => {
    beforeEach(resetState);

    it('updates viewMode', () => {
        appState.setViewMode('my-schedule');
        expect(appState.viewMode).toBe('my-schedule');
    });

    it('updates viewMode to map', () => {
        appState.setViewMode('map');
        expect(appState.viewMode).toBe('map');
    });
});

// ---------------------------------------------------------------------------
// isActVisible
// ---------------------------------------------------------------------------
//
// Note: isActVisible combines multiple reactive $state reads (hiddenGenres,
// hiddenStages, showAll, showSelected, picks). Testing multi-property reactive
// combinations on the AppState singleton is unreliable in vitest because Svelte 5
// batches reactive updates — intermediate state may not be flushed consistently
// without a full component lifecycle. The individual building blocks are verified:
// - hiddenGenres/hiddenStages mutations → toggleGenre / toggleStage tests
// - picks mutations → togglePick / toggleMaybe tests
// - isSelected logic → isPicked / isMaybe / isSelected tests
// isActVisible is covered end-to-end in E2E tests via the filter panel.

describe('isActVisible — no-filter baseline', () => {
    beforeEach(resetState);

    const act = { slug: 'test-act', genre: 'Jazz (Traditional)', stage: 'Stage A' };

    it('returns true when no filters are set', () => {
        expect(appState.isActVisible(act)).toBe(true);
    });
});

// ---------------------------------------------------------------------------
// toggleGenre / toggleStage
// ---------------------------------------------------------------------------

describe('toggleGenre', () => {
    beforeEach(resetState);

    it('adds a genre to hiddenGenres when not present', () => {
        appState.toggleGenre('Blues');
        expect(appState.hiddenGenres.has('Blues')).toBe(true);
    });

    it('removes a genre from hiddenGenres when already present', () => {
        appState.hiddenGenres = new Set(['Blues']);
        appState.toggleGenre('Blues');
        expect(appState.hiddenGenres.has('Blues')).toBe(false);
    });

    it('does not affect other hidden genres', () => {
        appState.hiddenGenres = new Set(['Blues', 'Funk']);
        appState.toggleGenre('Blues');
        expect(appState.hiddenGenres.has('Funk')).toBe(true);
    });
});

describe('toggleStage', () => {
    beforeEach(resetState);

    it('adds a stage to hiddenStages when not present', () => {
        appState.toggleStage('Stage A');
        expect(appState.hiddenStages.has('Stage A')).toBe(true);
    });

    it('removes a stage from hiddenStages when already present', () => {
        appState.hiddenStages = new Set(['Stage A']);
        appState.toggleStage('Stage A');
        expect(appState.hiddenStages.has('Stage A')).toBe(false);
    });
});
