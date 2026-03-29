/**
 * Map view utilities: coordinate conversion, act-at-time lookup,
 * countdown color interpolation, and time formatting.
 */

import type { ActSummary } from '$lib/types';
import { MAP_BOUNDS, MAX_LOOKAHEAD_MINUTES, MINUTES_PER_HOUR } from '$lib/constants';

// Countdown color endpoints: gray (inactive) ↔ dark green (active)
export const COUNTDOWN_GRAY = '#999999';
export const COUNTDOWN_GREEN = '#1a7a4a';

const HEX_BASE = 16;
const RGB_SHIFT_R = 16;
const RGB_SHIFT_G = 8;
const RGB_MASK = 0xff;
const HEX_PREFIX_OFFSET = 1;
const NOON_HOUR = 12;
const PERCENT = 100;

// ── Time parsing ────────────────────────────────────────────────────────

/** Parse "HH:MM" to minutes since midnight. */
export function parseTimeToMinutes(hhmm: string): number {
    const [h, m] = hhmm.split(':').map(Number);
    return h * MINUTES_PER_HOUR + m;
}

/** Format minutes since midnight as "H:MM AM/PM". */
export function formatTimeDisplay(minutes: number): string {
    const h = Math.floor(minutes / MINUTES_PER_HOUR);
    const m = minutes % MINUTES_PER_HOUR;
    const period = h >= NOON_HOUR ? 'PM' : 'AM';
    const h12 = h > NOON_HOUR ? h - NOON_HOUR : h === 0 ? NOON_HOUR : h;
    return `${h12}:${m.toString().padStart(2, '0')} ${period}`;
}

// ── Coordinate conversion ───────────────────────────────────────────────

/** Convert lat/lng to CSS percent position on the static map image. */
export function latLngToPercent(lat: number, lng: number): { x: number; y: number } {
    return {
        x: ((lng - MAP_BOUNDS.west) / (MAP_BOUNDS.east - MAP_BOUNDS.west)) * PERCENT,
        y: ((MAP_BOUNDS.north - lat) / (MAP_BOUNDS.north - MAP_BOUNDS.south)) * PERCENT
    };
}

// ── Act-at-time lookup ──────────────────────────────────────────────────

export interface StageStatus {
    stage: string;
    current: ActSummary | null;
    next: ActSummary | null;
    currentMinutesRemaining: number;
    currentFractionRemaining: number;
    nextMinutesUntil: number;
    nextFractionApproaching: number;
}

/** Compute current and next act status for a single stage at a given time. */
export function stageStatusAt(
    stageActs: ActSummary[],
    stage: string,
    timeMinutes: number
): StageStatus {
    const sorted = [...stageActs].sort(
        (a, b) => parseTimeToMinutes(a.start) - parseTimeToMinutes(b.start)
    );

    let current: ActSummary | null = null;
    let next: ActSummary | null = null;

    for (const act of sorted) {
        const start = parseTimeToMinutes(act.start);
        const end = parseTimeToMinutes(act.end);
        if (start <= timeMinutes && timeMinutes < end) {
            current = act;
        } else if (start > timeMinutes && !next) {
            next = act;
        }
    }

    const currentEnd = current ? parseTimeToMinutes(current.end) : 0;
    const currentStart = current ? parseTimeToMinutes(current.start) : 0;
    const currentMinutesRemaining = current ? currentEnd - timeMinutes : 0;
    const currentDuration = current ? Math.max(1, currentEnd - currentStart) : 1;
    const currentFractionRemaining = current ? currentMinutesRemaining / currentDuration : 0;

    const nextMinutesUntil = next ? parseTimeToMinutes(next.start) - timeMinutes : 0;
    const nextFractionApproaching = next
        ? Math.max(0, 1 - nextMinutesUntil / MAX_LOOKAHEAD_MINUTES)
        : 0;

    return {
        stage,
        current,
        next,
        currentMinutesRemaining,
        currentFractionRemaining,
        nextMinutesUntil,
        nextFractionApproaching
    };
}

/** Compute status for all stages that have acts in the given act list. */
export function allStageStatuses(
    acts: ActSummary[],
    stageLocations: Map<string, { lat: number; lng: number }>,
    timeMinutes: number
): StageStatus[] {
    const byStage = new Map<string, ActSummary[]>();
    for (const act of acts) {
        if (!byStage.has(act.stage)) byStage.set(act.stage, []);
        byStage.get(act.stage)!.push(act);
    }
    return [...byStage.entries()]
        .filter(([stage]) => stageLocations.has(stage))
        .map(([stage, stageActs]) => stageStatusAt(stageActs, stage, timeMinutes));
}

// ── Countdown color interpolation ───────────────────────────────────────

function hexToRgb(hex: string): [number, number, number] {
    const n = parseInt(hex.slice(HEX_PREFIX_OFFSET), HEX_BASE);
    return [(n >> RGB_SHIFT_R) & RGB_MASK, (n >> RGB_SHIFT_G) & RGB_MASK, n & RGB_MASK];
}

function rgbToHex(r: number, g: number, b: number): string {
    return (
        '#' +
        ((1 << (RGB_SHIFT_R + RGB_SHIFT_G)) + (r << RGB_SHIFT_R) + (g << RGB_SHIFT_G) + b)
            .toString(HEX_BASE)
            .slice(HEX_PREFIX_OFFSET)
    );
}

/**
 * Interpolate between gray and green.
 * fraction=0 → gray (idle/far), fraction=1 → green (active/imminent).
 */
export function countdownColor(fraction: number): string {
    const t = Math.max(0, Math.min(1, fraction));
    const [r1, g1, b1] = hexToRgb(COUNTDOWN_GRAY);
    const [r2, g2, b2] = hexToRgb(COUNTDOWN_GREEN);
    return rgbToHex(
        Math.round(r1 + (r2 - r1) * t),
        Math.round(g1 + (g2 - g1) * t),
        Math.round(b1 + (b2 - b1) * t)
    );
}
