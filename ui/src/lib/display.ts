/**
 * Display helpers for compact mobile cards.
 *
 * Two pieces:
 *   - `displayName()` strips a leading "The " from a band name so the card
 *     spends its limited horizontal real estate on distinguishing words. The
 *     full unmodified name still appears in the bio modal.
 *   - `shrinkOnTruncate` is a Svelte action that measures the rendered text
 *     vs. its container and toggles a "shrunk" class when more than 60% of
 *     the text would be hidden by ellipsis truncation. The shrink class then
 *     drops the font-size so a longer prefix of the name is visible.
 */

const SHRUNK_CLASS = 'fqf-card-name-shrunk';

/** Strip a leading "The " (case-insensitive) used in band names. */
export function displayName(name: string): string {
    return name.replace(/^the\s+/i, '');
}
export function displayStage(stage: string): string {
    let stage_short = stage.replace(/^the\s+|\s+stage$/i, '');
    if (stage_short.length > 24) {
        stage_short = `${stage_short.substring(0, 23)}...`;
    }
    return stage_short;
}

interface ShrinkOpts {
    /**
     * Visible-fraction threshold below which we apply the shrunk class.
     * `clientWidth / scrollWidth < threshold` => shrink.
     * 0.4 means "more than 60% of the text is hidden".
     */
    threshold?: number;
}

/**
 * Svelte action: watch a truncated element and toggle the shrunk class
 * whenever the visible fraction drops below the threshold. Re-measures on
 * any size change via ResizeObserver, so resizing the viewport or swapping
 * sibling content (e.g. stage chip → no chip) re-triggers the check.
 */
export function shrinkOnTruncate(node: HTMLElement, opts: ShrinkOpts = {}) {
    const threshold = opts.threshold ?? 0.4;

    function measure(): void {
        // First clear so the next measurement reflects the un-shrunk layout.
        // Otherwise the shrunk font would itself fit, causing oscillation.
        node.classList.remove(SHRUNK_CLASS);
        // Defer to next frame so the browser has flushed the class removal.
        requestAnimationFrame(() => {
            const cw = node.clientWidth;
            const sw = node.scrollWidth;
            if (cw === 0 || sw === 0) return;
            if (cw / sw < threshold) node.classList.add(SHRUNK_CLASS);
        });
    }

    const observer = new ResizeObserver(measure);
    observer.observe(node);
    // Also observe the parent — when sibling layout changes (e.g. the stage
    // chip appears or disappears), our clientWidth changes without our own
    // box resizing, so the inner observer wouldn't fire.
    if (node.parentElement) observer.observe(node.parentElement);

    measure();

    return {
        update() {
            measure();
        },
        destroy() {
            observer.disconnect();
        }
    };
}
