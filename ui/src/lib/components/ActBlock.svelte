<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';
    import {
        FLEUR_PATH,
        PICKED_FLEUR_FILL,
        CONFLICT_COLORS,
        CONFLICT_COLOR_TEXT
    } from '$lib/constants';
    import { timeToMinutes } from '$lib/conflict';
    import { formatTime12 } from '$lib/map-utils';

    const MIN_HEIGHT_FOR_TIME = 50;
    const MIN_HEIGHT_FOR_GENRE = 65;
    const MIN_HEIGHT_FOR_CONFLICT_DETAIL = 70;

    interface Props {
        act: ActSummary;
        top: number;
        height: number;
        isPicked: boolean;
        conflictLevel: ConflictLevel;
        allActs: ActSummary[];
        picks: Set<string>;
        onToggle: () => void;
        onDetail: () => void;
        readOnly?: boolean;
    }

    let {
        act,
        top,
        height,
        isPicked,
        conflictLevel,
        allActs,
        picks,
        onToggle,
        onDetail,
        readOnly = false
    }: Props = $props();

    const showTime = $derived(height > MIN_HEIGHT_FOR_TIME);
    const showGenre = $derived(height > MIN_HEIGHT_FOR_GENRE);

    const blockClass = $derived.by(() => {
        let cls = 'fqf-act-block';
        if (isPicked) cls += ' picked';
        return cls;
    });

    const conflictBorderStyle = $derived.by(() => {
        if (!isPicked || conflictLevel === 'none') return '';
        const color = CONFLICT_COLORS[conflictLevel];
        return `border-left: 3px solid ${color}; border-bottom: 2px solid ${color};`;
    });

    const worstConflictAct = $derived.by(() => {
        if (!isPicked || conflictLevel === 'none') return null;
        let worst: ActSummary | null = null;
        let worstOverlap = 0;
        for (const other of allActs) {
            if (other.slug === act.slug || !picks.has(other.slug) || other.date !== act.date)
                continue;
            const s1 = timeToMinutes(act.start),
                e1 = timeToMinutes(act.end);
            const s2 = timeToMinutes(other.start),
                e2 = timeToMinutes(other.end);
            const overlap = Math.max(0, Math.min(e1, e2) - Math.max(s1, s2));
            if (overlap > worstOverlap) {
                worstOverlap = overlap;
                worst = other;
            }
        }
        return worst ? { act: worst, overlapMinutes: worstOverlap } : null;
    });

    const showConflictDetail = $derived(
        height > MIN_HEIGHT_FOR_CONFLICT_DETAIL &&
            isPicked &&
            conflictLevel !== 'none' &&
            worstConflictAct !== null
    );
</script>

<div
    class="absolute left-0.5 right-1 overflow-hidden cursor-pointer select-none {blockClass}"
    style="top: {top}px; height: {height}px; {conflictBorderStyle}"
    onclick={onDetail}
    role="button"
    tabindex="0"
    onkeydown={(e) => e.key === 'Enter' && onDetail()}
>
    <div class="flex flex-col gap-0 p-1.5 h-full">
        <div class="flex items-start gap-1">
            {#if !readOnly}
                <button
                    class="fqf-fleur mt-0.5 shrink-0"
                    style="width: 1rem; height: 1rem;"
                    onclick={(e) => {
                        e.stopPropagation();
                        onToggle();
                    }}
                    aria-label={isPicked
                        ? `Remove ${act.name} from picks`
                        : `Add ${act.name} to picks`}
                >
                    {#if isPicked}
                        <svg viewBox="0 0 16 16" width="14" height="14" fill={PICKED_FLEUR_FILL}>
                            <path d={FLEUR_PATH} />
                        </svg>
                    {:else}
                        <svg
                            viewBox="0 0 16 16"
                            width="14"
                            height="14"
                            fill="none"
                            stroke="rgba(74, 26, 107, 0.3)"
                            stroke-width="0.75"
                        >
                            <path d={FLEUR_PATH} />
                        </svg>
                    {/if}
                </button>
            {/if}
            <div class="min-w-0 flex-1">
                <p class="text-xs font-semibold leading-tight truncate">{act.name}</p>
                {#if showTime}
                    <p class="text-xs opacity-60 mt-0.5">
                        {formatTime12(act.start)}&#8211;{formatTime12(act.end)}
                    </p>
                {/if}
                {#if showGenre}
                    <p class="text-[9px] italic opacity-50 truncate">{act.genre}</p>
                {/if}
            </div>
        </div>
        {#if showConflictDetail && worstConflictAct}
            {@const conflictColorText = CONFLICT_COLOR_TEXT[conflictLevel]}
            {@const indicator = conflictLevel === 'red' ? '🚫' : '⚠️'}
            <div class="mt-auto text-[10px] leading-tight" style="color: {conflictColorText};">
                <p class="truncate">
                    {indicator}
                    {worstConflictAct.overlapMinutes}m overlap –
                </p>
                <p class="wrap pl-4">
                    {worstConflictAct.act.name}
                    at {worstConflictAct.act.stage}
                </p>
            </div>
        {/if}
    </div>
</div>
