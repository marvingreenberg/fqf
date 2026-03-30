import { describe, it, expect } from 'vitest';
import type { ActSummary } from '$lib/types';
import {
    parseTimeToMinutes,
    formatTimeDisplay,
    formatTime12,
    latLngToPercent,
    stageStatusAt,
    allStageStatuses,
    countdownColor,
    pickedActsForDay,
    buildScheduleMarkers,
    buildPathArrows,
    markerFillColor,
    MIN_PATH_DISTANCE_METERS,
    SCHEDULE_MARKER_PURPLE,
    COUNTDOWN_GREEN,
    COUNTDOWN_GRAY
} from '$lib/map-utils';
import { MAP_BOUNDS, CONFLICT_COLORS } from '$lib/constants';

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

describe('formatTime12', () => {
    it('converts afternoon hour correctly', () => {
        expect(formatTime12('14:30')).toBe('2:30');
    });

    it('keeps noon as 12:00', () => {
        expect(formatTime12('12:00')).toBe('12:00');
    });

    it('converts midnight to 12:00', () => {
        expect(formatTime12('00:00')).toBe('12:00');
    });

    it('preserves morning hours as-is', () => {
        expect(formatTime12('11:00')).toBe('11:00');
    });

    it('zero-pads minutes', () => {
        expect(formatTime12('13:05')).toBe('1:05');
    });

    it('converts 22:00 to 10:00', () => {
        expect(formatTime12('22:00')).toBe('10:00');
    });
});

describe('pickedActsForDay', () => {
    const locations = new Map([
        ['Stage A', { lat: 29.955, lng: -90.063 }],
        ['Stage B', { lat: 29.96, lng: -90.058 }]
    ]);

    const THU = '2026-04-16';
    const FRI = '2026-04-17';

    const acts: ActSummary[] = [
        {
            slug: 'thu-a',
            name: 'Thu A',
            stage: 'Stage A',
            date: THU,
            start: '14:00',
            end: '15:00',
            genre: 'Jazz (Traditional)'
        },
        {
            slug: 'thu-b',
            name: 'Thu B',
            stage: 'Stage B',
            date: THU,
            start: '12:00',
            end: '13:00',
            genre: 'Blues'
        },
        {
            slug: 'fri-a',
            name: 'Fri A',
            stage: 'Stage A',
            date: FRI,
            start: '11:00',
            end: '12:00',
            genre: 'Funk'
        }
    ];

    it('returns only picked acts for the target date', () => {
        const picks = new Set(['thu-a', 'thu-b', 'fri-a']);
        const result = pickedActsForDay(acts, picks, THU, locations);
        expect(result.map((a) => a.slug)).toEqual(['thu-b', 'thu-a']);
    });

    it('excludes unpicked acts', () => {
        const picks = new Set(['thu-a']);
        const result = pickedActsForDay(acts, picks, THU, locations);
        expect(result.map((a) => a.slug)).toEqual(['thu-a']);
    });

    it('excludes acts from other dates', () => {
        const picks = new Set(['thu-a', 'fri-a']);
        const result = pickedActsForDay(acts, picks, THU, locations);
        expect(result.map((a) => a.slug)).toEqual(['thu-a']);
    });

    it('returns empty array when no picks match date', () => {
        const picks = new Set(['fri-a']);
        const result = pickedActsForDay(acts, picks, THU, locations);
        expect(result).toHaveLength(0);
    });

    it('sorts by start time then stage latitude when times match', () => {
        const tieActs: ActSummary[] = [
            {
                slug: 'high-lat',
                name: 'High',
                stage: 'Stage B',
                date: THU,
                start: '14:00',
                end: '15:00',
                genre: 'Jazz (Traditional)'
            },
            {
                slug: 'low-lat',
                name: 'Low',
                stage: 'Stage A',
                date: THU,
                start: '14:00',
                end: '15:00',
                genre: 'Blues'
            }
        ];
        const picks = new Set(['high-lat', 'low-lat']);
        const result = pickedActsForDay(tieActs, picks, THU, locations);
        // Stage A lat=29.955 < Stage B lat=29.96, so Stage A comes first
        expect(result[0].slug).toBe('low-lat');
        expect(result[1].slug).toBe('high-lat');
    });
});

describe('buildScheduleMarkers', () => {
    const locations = new Map([
        ['Stage A', { lat: 29.955, lng: -90.063 }],
        ['Stage B', { lat: 29.96, lng: -90.058 }]
    ]);

    const orderedActs: ActSummary[] = [
        {
            slug: 'act-1',
            name: 'First',
            stage: 'Stage A',
            date: '2026-04-16',
            start: '11:00',
            end: '12:00',
            genre: 'Jazz (Traditional)'
        },
        {
            slug: 'act-2',
            name: 'Second',
            stage: 'Stage B',
            date: '2026-04-16',
            start: '13:00',
            end: '14:00',
            genre: 'Blues'
        }
    ];

    it('assigns order 1 to first act', () => {
        const markers = buildScheduleMarkers(orderedActs, locations);
        expect(markers[0].order).toBe(1);
        expect(markers[0].isFirst).toBe(true);
    });

    it('assigns sequential order numbers', () => {
        const markers = buildScheduleMarkers(orderedActs, locations);
        expect(markers.map((m) => m.order)).toEqual([1, 2]);
    });

    it('marks only first act as isFirst', () => {
        const markers = buildScheduleMarkers(orderedActs, locations);
        expect(markers[0].isFirst).toBe(true);
        expect(markers[1].isFirst).toBe(false);
    });

    it('skips acts with no stage location', () => {
        const actsWithUnknownStage: ActSummary[] = [
            { ...orderedActs[0], stage: 'Unknown Stage' },
            orderedActs[1]
        ];
        const markers = buildScheduleMarkers(actsWithUnknownStage, locations);
        expect(markers).toHaveLength(1);
        expect(markers[0].act.slug).toBe('act-2');
    });

    it('detects overlap conflict between acts', () => {
        const conflictingActs: ActSummary[] = [
            {
                slug: 'c1',
                name: 'C1',
                stage: 'Stage A',
                date: '2026-04-16',
                start: '11:00',
                end: '13:00',
                genre: 'Jazz (Traditional)'
            },
            {
                slug: 'c2',
                name: 'C2',
                stage: 'Stage B',
                date: '2026-04-16',
                start: '12:00',
                end: '14:00',
                genre: 'Blues'
            }
        ];
        const markers = buildScheduleMarkers(conflictingActs, locations);
        expect(markers[0].conflict).toBe('red');
        expect(markers[1].conflict).toBe('red');
    });

    it('has no conflict for non-overlapping acts', () => {
        const markers = buildScheduleMarkers(orderedActs, locations);
        expect(markers[0].conflict).toBe('none');
        expect(markers[1].conflict).toBe('none');
    });
});

describe('buildPathArrows', () => {
    // Stage A ≈ 29.955,-90.063 and Stage B ≈ 29.96,-90.058 are ~750m apart
    const locations = new Map([
        ['Stage A', { lat: 29.955, lng: -90.063 }],
        ['Stage B', { lat: 29.96, lng: -90.058 }]
    ]);

    const farActs: ActSummary[] = [
        {
            slug: 'a',
            name: 'A',
            stage: 'Stage A',
            date: '2026-04-16',
            start: '11:00',
            end: '12:00',
            genre: 'Jazz (Traditional)'
        },
        {
            slug: 'b',
            name: 'B',
            stage: 'Stage B',
            date: '2026-04-16',
            start: '13:00',
            end: '14:00',
            genre: 'Blues'
        }
    ];

    const sameStageActs: ActSummary[] = [
        { ...farActs[0], slug: 'x1' },
        { ...farActs[1], slug: 'x2', stage: 'Stage A' }
    ];

    it('draws an arrow between stages that are far apart', () => {
        const arrows = buildPathArrows(farActs, locations);
        expect(arrows).toHaveLength(1);
    });

    it('skips arrow when acts are at the same stage (distance = 0)', () => {
        const arrows = buildPathArrows(sameStageActs, locations);
        expect(arrows).toHaveLength(0);
    });

    it('records the distance in meters', () => {
        const arrows = buildPathArrows(farActs, locations);
        expect(arrows[0].distanceMeters).toBeGreaterThan(MIN_PATH_DISTANCE_METERS);
    });

    it('returns empty array for a single act', () => {
        const arrows = buildPathArrows([farActs[0]], locations);
        expect(arrows).toHaveLength(0);
    });

    it('skips acts with missing location', () => {
        const actsWithUnknown: ActSummary[] = [{ ...farActs[0], stage: 'Unknown' }, farActs[1]];
        const arrows = buildPathArrows(actsWithUnknown, locations);
        expect(arrows).toHaveLength(0);
    });
});

describe('markerFillColor', () => {
    it('returns purple for first marker regardless of conflict', () => {
        expect(markerFillColor(true, 'red')).toBe(SCHEDULE_MARKER_PURPLE);
        expect(markerFillColor(true, 'none')).toBe(SCHEDULE_MARKER_PURPLE);
    });

    it('returns green for non-first with no conflict', () => {
        expect(markerFillColor(false, 'none')).toBe(CONFLICT_COLORS.none);
    });

    it('returns yellow for non-first with yellow conflict', () => {
        expect(markerFillColor(false, 'yellow')).toBe(CONFLICT_COLORS.yellow);
    });

    it('returns red for non-first with red conflict', () => {
        expect(markerFillColor(false, 'red')).toBe(CONFLICT_COLORS.red);
    });
});
