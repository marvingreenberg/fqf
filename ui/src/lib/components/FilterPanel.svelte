<script lang="ts">
    import { appState } from '$lib/stores.svelte';

    let { genres, stages }: { genres: string[]; stages: string[] } = $props();

    let expanded = $state(false);

    const sortedGenres = $derived([...genres].sort());
    const sortedStages = $derived(stages);
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
            {#if !appState.showAll}
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
            <div class="flex items-center gap-2 mb-2">
                <p class="fqf-filter-section-label">Genres</p>
            </div>
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
