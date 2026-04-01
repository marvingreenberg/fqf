<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import type { ActSummary, ActDetail, MobileSortMode, ViewMode } from '$lib/types';
    import { FESTIVAL_DATES } from '$lib/types';
    import { listActs, getAct, listStages, loadSharedSchedule } from '$lib/api';
    import DayTabs from '$lib/components/DayTabs.svelte';
    import ScheduleGrid from '$lib/components/ScheduleGrid.svelte';
    import MobileSchedule from '$lib/components/MobileSchedule.svelte';
    import MySchedule from '$lib/components/MySchedule.svelte';
    import MapView from '$lib/components/MapView.svelte';
    import ShareLoginPane from '$lib/components/ShareLoginPane.svelte';
    import ActDetailModal from '$lib/components/ActDetailModal.svelte';

    const MOBILE_BREAKPOINT = 768;
    const CACHE_TTL_MS = 10 * 60 * 1000;

    type SharedViewMode = Exclude<ViewMode, 'share'>;

    const VIEW_TABS: { value: SharedViewMode; label: () => string }[] = [
        { value: 'grid', label: () => 'All Acts' },
        { value: 'map', label: () => 'Map' },
        { value: 'my-schedule', label: () => `Their Schedule (${picks.size})` }
    ];

    const SORT_MODES: { value: MobileSortMode; label: string }[] = [
        { value: 'by-time', label: 'By Time' },
        { value: 'by-stage', label: 'By Stage' }
    ];

    let acts = $state<ActSummary[]>([]);
    let allActs = $state<ActSummary[]>([]);
    let allActsLoaded = $state(false);
    let loading = $state(false);
    let sharedLoading = $state(true);
    let sharedError = $state<string | null>(null);
    let ownerName = $state('');
    // Show the login/context pane until the user dismisses it
    let showLoginPane = $state(true);
    let picks = $state<Set<string>>(new Set());
    let detailAct = $state<ActDetail | null>(null);
    let detailLoading = $state(false);
    let innerWidth = $state(MOBILE_BREAKPOINT + 1);
    let stageLocations = $state(new Map<string, { lat: number; lng: number }>());
    let selectedDate = $state<string>(FESTIVAL_DATES[0]);
    let viewMode = $state<SharedViewMode>('grid');
    let mobileSortMode = $state<MobileSortMode>('by-time');

    const isMobile = $derived(innerWidth < MOBILE_BREAKPOINT);

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

    // Reload acts when day or relevant view mode changes
    let prevDate = $state('');
    let prevViewMode = $state<SharedViewMode>('grid');

    $effect(() => {
        const date = selectedDate;
        const mode = viewMode;

        if (mode === 'my-schedule' && !allActsLoaded) {
            loadAllActs();
        } else if (
            (mode === 'grid' || mode === 'mobile') &&
            (date !== prevDate || mode !== prevViewMode)
        ) {
            prevDate = date;
            prevViewMode = mode;
            loadActs(date);
        }
        prevViewMode = mode;
    });

    onMount(async () => {
        const shareHash = $page.params.share_hash;

        // Fetch the shared schedule and stage locations in parallel
        const [, stagesResp] = await Promise.allSettled([
            (async () => {
                try {
                    const resp = await loadSharedSchedule(shareHash);
                    ownerName = resp.name;
                    picks = new Set(resp.picks);
                } catch {
                    sharedError = 'Schedule not found. The link may be invalid or expired.';
                } finally {
                    sharedLoading = false;
                }
            })(),
            listStages()
        ]);

        if (stagesResp.status === 'fulfilled') {
            stageLocations = new Map(
                stagesResp.value.stages.map((s) => [s.name, { lat: s.lat, lng: s.lng }])
            );
        }

        loadActs(selectedDate);
        prevDate = selectedDate;
    });
</script>

<svelte:window bind:innerWidth />

{#if sharedLoading}
    <div class="flex items-center justify-center h-full flex-1">
        <p style="color: var(--mg-purple); opacity: 0.6;">Loading shared schedule…</p>
    </div>
{:else if sharedError}
    <div class="flex flex-col items-center justify-center h-full flex-1 gap-4">
        <p class="text-lg font-medium" style="color: var(--mg-purple-deep);">{sharedError}</p>
        <a href="/fq2026" class="text-sm underline" style="color: var(--mg-purple);">
            Go to my schedule
        </a>
    </div>
{:else if showLoginPane}
    <!-- Context-specific login pane — shown until the user dismisses via "See" -->
    <div
        class="fixed inset-0 z-50 flex items-center justify-center"
        style="background: rgba(26, 10, 40, 0.88);"
    >
        <ShareLoginPane
            shareName={ownerName}
            shareHash={$page.params.share_hash}
            ondismiss={() => (showLoginPane = false)}
        />
    </div>
{:else}
    <div class="flex flex-col h-full overflow-hidden">
        <header class="shrink-0 fqf-controls-bar px-4 py-2">
            <div class="flex items-center justify-between">
                <h1 class="text-base font-semibold" style="color: var(--mg-gold-bright);">
                    {ownerName}'s Schedule
                </h1>
                {#if isMobile && viewMode !== 'my-schedule'}
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
                {#each VIEW_TABS as tab (tab.value)}
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

        {#if viewMode !== 'my-schedule' && viewMode !== 'map'}
            <DayTabs bind:selectedDate />
        {/if}

        <div class="flex-1 overflow-hidden relative">
            {#if viewMode === 'my-schedule'}
                <MySchedule
                    {allActs}
                    {picks}
                    maybes={new Set()}
                    {stageLocations}
                    onTogglePick={() => {}}
                    onToggleMaybe={() => {}}
                    onActDetail={openDetail}
                    readOnly={true}
                />
            {:else if viewMode === 'map'}
                <MapView {acts} {stageLocations} onActDetail={openDetail} />
            {:else if loading}
                <div class="flex items-center justify-center h-full">
                    <p style="color: var(--mg-purple); opacity: 0.6;">Loading schedule…</p>
                </div>
            {:else if isMobile}
                <MobileSchedule
                    {acts}
                    {picks}
                    maybes={new Set()}
                    sortMode={mobileSortMode}
                    onTogglePick={() => {}}
                    onToggleMaybe={() => {}}
                    onActDetail={openDetail}
                    readOnly={true}
                />
            {:else}
                <ScheduleGrid
                    {acts}
                    {picks}
                    maybes={new Set()}
                    onTogglePick={() => {}}
                    onToggleMaybe={() => {}}
                    onActDetail={openDetail}
                    readOnly={true}
                />
            {/if}
        </div>
    </div>
{/if}

{#if detailAct || detailLoading}
    <ActDetailModal
        act={detailAct}
        loading={detailLoading}
        {stageLocations}
        isPicked={false}
        isMaybe={false}
        readOnly={true}
        onClose={closeDetail}
    />
{/if}
