<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';
    import { CONFLICT_COLORS } from '$lib/constants';

    const MIN_HEIGHT_FOR_TIME = 50;

    interface Props {
        act: ActSummary;
        top: number;
        height: number;
        isPicked: boolean;
        conflictLevel: ConflictLevel;
        onToggle: () => void;
        onDetail: () => void;
    }

    let { act, top, height, isPicked, conflictLevel, onToggle, onDetail }: Props = $props();

    const borderColor = $derived(isPicked ? CONFLICT_COLORS[conflictLevel] : 'transparent');
    const showTime = $derived(height > MIN_HEIGHT_FOR_TIME);
</script>

<div
    class="absolute left-0 right-1 rounded overflow-hidden cursor-pointer select-none
           fqf-act-block border-l-4"
    style="top: {top}px; height: {height}px; border-left-color: {borderColor};"
    onclick={onDetail}
    role="button"
    tabindex="0"
    onkeydown={(e) => e.key === 'Enter' && onDetail()}
>
    <div class="flex items-start gap-1 p-1 h-full">
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
                <!-- Filled gold fleur-de-lis -->
                <svg viewBox="0 0 16 16" width="14" height="14" fill="var(--mg-gold-rich)">
                    <path
                        d="M8 0C8 0 6.5 3.5 6.5 5.5C6.5 7 7 8 8 9C9 8 9.5 7 9.5 5.5C9.5 3.5 8 0 8 0ZM4.5 6C2.5 6 0 7.5 0 7.5C0 7.5 2 9 4.5 9C5.5 9 6.5 8.5 7 8C6 7.5 5.5 7 4.5 6ZM11.5 6C10.5 7 10 7.5 9 8C9.5 8.5 10.5 9 11.5 9C14 9 16 7.5 16 7.5C16 7.5 13.5 6 11.5 6ZM8 10C7 10 5 10.5 5 12C5 14 8 16 8 16C8 16 11 14 11 12C11 10.5 9 10 8 10Z"
                    />
                </svg>
            {:else}
                <!-- Outline fleur-de-lis -->
                <svg
                    viewBox="0 0 16 16"
                    width="14"
                    height="14"
                    fill="none"
                    stroke="rgba(74, 26, 107, 0.35)"
                    stroke-width="0.75"
                >
                    <path
                        d="M8 0C8 0 6.5 3.5 6.5 5.5C6.5 7 7 8 8 9C9 8 9.5 7 9.5 5.5C9.5 3.5 8 0 8 0ZM4.5 6C2.5 6 0 7.5 0 7.5C0 7.5 2 9 4.5 9C5.5 9 6.5 8.5 7 8C6 7.5 5.5 7 4.5 6ZM11.5 6C10.5 7 10 7.5 9 8C9.5 8.5 10.5 9 11.5 9C14 9 16 7.5 16 7.5C16 7.5 13.5 6 11.5 6ZM8 10C7 10 5 10.5 5 12C5 14 8 16 8 16C8 16 11 14 11 12C11 10.5 9 10 8 10Z"
                    />
                </svg>
            {/if}
        </button>
        <div class="min-w-0 flex-1">
            <p class="text-xs font-semibold leading-tight truncate">{act.name}</p>
            {#if showTime}
                <p class="text-xs opacity-60 mt-0.5">{act.start}–{act.end}</p>
            {/if}
        </div>
    </div>
</div>
