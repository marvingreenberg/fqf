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

    const MOBILE_BREAKPOINT = 768;

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
        { value: 'grid', label: () => 'All Acts' },
        { value: 'map', label: () => 'Map' },
        { value: 'my-schedule', label: () => `My Schedule (${appState.picks.size})` },
        { value: 'share', label: () => `Share (${appState.sharedSchedules.length})` }
    ];

    async function loadActs(date: string): Promise<void> {
        loading = true;
        try {
            const resp = await listActs({ date });
            acts = resp.acts;
        } finally {
            loading = false;
        }
    }

    async function loadAllActs(): Promise<void> {
        if (allActsLoaded) return;
        const resp = await listActs();
        allActs = resp.acts;
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

    async function loadPendingShare(): Promise<void> {
        const shareId = appState.pendingShareId;
        if (!shareId) return;
        try {
            const resp = await loadSharedSchedule(shareId);
            await appState.addSharedSchedule({
                share_id: shareId,
                name: appState.pendingShareName ?? resp.name,
                picks: resp.picks,
                acts: resp.acts
            });
            appState.pendingShareId = null;
            appState.pendingShareName = null;
            appState.viewMode = 'share';
        } catch {
            // Share not found — silently drop the pending share
            appState.pendingShareId = null;
            appState.pendingShareName = null;
        }
    }

    $effect(() => {
        if (appState.viewMode === 'my-schedule') {
            loadAllActs();
        }
    });

    $effect(() => {
        if (appState.viewMode !== 'my-schedule') {
            loadActs(appState.selectedDate);
        }
    });

    // Load pending share once confirmed
    $effect(() => {
        if (appState.confirmed && appState.pendingShareId) {
            loadPendingShare();
        }
    });

    onMount(async () => {
        loadActs(appState.selectedDate);
        const resp = await listStages();
        stageLocations = new Map(resp.stages.map((s) => [s.name, { lat: s.lat, lng: s.lng }]));
    });
</script>

<svelte:window bind:innerWidth />

<div class="flex flex-col h-full overflow-hidden">
    <header class="shrink-0 fqf-controls-bar px-4 py-2">
        <div class="flex items-center justify-between">
            <h1 class="text-base font-semibold" style="color: var(--mg-purple-deep);">
                FQF 2026 Schedule Builder
            </h1>
            {#if isMobile && appState.viewMode !== 'my-schedule' && appState.viewMode !== 'share'}
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
                    onclick={() => (appState.viewMode = tab.value)}
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
                {stageLocations}
                onTogglePick={(slug) => appState.togglePick(slug)}
                onActDetail={openDetail}
            />
        {:else if appState.viewMode === 'map'}
            <MapView {acts} {stageLocations} onActDetail={openDetail} />
        {:else if appState.viewMode === 'share'}
            <ShareView />
        {:else if loading}
            <div class="flex items-center justify-center h-full">
                <p style="color: var(--mg-purple); opacity: 0.6;">Loading schedule…</p>
            </div>
        {:else if isMobile}
            <MobileSchedule
                acts={visibleActs}
                picks={appState.picks}
                sortMode={appState.mobileSortMode}
                onTogglePick={(slug) => appState.togglePick(slug)}
                onActDetail={openDetail}
            />
        {:else}
            <ScheduleGrid
                acts={visibleActs}
                picks={appState.picks}
                onTogglePick={(slug) => appState.togglePick(slug)}
                onActDetail={openDetail}
            />
        {/if}
    </div>
</div>

<!-- Act detail modal -->
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
            <!-- Purple accent strip -->
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
                    {@const isPicked = appState.isPicked(detailAct.slug)}
                    <!-- Header row: fleur + web links + name + genre -->
                    <div class="flex items-center gap-2 mb-3">
                        <!-- Fleur-de-lis pick button -->
                        <button
                            class="fqf-fleur shrink-0"
                            style="width: 1.5rem; height: 1.5rem;"
                            title={isPicked ? 'Remove from picks' : 'Add to picks'}
                            onclick={() => appState.togglePick(detailAct.slug)}
                        >
                            <svg
                                viewBox="0 0 16 16"
                                width="20"
                                height="20"
                                fill={isPicked ? 'var(--mg-green-deep)' : 'none'}
                                stroke={isPicked ? 'none' : 'rgba(74, 26, 107, 0.3)'}
                                stroke-width="0.75"
                            >
                                <path
                                    d="M8 0C8 0 6.5 3.5 6.5 5.5C6.5 7 7 8 8 9C9 8 9.5 7 9.5 5.5C9.5 3.5 8 0 8 0ZM4.5 6C2.5 6 0 7.5 0 7.5C0 7.5 2 9 4.5 9C5.5 9 6.5 8.5 7 8C6 7.5 5.5 7 4.5 6ZM11.5 6C10.5 7 10 7.5 9 8C9.5 8.5 10.5 9 11.5 9C14 9 16 7.5 16 7.5C16 7.5 13.5 6 11.5 6ZM8 10C7 10 5 10.5 5 12C5 14 8 16 8 16C8 16 11 14 11 12C11 10.5 9 10 8 10Z"
                                />
                            </svg>
                        </button>

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

                        <!-- Band name -->
                        <h2
                            class="flex-1 min-w-0 text-xl font-bold leading-snug"
                            style="font-family: 'Playfair Display', Georgia, serif; color: var(--mg-purple-deep);"
                        >
                            {detailAct.name}
                        </h2>

                        <!-- Genre badge -->
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

                    <p class="text-sm leading-relaxed whitespace-pre-line">
                        {detailAct.about || 'No bio available yet.'}
                    </p>
                {/if}
            </div>
        </div>
    </div>
{/if}
