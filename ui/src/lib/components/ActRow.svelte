<script lang="ts">
    import type { ActSummary } from '$lib/types';
    import type { Snippet } from 'svelte';

    const FLEUR_PATH =
        'M8 0C8 0 6.5 3.5 6.5 5.5C6.5 7 7 8 8 9C9 8 9.5 7 9.5 5.5C9.5 3.5 8 0 8 0ZM4.5 6C2.5 6 0 7.5 0 7.5C0 7.5 2 9 4.5 9C5.5 9 6.5 8.5 7 8C6 7.5 5.5 7 4.5 6ZM11.5 6C10.5 7 10 7.5 9 8C9.5 8.5 10.5 9 11.5 9C14 9 16 7.5 16 7.5C16 7.5 13.5 6 11.5 6ZM8 10C7 10 5 10.5 5 12C5 14 8 16 8 16C8 16 11 14 11 12C11 10.5 9 10 8 10Z';

    interface Props {
        act: ActSummary;
        isPicked: boolean;
        conflictColor: string;
        readOnly?: boolean;
        onTogglePick: (slug: string) => void;
        onActDetail: (act: ActSummary) => void;
        /** Optional content below stage/time in the main info section (e.g. distance info) */
        extraMain?: Snippet;
        /** Optional content in the right column before the genre label (e.g. badges) */
        extra?: Snippet;
    }

    let {
        act,
        isPicked,
        conflictColor,
        readOnly = false,
        onTogglePick,
        onActDetail,
        extraMain,
        extra
    }: Props = $props();
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<div
    class="fqf-list-row flex items-center gap-3 px-3 py-2.5 border-l-4"
    style="border-left-color: {conflictColor};"
    onclick={() => onActDetail(act)}
>
    {#if !readOnly}
        <button
            class="fqf-fleur shrink-0"
            style="width: 1.25rem; height: 1.25rem;"
            onclick={(e) => {
                e.stopPropagation();
                onTogglePick(act.slug);
            }}
            aria-label={isPicked ? `Remove ${act.name} from picks` : `Add ${act.name} to picks`}
        >
            {#if isPicked}
                <svg viewBox="0 0 16 16" width="18" height="18" fill="var(--mg-gold-rich)">
                    <path d={FLEUR_PATH} />
                </svg>
            {:else}
                <svg
                    viewBox="0 0 16 16"
                    width="18"
                    height="18"
                    fill="none"
                    stroke="rgba(74, 26, 107, 0.3)"
                    stroke-width="0.75"
                >
                    <path d={FLEUR_PATH} />
                </svg>
            {/if}
        </button>
    {/if}

    <div class="flex-1 min-w-0">
        <p class="text-sm font-semibold truncate">{act.name}</p>
        <p class="text-xs truncate" style="color: rgba(74, 26, 107, 0.5);">
            {act.start}&#8211;{act.end} &middot; {act.stage}
        </p>
        {#if extraMain}
            {@render extraMain()}
        {/if}
    </div>

    <div class="shrink-0 flex items-center gap-1.5">
        {#if extra}
            {@render extra()}
        {/if}
        <span class="text-xs italic" style="color: rgba(74, 26, 107, 0.45);">
            {act.genre}
        </span>
    </div>
</div>
