<script lang="ts">
    import { appState } from '$lib/stores.svelte';

    let { genres, stages }: { genres: string[]; stages: string[] } = $props();

    let expanded = $state(false);

    const sortedGenres = $derived([...genres].sort());
    const sortedStages = $derived([...stages].sort());
</script>

<div class="border-b border-surface-300 bg-surface-50">
    <div class="flex items-center gap-3 px-4 py-2">
        <button
            class="text-sm font-medium text-surface-700 hover:text-surface-900 transition-colors"
            onclick={() => (expanded = !expanded)}
            aria-expanded={expanded}
        >
            Filters {expanded ? '▲' : '▼'}
        </button>

        {#if !expanded}
            <label
                class="flex items-center gap-1.5 text-sm text-surface-600 cursor-pointer select-none"
            >
                <input
                    type="checkbox"
                    checked={appState.showAll}
                    onchange={() => (appState.showAll = !appState.showAll)}
                    class="accent-primary-600"
                />
                Show All
            </label>
        {/if}

        {#if !appState.showAll && (appState.hiddenGenres.size > 0 || appState.hiddenStages.size > 0)}
            <span class="text-xs text-warning-600 font-medium">
                {appState.hiddenGenres.size + appState.hiddenStages.size} filter(s) active
            </span>
        {/if}
    </div>

    {#if expanded}
        <div class="px-4 pb-3 flex gap-8">
            <!-- Genres column -->
            <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-2">
                    <p class="text-xs font-semibold text-surface-500 uppercase tracking-wide">
                        Genres
                    </p>
                    <label
                        class="flex items-center gap-1 text-xs text-surface-600 cursor-pointer select-none ml-auto"
                    >
                        <input
                            type="checkbox"
                            checked={appState.showAll}
                            onchange={() => (appState.showAll = !appState.showAll)}
                            class="accent-primary-600"
                        />
                        Show All
                    </label>
                </div>
                <div class="flex flex-col gap-0.5">
                    {#each sortedGenres as genre (genre)}
                        <label
                            class="flex items-center gap-1.5 text-sm text-surface-700 cursor-pointer select-none hover:text-surface-900"
                        >
                            <input
                                type="checkbox"
                                checked={!appState.hiddenGenres.has(genre)}
                                onchange={() => appState.toggleGenre(genre)}
                                disabled={appState.showAll}
                                class="accent-primary-600"
                            />
                            {genre}
                        </label>
                    {/each}
                </div>
            </div>

            <!-- Stages column -->
            <div class="flex-1 min-w-0">
                <p class="text-xs font-semibold text-surface-500 uppercase tracking-wide mb-2">
                    Stages
                </p>
                <div class="flex flex-col gap-0.5">
                    {#each sortedStages as stage (stage)}
                        <label
                            class="flex items-center gap-1.5 text-sm text-surface-700 cursor-pointer select-none hover:text-surface-900"
                        >
                            <input
                                type="checkbox"
                                checked={!appState.hiddenStages.has(stage)}
                                onchange={() => appState.toggleStage(stage)}
                                disabled={appState.showAll}
                                class="accent-primary-600"
                            />
                            {stage}
                        </label>
                    {/each}
                </div>
            </div>
        </div>
    {/if}
</div>
