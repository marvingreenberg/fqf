<script lang="ts">
    import { onMount } from 'svelte';
    import type { Snippet } from 'svelte';
    import type { ActSummary, ActDetail, MobileSortMode } from '$lib/types';
    import { listActs, getAct, listStages } from '$lib/api';
    import DayTabs from '$lib/components/DayTabs.svelte';
    import ScheduleGrid from '$lib/components/ScheduleGrid.svelte';
    import MobileSchedule from '$lib/components/MobileSchedule.svelte';
    import MySchedule from '$lib/components/MySchedule.svelte';
    import MapView from '$lib/components/MapView.svelte';
    import ActDetailModal from '$lib/components/ActDetailModal.svelte';
    import HelpPanel from '$lib/components/HelpPanel.svelte';

    const MOBILE_BREAKPOINT = 768;
    const CACHE_TTL_MS = 10 * 60 * 1000;

    interface ViewTab {
        value: string;
        label: () => string;
    }

    interface Props {
        /** Currently selected view mode — bindable. */
        viewMode: string;
        /** Currently selected date string ("YYYY-MM-DD") — bindable. */
        selectedDate: string;
        /** Current sort mode for mobile — bindable. */
        mobileSortMode: MobileSortMode;
        /** Acts the user has picked. */
        picks: Set<string>;
        /** Acts marked as maybe (pass an empty set for read-only views). */
        maybes: Set<string>;
        /** When true, toggle buttons are hidden and callbacks are no-ops. */
        readOnly: boolean;
        /** Title shown in the controls bar. */
        title: string;
        /** Tab definitions for the view mode switcher. */
        viewTabs: ViewTab[];
        /**
         * View mode values that should trigger loading all acts (instead of
         * per-day acts). E.g. ['my-schedule', 'share', 'map'].
         */
        loadAllForModes: string[];
        /**
         * Optional filter function applied to per-day acts before rendering.
         * When not provided, all loaded acts are displayed.
         */
        actFilter?: (act: ActSummary) => boolean;
        /**
         * Optional slot rendered between the day-tabs row and the main content
         * area when in all-acts mode (e.g. FilterPanel).
         */
        filterPanel?: Snippet;
        /**
         * Optional slot for a custom view rendered when viewMode is not one of
         * the built-in modes ('all-acts', 'my-schedule', 'map').
         * Receives { allActs } for convenience.
         */
        extraView?: Snippet<[{ allActs: ActSummary[] }]>;
        /** Called when the user toggles a pick. */
        onTogglePick?: (slug: string) => void;
        /** Called when the user toggles a maybe. */
        onToggleMaybe?: (slug: string) => void;
        /**
         * Called each time the all-acts list is (re-)loaded, so the parent
         * can react (e.g. update a derived `allActs` variable in appState).
         */
        onAllActsLoaded?: (acts: ActSummary[]) => void;
        /**
         * Called each time a per-day acts list is loaded (e.g. to populate
         * filter dropdowns in the parent).
         */
        onDayActsLoaded?: (acts: ActSummary[]) => void;
    }

    let {
        viewMode = $bindable(),
        selectedDate = $bindable(),
        mobileSortMode = $bindable(),
        picks,
        maybes,
        readOnly,
        title,
        viewTabs,
        loadAllForModes,
        actFilter,
        filterPanel,
        extraView,
        onTogglePick,
        onToggleMaybe,
        onAllActsLoaded,
        onDayActsLoaded
    }: Props = $props();

    const SORT_MODES: { value: MobileSortMode; label: string }[] = [
        { value: 'by-time', label: 'By Time' },
        { value: 'by-stage', label: 'By Stage' }
    ];

    let showHelp = $state(false);
    let acts = $state<ActSummary[]>([]);
    let allActs = $state<ActSummary[]>([]);
    let allActsLoaded = $state(false);
    let loading = $state(false);
    let detailAct = $state<ActDetail | null>(null);
    let detailLoading = $state(false);
    let innerWidth = $state(MOBILE_BREAKPOINT + 1);
    let stageLocations = $state(new Map<string, { lat: number; lng: number }>());

    const isMobile = $derived(innerWidth < MOBILE_BREAKPOINT);

    // Apply the optional caller-supplied filter; fall back to all loaded acts.
    const displayActs = $derived(actFilter ? acts.filter(actFilter) : acts);

    // Whether the current viewMode is one of the shell's built-in views.
    const isBuiltinMode = $derived(
        viewMode === 'all-acts' || viewMode === 'my-schedule' || viewMode === 'map'
    );

    // Cache acts per date with TTL to avoid redundant API calls
    const actsCache = new Map<string, { acts: ActSummary[]; fetchedAt: number }>();

    function isCacheFresh(key: string): boolean {
        const entry = actsCache.get(key);
        if (!entry) return false;
        return Date.now() - entry.fetchedAt < CACHE_TTL_MS;
    }

    async function loadActs(date: string): Promise<void> {
        // 1. In-memory cache (hot path within a session)
        if (isCacheFresh(date)) {
            acts = actsCache.get(date)!.acts;
            onDayActsLoaded?.(acts);
            return;
        }

        // 2. localStorage cache — serve immediately while API request runs in background
        const { appState } = await import('$lib/stores.svelte');
        const lsCached = appState.loadCachedActs(date);
        if (lsCached) {
            acts = lsCached;
            actsCache.set(date, { acts: lsCached, fetchedAt: Date.now() });
            onDayActsLoaded?.(acts);
            // Still fetch in background to refresh cache (no loading spinner since we have data)
            listActs({ date })
                .then((resp) => {
                    acts = resp.acts;
                    actsCache.set(date, { acts: resp.acts, fetchedAt: Date.now() });
                    appState.cacheActs(date, resp.acts);
                    onDayActsLoaded?.(acts);
                })
                .catch(() => {
                    /* offline — cached data is fine */
                });
            return;
        }

        // 3. Cold load from API
        loading = true;
        try {
            const resp = await listActs({ date });
            acts = resp.acts;
            actsCache.set(date, { acts: resp.acts, fetchedAt: Date.now() });
            appState.cacheActs(date, resp.acts);
            onDayActsLoaded?.(acts);
        } catch {
            // API unavailable and no cached data — acts stays empty
        } finally {
            loading = false;
        }
    }

    async function loadAllActs(): Promise<void> {
        if (allActsLoaded && isCacheFresh('all')) return;

        // Check localStorage for a cached all-acts list
        const { appState } = await import('$lib/stores.svelte');
        const lsCached = appState.loadCachedActs('all');
        if (lsCached) {
            allActs = lsCached;
            actsCache.set('all', { acts: lsCached, fetchedAt: Date.now() });
            allActsLoaded = true;
            onAllActsLoaded?.(allActs);
            // Background refresh
            listActs()
                .then((resp) => {
                    allActs = resp.acts;
                    actsCache.set('all', { acts: resp.acts, fetchedAt: Date.now() });
                    appState.cacheActs('all', resp.acts);
                    onAllActsLoaded?.(allActs);
                })
                .catch(() => {
                    /* offline — cached data is fine */
                });
            return;
        }

        try {
            const resp = await listActs();
            allActs = resp.acts;
            actsCache.set('all', { acts: resp.acts, fetchedAt: Date.now() });
            appState.cacheActs('all', resp.acts);
            allActsLoaded = true;
            onAllActsLoaded?.(allActs);
        } catch {
            // API unavailable and no cached data — allActs stays empty
        }
    }

    async function openDetail(act: ActSummary): Promise<void> {
        detailLoading = true;
        detailAct = null;
        try {
            detailAct = await getAct(act.slug);
        } finally {
            detailLoading = false;
        }
    }

    function closeDetail(): void {
        detailAct = null;
    }

    // Reload acts when day or view mode changes
    let prevDate = $state('');
    let prevViewMode = $state('');

    $effect(() => {
        const date = selectedDate;
        const mode = viewMode;

        if (loadAllForModes.includes(mode) && !allActsLoaded) {
            loadAllActs();
        }
        if (
            (mode === 'all-acts' || mode === 'map') &&
            (date !== prevDate || mode !== prevViewMode)
        ) {
            prevDate = date;
            prevViewMode = mode;
            loadActs(date);
        }
        prevViewMode = mode;
    });

    onMount(async () => {
        loadActs(selectedDate);
        prevDate = selectedDate;

        // Cache-first stage load: serve cached data immediately, refresh in background.
        const { appState } = await import('$lib/stores.svelte');
        const cachedStages = appState.loadCachedStages();
        if (cachedStages) {
            stageLocations = new Map(cachedStages.map((s) => [s.name, { lat: s.lat, lng: s.lng }]));
        }
        try {
            const resp = await listStages();
            stageLocations = new Map(resp.stages.map((s) => [s.name, { lat: s.lat, lng: s.lng }]));
            appState.cacheStages(
                resp.stages.map((s) => ({ name: s.name, lat: s.lat, lng: s.lng }))
            );
        } catch {
            // API unavailable — cached data (if any) is already in stageLocations
        }
    });
</script>

<svelte:window bind:innerWidth />

<div class="flex flex-col h-full overflow-hidden">
    <header class="shrink-0 fqf-controls-bar px-4 py-2">
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
                <h1 class="text-base font-semibold" style="color: var(--mg-gold-bright);">
                    {title}
                </h1>
                <button
                    class="flex items-center justify-center w-5 h-5 rounded-full text-xs font-bold"
                    style="background: rgba(212, 168, 67, 0.3); color: var(--mg-gold-bright); border: 1px solid rgba(212, 168, 67, 0.5);"
                    onclick={() => (showHelp = true)}
                    aria-label="Help"
                    title="About this app"
                >
                    ℹ
                </button>
            </div>
            {#if isMobile && viewMode === 'all-acts'}
                <div class="flex gap-1">
                    {#each SORT_MODES as mode (mode.value)}
                        <button
                            class="fqf-sort-pill {mobileSortMode === mode.value
                                ? 'fqf-sort-pill-active'
                                : 'fqf-sort-pill-inactive'}"
                            onclick={() => (mobileSortMode = mode.value)}
                        >
                            {mode.label}
                        </button>
                    {/each}
                </div>
            {/if}
        </div>

        <div class="flex gap-1.5 mt-2">
            {#each viewTabs as tab (tab.value)}
                <button
                    class="fqf-view-pill {viewMode === tab.value
                        ? 'fqf-view-pill-active'
                        : 'fqf-view-pill-inactive'}"
                    onclick={() => (viewMode = tab.value)}
                >
                    {tab.label()}
                </button>
            {/each}
        </div>
    </header>

    {#if viewMode === 'all-acts'}
        <DayTabs bind:selectedDate />
        {#if filterPanel}
            {@render filterPanel()}
        {/if}
    {/if}

    <div class="flex-1 overflow-hidden relative">
        {#if viewMode === 'my-schedule'}
            <MySchedule
                {allActs}
                {picks}
                {maybes}
                {stageLocations}
                onTogglePick={(slug) => onTogglePick?.(slug)}
                onToggleMaybe={(slug) => onToggleMaybe?.(slug)}
                onActDetail={openDetail}
                {readOnly}
            />
        {:else if viewMode === 'map'}
            <MapView
                {acts}
                {allActs}
                {picks}
                {selectedDate}
                {stageLocations}
                onActDetail={openDetail}
                onDayChange={(d) => {
                    selectedDate = d;
                }}
            />
        {:else if !isBuiltinMode && extraView}
            {@render extraView({ allActs })}
        {:else if loading}
            <div class="flex items-center justify-center h-full">
                <p style="color: var(--mg-purple); opacity: 0.6;">Loading schedule…</p>
            </div>
        {:else if isMobile}
            <MobileSchedule
                acts={displayActs}
                {picks}
                {maybes}
                sortMode={mobileSortMode}
                onTogglePick={(slug) => onTogglePick?.(slug)}
                onToggleMaybe={(slug) => onToggleMaybe?.(slug)}
                onActDetail={openDetail}
                {readOnly}
            />
        {:else}
            <ScheduleGrid
                acts={displayActs}
                {picks}
                {maybes}
                onTogglePick={(slug) => onTogglePick?.(slug)}
                onToggleMaybe={(slug) => onToggleMaybe?.(slug)}
                onActDetail={openDetail}
                {readOnly}
            />
        {/if}
    </div>
</div>

{#if detailAct || detailLoading}
    <ActDetailModal
        act={detailAct}
        loading={detailLoading}
        {stageLocations}
        isPicked={detailAct ? picks.has(detailAct.slug) : false}
        isMaybe={detailAct ? maybes.has(detailAct.slug) : false}
        {readOnly}
        onTogglePick={() => detailAct && onTogglePick?.(detailAct.slug)}
        onToggleMaybe={() => detailAct && onToggleMaybe?.(detailAct.slug)}
        onClose={closeDetail}
    />
{/if}

{#if showHelp}
    <HelpPanel onClose={() => (showHelp = false)} />
{/if}
