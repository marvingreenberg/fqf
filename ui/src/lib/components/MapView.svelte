<script lang="ts">
    import type { ActSummary } from '$lib/types';
    import {
        GRID_START_HOUR,
        GRID_END_HOUR,
        MINUTES_PER_HOUR,
        SCRUBBER_STEP_MINUTES,
        FESTIVAL_START_ISO
    } from '$lib/constants';
    import { latLngToPercent, allStageStatuses, formatTimeDisplay } from '$lib/map-utils';
    import StageMarker from '$lib/components/StageMarker.svelte';

    interface Props {
        acts: ActSummary[];
        stageLocations: Map<string, { lat: number; lng: number }>;
        onActDetail?: (act: ActSummary) => void;
    }

    let { acts, stageLocations, onActDetail }: Props = $props();

    const SCRUBBER_START = GRID_START_HOUR * MINUTES_PER_HOUR;
    const SCRUBBER_END = GRID_END_HOUR * MINUTES_PER_HOUR;
    const DEFAULT_HOUR = 12;
    const DEFAULT_TIME = DEFAULT_HOUR * MINUTES_PER_HOUR;
    const NOW_UPDATE_MS = 60_000;

    let manualMinutes = $state(DEFAULT_TIME);
    let useNow = $state(false);
    let nowMinutes = $state(DEFAULT_TIME);
    let nowInterval: ReturnType<typeof setInterval> | null = null;

    function computeNowMinutes(): number {
        const festivalStart = new Date(FESTIVAL_START_ISO);
        const now = new Date();
        // Before festival: clamp to festival start
        if (now < festivalStart) return SCRUBBER_START;
        const minutesSinceMidnight = now.getHours() * MINUTES_PER_HOUR + now.getMinutes();
        const rounded =
            Math.floor(minutesSinceMidnight / SCRUBBER_STEP_MINUTES) * SCRUBBER_STEP_MINUTES;
        return Math.max(SCRUBBER_START, Math.min(SCRUBBER_END, rounded));
    }

    $effect(() => {
        if (useNow) {
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

    const currentMinutes = $derived(useNow ? nowMinutes : manualMinutes);
    const statuses = $derived(allStageStatuses(acts, stageLocations, currentMinutes));
    const timeLabel = $derived(formatTimeDisplay(currentMinutes));
</script>

<div class="flex flex-col h-full overflow-hidden">
    <!-- Time scrubber -->
    <div class="fqf-time-scrubber flex items-center gap-3 px-4 py-2">
        <span
            class="text-sm font-semibold shrink-0"
            style="color: var(--mg-purple-deep); min-width: 5.5rem;"
        >
            {timeLabel}
        </span>

        {#if !useNow}
            <input
                type="range"
                min={SCRUBBER_START}
                max={SCRUBBER_END}
                step={SCRUBBER_STEP_MINUTES}
                bind:value={manualMinutes}
                class="flex-1"
                aria-label="Festival time"
            />
        {:else}
            <span class="flex-1 text-xs italic" style="color: var(--mg-green-deep); opacity: 0.7;">
                Live clock (updates every minute)
            </span>
        {/if}

        <label
            class="flex items-center gap-1.5 text-xs shrink-0 cursor-pointer select-none"
            style="color: var(--mg-purple-deep);"
        >
            <input type="checkbox" bind:checked={useNow} class="accent-purple-700" />
            Now
        </label>
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

            <!-- Stage markers positioned by lat/lng -->
            {#each statuses as status (status.stage)}
                {@const loc = stageLocations.get(status.stage)}
                {#if loc}
                    {@const pos = latLngToPercent(loc.lat, loc.lng)}
                    <StageMarker {status} {onActDetail} style="left: {pos.x}%; top: {pos.y}%;" />
                {/if}
            {/each}
        </div>
    </div>
</div>
