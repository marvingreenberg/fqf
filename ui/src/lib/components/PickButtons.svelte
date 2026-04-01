<script lang="ts">
    import { FLEUR_PATH, QUESTION_PATH, PICKED_FLEUR_FILL } from '$lib/constants';

    const FLEUR_VIEWBOX = '0 0 16 16';
    const UNPICKED_STROKE = 'rgba(74, 26, 107, 0.3)';
    const UNPICKED_STROKE_WIDTH = 0.75;

    interface Props {
        isPicked: boolean;
        isMaybe: boolean;
        size?: number;
        onTogglePick: () => void;
        onToggleMaybe: () => void;
        ariaName?: string;
    }

    let {
        isPicked,
        isMaybe,
        size = 14,
        onTogglePick,
        onToggleMaybe,
        ariaName = 'act'
    }: Props = $props();
</script>

<div class="flex items-center gap-0.5 shrink-0">
    <button
        class="fqf-fleur"
        style="width: {size / 14}rem; height: {size / 14}rem;"
        onclick={(e) => {
            e.stopPropagation();
            onTogglePick();
        }}
        aria-label={isPicked ? `Remove ${ariaName} from picks` : `Add ${ariaName} to picks`}
    >
        <svg
            viewBox={FLEUR_VIEWBOX}
            width={size}
            height={size}
            fill={isPicked ? PICKED_FLEUR_FILL : 'none'}
            stroke={isPicked ? 'none' : UNPICKED_STROKE}
            stroke-width={isPicked ? 0 : UNPICKED_STROKE_WIDTH}
        >
            <path d={FLEUR_PATH} />
        </svg>
    </button>
    <button
        class="fqf-fleur"
        style="width: {size / 14}rem; height: {size / 14}rem;"
        onclick={(e) => {
            e.stopPropagation();
            onToggleMaybe();
        }}
        aria-label={isMaybe ? `Remove ${ariaName} from maybes` : `Mark ${ariaName} as maybe`}
    >
        <svg
            viewBox={FLEUR_VIEWBOX}
            width={size}
            height={size}
            fill={isMaybe ? PICKED_FLEUR_FILL : 'none'}
            stroke={isMaybe ? 'none' : UNPICKED_STROKE}
            stroke-width={isMaybe ? 0 : UNPICKED_STROKE_WIDTH}
        >
            <path d={QUESTION_PATH} />
        </svg>
    </button>
</div>
