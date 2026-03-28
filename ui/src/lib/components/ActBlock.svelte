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
           fqf-act-block transition-colors border-l-4"
    style="top: {top}px; height: {height}px; border-left-color: {borderColor};"
    onclick={onDetail}
    role="button"
    tabindex="0"
    onkeydown={(e) => e.key === 'Enter' && onDetail()}
>
    <div class="flex items-start gap-1 p-1 h-full">
        <button
            class="mt-0.5 shrink-0 w-4 h-4 rounded border border-surface-400
                   bg-surface-50 flex items-center justify-center hover:bg-primary-100 transition-colors"
            onclick={(e) => {
                e.stopPropagation();
                onToggle();
            }}
            aria-label={isPicked ? `Remove ${act.name} from picks` : `Add ${act.name} to picks`}
        >
            {#if isPicked}
                <svg class="w-3 h-3 text-primary-600" viewBox="0 0 12 12" fill="currentColor">
                    <path
                        d="M10 3L5 8.5 2 5.5"
                        stroke="currentColor"
                        stroke-width="1.5"
                        fill="none"
                        stroke-linecap="round"
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
