/**
 * Geographic distance utilities for stage proximity calculations.
 * Uses Haversine formula with a walking correction factor for the
 * French Quarter street grid.
 */

import {
    METERS_TO_FEET,
    FEET_ROUNDING,
    MIN_DISPLAY_FEET,
    CLOSE_DISTANCE_FT,
    MEDIUM_DISTANCE_FT,
    DISTANCE_COLORS
} from '$lib/constants';

const EARTH_RADIUS_M = 6_371_000;
const WALKING_CORRECTION = 1.25;
const MAX_ABBREV_LENGTH = 10;
const ABBREV_CUTOFF = 9;

function toRadians(deg: number): number {
    return (deg * Math.PI) / 180;
}

/** Straight-line distance in meters between two lat/lng points. */
export function haversineMeters(lat1: number, lng1: number, lat2: number, lng2: number): number {
    const dLat = toRadians(lat2 - lat1);
    const dLng = toRadians(lng2 - lng1);
    const a =
        Math.sin(dLat / 2) ** 2 +
        Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) * Math.sin(dLng / 2) ** 2;
    return EARTH_RADIUS_M * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

/** Approximate walking distance — haversine × 1.25 for street grid. */
export function walkingDistanceMeters(
    lat1: number,
    lng1: number,
    lat2: number,
    lng2: number
): number {
    return haversineMeters(lat1, lng1, lat2, lng2) * WALKING_CORRECTION;
}

/** Format a distance in meters for display as rounded feet. */
export function formatDistance(meters: number): string {
    const feet = meters * METERS_TO_FEET;
    const rounded = Math.max(MIN_DISPLAY_FEET, Math.round(feet / FEET_ROUNDING) * FEET_ROUNDING);
    return `${rounded} ft`;
}

/** Return inline CSS style for distance-based color coding. */
export function distanceStyle(meters: number): string {
    const feet = meters * METERS_TO_FEET;
    if (feet < CLOSE_DISTANCE_FT) return `color: ${DISTANCE_COLORS.close};`;
    if (feet < MEDIUM_DISTANCE_FT) return `color: ${DISTANCE_COLORS.medium};`;
    return `color: ${DISTANCE_COLORS.far}; font-weight: 700;`;
}

/**
 * Abbreviate a stage name to at most 10 characters.
 * Strips trailing " Stage" first, then truncates with "…" if needed.
 */
export function shortenStageName(name: string): string {
    const trimmed = name.replace(/ Stage$/, '');
    if (trimmed.length <= MAX_ABBREV_LENGTH) return trimmed;
    return trimmed.slice(0, ABBREV_CUTOFF) + '\u2026';
}
