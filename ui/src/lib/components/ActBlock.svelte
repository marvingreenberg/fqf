<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';
    import { FLEUR_PATH } from '$lib/constants';

    const MIN_HEIGHT_FOR_TIME = 50;
    const MIN_HEIGHT_FOR_ICON = 40;

    interface Props {
        act: ActSummary;
        top: number;
        height: number;
        isPicked: boolean;
        conflictLevel: ConflictLevel;
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
        onToggle,
        onDetail,
        readOnly = false
    }: Props = $props();

    const showTime = $derived(height > MIN_HEIGHT_FOR_TIME);
    const showConflictIcon = $derived(
        height > MIN_HEIGHT_FOR_ICON && isPicked && conflictLevel !== 'none'
    );

    const blockClass = $derived.by(() => {
        let cls = 'fqf-act-block';
        if (isPicked && conflictLevel === 'yellow') cls += ' conflict-yellow';
        else if (isPicked && conflictLevel === 'red') cls += ' conflict-red';
        else if (isPicked) cls += ' picked';
        return cls;
    });
</script>

<div
    class="absolute left-0.5 right-1 overflow-hidden cursor-pointer select-none {blockClass}"
    style="top: {top}px; height: {height}px;"
    onclick={onDetail}
    role="button"
    tabindex="0"
    onkeydown={(e) => e.key === 'Enter' && onDetail()}
>
    <div class="flex items-start gap-1 p-1.5 h-full">
        {#if !readOnly}
            <button
                class="fqf-fleur mt-0.5 shrink-0"
                style="width: 1rem; height: 1rem;"
                onclick={(e) => {
                    e.stopPropagation();
                    onToggle();
                }}
                aria-label={isPicked ? `Remove ${act.name} from picks` : `Add ${act.name} to picks`}
            >
                {#if isPicked}
                    <svg viewBox="0 0 16 16" width="14" height="14" fill="var(--mg-gold-rich)">
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
                <p class="text-xs opacity-60 mt-0.5">{act.start}&#8211;{act.end}</p>
            {/if}
        </div>
        {#if showConflictIcon}
            <span
                class="shrink-0 mt-0.5"
                title={conflictLevel === 'red' ? 'Major time conflict' : 'Minor time conflict'}
            >
                {#if conflictLevel === 'red'}
                    <svg viewBox="0 0 16 16" width="14" height="14" fill="#b42828">
                        <circle cx="8" cy="8" r="7" fill="#b42828" />
                        <text
                            x="8"
                            y="12"
                            text-anchor="middle"
                            fill="white"
                            font-size="12"
                            font-weight="bold">!</text
                        >
                    </svg>
                {:else}
                    <svg viewBox="0 0 18 16" width="14" height="13" fill="none">
                        <path
                            d="M9 1L17 15H1L9 1Z"
                            fill="var(--mg-gold-rich)"
                            stroke="var(--mg-gold-rich)"
                        />
                        <text
                            x="9"
                            y="14"
                            text-anchor="middle"
                            fill="var(--mg-purple-deep)"
                            font-size="11"
                            font-weight="bold">!</text
                        >
                    </svg>
                {/if}
            </span>
        {/if}
    </div>
</div>
