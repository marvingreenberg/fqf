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

    const hasActiveFilters = $derived(
        !appState.showAll && (appState.hiddenGenres.size > 0 || appState.hiddenStages.size > 0)
    );

    const hiddenSelectionCount = $derived(
        hasActiveFilters
            ? acts.filter(
                  (a) =>
                      appState.isSelected(a.slug) &&
                      (appState.hiddenGenres.has(a.genre) || appState.hiddenStages.has(a.stage))
              ).length
            : 0
    );

    const showOverrideControls = $derived(hasActiveFilters && hiddenSelectionCount > 0);
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
        {#if appState.hiddenGenres.size || appState.hiddenStages.size}
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
            {#if showOverrideControls}
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
                <span class="text-xs font-medium" style="color: var(--mg-gold-rich);">
                    Hides {hiddenSelectionCount} selection{hiddenSelectionCount === 1 ? '' : 's'}
                </span>
            {/if}
            {#if !appState.showAll && !showOverrideControls}
                <span class="text-xs font-medium" style="color: var(--mg-gold-rich);">
                    {appState.hiddenGenres.size + appState.hiddenStages.size} filter(s) active
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
