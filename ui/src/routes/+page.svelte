<script lang="ts">
    import { onMount } from 'svelte';
    import type { ActSummary, ActDetail, MobileSortMode, ViewMode } from '$lib/types';
    import { listActs, getAct } from '$lib/api';
    import { appState } from '$lib/stores.svelte';
    import DayTabs from '$lib/components/DayTabs.svelte';
    import ScheduleGrid from '$lib/components/ScheduleGrid.svelte';
    import MobileSchedule from '$lib/components/MobileSchedule.svelte';
    import MySchedule from '$lib/components/MySchedule.svelte';
    import MergeView from '$lib/components/MergeView.svelte';
    import FilterPanel from '$lib/components/FilterPanel.svelte';

    const MOBILE_BREAKPOINT = 768;

    let acts = $state<ActSummary[]>([]);
    let allActs = $state<ActSummary[]>([]);
    let allActsLoaded = $state(false);
    let loading = $state(false);
    let detailAct = $state<ActDetail | null>(null);
    let detailLoading = $state(false);
    let innerWidth = $state(MOBILE_BREAKPOINT + 1);

    const isMobile = $derived(innerWidth < MOBILE_BREAKPOINT);

    const uniqueGenres = $derived([...new Set(acts.map((a) => a.genre))].sort());
    const uniqueStages = $derived([...new Set(acts.map((a) => a.stage))].sort());
    const visibleActs = $derived(acts.filter((a) => appState.isActVisible(a)));

    const SORT_MODES: { value: MobileSortMode; label: string }[] = [
        { value: 'by-time', label: 'By Time' },
        { value: 'by-stage', label: 'By Stage' }
    ];

    const VIEW_TABS: { value: ViewMode; label: () => string }[] = [
        { value: 'grid', label: () => 'All Acts' },
        { value: 'my-schedule', label: () => `My Schedule (${appState.picks.size})` },
        { value: 'merge', label: () => 'Merge' }
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

    onMount(() => {
        loadActs(appState.selectedDate);
    });
</script>

<svelte:window bind:innerWidth />

<div class="flex flex-col h-screen overflow-hidden">
    <header class="shrink-0 fqf-controls-bar px-4 py-2">
        <div class="flex items-center justify-between">
            <h1 class="text-base font-semibold" style="color: var(--mg-purple-deep);">
                FQF 2026 Schedule Builder
            </h1>
            {#if isMobile && appState.viewMode !== 'my-schedule' && appState.viewMode !== 'merge'}
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

    {#if appState.viewMode !== 'my-schedule' && appState.viewMode !== 'merge'}
        <DayTabs bind:selectedDate={appState.selectedDate} />
        <FilterPanel genres={uniqueGenres} stages={uniqueStages} />
    {/if}

    <div class="flex-1 overflow-hidden relative">
        {#if appState.viewMode === 'my-schedule'}
            <MySchedule
                {allActs}
                picks={appState.picks}
                onTogglePick={(slug) => appState.togglePick(slug)}
                onActDetail={openDetail}
            />
        {:else if appState.viewMode === 'merge'}
            <MergeView />
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
                    <div class="flex items-start gap-3 mb-4">
                        <div class="flex-1 min-w-0">
                            <h2
                                class="text-xl font-bold leading-snug"
                                style="font-family: 'Playfair Display', Georgia, serif; color: var(--mg-purple-deep);"
                            >
                                {detailAct.name}
                            </h2>
                            <p class="text-sm mt-1" style="color: rgba(74, 26, 107, 0.55);">
                                {detailAct.stage}
                            </p>
                        </div>
                        <span class="fqf-genre-badge shrink-0">
                            {detailAct.genre}
                        </span>
                    </div>

                    <p class="text-sm mb-4" style="color: rgba(26, 26, 26, 0.55);">
                        {detailAct.start}–{detailAct.end}
                    </p>

                    <p class="text-sm leading-relaxed whitespace-pre-line">
                        {detailAct.about || 'No bio available yet.'}
                    </p>
                {/if}
            </div>
        </div>
    </div>
{/if}
