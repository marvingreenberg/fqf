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

// Question mark SVG path — 16x16 viewBox, unfilled circle with ? inside
export const QUESTION_PATH =
    'M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8S12.42 0 8 0ZM8 14.5C4.42 14.5 1.5 11.58 1.5 8S4.42 1.5 8 1.5 14.5 4.42 14.5 8 11.58 14.5 8 14.5ZM8.8 11h-1.6v-1.6h1.6V11ZM10.72 6.94c-.18.32-.52.68-1.02 1.08-.34.27-.55.49-.64.66-.09.17-.13.41-.13.72H7.37c0-.52.08-.92.25-1.19.17-.27.49-.58.97-.93.37-.27.62-.51.74-.71.12-.2.18-.43.18-.68 0-.32-.11-.58-.34-.78-.23-.2-.54-.3-.94-.3-.4 0-.72.1-.96.31-.24.21-.37.5-.39.87H5.28c.03-.75.29-1.33.79-1.75.5-.42 1.14-.63 1.93-.63.82 0 1.48.2 1.96.6.48.4.72.93.72 1.59 0 .4-.11.76-.33 1.08l.37-.01Z';

// Maybe selection gradient for desktop grid blocks
export const MAYBE_GRADIENT =
    'linear-gradient(to right, rgba(34,197,94,0.2), rgba(200,200,200,0.2))';
