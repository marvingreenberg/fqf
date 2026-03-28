import type { ActSummary, ConflictLevel } from '$lib/types';
import { CONFLICT_THRESHOLD } from '$lib/constants';

export function timeToMinutes(time: string): number {
    const [h, m] = time.split(':').map(Number);
    return h * 60 + m;
}

export function calculateOverlapRatio(s1: number, e1: number, s2: number, e2: number): number {
    if (s1 > s2) {
        [s1, e1, s2, e2] = [s2, e2, s1, e1];
    }
    const overlap = Math.max(0, Math.min(e1, e2) - s2);
    if (overlap === 0) return 0;
    const totalSpan = Math.max(e1, e2) - s1;
    return overlap / totalSpan;
}

export function getConflictLevel(ratio: number): ConflictLevel {
    if (ratio === 0) return 'none';
    if (ratio < CONFLICT_THRESHOLD) return 'yellow';
    return 'red';
}

const CONFLICT_SEVERITY: Record<ConflictLevel, number> = {
    none: 0,
    yellow: 1,
    red: 2
};

/** Check conflict level between exactly two acts. */
export function getConflictBetweenActs(a: ActSummary, b: ActSummary): ConflictLevel {
    if (a.date !== b.date) return 'none';
    const s1 = timeToMinutes(a.start);
    const e1 = timeToMinutes(a.end);
    const s2 = timeToMinutes(b.start);
    const e2 = timeToMinutes(b.end);
    return getConflictLevel(calculateOverlapRatio(s1, e1, s2, e2));
}

export function getWorstConflict(
    act: ActSummary,
    allActs: ActSummary[],
    picks: Set<string>
): ConflictLevel {
    let worst: ConflictLevel = 'none';
    const s1 = timeToMinutes(act.start);
    const e1 = timeToMinutes(act.end);

    for (const other of allActs) {
        if (other.slug === act.slug) continue;
        if (!picks.has(other.slug)) continue;
        if (other.date !== act.date) continue;

        const s2 = timeToMinutes(other.start);
        const e2 = timeToMinutes(other.end);
        const ratio = calculateOverlapRatio(s1, e1, s2, e2);
        const level = getConflictLevel(ratio);

        if (CONFLICT_SEVERITY[level] > CONFLICT_SEVERITY[worst]) {
            worst = level;
        }
        if (worst === 'red') break;
    }

    return worst;
}
