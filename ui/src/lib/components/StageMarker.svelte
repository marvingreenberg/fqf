<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';
    import type { StageStatus } from '$lib/map-utils';
    import { SHOW_NEXT_THRESHOLD_MINUTES, CONFLICT_COLORS } from '$lib/constants';
    import { getWorstConflict } from '$lib/conflict';
    import { isMaybe as _isMaybe } from '$lib/picks';
    import MapActLabel from '$lib/components/MapActLabel.svelte';

    const PICKED_BORDER_LEFT_PX = 3;
    const PICKED_BORDER_BOTTOM_PX = 2;
    const UNSELECTED_FLEUR_FILL = '#c8c8c8';

    interface Props {
        status: StageStatus;
        picks: Set<string>;
        allActs: ActSummary[];
        onActDetail?: (act: ActSummary) => void;
    }

    let { status, picks, allActs, onActDetail }: Props = $props();

    const showNext = $derived(
        !status.current ||
            (status.currentMinutesRemaining < SHOW_NEXT_THRESHOLD_MINUTES && status.next !== null)
    );

    const displayAct = $derived(showNext ? status.next : status.current);

    const isPicked = $derived(displayAct ? picks.has(displayAct.slug) : false);

    const isMaybeAct = $derived(displayAct ? _isMaybe(displayAct.slug, picks) : false);

    const conflict = $derived.by((): ConflictLevel => {
        if (!displayAct || !isPicked) return 'none';
        return getWorstConflict(displayAct, allActs, picks);
    });

    const fleurFill = $derived(
        isPicked || isMaybeAct ? CONFLICT_COLORS.none : UNSELECTED_FLEUR_FILL
    );

    const timeText = $derived.by(() => {
        if (showNext && status.next) return `${status.nextMinutesUntil}m`;
        if (!showNext && status.current) return `${status.currentMinutesRemaining}m`;
        return '';
    });

    const borderStyle = $derived.by(() => {
        if (!isPicked) return '';
        const color = CONFLICT_COLORS[conflict];
        return `border-left: ${PICKED_BORDER_LEFT_PX}px solid ${color}; border-bottom: ${PICKED_BORDER_BOTTOM_PX}px solid ${color};`;
    });
</script>

{#if displayAct}
    <MapActLabel
        name={displayAct.name}
        {fleurFill}
        {borderStyle}
        isPicked={isPicked || isMaybeAct}
        isMaybe={isMaybeAct}
        onclick={(e) => {
            e.stopPropagation();
            onActDetail?.(displayAct);
        }}
    >
        {#snippet prefix()}
            {#if showNext}
                <span class="text-[10px] shrink-0">&#9203;</span>
                <span class="text-[9px] shrink-0" style="color: var(--mg-purple-deep);">
                    in {timeText}
                </span>
            {/if}
        {/snippet}
        {#snippet postfix()}
            {#if !showNext}
                <span class="text-[9px] shrink-0" style="color: var(--mg-purple-deep);">
                    {timeText}
                </span>
                <span class="text-[10px] shrink-0">&#9834;</span>
            {/if}
        {/snippet}
    </MapActLabel>
{/if}
