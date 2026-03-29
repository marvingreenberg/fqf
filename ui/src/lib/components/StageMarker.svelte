<script lang="ts">
    import type { ActSummary } from '$lib/types';
    import type { StageStatus } from '$lib/map-utils';
    import { countdownColor } from '$lib/map-utils';
    import { SHOW_NEXT_THRESHOLD_MINUTES } from '$lib/constants';

    interface Props {
        status: StageStatus;
        style: string;
        onActDetail?: (act: ActSummary) => void;
    }

    let { status, style, onActDetail }: Props = $props();

    // Show current act unless <15 min remaining, then switch to next
    const showNext = $derived(
        !status.current ||
            (status.currentMinutesRemaining < SHOW_NEXT_THRESHOLD_MINUTES && status.next !== null)
    );

    const displayAct = $derived(showNext ? status.next : status.current);

    const dotColor = $derived.by(() => {
        if (showNext && status.next) return countdownColor(status.nextFractionApproaching);
        if (!showNext && status.current) return countdownColor(status.currentFractionRemaining);
        return null;
    });

    const timeText = $derived.by(() => {
        if (showNext && status.next) return `${status.nextMinutesUntil}m`;
        if (!showNext && status.current) return `${status.currentMinutesRemaining}m`;
        return '';
    });
</script>

{#if displayAct}
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div
        class="absolute -translate-x-1/2 -translate-y-full"
        {style}
        onclick={(e) => {
            e.stopPropagation();
            onActDetail?.(displayAct);
        }}
    >
        <div class="fqf-map-marker fqf-map-act-row flex items-center gap-1">
            {#if showNext}
                <span class="text-[9px] shrink-0">&#9203;</span>
                <span class="text-[8px] shrink-0" style="color: var(--mg-purple-deep);">
                    {timeText}
                </span>
            {/if}
            <span class="inline-block w-2 h-2 rounded-full shrink-0" style="background: {dotColor};"
            ></span>
            <span
                class="text-[9px] font-medium truncate"
                style="max-width: 110px; color: var(--mg-text);"
            >
                {displayAct.name}
            </span>
            {#if !showNext}
                <span class="text-[8px] shrink-0" style="color: var(--mg-purple-deep);">
                    {timeText}
                </span>
                <span class="text-[9px] shrink-0">&#9834;</span>
            {/if}
        </div>
        <div class="fqf-map-pin"></div>
    </div>
{/if}
