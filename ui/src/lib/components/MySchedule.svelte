<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';
    import { DAY_LABELS } from '$lib/types';
    import { getWorstConflict, getConflictBetweenActs } from '$lib/conflict';
    import { CONFLICT_COLORS } from '$lib/constants';
    import {
        walkingDistanceMeters,
        formatDistance,
        shortenStageName,
        distanceStyle
    } from '$lib/distance';

    interface Props {
        allActs: ActSummary[];
        picks: Set<string>;
        stageLocations: Map<string, { lat: number; lng: number }>;
        onTogglePick: (slug: string) => void;
        onActDetail: (act: ActSummary) => void;
    }

    let { allActs, picks, stageLocations, onTogglePick, onActDetail }: Props = $props();

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

    interface DistanceEntry {
        distance: number;
        fromStage: string;
    }

    const distanceInfo = $derived.by(() => {
        const info = new Map<string, DistanceEntry>();
        if (stageLocations.size === 0) return info;
        for (const group of groupedByDay) {
            let anchor: ActSummary | null = null;
            for (let i = 0; i < group.acts.length; i++) {
                if (i === 0) {
                    anchor = group.acts[0];
                    continue;
                }
                const prev = group.acts[i - 1];
                const curr = group.acts[i];
                const conflict = getConflictBetweenActs(prev, curr);
                const refAct = conflict === 'red' ? anchor : prev;
                if (!refAct || refAct.stage === curr.stage) {
                    if (conflict !== 'red') anchor = curr;
                    continue;
                }
                const from = stageLocations.get(refAct.stage);
                const to = stageLocations.get(curr.stage);
                if (from && to) {
                    const dist = walkingDistanceMeters(from.lat, from.lng, to.lat, to.lng);
                    info.set(curr.slug, { distance: dist, fromStage: refAct.stage });
                }
                if (conflict !== 'red') anchor = curr;
            }
        }
        return info;
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
        yellow: 'background: rgba(212,168,67,0.2); color: #7a5a00; border: 1px solid rgba(212,168,67,0.5);',
        red: 'background: rgba(220,38,38,0.12); color: #991b1b; border: 1px solid rgba(220,38,38,0.3);'
    };
</script>

<div class="flex flex-col overflow-y-auto h-full">
    {#if pickedActs.length === 0}
        <div
            class="flex flex-col items-center justify-center h-full gap-2"
            style="color: rgba(74, 26, 107, 0.5);"
        >
            <p class="text-lg font-medium">No acts picked yet</p>
            <p class="text-sm">Use the All Acts view to add acts to your schedule.</p>
        </div>
    {:else}
        {#each groupedByDay as group (group.date)}
            <div class="sticky top-0 z-10 fqf-group-header px-3 py-1.5">
                <span>{DAY_LABELS[group.date] ?? group.date}</span>
            </div>

            {#each group.acts as act (act.slug)}
                <!-- svelte-ignore a11y_no_static_element_interactions -->
                <!-- svelte-ignore a11y_click_events_have_key_events -->
                <div
                    class="fqf-list-row flex items-center gap-3 px-3 py-2.5 border-l-4"
                    style="border-left-color: {conflictColor(act)};"
                    onclick={() => onActDetail(act)}
                >
                    <button
                        class="fqf-fleur shrink-0"
                        style="width: 1.25rem; height: 1.25rem;"
                        onclick={(e) => {
                            e.stopPropagation();
                            onTogglePick(act.slug);
                        }}
                        aria-label="Remove {act.name} from picks"
                    >
                        <!-- Always picked in this view — show filled gold fleur-de-lis -->
                        <svg viewBox="0 0 16 16" width="18" height="18" fill="var(--mg-gold-rich)">
                            <path
                                d="M8 0C8 0 6.5 3.5 6.5 5.5C6.5 7 7 8 8 9C9 8 9.5 7 9.5 5.5C9.5 3.5 8 0 8 0ZM4.5 6C2.5 6 0 7.5 0 7.5C0 7.5 2 9 4.5 9C5.5 9 6.5 8.5 7 8C6 7.5 5.5 7 4.5 6ZM11.5 6C10.5 7 10 7.5 9 8C9.5 8.5 10.5 9 11.5 9C14 9 16 7.5 16 7.5C16 7.5 13.5 6 11.5 6ZM8 10C7 10 5 10.5 5 12C5 14 8 16 8 16C8 16 11 14 11 12C11 10.5 9 10 8 10Z"
                            />
                        </svg>
                    </button>

                    <div class="flex-1 min-w-0">
                        <p class="text-sm font-semibold truncate">{act.name}</p>
                        <p class="text-xs truncate" style="color: rgba(74, 26, 107, 0.5);">
                            {act.stage} &middot; {act.start}–{act.end}
                        </p>
                        {#if distanceInfo.has(act.slug)}
                            {@const d = distanceInfo.get(act.slug)!}
                            <p class="text-[10px] mt-0.5" style={distanceStyle(d.distance)}>
                                {formatDistance(d.distance)} from {shortenStageName(d.fromStage)}
                            </p>
                        {/if}
                    </div>

                    <div class="shrink-0 flex items-center gap-1.5">
                        {#if hasConflict(act)}
                            {@const level = conflictLevel(act)}
                            {#if level !== 'none'}
                                <span
                                    class="px-1.5 py-0.5 rounded text-xs font-medium"
                                    style={CONFLICT_BADGE_COLORS[level]}
                                >
                                    conflict
                                </span>
                            {/if}
                        {/if}
                        <span class="text-xs italic" style="color: rgba(74, 26, 107, 0.45);">
                            {act.genre}
                        </span>
                    </div>
                </div>
            {/each}
        {/each}
    {/if}
</div>
