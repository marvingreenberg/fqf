<script lang="ts">
    import { onMount } from 'svelte';
    import type { ActSummary, ActDetail, MobileSortMode, ViewMode } from '$lib/types';
    import { listActs, getAct } from '$lib/api';
    import { appState } from '$lib/stores.svelte';
    import DayTabs from '$lib/components/DayTabs.svelte';
    import ScheduleGrid from '$lib/components/ScheduleGrid.svelte';
    import MobileSchedule from '$lib/components/MobileSchedule.svelte';
    import MySchedule from '$lib/components/MySchedule.svelte';

    const MOBILE_BREAKPOINT = 768;

    let acts = $state<ActSummary[]>([]);
    let allActs = $state<ActSummary[]>([]);
    let allActsLoaded = $state(false);
    let loading = $state(false);
    let detailAct = $state<ActDetail | null>(null);
    let detailLoading = $state(false);
    let innerWidth = $state(MOBILE_BREAKPOINT + 1);

    const isMobile = $derived(innerWidth < MOBILE_BREAKPOINT);

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
    <header class="shrink-0 bg-surface-100 border-b border-surface-300 px-4 py-2">
        <div class="flex items-center justify-between">
            <h1 class="text-xl font-bold">FQF 2026 Schedule Builder</h1>
            {#if isMobile && appState.viewMode !== 'my-schedule' && appState.viewMode !== 'merge'}
                <div class="flex gap-1">
                    {#each SORT_MODES as mode (mode.value)}
                        <button
                            class="px-2 py-1 text-xs rounded font-medium transition-colors
                                   {appState.mobileSortMode === mode.value
                                ? 'bg-primary-600 text-white'
                                : 'bg-surface-200 text-surface-700 hover:bg-surface-300'}"
                            onclick={() => (appState.mobileSortMode = mode.value)}
                        >
                            {mode.label}
                        </button>
                    {/each}
                </div>
            {/if}
        </div>

        <div class="flex gap-1 mt-2">
            {#each VIEW_TABS as tab (tab.value)}
                <button
                    class="px-3 py-1 text-sm rounded font-medium transition-colors
                           {appState.viewMode === tab.value
                        ? 'bg-primary-600 text-white'
                        : 'bg-surface-200 text-surface-700 hover:bg-surface-300'}"
                    onclick={() => (appState.viewMode = tab.value)}
                >
                    {tab.label()}
                </button>
            {/each}
        </div>
    </header>

    {#if appState.viewMode !== 'my-schedule' && appState.viewMode !== 'merge'}
        <DayTabs bind:selectedDate={appState.selectedDate} />
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
            <div class="flex items-center justify-center h-full text-surface-500">
                <p>Merge view coming soon.</p>
            </div>
        {:else if loading}
            <div class="flex items-center justify-center h-full">
                <p class="text-surface-500">Loading schedule…</p>
            </div>
        {:else if isMobile}
            <MobileSchedule
                {acts}
                picks={appState.picks}
                sortMode={appState.mobileSortMode}
                onTogglePick={(slug) => appState.togglePick(slug)}
                onActDetail={openDetail}
            />
        {:else}
            <ScheduleGrid
                {acts}
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
            class="bg-surface-50 rounded-xl shadow-xl max-w-lg w-full mx-4 p-6 relative"
            onclick={(e) => e.stopPropagation()}
            role="document"
        >
            <button
                class="absolute top-4 right-4 text-surface-500 hover:text-surface-900 text-xl leading-none"
                onclick={closeDetail}
                aria-label="Close"
            >
                ✕
            </button>

            {#if detailLoading}
                <p class="text-surface-500">Loading…</p>
            {:else if detailAct}
                <div class="flex items-start gap-3 mb-4">
                    <div class="flex-1 min-w-0">
                        <h2 class="text-xl font-bold leading-snug">{detailAct.name}</h2>
                        <p class="text-sm text-surface-500 mt-1">{detailAct.stage}</p>
                    </div>
                    <span
                        class="shrink-0 px-2 py-0.5 rounded text-xs font-medium bg-primary-100 text-primary-800"
                    >
                        {detailAct.genre}
                    </span>
                </div>

                <p class="text-sm text-surface-600 mb-4">
                    {detailAct.start}–{detailAct.end}
                </p>

                <p class="text-sm leading-relaxed whitespace-pre-line">
                    {detailAct.about || 'No bio available yet.'}
                </p>
            {/if}
        </div>
    </div>
{/if}
