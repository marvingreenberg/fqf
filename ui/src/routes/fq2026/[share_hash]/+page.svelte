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
                    {stageLocations}
                    onTogglePick={() => {}}
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
                    sortMode={mobileSortMode}
                    onTogglePick={() => {}}
                    onActDetail={openDetail}
                    readOnly={true}
                />
            {:else}
                <ScheduleGrid
                    {acts}
                    {picks}
                    onTogglePick={() => {}}
                    onActDetail={openDetail}
                    readOnly={true}
                />
            {/if}
        </div>
    </div>
{/if}

<!-- Act detail modal (read-only: no pick toggle button) -->
{#if detailAct || detailLoading}
    <div
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
        onclick={closeDetail}
        role="dialog"
        aria-modal="true"
        aria-label="Act detail"
        onkeydown={(e) => e.key === 'Escape' && closeDetail()}
        tabindex="-1"
    >
        <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <div
            class="fqf-modal-card max-w-lg w-full mx-4 relative"
            onclick={(e) => e.stopPropagation()}
            role="document"
        >
            <div class="fqf-modal-header-strip"></div>

            <div class="p-6">
                <button
                    class="absolute top-5 right-4 text-xl leading-none"
                    style="color: rgba(74, 26, 107, 0.5);"
                    onclick={closeDetail}
                    aria-label="Close"
                >
                    ✕
                </button>

                {#if detailLoading}
                    <p style="color: var(--mg-purple); opacity: 0.6;">Loading…</p>
                {:else if detailAct}
                    <div class="flex items-center gap-2 mb-3">
                        <!-- Web links -->
                        {#if detailAct.websites.length > 0}
                            {#each detailAct.websites as url}
                                <a
                                    href={url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    title={new URL(url).hostname.replace('www.', '')}
                                    class="shrink-0 hover:scale-110 transition-transform"
                                    style="color: var(--mg-purple);"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="18"
                                        height="18"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        stroke-width="2"
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                    >
                                        <circle cx="12" cy="12" r="10" />
                                        <path d="M2 12h20" />
                                        <path
                                            d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"
                                        />
                                    </svg>
                                </a>
                            {/each}
                        {/if}

                        <!-- Map link -->
                        {#if stageLocations.has(detailAct.stage)}
                            {@const loc = stageLocations.get(detailAct.stage)}
                            <a
                                href="https://www.google.com/maps/dir/?api=1&destination={loc?.lat},{loc?.lng}"
                                target="_blank"
                                rel="noopener noreferrer"
                                title="Directions to {detailAct.stage}"
                                class="shrink-0 hover:scale-110 transition-transform"
                                style="color: var(--mg-green-deep);"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="18"
                                    height="18"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                >
                                    <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z" />
                                    <circle cx="12" cy="10" r="3" />
                                </svg>
                            </a>
                        {/if}

                        <h2
                            class="flex-1 min-w-0 text-xl font-bold leading-snug"
                            style="font-family: 'Playfair Display', Georgia, serif; color: var(--mg-purple-deep);"
                        >
                            {detailAct.name}
                        </h2>

                        <span class="fqf-genre-badge shrink-0">
                            {detailAct.genre}
                        </span>
                    </div>

                    <p
                        class="text-sm mb-3 flex items-center gap-1.5"
                        style="color: rgba(74, 26, 107, 0.55);"
                    >
                        {detailAct.stage} &middot; {detailAct.start}&#8211;{detailAct.end}
                    </p>

                    <p class="text-sm leading-relaxed">
                        {detailAct.about || 'No bio available yet.'}
                    </p>
                {/if}
            </div>
        </div>
    </div>
{/if}
