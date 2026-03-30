<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';

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
                        <path
                            d="M8 0C8 0 6.5 3.5 6.5 5.5C6.5 7 7 8 8 9C9 8 9.5 7 9.5 5.5C9.5 3.5 8 0 8 0ZM4.5 6C2.5 6 0 7.5 0 7.5C0 7.5 2 9 4.5 9C5.5 9 6.5 8.5 7 8C6 7.5 5.5 7 4.5 6ZM11.5 6C10.5 7 10 7.5 9 8C9.5 8.5 10.5 9 11.5 9C14 9 16 7.5 16 7.5C16 7.5 13.5 6 11.5 6ZM8 10C7 10 5 10.5 5 12C5 14 8 16 8 16C8 16 11 14 11 12C11 10.5 9 10 8 10Z"
                        />
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
                        <path
                            d="M8 0C8 0 6.5 3.5 6.5 5.5C6.5 7 7 8 8 9C9 8 9.5 7 9.5 5.5C9.5 3.5 8 0 8 0ZM4.5 6C2.5 6 0 7.5 0 7.5C0 7.5 2 9 4.5 9C5.5 9 6.5 8.5 7 8C6 7.5 5.5 7 4.5 6ZM11.5 6C10.5 7 10 7.5 9 8C9.5 8.5 10.5 9 11.5 9C14 9 16 7.5 16 7.5C16 7.5 13.5 6 11.5 6ZM8 10C7 10 5 10.5 5 12C5 14 8 16 8 16C8 16 11 14 11 12C11 10.5 9 10 8 10Z"
                        />
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
