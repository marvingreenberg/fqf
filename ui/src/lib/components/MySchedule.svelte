<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';
    import { DAY_LABELS } from '$lib/types';
    import { getWorstConflict, getConflictBetweenActs } from '$lib/conflict';
    import { CONFLICT_COLORS } from '$lib/constants';
    import { isPicked as _isPicked, isSelected } from '$lib/picks';
    import {
        walkingDistanceMeters,
        formatDistance,
        shortenStageName,
        distanceStyle
    } from '$lib/distance';
    import ActRow from './ActRow.svelte';

    interface Props {
        allActs: ActSummary[];
        picks: Set<string>;
        maybes: Set<string>;
        stageLocations: Map<string, { lat: number; lng: number }>;
        onTogglePick: (slug: string) => void;
        onToggleMaybe: (slug: string) => void;
        onActDetail: (act: ActSummary) => void;
        readOnly?: boolean;
    }

    let {
        allActs,
        picks,
        maybes,
        stageLocations,
        onTogglePick,
        onToggleMaybe,
        onActDetail,
        readOnly = false
    }: Props = $props();

    const pickedActs = $derived(
        allActs
            .filter((act) => isSelected(act.slug, picks))
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
            // Only picked (not maybe) acts participate in the distance chain.
            const pickedOnly = group.acts.filter((a) => _isPicked(a.slug, picks));
            let anchor: ActSummary | null = null;
            for (let i = 0; i < pickedOnly.length; i++) {
                if (i === 0) {
                    anchor = pickedOnly[0];
                    continue;
                }
                const prev = pickedOnly[i - 1];
                const curr = pickedOnly[i];
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

    const NO_CONFLICT: ConflictLevel = 'none';

    function conflictLevel(act: ActSummary): ConflictLevel {
        if (!_isPicked(act.slug, picks)) return NO_CONFLICT;
        return getWorstConflict(act, allActs, picks);
    }

    function conflictColor(act: ActSummary): string {
        return CONFLICT_COLORS[conflictLevel(act)];
    }

    function hasConflict(act: ActSummary): boolean {
        return conflictLevel(act) !== NO_CONFLICT;
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
            {#if !readOnly}
                <p class="text-sm">Use the All Acts view to add acts to your schedule.</p>
            {/if}
        </div>
    {:else}
        {#each groupedByDay as group (group.date)}
            <div class="sticky top-0 z-10 fqf-group-header px-3 py-1.5">
                <span>{DAY_LABELS[group.date] ?? group.date}</span>
            </div>

            {#each group.acts as act (act.slug)}
                <ActRow
                    {act}
                    isPicked={_isPicked(act.slug, picks)}
                    isMaybe={maybes.has(act.slug)}
                    conflictColor={conflictColor(act)}
                    {readOnly}
                    {onTogglePick}
                    {onToggleMaybe}
                    {onActDetail}
                >
                    {#snippet extraMain()}
                        {#if distanceInfo.has(act.slug)}
                            {@const d = distanceInfo.get(act.slug)!}
                            <p class="text-[10px] mt-0.5" style={distanceStyle(d.distance)}>
                                {formatDistance(d.distance)} from {shortenStageName(d.fromStage)}
                            </p>
                        {/if}
                    {/snippet}
                    {#snippet extra()}
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
                    {/snippet}
                </ActRow>
            {/each}
        {/each}
    {/if}
</div>
