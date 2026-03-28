/**
 * Geographic distance utilities for stage proximity calculations.
 * Uses Haversine formula with a walking correction factor for the
 * French Quarter street grid.
 */

const EARTH_RADIUS_M = 6_371_000;
const WALKING_CORRECTION = 1.25;
const MAX_ABBREV_LENGTH = 10;
const ABBREV_CUTOFF = 9;
const KM_THRESHOLD = 1000;

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

/** Format a distance in meters for display: "100m" or "1.2km". */
export function formatDistance(meters: number): string {
    const rounded = Math.round(meters);
    if (rounded < KM_THRESHOLD) return `${rounded}m`;
    return `${(rounded / KM_THRESHOLD).toFixed(1)}km`;
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
