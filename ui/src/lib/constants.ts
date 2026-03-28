export const PIXELS_PER_MINUTE = 2;
export const GRID_START_HOUR = 11;
export const GRID_END_HOUR = 22;
export const GRID_COLUMN_MIN_WIDTH = 140;

export const CONFLICT_THRESHOLD = 0.3;

export const CONFLICT_COLORS = {
    none: '#22c55e', // green-500
    yellow: '#eab308', // yellow-500
    red: '#ef4444' // red-500
} as const;

export const MAX_MERGE_TOKENS = 5;

// Distance display (feet)
export const METERS_TO_FEET = 3.28084;
export const FEET_ROUNDING = 100;
export const MIN_DISPLAY_FEET = 100;
export const CLOSE_DISTANCE_FT = 600;
export const MEDIUM_DISTANCE_FT = 1200;

export const DISTANCE_COLORS = {
    close: '#1a7a4a',
    medium: '#d97706',
    far: '#991b1b'
} as const;

// Map view — bounds must match the static image in ui/static/fqf-map.png
// Computed for center 29.95626,-90.06250 zoom 16, 900x750px
export const MAP_BOUNDS = {
    north: 29.9635,
    south: 29.949,
    east: -90.053,
    west: -90.072
} as const;

export const MAX_LOOKAHEAD_MINUTES = 60;
