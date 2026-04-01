<script lang="ts">
    import type { ActSummary } from '$lib/types';
    import { appState, type MapMode } from '$lib/stores.svelte';
    import { FESTIVAL_DATES, DAY_LABELS } from '$lib/types';
    import {
        GRID_START_HOUR,
        GRID_END_HOUR,
        MINUTES_PER_HOUR,
        SCRUBBER_STEP_MINUTES,
        FESTIVAL_START_ISO,
        CONFLICT_COLORS
    } from '$lib/constants';
    import {
        latLngToPercent,
        allStageStatuses,
        formatTimeDisplay,
        pickedActsForDay,
        buildScheduleMarkers,
        buildPathArrows,
        SCHEDULE_MARKER_PURPLE,
        formatTime12
    } from '$lib/map-utils';
    import StageMarker from '$lib/components/StageMarker.svelte';
    import MapActLabel from '$lib/components/MapActLabel.svelte';

    type MapMode = 'scroll' | 'now' | 'my-schedule';

    interface Props {
        acts: ActSummary[];
        allActs: ActSummary[];
        picks: Set<string>;
        selectedDate: string;
        stageLocations: Map<string, { lat: number; lng: number }>;
        onActDetail?: (act: ActSummary) => void;
        onDayChange?: (date: string) => void;
    }

    let { acts, allActs, picks, selectedDate, stageLocations, onActDetail, onDayChange }: Props =
        $props();

    const SCRUBBER_START = GRID_START_HOUR * MINUTES_PER_HOUR;
    const SCRUBBER_END = GRID_END_HOUR * MINUTES_PER_HOUR;
    const DEFAULT_HOUR = GRID_START_HOUR;
    const DEFAULT_TIME = DEFAULT_HOUR * MINUTES_PER_HOUR;
    const NOW_UPDATE_MS = 60_000;
    // My Schedule circle sizes (px) — first is prominent, rest subdued
    const FIRST_MARKER_SIZE = 22;
    const OTHER_MARKER_SIZE = 16;
    const FIRST_CIRCLE_FONT = 10;
    const OTHER_CIRCLE_FONT = 8;
    // My Schedule conflict borders — thinner than time-view (less prominent)
    const SCHED_BORDER_LEFT_PX = 2;
    const SCHED_BORDER_BOTTOM_PX = 1;
    const MUSIC_NOTE_STYLE =
        'background: rgba(212, 168, 67, 0.35); border: 1px solid rgba(0, 0, 0, 0.5); border-radius: 3px;';
    // Marker position offset from stage point (rem)
    const MARKER_OFFSET_REM = 0.3;
    // Stacking: vertical offset per additional act at same stage (rem)
    const STACK_VERTICAL_REM = 1.4;
    const STACK_HORIZONTAL_REM = 0.3;
    // SVG arrow layout
    const ARROW_MARKER_ID = 'fqf-path-arrow';
    const ARROW_MIDPOINT = 0.5;
    const LABEL_OFFSET_PX = 6;

    // appState.mapMode, appState.mapManualMinutes, appState.mapShowPaths live in appState to survive tab switches
    let nowMinutes = $state(DEFAULT_TIME);
    let nowInterval: ReturnType<typeof setInterval> | null = null;

    function computeNowMinutes(): number {
        const festivalStart = new Date(FESTIVAL_START_ISO);
        const now = new Date();
        if (now < festivalStart) return SCRUBBER_START;
        const minutesSinceMidnight = now.getHours() * MINUTES_PER_HOUR + now.getMinutes();
        const rounded =
            Math.floor(minutesSinceMidnight / SCRUBBER_STEP_MINUTES) * SCRUBBER_STEP_MINUTES;
        return Math.max(SCRUBBER_START, Math.min(SCRUBBER_END, rounded));
    }

    $effect(() => {
        if (appState.mapMode === 'now') {
            nowMinutes = computeNowMinutes();
            nowInterval = setInterval(() => {
                nowMinutes = computeNowMinutes();
            }, NOW_UPDATE_MS);
        }
        return () => {
            if (nowInterval) {
                clearInterval(nowInterval);
                nowInterval = null;
            }
        };
    });

    const currentMinutes = $derived(
        appState.mapMode === 'now' ? nowMinutes : appState.mapManualMinutes
    );
    const timeLabel = $derived(formatTimeDisplay(currentMinutes));

    // Scroll / Now mode — existing stage-status markers
    const statuses = $derived(
        appState.mapMode !== 'my-schedule'
            ? allStageStatuses(acts, stageLocations, currentMinutes)
            : []
    );

    // Music note markers at active stage locations (all map modes)
    const activeStagePositions = $derived.by(() => {
        const stages = new Set(acts.map((a) => a.stage));
        return [...stages]
            .filter((s) => stageLocations.has(s))
            .map((s) => ({
                stage: s,
                pos: latLngToPercent(stageLocations.get(s)!.lat, stageLocations.get(s)!.lng)
            }));
    });

    // My Schedule mode
    const orderedPicks = $derived(
        appState.mapMode === 'my-schedule'
            ? pickedActsForDay(allActs, picks, selectedDate, stageLocations)
            : []
    );
    const scheduleMarkers = $derived(
        appState.mapMode === 'my-schedule' ? buildScheduleMarkers(orderedPicks, stageLocations) : []
    );
    const pathArrows = $derived(
        appState.mapMode === 'my-schedule' && appState.mapShowPaths
            ? buildPathArrows(orderedPicks, stageLocations)
            : []
    );

    function markerLabel(order: number, act: ActSummary): string {
        return `${order}  ${formatTime12(act.start)}–${formatTime12(act.end)}  ${act.name}`;
    }

    // SVG arrow: midpoint for label placement
    function midpoint(
        from: { x: number; y: number },
        to: { x: number; y: number }
    ): { x: number; y: number } {
        return {
            x: from.x + (to.x - from.x) * ARROW_MIDPOINT,
            y: from.y + (to.y - from.y) * ARROW_MIDPOINT
        };
    }

    function formatDistanceM(meters: number): string {
        return `${Math.round(meters)}m`;
    }
</script>

<div class="flex flex-col h-full overflow-hidden">
    <!-- Control bar -->
    <div class="fqf-time-scrubber shrink-0 flex flex-col gap-2 px-4 py-2">
        <!-- Row 1: Day tabs + mode radio -->
        <div class="flex items-center gap-4 flex-wrap">
            <!-- Day selector -->
            <div class="flex gap-1">
                {#each FESTIVAL_DATES as d}
                    <button
                        class="fqf-day-tab {selectedDate === d ? 'fqf-day-tab-active' : ''}"
                        onclick={() => onDayChange?.(d)}
                    >
                        {DAY_LABELS[d]}
                    </button>
                {/each}
            </div>

            <!-- Triple radio -->
            <div class="flex items-center gap-3 text-xs" style="color: var(--mg-purple-deep);">
                {#each [{ value: 'scroll', label: 'Scroll Time' }, { value: 'now', label: 'Now' }, { value: 'my-schedule', label: 'My Schedule' }] as mode (mode.value)}
                    <label class="flex items-center gap-1 cursor-pointer select-none">
                        <input
                            type="radio"
                            name="map-mode"
                            value={mode.value}
                            checked={appState.mapMode === mode.value}
                            onchange={() => (appState.mapMode = mode.value as MapMode)}
                            class="accent-purple-700"
                        />
                        {mode.label}
                    </label>
                {/each}
            </div>
        </div>

        <!-- Row 2: time scrubber (Scroll Time only) or Show Paths (My Schedule only) -->
        {#if appState.mapMode === 'scroll'}
            <div class="flex items-center gap-3">
                <span
                    class="text-sm font-semibold shrink-0"
                    style="color: var(--mg-purple-deep); min-width: 5.5rem;"
                >
                    {timeLabel}
                </span>
                <input
                    type="range"
                    min={SCRUBBER_START}
                    max={SCRUBBER_END}
                    step={SCRUBBER_STEP_MINUTES}
                    bind:value={appState.mapManualMinutes}
                    class="flex-1"
                    aria-label="Festival time"
                />
            </div>
        {:else if appState.mapMode === 'now'}
            <span class="text-xs italic" style="color: var(--mg-green-deep); opacity: 0.7;">
                Live clock (updates every minute)
            </span>
        {:else}
            <label
                class="flex items-center gap-1.5 text-xs cursor-pointer select-none"
                style="color: var(--mg-purple-deep);"
            >
                <input
                    type="checkbox"
                    bind:checked={appState.mapShowPaths}
                    class="accent-purple-700"
                />
                Show Paths
            </label>
        {/if}
    </div>

    <!-- Map container -->
    <div class="flex-1 overflow-auto">
        <div class="relative mx-auto" style="max-width: 900px; min-width: 700px;">
            <img
                src="/fqf-map.png"
                alt="French Quarter Festival area map"
                class="w-full h-auto block"
                draggable="false"
            />

            <!-- Music note markers at active stage locations -->
            {#each activeStagePositions as { pos, stage } (stage)}
                <div
                    class="absolute -translate-x-1/2 -translate-y-1/2 pointer-events-none"
                    style="left: {pos.x}%; top: {pos.y}%;"
                >
                    <span class="text-[10px] px-0.5" style={MUSIC_NOTE_STYLE}> 🎶 </span>
                </div>
            {/each}

            {#if appState.mapMode !== 'my-schedule'}
                <!-- Scroll Time / Now: stage-status markers -->
                {#each statuses as status (status.stage)}
                    {@const loc = stageLocations.get(status.stage)}
                    {#if loc}
                        {@const pos = latLngToPercent(loc.lat, loc.lng)}
                        <div
                            class="absolute"
                            style="left: calc({pos.x}% + {MARKER_OFFSET_REM}rem); top: calc({pos.y}% + {MARKER_OFFSET_REM}rem);"
                        >
                            <StageMarker {status} {picks} {onActDetail} {allActs} />
                        </div>
                    {/if}
                {/each}
            {:else}
                <!-- My Schedule: path arrows (SVG overlay) -->
                {#if appState.mapShowPaths && pathArrows.length > 0}
                    <svg
                        class="absolute inset-0 w-full h-full pointer-events-none"
                        style="overflow: visible;"
                        aria-hidden="true"
                    >
                        <defs>
                            <marker
                                id={ARROW_MARKER_ID}
                                markerWidth="8"
                                markerHeight="8"
                                refX="4"
                                refY="2"
                                orient="auto"
                            >
                                <path d="M0,0 L0,4 L6,2 z" fill="#7c3aed" />
                            </marker>
                        </defs>
                        {#each pathArrows as arrow, i (i)}
                            {@const mid = midpoint(arrow.from, arrow.to)}
                            <line
                                x1="{arrow.from.x}%"
                                y1="{arrow.from.y}%"
                                x2="{arrow.to.x}%"
                                y2="{arrow.to.y}%"
                                stroke="#7c3aed"
                                stroke-width="2"
                                stroke-dasharray="6 3"
                                marker-end="url(#{ARROW_MARKER_ID})"
                                opacity="0.75"
                            />
                            <text
                                x="{mid.x}%"
                                y="{mid.y}%"
                                dy="-{LABEL_OFFSET_PX}"
                                text-anchor="middle"
                                font-size="9"
                                fill="#7c3aed"
                                font-weight="600"
                            >
                                {formatDistanceM(arrow.distanceMeters)}
                            </text>
                        {/each}
                    </svg>
                {/if}

                <!-- My Schedule: numbered act markers -->
                {#each scheduleMarkers as marker (marker.act.slug)}
                    {@const size = marker.isFirst ? FIRST_MARKER_SIZE : OTHER_MARKER_SIZE}
                    {@const circleBg = marker.isFirst ? SCHEDULE_MARKER_PURPLE : '#ffffff'}
                    {@const circleText = marker.isFirst ? '#ffffff' : 'var(--mg-text)'}
                    {@const circleBorder = marker.isFirst
                        ? 'none'
                        : '1.5px solid rgba(74, 26, 107, 0.35)'}
                    {@const conflictColor = CONFLICT_COLORS[marker.conflict]}
                    {@const borderStyle = `border-left: ${SCHED_BORDER_LEFT_PX}px solid ${conflictColor}; border-bottom: ${SCHED_BORDER_BOTTOM_PX}px solid ${conflictColor};`}
                    <div
                        class="absolute"
                        style="left: calc({marker.pos
                            .x}% + {MARKER_OFFSET_REM}rem + {marker.stageOffset *
                            STACK_HORIZONTAL_REM}rem); top: calc({marker.pos
                            .y}% + {MARKER_OFFSET_REM}rem + {marker.stageOffset *
                            STACK_VERTICAL_REM}rem);"
                    >
                        <MapActLabel
                            name={marker.act.name}
                            fleurFill={CONFLICT_COLORS.none}
                            {borderStyle}
                            isPicked={true}
                            title={markerLabel(marker.order, marker.act)}
                            onclick={(e) => {
                                e.stopPropagation();
                                onActDetail?.(marker.act);
                            }}
                        >
                            {#snippet prefix()}
                                <div
                                    class="flex items-center justify-center rounded-full shrink-0 font-bold"
                                    style="width: {size}px; height: {size}px; background: {circleBg}; color: {circleText}; font-size: {marker.isFirst
                                        ? FIRST_CIRCLE_FONT
                                        : OTHER_CIRCLE_FONT}px; border: {circleBorder}; box-shadow: 0 1px 3px rgba(0,0,0,0.2);"
                                >
                                    {marker.order}
                                </div>
                                <span
                                    class="text-[9px] shrink-0"
                                    style="color: var(--mg-purple-deep);"
                                >
                                    {formatTime12(marker.act.start)}–{formatTime12(marker.act.end)}
                                </span>
                            {/snippet}
                        </MapActLabel>
                    </div>
                {/each}

                {#if scheduleMarkers.length === 0}
                    <div
                        class="absolute inset-0 flex items-center justify-center pointer-events-none"
                    >
                        <p
                            class="text-sm px-4 py-2 rounded"
                            style="background: rgba(255,255,255,0.85); color: var(--mg-purple-deep);"
                        >
                            No picks for this day yet.
                        </p>
                    </div>
                {/if}
            {/if}
        </div>
    </div>
</div>
