<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';
    import {
        PIXELS_PER_MINUTE,
        GRID_START_HOUR,
        GRID_END_HOUR,
        GRID_COLUMN_MIN_WIDTH
    } from '$lib/constants';
    import { timeToMinutes, getWorstConflict } from '$lib/conflict';
    import ActBlock from './ActBlock.svelte';

    // Big mode bumps the stage column min-width and the visibility thresholds
    // so the larger fonts don't trip the existing truncation/clipping logic.
    // Vertical density (PIXELS_PER_MINUTE) intentionally stays the same so the
    // overall scroll length of the grid doesn't shift.
    const BIG_COLUMN_MIN_WIDTH = 180;
    const BIG_MIN_HEIGHT_FOR_TIME = 60;
    const BIG_MIN_HEIGHT_FOR_GENRE = 78;
    const BIG_MIN_HEIGHT_FOR_CONFLICT = 84;
    const BIG_PICK_BUTTON_SIZE = 18;
    const SMALL_MIN_HEIGHT_FOR_TIME = 50;
    const SMALL_MIN_HEIGHT_FOR_GENRE = 65;
    const SMALL_MIN_HEIGHT_FOR_CONFLICT = 70;
    const SMALL_PICK_BUTTON_SIZE = 14;

    interface Props {
        acts: ActSummary[];
        picks: Set<string>;
        maybes: Set<string>;
        displayBig?: boolean;
        onTogglePick: (slug: string) => void;
        onToggleMaybe: (slug: string) => void;
        onActDetail: (act: ActSummary) => void;
        readOnly?: boolean;
    }

    let {
        acts,
        picks,
        maybes,
        displayBig = false,
        onTogglePick,
        onToggleMaybe,
        onActDetail,
        readOnly = false
    }: Props = $props();

    const colMinWidth = $derived(displayBig ? BIG_COLUMN_MIN_WIDTH : GRID_COLUMN_MIN_WIDTH);
    const minHeightForTime = $derived(
        displayBig ? BIG_MIN_HEIGHT_FOR_TIME : SMALL_MIN_HEIGHT_FOR_TIME
    );
    const minHeightForGenre = $derived(
        displayBig ? BIG_MIN_HEIGHT_FOR_GENRE : SMALL_MIN_HEIGHT_FOR_GENRE
    );
    const minHeightForConflict = $derived(
        displayBig ? BIG_MIN_HEIGHT_FOR_CONFLICT : SMALL_MIN_HEIGHT_FOR_CONFLICT
    );
    const pickButtonSize = $derived(displayBig ? BIG_PICK_BUTTON_SIZE : SMALL_PICK_BUTTON_SIZE);

    const GRID_START_MINUTES = GRID_START_HOUR * 60;
    const GRID_END_MINUTES = GRID_END_HOUR * 60;
    const GRID_HEIGHT = (GRID_END_MINUTES - GRID_START_MINUTES) * PIXELS_PER_MINUTE;
    const TIME_LABEL_INTERVAL = 30;
    const TIME_LABEL_WIDTH = 48;

    // Build time label rows at 30-minute intervals
    const timeLabels = $derived.by(() => {
        const labels: { label: string; top: number }[] = [];
        for (let min = GRID_START_MINUTES; min <= GRID_END_MINUTES; min += TIME_LABEL_INTERVAL) {
            const h = Math.floor(min / 60);
            const m = min % 60;
            const suffix = h >= 12 ? 'pm' : 'am';
            const displayH = h > 12 ? h - 12 : h;
            const label =
                m === 0 ? `${displayH}${suffix}` : `${displayH}:${String(m).padStart(2, '0')}`;
            const top = (min - GRID_START_MINUTES) * PIXELS_PER_MINUTE;
            labels.push({ label, top });
        }
        return labels;
    });

    // Group acts by stage, preserving first-seen order
    const stageColumns = $derived.by(() => {
        const order: string[] = [];
        const byStage = new Map<string, ActSummary[]>();
        for (const act of acts) {
            if (!byStage.has(act.stage)) {
                order.push(act.stage);
                byStage.set(act.stage, []);
            }
            byStage.get(act.stage)!.push(act);
        }
        return order.map((stage) => ({ stage, acts: byStage.get(stage)! }));
    });

    function actTop(act: ActSummary): number {
        return (timeToMinutes(act.start) - GRID_START_MINUTES) * PIXELS_PER_MINUTE;
    }

    function actHeight(act: ActSummary): number {
        const start = Math.max(timeToMinutes(act.start), GRID_START_MINUTES);
        const end = Math.min(timeToMinutes(act.end), GRID_END_MINUTES);
        return Math.max((end - start) * PIXELS_PER_MINUTE, 20);
    }

    function conflictLevel(act: ActSummary): ConflictLevel {
        if (!picks.has(act.slug)) return 'none';
        return getWorstConflict(act, acts, picks);
    }
</script>

<div class="flex overflow-auto h-full">
    <!-- Time labels: sticky left -->
    <div
        class="sticky left-0 z-20 fqf-time-col shrink-0 border-r border-surface-300"
        style="width: {TIME_LABEL_WIDTH}px;"
    >
        <!-- Spacer matching sticky stage header height -->
        <div class="h-14 border-b border-surface-300"></div>
        <!-- Time axis -->
        <div class="relative" style="height: {GRID_HEIGHT}px;">
            {#each timeLabels as { label, top }}
                <span
                    class="absolute right-2 text-xs font-medium fqf-time-label -translate-y-2"
                    style="top: {top}px;"
                >
                    {label}
                </span>
            {/each}
        </div>
    </div>

    <!-- Stage columns -->
    <div class="flex flex-1">
        {#each stageColumns as { stage, acts: stageActs }}
            <div class="shrink-0 border-r border-surface-200" style="min-width: {colMinWidth}px;">
                <!-- Stage header: sticky top -->
                <div
                    class="sticky top-0 z-10 h-14 flex items-center justify-center px-2
                           fqf-stage-header border-b border-surface-300 text-center"
                >
                    <span class="text-xs font-bold leading-tight line-clamp-2">{stage}</span>
                </div>

                <!-- Act blocks -->
                <div class="relative fqf-grid-bg" style="height: {GRID_HEIGHT}px;">
                    {#each stageActs as act (act.slug)}
                        <ActBlock
                            {act}
                            top={actTop(act)}
                            height={actHeight(act)}
                            isPicked={picks.has(act.slug)}
                            isMaybe={maybes.has(act.slug)}
                            conflictLevel={conflictLevel(act)}
                            allActs={acts}
                            {picks}
                            {minHeightForTime}
                            {minHeightForGenre}
                            {minHeightForConflict}
                            {pickButtonSize}
                            onToggle={() => onTogglePick(act.slug)}
                            onToggleMaybe={() => onToggleMaybe(act.slug)}
                            onDetail={() => onActDetail(act)}
                            {readOnly}
                        />
                    {/each}
                </div>
            </div>
        {/each}
    </div>
</div>
