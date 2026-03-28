<script lang="ts">
    import type { ActSummary } from '$lib/types';
    import { GRID_START_HOUR, GRID_END_HOUR, MINUTES_PER_HOUR } from '$lib/constants';
    import { latLngToPercent, allStageStatuses, formatTimeDisplay } from '$lib/map-utils';
    import StageMarker from '$lib/components/StageMarker.svelte';

    interface Props {
        acts: ActSummary[];
        stageLocations: Map<string, { lat: number; lng: number }>;
    }

    let { acts, stageLocations }: Props = $props();

    const SCRUBBER_START = GRID_START_HOUR * MINUTES_PER_HOUR;
    const SCRUBBER_END = GRID_END_HOUR * MINUTES_PER_HOUR;
    const DEFAULT_HOUR = 12;
    const DEFAULT_TIME = DEFAULT_HOUR * MINUTES_PER_HOUR;

    let currentMinutes = $state(DEFAULT_TIME);

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
        <input
            type="range"
            min={SCRUBBER_START}
            max={SCRUBBER_END}
            step={1}
            bind:value={currentMinutes}
            class="flex-1"
            aria-label="Festival time"
        />
    </div>

    <!-- Map container -->
    <div class="flex-1 overflow-auto">
        <div class="relative mx-auto" style="max-width: 900px;">
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
                    <StageMarker {status} style="left: {pos.x}%; top: {pos.y}%;" />
                {/if}
            {/each}
        </div>
    </div>
</div>
