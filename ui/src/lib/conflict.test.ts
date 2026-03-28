import { describe, it, expect } from 'vitest';
import {
    timeToMinutes,
    calculateOverlapRatio,
    getConflictLevel,
    getConflictBetweenActs,
    getWorstConflict
} from '$lib/conflict';
import type { ActSummary } from '$lib/types';

describe('timeToMinutes', () => {
    it('converts HH:MM to minutes since midnight', () => {
        expect(timeToMinutes('14:30')).toBe(870);
    });

    it('handles midnight', () => {
        expect(timeToMinutes('00:00')).toBe(0);
    });

    it('handles 11 AM', () => {
        expect(timeToMinutes('11:00')).toBe(660);
    });
});

describe('calculateOverlapRatio', () => {
    it('returns 0 for non-overlapping acts', () => {
        expect(calculateOverlapRatio(660, 720, 780, 840)).toBe(0);
    });

    it('calculates partial overlap', () => {
        // Act 1: 14:00-15:00 (840-900), Act 2: 14:30-15:30 (870-930)
        // overlap = min(900,930) - 870 = 30, span = max(900,930) - 840 = 90
        const ratio = calculateOverlapRatio(840, 900, 870, 930);
        expect(ratio).toBeCloseTo(30 / 90);
    });

    it('handles containment correctly', () => {
        // Act 1: 14:00-16:00 (840-960), Act 2: 14:30-15:00 (870-900)
        // overlap = min(960,900) - 870 = 30, span = max(960,900) - 840 = 120
        const ratio = calculateOverlapRatio(840, 960, 870, 900);
        expect(ratio).toBeCloseTo(30 / 120);
    });

    it('handles reversed order (s2 < s1)', () => {
        const ratio = calculateOverlapRatio(870, 930, 840, 900);
        expect(ratio).toBeCloseTo(30 / 90);
    });

    it('returns 0 for adjacent acts (no gap, no overlap)', () => {
        expect(calculateOverlapRatio(840, 900, 900, 960)).toBe(0);
    });
});

describe('getConflictLevel', () => {
    it('returns none for 0', () => {
        expect(getConflictLevel(0)).toBe('none');
    });

    it('returns yellow for small overlap', () => {
        expect(getConflictLevel(0.15)).toBe('yellow');
    });

    it('returns red at threshold', () => {
        expect(getConflictLevel(0.3)).toBe('red');
    });

    it('returns red above threshold', () => {
        expect(getConflictLevel(0.75)).toBe('red');
    });
});

function makeAct(start: string, end: string, slug: string = 'test'): ActSummary {
    return { slug, name: 'Test', stage: 'Stage', date: '2026-04-16', start, end, genre: 'Unknown' };
}

describe('getConflictBetweenActs', () => {
    it('returns none for non-overlapping acts', () => {
        const a = makeAct('14:00', '15:00', 'a');
        const b = makeAct('16:00', '17:00', 'b');
        expect(getConflictBetweenActs(a, b)).toBe('none');
    });

    it('returns yellow for small overlap', () => {
        const a = makeAct('14:00', '15:00', 'a');
        const b = makeAct('14:50', '15:50', 'b');
        expect(getConflictBetweenActs(a, b)).toBe('yellow');
    });

    it('returns red for large overlap', () => {
        const a = makeAct('14:00', '15:00', 'a');
        const b = makeAct('14:10', '15:30', 'b');
        expect(getConflictBetweenActs(a, b)).toBe('red');
    });

    it('returns none for different dates', () => {
        const a = makeAct('14:00', '15:00', 'a');
        const b = { ...makeAct('14:00', '15:00', 'b'), date: '2026-04-17' };
        expect(getConflictBetweenActs(a, b)).toBe('none');
    });
});

describe('getWorstConflict', () => {
    it('returns none when no other picks', () => {
        const act = makeAct('14:00', '15:00', 'a');
        expect(getWorstConflict(act, [], new Set(['a']))).toBe('none');
    });

    it('returns none when no overlap', () => {
        const act = makeAct('14:00', '15:00', 'a');
        const allActs = [act, makeAct('16:00', '17:00', 'b')];
        expect(getWorstConflict(act, allActs, new Set(['a', 'b']))).toBe('none');
    });

    it('returns worst conflict level among all picked acts', () => {
        const act = makeAct('14:00', '15:00', 'a');
        const b = makeAct('14:50', '15:50', 'b');
        const c = makeAct('14:10', '15:30', 'c');
        const allActs = [act, b, c];
        expect(getWorstConflict(act, allActs, new Set(['a', 'b', 'c']))).toBe('red');
    });

    it('ignores acts on different dates', () => {
        const act = makeAct('14:00', '15:00', 'a');
        const other = { ...makeAct('14:00', '15:00', 'b'), date: '2026-04-17' };
        expect(getWorstConflict(act, [act, other], new Set(['a', 'b']))).toBe('none');
    });
});
