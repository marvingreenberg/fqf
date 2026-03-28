<script lang="ts">
    import { onMount } from 'svelte';
    import type { ActSummary, ActDetail } from '$lib/types';
    import { listActs, getAct } from '$lib/api';
    import { appState } from '$lib/stores.svelte';
    import DayTabs from '$lib/components/DayTabs.svelte';
    import ScheduleGrid from '$lib/components/ScheduleGrid.svelte';

    let acts = $state<ActSummary[]>([]);
    let loading = $state(false);
    let detailAct = $state<ActDetail | null>(null);
    let detailLoading = $state(false);

    async function loadActs(date: string): Promise<void> {
        loading = true;
        try {
            const resp = await listActs({ date });
            acts = resp.acts;
        } finally {
            loading = false;
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

    $effect(() => {
        loadActs(appState.selectedDate);
    });

    onMount(() => {
        loadActs(appState.selectedDate);
    });
</script>

<div class="flex flex-col h-screen overflow-hidden">
    <header class="shrink-0 bg-surface-100 border-b border-surface-300 px-4 py-2">
        <h1 class="text-xl font-bold">FQF 2026 Schedule Builder</h1>
    </header>

    <DayTabs bind:selectedDate={appState.selectedDate} />

    <div class="flex-1 overflow-hidden relative">
        {#if loading}
            <div class="flex items-center justify-center h-full">
                <p class="text-surface-500">Loading schedule…</p>
            </div>
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
