<script lang="ts">
    import type { ActSummary } from '$lib/types';
    import { FESTIVAL_DATES, DAY_LABELS } from '$lib/types';
    import {
        GRID_START_HOUR,
        GRID_END_HOUR,
        MINUTES_PER_HOUR,
        SCRUBBER_STEP_MINUTES,
        FESTIVAL_START_ISO
    } from '$lib/constants';
    import {
        latLngToPercent,
        allStageStatuses,
        formatTimeDisplay,
        pickedActsForDay,
        buildScheduleMarkers,
        buildPathArrows,
        markerFillColor,
        formatTime12
    } from '$lib/map-utils';
    import StageMarker from '$lib/components/StageMarker.svelte';

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
    const DEFAULT_HOUR = 12;
    const DEFAULT_TIME = DEFAULT_HOUR * MINUTES_PER_HOUR;
    const NOW_UPDATE_MS = 60_000;
    // Marker sizes in CSS px
    const FIRST_MARKER_SIZE = 28;
    const OTHER_MARKER_SIZE = 20;
    // SVG arrow layout
    const ARROW_MARKER_ID = 'fqf-path-arrow';
    const ARROW_MIDPOINT = 0.5;
    const LABEL_OFFSET_PX = 6;

    let mapMode = $state<MapMode>('scroll');
    let manualMinutes = $state(DEFAULT_TIME);
    let showPaths = $state(false);
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
        if (mapMode === 'now') {
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

    const currentMinutes = $derived(mapMode === 'now' ? nowMinutes : manualMinutes);
    const timeLabel = $derived(formatTimeDisplay(currentMinutes));

    // Scroll / Now mode — existing stage-status markers
    const statuses = $derived(
        mapMode !== 'my-schedule' ? allStageStatuses(acts, stageLocations, currentMinutes) : []
    );

    // My Schedule mode
    const orderedPicks = $derived(
        mapMode === 'my-schedule'
            ? pickedActsForDay(allActs, picks, selectedDate, stageLocations)
            : []
    );
    const scheduleMarkers = $derived(
        mapMode === 'my-schedule' ? buildScheduleMarkers(orderedPicks, stageLocations) : []
    );
    const pathArrows = $derived(
        mapMode === 'my-schedule' && showPaths ? buildPathArrows(orderedPicks, stageLocations) : []
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
                            checked={mapMode === mode.value}
                            onchange={() => (mapMode = mode.value as MapMode)}
                            class="accent-purple-700"
                        />
                        {mode.label}
                    </label>
                {/each}
            </div>
        </div>

        <!-- Row 2: time scrubber (Scroll Time only) or Show Paths (My Schedule only) -->
        {#if mapMode === 'scroll'}
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
                    bind:value={manualMinutes}
                    class="flex-1"
                    aria-label="Festival time"
                />
            </div>
        {:else if mapMode === 'now'}
            <span class="text-xs italic" style="color: var(--mg-green-deep); opacity: 0.7;">
                Live clock (updates every minute)
            </span>
        {:else}
            <label
                class="flex items-center gap-1.5 text-xs cursor-pointer select-none"
                style="color: var(--mg-purple-deep);"
            >
                <input type="checkbox" bind:checked={showPaths} class="accent-purple-700" />
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

            {#if mapMode !== 'my-schedule'}
                <!-- Scroll Time / Now: existing stage-status markers -->
                {#each statuses as status (status.stage)}
                    {@const loc = stageLocations.get(status.stage)}
                    {#if loc}
                        {@const pos = latLngToPercent(loc.lat, loc.lng)}
                        <StageMarker
                            {status}
                            {onActDetail}
                            style="left: {pos.x}%; top: {pos.y}%;"
                        />
                    {/if}
                {/each}
            {:else}
                <!-- My Schedule: path arrows (SVG overlay) -->
                {#if showPaths && pathArrows.length > 0}
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
                    {@const fill = markerFillColor(marker.isFirst, marker.conflict)}
                    <!-- svelte-ignore a11y_click_events_have_key_events -->
                    <!-- svelte-ignore a11y_no_static_element_interactions -->
                    <div
                        class="absolute -translate-x-1/2 -translate-y-full cursor-pointer"
                        style="left: {marker.pos.x}%; top: {marker.pos.y}%;"
                        onclick={(e) => {
                            e.stopPropagation();
                            onActDetail?.(marker.act);
                        }}
                        title={markerLabel(marker.order, marker.act)}
                    >
                        <div class="flex items-center gap-1 fqf-map-marker fqf-map-act-row">
                            <!-- Numbered circle -->
                            <div
                                class="flex items-center justify-center rounded-full shrink-0 font-bold text-white"
                                style="width: {size}px; height: {size}px; background: {fill}; font-size: {marker.isFirst
                                    ? 12
                                    : 10}px; box-shadow: 0 1px 4px rgba(0,0,0,0.35);"
                            >
                                {marker.order}
                            </div>
                            <!-- Label: time range + name -->
                            <span
                                class="text-[9px] font-medium truncate"
                                style="max-width: 120px; color: var(--mg-text);"
                            >
                                {formatTime12(marker.act.start)}–{formatTime12(marker.act.end)}
                                {marker.act.name}
                            </span>
                        </div>
                        <div class="fqf-map-pin"></div>
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
