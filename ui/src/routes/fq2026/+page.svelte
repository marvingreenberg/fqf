<script lang="ts">
    import { onMount } from 'svelte';
    import type { ActSummary, ActDetail, MobileSortMode, ViewMode } from '$lib/types';
    import { listActs, getAct, listStages, loadSharedSchedule } from '$lib/api';
    import { appState } from '$lib/stores.svelte';
    import DayTabs from '$lib/components/DayTabs.svelte';
    import ScheduleGrid from '$lib/components/ScheduleGrid.svelte';
    import MobileSchedule from '$lib/components/MobileSchedule.svelte';
    import MySchedule from '$lib/components/MySchedule.svelte';
    import ShareView from '$lib/components/ShareView.svelte';
    import MapView from '$lib/components/MapView.svelte';
    import FilterPanel from '$lib/components/FilterPanel.svelte';
    import ActDetailModal from '$lib/components/ActDetailModal.svelte';

    const MOBILE_BREAKPOINT = 768;
    const CACHE_TTL_MS = 10 * 60 * 1000;

    let acts = $state<ActSummary[]>([]);
    let allActs = $state<ActSummary[]>([]);
    let allActsLoaded = $state(false);
    let loading = $state(false);
    let detailAct = $state<ActDetail | null>(null);
    let detailLoading = $state(false);
    let innerWidth = $state(MOBILE_BREAKPOINT + 1);
    let stageLocations = $state(new Map<string, { lat: number; lng: number }>());

    const isMobile = $derived(innerWidth < MOBILE_BREAKPOINT);

    const uniqueGenres = $derived([...new Set(acts.map((a) => a.genre))].sort());
    const uniqueStages = $derived([...new Set(acts.map((a) => a.stage))]);
    const visibleActs = $derived(acts.filter((a) => appState.isActVisible(a)));

    const SORT_MODES: { value: MobileSortMode; label: string }[] = [
        { value: 'by-time', label: 'By Time' },
        { value: 'by-stage', label: 'By Stage' }
    ];

    const VIEW_TABS: { value: ViewMode; label: () => string }[] = [
        { value: 'all-acts', label: () => 'All Acts' },
        { value: 'map', label: () => 'Map' },
        { value: 'my-schedule', label: () => `My Schedule (${appState.picks.size})` },
        { value: 'share', label: () => `Share (${appState.sharedSchedules.length})` }
    ];

    // Cache acts per date with TTL to avoid redundant API calls
    const actsCache = new Map<string, { acts: ActSummary[]; fetchedAt: number }>();

    function isCacheFresh(key: string): boolean {
        const entry = actsCache.get(key);
        if (!entry) return false;
        return Date.now() - entry.fetchedAt < CACHE_TTL_MS;
    }

    async function loadActs(date: string): Promise<void> {
        if (isCacheFresh(date)) {
            acts = actsCache.get(date)!.acts;
            return;
        }
        loading = true;
        try {
            const resp = await listActs({ date });
            acts = resp.acts;
            actsCache.set(date, { acts: resp.acts, fetchedAt: Date.now() });
        } finally {
            loading = false;
        }
    }

    async function loadAllActs(): Promise<void> {
        if (allActsLoaded && isCacheFresh('all')) return;
        const resp = await listActs();
        allActs = resp.acts;
        actsCache.set('all', { acts: resp.acts, fetchedAt: Date.now() });
        allActsLoaded = true;
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

    async function loadPendingShare(shareId: string, shareName: string | null): Promise<void> {
        // Skip if this is our own share link
        if (appState.ownShareId && shareId === appState.ownShareId) {
            appState.setViewMode('my-schedule');
            return;
        }
        try {
            const resp = await loadSharedSchedule(shareId);
            await appState.addSharedSchedule({
                share_id: shareId,
                name: shareName ?? resp.name,
                picks: resp.picks,
                acts: resp.acts
            });
            appState.setViewMode('share');
        } catch {
            // Share not found — silently ignore
        }
    }

    // Reload acts when day or relevant view mode changes
    let prevDate = $state('');
    let prevViewMode = $state<ViewMode>('all-acts');

    $effect(() => {
        const date = appState.selectedDate;
        const mode = appState.viewMode;

        if ((mode === 'my-schedule' || mode === 'share' || mode === 'map') && !allActsLoaded) {
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

    // Load pending share once confirmed — capture and clear to prevent re-entry
    $effect(() => {
        const confirmed = appState.confirmed;
        const shareId = appState.pendingShareId;
        const shareName = appState.pendingShareName;
        if (confirmed && shareId) {
            appState.pendingShareId = null;
            appState.pendingShareName = null;
            loadPendingShare(shareId, shareName);
        }
    });

    onMount(async () => {
        loadActs(appState.selectedDate);
        prevDate = appState.selectedDate;
        const resp = await listStages();
        stageLocations = new Map(resp.stages.map((s) => [s.name, { lat: s.lat, lng: s.lng }]));
    });
</script>

<svelte:window bind:innerWidth />

<div class="flex flex-col h-full overflow-hidden">
    <header class="shrink-0 fqf-controls-bar px-4 py-2">
        <div class="flex items-center justify-between">
            <h1 class="text-base font-semibold" style="color: var(--mg-gold-bright);">
                FQF 2026 Schedule Builder
            </h1>
            {#if isMobile && appState.viewMode === 'all-acts'}
                <div class="flex gap-1">
                    {#each SORT_MODES as mode (mode.value)}
                        <button
                            class="fqf-sort-pill {appState.mobileSortMode === mode.value
                                ? 'fqf-sort-pill-active'
                                : 'fqf-sort-pill-inactive'}"
                            onclick={() => (appState.mobileSortMode = mode.value)}
                        >
                            {mode.label}
                        </button>
                    {/each}
                </div>
            {/if}
        </div>

        <div class="flex gap-1.5 mt-2">
            {#each VIEW_TABS as tab (tab.value)}
                <button
                    class="fqf-view-pill {appState.viewMode === tab.value
                        ? 'fqf-view-pill-active'
                        : 'fqf-view-pill-inactive'}"
                    onclick={() => appState.setViewMode(tab.value)}
                >
                    {tab.label()}
                </button>
            {/each}
        </div>
    </header>

    {#if appState.viewMode !== 'my-schedule' && appState.viewMode !== 'share' && appState.viewMode !== 'map'}
        <DayTabs bind:selectedDate={appState.selectedDate} />
        <FilterPanel genres={uniqueGenres} stages={uniqueStages} />
    {/if}

    <div class="flex-1 overflow-hidden relative">
        {#if appState.viewMode === 'my-schedule'}
            <MySchedule
                {allActs}
                picks={appState.picks}
                maybes={appState.maybes}
                {stageLocations}
                onTogglePick={(slug) => appState.togglePick(slug)}
                onToggleMaybe={(slug) => appState.toggleMaybe(slug)}
                onActDetail={openDetail}
            />
        {:else if appState.viewMode === 'map'}
            <MapView
                {acts}
                {allActs}
                picks={appState.picks}
                selectedDate={appState.selectedDate}
                {stageLocations}
                onActDetail={openDetail}
                onDayChange={(d) => {
                    appState.selectedDate = d;
                }}
            />
        {:else if appState.viewMode === 'share'}
            <ShareView
                selfActs={allActs}
                onTogglePick={(slug) => appState.togglePick(slug)}
                onToggleMaybe={(slug) => appState.toggleMaybe(slug)}
                onActDetail={openDetail}
            />
        {:else if loading}
            <div class="flex items-center justify-center h-full">
                <p style="color: var(--mg-purple); opacity: 0.6;">Loading schedule…</p>
            </div>
        {:else if isMobile}
            <MobileSchedule
                acts={visibleActs}
                picks={appState.picks}
                maybes={appState.maybes}
                sortMode={appState.mobileSortMode}
                onTogglePick={(slug) => appState.togglePick(slug)}
                onToggleMaybe={(slug) => appState.toggleMaybe(slug)}
                onActDetail={openDetail}
            />
        {:else}
            <ScheduleGrid
                acts={visibleActs}
                picks={appState.picks}
                maybes={appState.maybes}
                onTogglePick={(slug) => appState.togglePick(slug)}
                onToggleMaybe={(slug) => appState.toggleMaybe(slug)}
                onActDetail={openDetail}
            />
        {/if}
    </div>
</div>

{#if detailAct || detailLoading}
    <ActDetailModal
        act={detailAct}
        loading={detailLoading}
        {stageLocations}
        isPicked={detailAct ? appState.isPicked(detailAct.slug) : false}
        isMaybe={detailAct ? appState.isMaybe(detailAct.slug) : false}
        readOnly={false}
        onTogglePick={() => detailAct && appState.togglePick(detailAct.slug)}
        onToggleMaybe={() => detailAct && appState.toggleMaybe(detailAct.slug)}
        onClose={closeDetail}
    />
{/if}
