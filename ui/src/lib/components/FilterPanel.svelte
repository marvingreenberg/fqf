<script lang="ts">
    import { appState } from '$lib/stores.svelte';
    import type { ActSummary } from '$lib/types';

    let {
        genres,
        stages,
        acts = []
    }: { genres: string[]; stages: string[]; acts?: ActSummary[] } = $props();

    let expanded = $state(false);

    const sortedGenres = $derived([...genres].sort());
    const sortedStages = $derived(stages);

    const hasFilters = $derived(appState.hiddenGenres.size > 0 || appState.hiddenStages.size > 0);

    const hiddenSelectionCount = $derived(
        hasFilters && !appState.showAll
            ? acts.filter((a) => appState.isSelected(a.slug) && !appState.isActVisible(a)).length
            : 0
    );
</script>

<div class="fqf-filter-panel border-b">
    <div class="flex items-center gap-3 px-4 py-2">
        <button
            class="text-sm font-medium transition-colors"
            style="color: var(--mg-purple-deep);"
            onclick={() => (expanded = !expanded)}
            aria-expanded={expanded}
        >
            Filters {expanded ? '▲' : '▼'}
        </button>
        {#if hasFilters}
            <label
                class="flex items-center gap-1.5 text-sm cursor-pointer select-none"
                style="color: rgba(74, 26, 107, 0.65);"
            >
                <input
                    type="checkbox"
                    checked={appState.showAll}
                    onchange={() => (appState.showAll = !appState.showAll)}
                    class="shrink-0"
                />
                Show All
            </label>
            <label
                class="flex items-center gap-1.5 text-sm cursor-pointer select-none"
                style="color: rgba(74, 26, 107, 0.65);"
            >
                <input
                    type="checkbox"
                    checked={appState.showSelected}
                    onchange={() => (appState.showSelected = !appState.showSelected)}
                    class="shrink-0"
                />
                Show Selected
            </label>
            <span class="text-xs font-medium fqf-filter-warning">
                {appState.hiddenGenres.size + appState.hiddenStages.size} filter(s) active
            </span>
            {#if hiddenSelectionCount}
                <span class="text-xs font-medium fqf-filter-warning">
                    - {hiddenSelectionCount} selection(s) hidden
                </span>
            {/if}
        {/if}
    </div>

    {#if expanded}
        <div class="px-4 pb-3 flex gap-8">
            <!-- Genres column -->
            <div class="flex-1 min-w-0">
                <p class="fqf-filter-section-label mb-2">Genres</p>
                <div class="flex flex-col gap-0.5">
                    {#each sortedGenres as genre (genre)}
                        <label
                            class="flex items-center gap-1.5 text-sm cursor-pointer select-none"
                            style="color: var(--mg-text);"
                        >
                            <input
                                type="checkbox"
                                checked={!appState.hiddenGenres.has(genre)}
                                onchange={() => appState.toggleGenre(genre)}
                                disabled={appState.showAll}
                                class="shrink-0"
                            />
                            {genre}
                        </label>
                    {/each}
                </div>
            </div>

            <!-- Stages column -->
            <div class="flex-1 min-w-0">
                <p class="fqf-filter-section-label mb-2">Stages</p>
                <div class="flex flex-col gap-0.5">
                    {#each sortedStages as stage (stage)}
                        <label
                            class="flex items-center gap-1.5 text-sm cursor-pointer select-none"
                            style="color: var(--mg-text);"
                        >
                            <input
                                type="checkbox"
                                checked={!appState.hiddenStages.has(stage)}
                                onchange={() => appState.toggleStage(stage)}
                                disabled={appState.showAll}
                                class="shrink-0"
                            />
                            {stage}
                        </label>
                    {/each}
                </div>
            </div>
        </div>
    {/if}
</div>
