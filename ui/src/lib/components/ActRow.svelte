<script lang="ts">
    import type { ActSummary } from '$lib/types';
    import type { Snippet } from 'svelte';
    import { formatTime12 } from '$lib/map-utils';
    import { displayName, shrinkOnTruncate } from '$lib/display';
    import PickButtons from '$lib/components/PickButtons.svelte';

    interface Props {
        act: ActSummary;
        isPicked: boolean;
        isMaybe: boolean;
        conflictColor: string;
        readOnly?: boolean;
        /**
         * Whether to render the stage on its own line below the name. False
         * when the surrounding view groups by stage (the group header carries
         * the stage already), true otherwise.
         */
        showStage?: boolean;
        onTogglePick: (slug: string) => void;
        onToggleMaybe: (slug: string) => void;
        onActDetail: (act: ActSummary) => void;
        /** Optional left content on the third line (e.g. distance info). */
        extraMain?: Snippet;
        /** Optional right content on the third line (e.g. conflict badge). */
        extra?: Snippet;
    }

    let {
        act,
        isPicked,
        isMaybe,
        conflictColor,
        readOnly = false,
        showStage = true,
        onTogglePick,
        onToggleMaybe,
        onActDetail,
        extraMain,
        extra
    }: Props = $props();

    // Indent for secondary rows so they line up with where the name starts.
    // PickButtons (size 18 → ≈43px) + parent gap-3 (12px) ≈ 55px.
    // In readOnly mode there are no pick buttons so the indent collapses.
    const secondaryIndentClass = $derived(readOnly ? '' : 'pl-[55px]');
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<div
    class="fqf-list-row flex flex-col gap-1 px-3 py-2.5 border-l-4"
    style="border-left-color: {conflictColor};"
    onclick={() => onActDetail(act)}
>
    <div class="flex items-center gap-3 min-w-0">
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

        <p class="fqf-card-name flex-1 min-w-0 truncate" use:shrinkOnTruncate>
            {displayName(act.name)}
        </p>

        <span class="fqf-card-time shrink-0">
            {formatTime12(act.start)}&#8211;{formatTime12(act.end)}
        </span>
    </div>

    {#if showStage}
        <div class="flex {secondaryIndentClass}">
            <span class="fqf-card-stage-chip" title={act.stage}>{act.stage}</span>
        </div>
    {/if}

    {#if extraMain || extra}
        <div class="flex items-center gap-2 {secondaryIndentClass}">
            <div class="flex-1 min-w-0">
                {#if extraMain}{@render extraMain()}{/if}
            </div>
            {#if extra}
                <div class="shrink-0">{@render extra()}</div>
            {/if}
        </div>
    {/if}
</div>
