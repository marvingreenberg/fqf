import { describe, it, expect } from 'vitest';
import type { ActSummary } from '$lib/types';
import {
    parseTimeToMinutes,
    formatTimeDisplay,
    latLngToPercent,
    stageStatusAt,
    allStageStatuses,
    countdownColor,
    COUNTDOWN_GREEN,
    COUNTDOWN_GRAY
} from '$lib/map-utils';
import { MAP_BOUNDS } from '$lib/constants';

describe('parseTimeToMinutes', () => {
    it('parses noon', () => {
        expect(parseTimeToMinutes('12:00')).toBe(720);
    });

    it('parses morning with leading zero', () => {
        expect(parseTimeToMinutes('09:30')).toBe(570);
    });

    it('parses evening time', () => {
        expect(parseTimeToMinutes('21:45')).toBe(1305);
    });

    it('parses 11:00 AM (festival start)', () => {
        expect(parseTimeToMinutes('11:00')).toBe(660);
    });
});

describe('formatTimeDisplay', () => {
    it('formats noon as 12:00 PM', () => {
        expect(formatTimeDisplay(720)).toBe('12:00 PM');
    });

    it('formats 11 AM', () => {
        expect(formatTimeDisplay(660)).toBe('11:00 AM');
    });

    it('formats 1:30 PM', () => {
        expect(formatTimeDisplay(810)).toBe('1:30 PM');
    });

    it('formats 9:00 PM', () => {
        expect(formatTimeDisplay(1260)).toBe('9:00 PM');
    });

    it('formats 10:00 PM (festival end)', () => {
        expect(formatTimeDisplay(1320)).toBe('10:00 PM');
    });
});

describe('latLngToPercent', () => {
    it('maps approximate center to ~50%', () => {
        const center = latLngToPercent(29.95626, -90.0625);
        expect(center.x).toBeCloseTo(50, 0);
        expect(center.y).toBeCloseTo(50, 0);
    });

    it('maps NW corner to 0,0', () => {
        const nw = latLngToPercent(MAP_BOUNDS.north, MAP_BOUNDS.west);
        expect(nw.x).toBeCloseTo(0, 1);
        expect(nw.y).toBeCloseTo(0, 1);
    });

    it('maps SE corner to 100,100', () => {
        const se = latLngToPercent(MAP_BOUNDS.south, MAP_BOUNDS.east);
        expect(se.x).toBeCloseTo(100, 1);
        expect(se.y).toBeCloseTo(100, 1);
    });

    it('places Fish Fry stage correctly (south-center)', () => {
        const pos = latLngToPercent(29.95107, -90.0628);
        expect(pos.x).toBeCloseTo(48.4, 0);
        expect(pos.y).toBeCloseTo(85.7, 0);
    });

    it('places Entergy stage correctly (north-east)', () => {
        const pos = latLngToPercent(29.96145, -90.05825);
        expect(pos.x).toBeCloseTo(72.4, 0);
        expect(pos.y).toBeCloseTo(14.1, 0);
    });
});

describe('stageStatusAt', () => {
    const TEST_STAGE = 'Test Stage';
    const testActs: ActSummary[] = [
        {
            slug: 'act-a',
            name: 'Act A',
            stage: TEST_STAGE,
            date: '2026-04-16',
            start: '14:00',
            end: '15:00',
            genre: 'Jazz (Traditional)'
        },
        {
            slug: 'act-b',
            name: 'Act B',
            stage: TEST_STAGE,
            date: '2026-04-16',
            start: '15:30',
            end: '16:30',
            genre: 'Blues'
        }
    ];

    it('finds current act when time is during a set', () => {
        const status = stageStatusAt(testActs, TEST_STAGE, 14 * 60 + 30);
        expect(status.current?.slug).toBe('act-a');
        expect(status.currentMinutesRemaining).toBe(30);
    });

    it('finds next act when time is during a set', () => {
        const status = stageStatusAt(testActs, TEST_STAGE, 14 * 60 + 30);
        expect(status.next?.slug).toBe('act-b');
        expect(status.nextMinutesUntil).toBe(60);
    });

    it('returns null current between acts', () => {
        const status = stageStatusAt(testActs, TEST_STAGE, 15 * 60 + 15);
        expect(status.current).toBeNull();
        expect(status.next?.slug).toBe('act-b');
        expect(status.nextMinutesUntil).toBe(15);
    });

    it('returns null next after all acts end', () => {
        const status = stageStatusAt(testActs, TEST_STAGE, 17 * 60);
        expect(status.current).toBeNull();
        expect(status.next).toBeNull();
    });

    it('returns null current before first act', () => {
        const status = stageStatusAt(testActs, TEST_STAGE, 11 * 60);
        expect(status.current).toBeNull();
        expect(status.next?.slug).toBe('act-a');
    });

    it('computes fraction remaining at midpoint of act', () => {
        const status = stageStatusAt(testActs, TEST_STAGE, 14 * 60 + 30);
        expect(status.currentFractionRemaining).toBeCloseTo(0.5);
    });

    it('computes fraction remaining at act start', () => {
        const status = stageStatusAt(testActs, TEST_STAGE, 14 * 60);
        expect(status.currentFractionRemaining).toBeCloseTo(1.0);
    });

    it('computes next-approaching fraction within lookahead', () => {
        // 15 min until next, MAX_LOOKAHEAD=60 → fraction = 1 - 15/60 = 0.75
        const status = stageStatusAt(testActs, TEST_STAGE, 15 * 60 + 15);
        expect(status.nextFractionApproaching).toBeCloseTo(0.75);
    });

    it('clamps next-approaching to 0 beyond lookahead', () => {
        // 3 hours before first act — well beyond 60 min lookahead
        const status = stageStatusAt(testActs, TEST_STAGE, 11 * 60);
        expect(status.nextFractionApproaching).toBe(0);
    });

    it('handles empty act list', () => {
        const status = stageStatusAt([], TEST_STAGE, 14 * 60);
        expect(status.current).toBeNull();
        expect(status.next).toBeNull();
    });
});

describe('allStageStatuses', () => {
    const locations = new Map([
        ['Stage A', { lat: 29.955, lng: -90.063 }],
        ['Stage B', { lat: 29.96, lng: -90.058 }],
        ['Stage C', { lat: 29.952, lng: -90.066 }]
    ]);

    const acts: ActSummary[] = [
        {
            slug: 'x',
            name: 'X',
            stage: 'Stage A',
            date: '2026-04-16',
            start: '14:00',
            end: '15:00',
            genre: 'Funk'
        },
        {
            slug: 'y',
            name: 'Y',
            stage: 'Stage B',
            date: '2026-04-16',
            start: '14:30',
            end: '15:30',
            genre: 'Blues'
        }
    ];

    it('returns status only for stages with acts', () => {
        const statuses = allStageStatuses(acts, locations, 14 * 60 + 30);
        const stageNames = statuses.map((s) => s.stage);
        expect(stageNames).toContain('Stage A');
        expect(stageNames).toContain('Stage B');
        expect(stageNames).not.toContain('Stage C');
    });

    it('computes correct current act per stage', () => {
        const statuses = allStageStatuses(acts, locations, 14 * 60 + 30);
        const a = statuses.find((s) => s.stage === 'Stage A')!;
        const b = statuses.find((s) => s.stage === 'Stage B')!;
        expect(a.current?.slug).toBe('x');
        expect(b.current?.slug).toBe('y');
    });
});

describe('countdownColor', () => {
    it('returns gray at fraction 0', () => {
        expect(countdownColor(0)).toBe(COUNTDOWN_GRAY);
    });

    it('returns green at fraction 1', () => {
        expect(countdownColor(1)).toBe(COUNTDOWN_GREEN);
    });

    it('returns a valid hex color at midpoint', () => {
        const mid = countdownColor(0.5);
        expect(mid).toMatch(/^#[0-9a-f]{6}$/);
        expect(mid).not.toBe(COUNTDOWN_GRAY);
        expect(mid).not.toBe(COUNTDOWN_GREEN);
    });

    it('clamps fraction above 1 to green', () => {
        expect(countdownColor(1.5)).toBe(COUNTDOWN_GREEN);
    });

    it('clamps fraction below 0 to gray', () => {
        expect(countdownColor(-0.5)).toBe(COUNTDOWN_GRAY);
    });
});
