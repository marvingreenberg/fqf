export const PIXELS_PER_MINUTE = 2;
export const GRID_START_HOUR = 11;
export const GRID_END_HOUR = 22;
export const GRID_COLUMN_MIN_WIDTH = 140;

export const CONFLICT_THRESHOLD = 0.3;

export const CONFLICT_COLORS = {
    none: '#22c55e',
    yellow: '#fcbf19',
    red: '#e02525'
} as const;

export const CONFLICT_COLOR_TEXT = {
    none: '#22c55e',
    yellow: '#7e610c',
    red: '#901b1b'
} as const;

export const PICKED_FLEUR_FILL = CONFLICT_COLORS.none;

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
export const SHOW_NEXT_THRESHOLD_MINUTES = 15;

export const MINUTES_PER_HOUR = 60;

export const SCRUBBER_STEP_MINUTES = 10;

// Festival start: Thu Apr 16, 2026, 11:00 AM Central
export const FESTIVAL_START_ISO = '2026-04-16T11:00:00-05:00';

export const FLEUR_PATH =
    'M8 0C8 0 6.5 3.5 6.5 5.5C6.5 7 7 8 8 9C9 8 9.5 7 9.5 5.5C9.5 3.5 8 0 8 0ZM4.5 6C2.5 6 0 7.5 0 7.5C0 7.5 2 9 4.5 9C5.5 9 6.5 8.5 7 8C6 7.5 5.5 7 4.5 6ZM11.5 6C10.5 7 10 7.5 9 8C9.5 8.5 10.5 9 11.5 9C14 9 16 7.5 16 7.5C16 7.5 13.5 6 11.5 6ZM8 10C7 10 5 10.5 5 12C5 14 8 16 8 16C8 16 11 14 11 12C11 10.5 9 10 8 10Z';
