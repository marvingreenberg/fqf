<script lang="ts">
    import type { Snippet } from 'svelte';
    import { FLEUR_PATH, QUESTION_PATH } from '$lib/constants';

    const FLEUR_SIZE = 14;
    const FLEUR_VIEWBOX = '0 0 16 16';
    const PICKED_BG = 'background: #e8f5e9;';
    const UNPICKED_BG = 'background: #f0f0f0;';

    interface Props {
        name: string;
        fleurFill: string;
        borderStyle?: string;
        isPicked?: boolean;
        isMaybe?: boolean;
        title?: string;
        prefix?: Snippet;
        postfix?: Snippet;
        onclick?: (e: MouseEvent) => void;
    }

    let {
        name,
        fleurFill,
        borderStyle = '',
        isPicked = false,
        isMaybe = false,
        title = '',
        prefix,
        postfix,
        onclick
    }: Props = $props();

    const iconPath = $derived(isMaybe ? QUESTION_PATH : FLEUR_PATH);
    const cardStyle = $derived(borderStyle + ' ' + (isPicked ? PICKED_BG : UNPICKED_BG));
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="cursor-pointer" {title} {onclick}>
    <div class="fqf-map-marker fqf-map-act-row flex items-center gap-1" style={cardStyle}>
        <svg
            class="shrink-0"
            width={FLEUR_SIZE}
            height={FLEUR_SIZE}
            viewBox={FLEUR_VIEWBOX}
            aria-hidden="true"
        >
            <path d={iconPath} fill={fleurFill} />
        </svg>
        {#if prefix}{@render prefix()}{/if}
        <span
            class="text-[10px] font-medium truncate"
            style="max-width: 120px; color: var(--mg-text);"
        >
            {name}
        </span>
        {#if postfix}{@render postfix()}{/if}
    </div>
    <div class="fqf-map-pin"></div>
</div>
