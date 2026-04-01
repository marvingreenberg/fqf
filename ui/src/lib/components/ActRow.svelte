<script lang="ts">
    import type { ActSummary } from '$lib/types';
    import type { Snippet } from 'svelte';
    import { formatTime12 } from '$lib/map-utils';
    import PickButtons from '$lib/components/PickButtons.svelte';

    interface Props {
        act: ActSummary;
        isPicked: boolean;
        isMaybe: boolean;
        conflictColor: string;
        readOnly?: boolean;
        onTogglePick: (slug: string) => void;
        onToggleMaybe: (slug: string) => void;
        onActDetail: (act: ActSummary) => void;
        /** Optional content below stage/time in the main info section (e.g. distance info) */
        extraMain?: Snippet;
        /** Optional content in the right column before the genre label (e.g. badges) */
        extra?: Snippet;
    }

    let {
        act,
        isPicked,
        isMaybe,
        conflictColor,
        readOnly = false,
        onTogglePick,
        onToggleMaybe,
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
        <PickButtons
            {isPicked}
            {isMaybe}
            size={18}
            onTogglePick={() => onTogglePick(act.slug)}
            onToggleMaybe={() => onToggleMaybe(act.slug)}
            ariaName={act.name}
        />
    {/if}

    <div class="flex-1 min-w-0">
        <p class="text-sm font-semibold truncate">{act.name}</p>
        <p class="text-xs truncate" style="color: rgba(74, 26, 107, 0.5);">
            {formatTime12(act.start)}&#8211;{formatTime12(act.end)} &middot; {act.stage}
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
