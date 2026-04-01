/**
 * Map view utilities: coordinate conversion, act-at-time lookup,
 * countdown color interpolation, and time formatting.
 */

import type { ActSummary, ConflictLevel } from '$lib/types';
import { getWorstConflict, timeToMinutes } from '$lib/conflict';
import {
    MAP_BOUNDS,
    MAX_LOOKAHEAD_MINUTES,
    MINUTES_PER_HOUR,
    CONFLICT_COLORS
} from '$lib/constants';
import { haversineMeters } from '$lib/distance';
import { isPicked as _isPicked, isMaybe as _isMaybe, isSelected } from '$lib/picks';

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

/** Parse "HH:MM" to minutes since midnight. Re-exported from conflict.ts for backward compat. */
export { timeToMinutes as parseTimeToMinutes };

/** Format minutes since midnight as "H:MM AM/PM". */
export function formatTimeDisplay(minutes: number): string {
    const h = Math.floor(minutes / MINUTES_PER_HOUR);
    const m = minutes % MINUTES_PER_HOUR;
    const period = h >= NOON_HOUR ? 'PM' : 'AM';
    const h12 = h > NOON_HOUR ? h - NOON_HOUR : h === 0 ? NOON_HOUR : h;
    return `${h12}:${m.toString().padStart(2, '0')} ${period}`;
}

/**
 * Format an "HH:MM" 24-hour time string to 12-hour without AM/PM suffix.
 * E.g. "14:30" → "2:30", "11:00" → "11:00".
 */
export function formatTime12(hhmm: string): string {
    const [h, m] = hhmm.split(':').map(Number);
    const h12 = h > NOON_HOUR ? h - NOON_HOUR : h === 0 ? NOON_HOUR : h;
    return `${h12}:${m.toString().padStart(2, '0')}`;
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
    const sorted = [...stageActs].sort((a, b) => timeToMinutes(a.start) - timeToMinutes(b.start));

    let current: ActSummary | null = null;
    let next: ActSummary | null = null;

    for (const act of sorted) {
        const start = timeToMinutes(act.start);
        const end = timeToMinutes(act.end);
        if (start <= timeMinutes && timeMinutes < end) {
            current = act;
        } else if (start > timeMinutes && !next) {
            next = act;
        }
    }

    const currentEnd = current ? timeToMinutes(current.end) : 0;
    const currentStart = current ? timeToMinutes(current.start) : 0;
    const currentMinutesRemaining = current ? currentEnd - timeMinutes : 0;
    const currentDuration = current ? Math.max(1, currentEnd - currentStart) : 1;
    const currentFractionRemaining = current ? currentMinutesRemaining / currentDuration : 0;

    const nextMinutesUntil = next ? timeToMinutes(next.start) - timeMinutes : 0;
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

// ── My Schedule map mode ────────────────────────────────────────────────

/** Minimum straight-line distance (meters) before drawing a path arrow. */
export const MIN_PATH_DISTANCE_METERS = 61; // ≈ 200 feet

export const SCHEDULE_MARKER_PURPLE = '#7c3aed';

export interface ScheduleMarker {
    act: ActSummary;
    order: number; // 1-based chronological index
    conflict: ConflictLevel;
    pos: { x: number; y: number }; // CSS % position
    isFirst: boolean;
    stageOffset: number; // 0-based index among markers at the same stage
    isMaybe: boolean;
}

export interface PathArrow {
    from: { x: number; y: number };
    to: { x: number; y: number };
    distanceMeters: number;
}

/**
 * Return picked acts for a specific date, sorted by start time then stage
 * latitude (ascending) when start times are equal.
 */
export function pickedActsForDay(
    allActs: ActSummary[],
    picks: Set<string>,
    date: string,
    stageLocations: Map<string, { lat: number; lng: number }>
): ActSummary[] {
    return allActs
        .filter((a) => isSelected(a.slug, picks) && a.date === date)
        .sort((a, b) => {
            const timeDiff = timeToMinutes(a.start) - timeToMinutes(b.start);
            if (timeDiff !== 0) return timeDiff;
            const aLat = stageLocations.get(a.stage)?.lat ?? 0;
            const bLat = stageLocations.get(b.stage)?.lat ?? 0;
            return aLat - bLat;
        });
}

/**
 * Build the ordered marker list for My Schedule mode.
 * Picked acts get sequential counters; maybe acts borrow a counter without advancing it.
 * Conflict level is computed only for picked acts; maybe acts always have conflict 'none'.
 */
export function buildScheduleMarkers(
    orderedActs: ActSummary[],
    stageLocations: Map<string, { lat: number; lng: number }>,
    picks: Set<string>
): ScheduleMarker[] {
    const stageCounts = new Map<string, number>();
    let pickedCounter = 0;
    let firstPickedSeen = false;

    return orderedActs
        .map((act) => {
            const loc = stageLocations.get(act.stage);
            if (!loc) return null;

            const actIsMaybe = _isMaybe(act.slug, picks);
            const conflict: ConflictLevel = actIsMaybe
                ? 'none'
                : computeConflictForAct(act, orderedActs, picks);

            const offset = stageCounts.get(act.stage) ?? 0;
            stageCounts.set(act.stage, offset + 1);

            let order: number;
            let isFirst = false;
            if (actIsMaybe) {
                const borrowedCounter = findOverlappingPickedCounter(act, orderedActs, picks);
                order = borrowedCounter !== null ? borrowedCounter : pickedCounter + 1;
            } else {
                pickedCounter++;
                order = pickedCounter;
                if (!firstPickedSeen) {
                    isFirst = true;
                    firstPickedSeen = true;
                }
            }

            return {
                act,
                order,
                conflict,
                pos: latLngToPercent(loc.lat, loc.lng),
                isFirst,
                stageOffset: offset,
                isMaybe: actIsMaybe
            };
        })
        .filter((m): m is ScheduleMarker => m !== null);
}

/** Compute worst conflict level — delegates to the shared conflict module. */
function computeConflictForAct(
    act: ActSummary,
    allPickedActs: ActSummary[],
    picks: Set<string>
): ConflictLevel {
    return getWorstConflict(act, allPickedActs, picks);
}

/**
 * Find the sequential counter of a picked act that overlaps with the given maybe act.
 * Iterates picked acts in order (same order as they'd receive counters) and returns
 * the counter of the first overlapping one, or null if none overlap.
 */
function findOverlappingPickedCounter(
    act: ActSummary,
    allActs: ActSummary[],
    picks: Set<string>
): number | null {
    const s1 = timeToMinutes(act.start);
    const e1 = timeToMinutes(act.end);
    let counter = 0;
    for (const other of allActs) {
        if (!_isPicked(other.slug, picks) || other.date !== act.date) continue;
        counter++;
        const s2 = timeToMinutes(other.start);
        const e2 = timeToMinutes(other.end);
        if (Math.max(0, Math.min(e1, e2) - Math.max(s1, s2)) > 0) {
            return counter;
        }
    }
    return null;
}

/**
 * Build path arrows between consecutive PICKED acts in the schedule.
 * Maybe acts are skipped — no arrows lead to or from them.
 * Only draws an arrow when the straight-line distance exceeds MIN_PATH_DISTANCE_METERS.
 */
export function buildPathArrows(
    orderedActs: ActSummary[],
    stageLocations: Map<string, { lat: number; lng: number }>,
    picks: Set<string>
): PathArrow[] {
    const pickedOnly = orderedActs.filter((a) => _isPicked(a.slug, picks));
    const arrows: PathArrow[] = [];
    for (let i = 0; i < pickedOnly.length - 1; i++) {
        const fromAct = pickedOnly[i];
        const toAct = pickedOnly[i + 1];
        const fromLoc = stageLocations.get(fromAct.stage);
        const toLoc = stageLocations.get(toAct.stage);
        if (!fromLoc || !toLoc) continue;
        const distMeters = haversineMeters(fromLoc.lat, fromLoc.lng, toLoc.lat, toLoc.lng);
        if (distMeters <= MIN_PATH_DISTANCE_METERS) continue;
        arrows.push({
            from: latLngToPercent(fromLoc.lat, fromLoc.lng),
            to: latLngToPercent(toLoc.lat, toLoc.lng),
            distanceMeters: distMeters
        });
    }
    return arrows;
}

/** Marker fill color based on conflict level. First act is always purple. */
export function markerFillColor(isFirst: boolean, conflict: ConflictLevel): string {
    if (isFirst) return SCHEDULE_MARKER_PURPLE;
    return CONFLICT_COLORS[conflict];
}
