<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';
    import { DAY_LABELS } from '$lib/types';
    import { getWorstConflict } from '$lib/conflict';
    import { CONFLICT_COLORS } from '$lib/constants';

    interface Props {
        allActs: ActSummary[];
        picks: Set<string>;
        onTogglePick: (slug: string) => void;
        onActDetail: (act: ActSummary) => void;
    }

    let { allActs, picks, onTogglePick, onActDetail }: Props = $props();

    const pickedActs = $derived(
        allActs
            .filter((act) => picks.has(act.slug))
            .sort((a, b) => a.date.localeCompare(b.date) || a.start.localeCompare(b.start))
    );

    const groupedByDay = $derived.by(() => {
        const byDate = new Map<string, ActSummary[]>();
        for (const act of pickedActs) {
            if (!byDate.has(act.date)) byDate.set(act.date, []);
            byDate.get(act.date)!.push(act);
        }
        return [...byDate.entries()].map(([date, acts]) => ({ date, acts }));
    });

    function conflictLevel(act: ActSummary): ConflictLevel {
        return getWorstConflict(act, allActs, picks);
    }

    function conflictColor(act: ActSummary): string {
        return CONFLICT_COLORS[conflictLevel(act)];
    }

    function hasConflict(act: ActSummary): boolean {
        return conflictLevel(act) !== 'none';
    }

    const CONFLICT_BADGE_COLORS: Record<Exclude<ConflictLevel, 'none'>, string> = {
        yellow: 'bg-yellow-100 text-yellow-800',
        red: 'bg-red-100 text-red-800'
    };
</script>

<div class="flex flex-col overflow-y-auto h-full">
    {#if pickedActs.length === 0}
        <div class="flex flex-col items-center justify-center h-full text-surface-500 gap-2">
            <p class="text-lg font-medium">No acts picked yet</p>
            <p class="text-sm">Use the All Acts view to add acts to your schedule.</p>
        </div>
    {:else}
        {#each groupedByDay as group (group.date)}
            <div class="sticky top-0 z-10 bg-surface-200 px-3 py-1.5 border-b border-surface-300">
                <span class="text-xs font-bold uppercase tracking-wider text-surface-600">
                    {DAY_LABELS[group.date] ?? group.date}
                </span>
            </div>

            {#each group.acts as act (act.slug)}
                <!-- svelte-ignore a11y_no_static_element_interactions -->
                <!-- svelte-ignore a11y_click_events_have_key_events -->
                <div
                    class="flex items-center gap-3 px-3 py-2.5 border-b border-surface-200
                           hover:bg-surface-100 transition-colors border-l-4"
                    style="border-left-color: {conflictColor(act)};"
                    onclick={() => onActDetail(act)}
                >
                    <button
                        class="shrink-0 w-5 h-5 rounded border border-primary-400 bg-primary-50
                               flex items-center justify-center hover:bg-primary-100 transition-colors"
                        onclick={(e) => {
                            e.stopPropagation();
                            onTogglePick(act.slug);
                        }}
                        aria-label="Remove {act.name} from picks"
                    >
                        <svg class="w-3 h-3 text-primary-600" viewBox="0 0 12 12" fill="none">
                            <path
                                d="M10 3L5 8.5 2 5.5"
                                stroke="currentColor"
                                stroke-width="1.5"
                                stroke-linecap="round"
                            />
                        </svg>
                    </button>

                    <div class="flex-1 min-w-0">
                        <p class="text-sm font-semibold truncate">{act.name}</p>
                        <p class="text-xs text-surface-500 truncate">
                            {act.stage} &middot; {act.start}–{act.end}
                        </p>
                    </div>

                    <div class="shrink-0 flex items-center gap-1.5">
                        {#if hasConflict(act)}
                            {@const level = conflictLevel(act)}
                            {#if level !== 'none'}
                                <span
                                    class="px-1.5 py-0.5 rounded text-xs font-medium {CONFLICT_BADGE_COLORS[
                                        level
                                    ]}"
                                >
                                    conflict
                                </span>
                            {/if}
                        {/if}
                        <span class="text-xs text-surface-400 italic">{act.genre}</span>
                    </div>
                </div>
            {/each}
        {/each}
    {/if}
</div>
