export const MAYBE_PREFIX = '?';

/** Strip the maybe prefix if present; always returns a bare slug. */
export function bareSlug(entry: string): string {
    return entry.startsWith(MAYBE_PREFIX) ? entry.slice(MAYBE_PREFIX.length) : entry;
}

/** True if the act is definitively picked (not maybe). Checks for bare slug in set. */
export function isPicked(slug: string, picks: Set<string>): boolean {
    return picks.has(slug);
}

/** True if the act is in the maybe state. Checks for ?slug in set. */
export function isMaybe(slug: string, picks: Set<string>): boolean {
    return picks.has(MAYBE_PREFIX + slug);
}

/** True if the act is picked or maybe. */
export function isSelected(slug: string, picks: Set<string>): boolean {
    return isPicked(slug, picks) || isMaybe(slug, picks);
}

/**
 * Toggle the picked state. Returns a new Set.
 * Unpicked → picked. Picked → unpicked. Maybe → picked (clears maybe).
 */
export function togglePick(slug: string, picks: Set<string>): Set<string> {
    const next = new Set(picks);
    const maybeEntry = MAYBE_PREFIX + slug;

    if (next.has(slug)) {
        next.delete(slug);
    } else {
        next.delete(maybeEntry);
        next.add(slug);
    }

    return next;
}

/**
 * Toggle the maybe state. Returns a new Set.
 * Unpicked → maybe. Maybe → unpicked. Picked → maybe (clears pick).
 */
export function toggleMaybe(slug: string, picks: Set<string>): Set<string> {
    const next = new Set(picks);
    const maybeEntry = MAYBE_PREFIX + slug;

    if (next.has(maybeEntry)) {
        next.delete(maybeEntry);
    } else {
        next.delete(slug);
        next.add(maybeEntry);
    }

    return next;
}
