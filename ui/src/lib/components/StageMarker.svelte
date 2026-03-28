<script lang="ts">
    import type { StageStatus } from '$lib/map-utils';
    import { countdownColor } from '$lib/map-utils';
    import { shortenStageName } from '$lib/distance';

    interface Props {
        status: StageStatus;
        style: string;
    }

    let { status, style }: Props = $props();

    const stageAbbrev = $derived(shortenStageName(status.stage));

    const currentColor = $derived(
        status.current ? countdownColor(status.currentFractionRemaining) : null
    );
    const nextColor = $derived(status.next ? countdownColor(status.nextFractionApproaching) : null);
</script>

<div class="absolute -translate-x-1/2 -translate-y-full" {style}>
    <div class="fqf-map-marker" class:fqf-map-marker-idle={!status.current && !status.next}>
        <div
            class="text-[9px] font-bold truncate"
            style="color: var(--mg-purple-deep); max-width: 120px;"
        >
            {stageAbbrev}
        </div>

        {#if status.current}
            <div class="flex items-center gap-1">
                <span
                    class="inline-block w-2 h-2 rounded-full shrink-0"
                    style="background: {currentColor};"
                ></span>
                <span class="text-[8px] truncate" style="max-width: 90px;">
                    {status.current.name}
                </span>
                <span class="text-[8px] opacity-60 shrink-0">
                    {status.currentMinutesRemaining}m
                </span>
            </div>
        {/if}

        {#if status.next}
            <div class="flex items-center gap-1">
                <span
                    class="inline-block w-2 h-2 rounded-full shrink-0"
                    style="background: {nextColor};"
                ></span>
                <span class="text-[8px] truncate opacity-60" style="max-width: 90px;">
                    {status.next.name}
                </span>
                <span class="text-[8px] opacity-40 shrink-0">
                    in {status.nextMinutesUntil}m
                </span>
            </div>
        {/if}

        {#if !status.current && !status.next}
            <div class="text-[8px] opacity-30">idle</div>
        {/if}
    </div>

    <!-- Pin point connecting marker to map location -->
    <div class="fqf-map-pin"></div>
</div>
