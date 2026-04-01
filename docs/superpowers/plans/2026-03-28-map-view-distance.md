# Map View & Distance Display Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a static-image map view showing stage locations with live current/next act info and countdown colors, plus convert distance display from meters to feet with color-coded thresholds.

**Architecture:** Static OpenStreetMap image served from `ui/static/`, with CSS absolute-positioned stage markers driven by lat/lng-to-percent conversion. A time scrubber controls a reactive computation of current/next act per stage with green-to-gray color interpolation. Distance utility converts meters to rounded feet with threshold-based coloring (green/orange/dark-red).

**Tech Stack:** SvelteKit / Svelte 5 runes, existing stage coordinate data from `/api/v1/stages`, OpenStreetMap static tiles (one-time download), CSS positioning. No new npm dependencies.

---

## File Map

### Modified files

| File | Responsibility |
|------|---------------|
| `ui/src/lib/constants.ts` | Add distance threshold constants + map bounds |
| `ui/src/lib/distance.ts` | Change `formatDistance` to feet, add `distanceStyle` |
| `ui/src/lib/distance.test.ts` | Updated tests for feet + new `distanceStyle` tests |
| `ui/src/lib/types.ts` | Add `'map'` to `ViewMode` union |
| `ui/src/lib/components/MySchedule.svelte` | Apply color styling to distance line |
| `ui/src/routes/+page.svelte` | Add Map tab, render MapView, hide FilterPanel for map |

### New files

| File | Responsibility |
|------|---------------|
| `ui/src/lib/map-utils.ts` | Coordinate conversion, act-at-time lookup, countdown color, time formatting |
| `ui/src/lib/map-utils.test.ts` | Tests for all map utilities |
| `ui/src/lib/components/MapView.svelte` | Map container: background image + time scrubber + positioned markers |
| `ui/src/lib/components/StageMarker.svelte` | Individual stage overlay: name, current/next act, countdown dot |
| `ui/static/fqf-map.png` | Pre-downloaded OpenStreetMap image (~900x750px) |

---

## Task 1: Distance Display — Feet with Color Coding

**Files:**
- Modify: `ui/src/lib/constants.ts`
- Modify: `ui/src/lib/distance.ts`
- Modify: `ui/src/lib/distance.test.ts`
- Modify: `ui/src/lib/components/MySchedule.svelte`

### Context

`formatDistance(meters)` currently returns `"350m"` or `"1.2km"`. It needs to return feet
rounded to the nearest 100 (e.g. `"300 ft"`, `"700 ft"`, `"3300 ft"`). A new `distanceStyle`
function returns inline CSS: green for <600 ft, orange for <1200 ft, dark red bold for >=1200 ft.

The existing `haversineMeters`, `walkingDistanceMeters`, and `shortenStageName` stay unchanged.

---

- [ ] **Step 1: Add distance constants**

In `ui/src/lib/constants.ts`, add after the `MAX_MERGE_TOKENS` line:

```typescript
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
```

---

- [ ] **Step 2: Write failing tests for feet formatting**

Replace the entire `formatDistance` describe block in `ui/src/lib/distance.test.ts` with:

```typescript
describe('formatDistance', () => {
    it('converts meters to feet rounded to nearest 100', () => {
        // 100m * 3.28084 = 328ft → rounds to 300
        expect(formatDistance(100)).toBe('300 ft');
    });

    it('rounds up to nearest 100', () => {
        // 200m * 3.28084 = 656ft → rounds to 700
        expect(formatDistance(200)).toBe('700 ft');
    });

    it('handles large distances', () => {
        // 1000m * 3.28084 = 3281ft → rounds to 3300
        expect(formatDistance(1000)).toBe('3300 ft');
    });

    it('enforces minimum of 100 ft for very short distances', () => {
        // 10m * 3.28084 = 33ft → rounds to 0 → clamped to 100
        expect(formatDistance(10)).toBe('100 ft');
    });
});
```

Also add a new describe block after `formatDistance`:

```typescript
import { distanceStyle } from '$lib/distance';
```

(Add `distanceStyle` to the existing import at the top of the file.)

```typescript
describe('distanceStyle', () => {
    it('returns green style for close distances', () => {
        // 100m = 328ft < 600
        expect(distanceStyle(100)).toContain('#1a7a4a');
    });

    it('returns orange style for medium distances', () => {
        // 250m = 820ft, between 600 and 1200
        expect(distanceStyle(250)).toContain('#d97706');
    });

    it('returns dark red bold style for far distances', () => {
        // 400m = 1312ft >= 1200
        const style = distanceStyle(400);
        expect(style).toContain('#991b1b');
        expect(style).toContain('font-weight: 700');
    });

    it('returns green for distances right at zero', () => {
        // 0m = 0ft < 600
        expect(distanceStyle(0)).toContain('#1a7a4a');
    });
});
```

---

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd ui && pnpm test -- --run src/lib/distance.test.ts`

Expected: FAIL — `formatDistance(100)` returns `"100m"` not `"300 ft"`, and `distanceStyle` does not exist.

---

- [ ] **Step 4: Update formatDistance and add distanceStyle**

In `ui/src/lib/distance.ts`:

1. Replace the import-less top section. Remove `KM_THRESHOLD`. Add imports and new constants:

```typescript
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
```

2. Replace `formatDistance`:

```typescript
/** Format a distance in meters for display as rounded feet. */
export function formatDistance(meters: number): string {
    const feet = meters * METERS_TO_FEET;
    const rounded = Math.max(MIN_DISPLAY_FEET, Math.round(feet / FEET_ROUNDING) * FEET_ROUNDING);
    return `${rounded} ft`;
}
```

3. Add `distanceStyle` after `formatDistance`:

```typescript
/** Return inline CSS style for distance-based color coding. */
export function distanceStyle(meters: number): string {
    const feet = meters * METERS_TO_FEET;
    if (feet < CLOSE_DISTANCE_FT) return `color: ${DISTANCE_COLORS.close};`;
    if (feet < MEDIUM_DISTANCE_FT) return `color: ${DISTANCE_COLORS.medium};`;
    return `color: ${DISTANCE_COLORS.far}; font-weight: 700;`;
}
```

---

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd ui && pnpm test -- --run src/lib/distance.test.ts`

Expected: All tests PASS.

---

- [ ] **Step 6: Update MySchedule.svelte distance display**

In `ui/src/lib/components/MySchedule.svelte`:

1. Update the import line (line 6) to also import `distanceStyle`:

```typescript
import { walkingDistanceMeters, formatDistance, shortenStageName, distanceStyle } from '$lib/distance';
```

2. Replace the distance `<p>` tag (lines 133-135):

Old:
```svelte
<p class="text-[10px] text-surface-400 mt-0.5">
    {formatDistance(d.distance)} from {shortenStageName(d.fromStage)}
</p>
```

New:
```svelte
<p class="text-[10px] mt-0.5" style={distanceStyle(d.distance)}>
    {formatDistance(d.distance)} from {shortenStageName(d.fromStage)}
</p>
```

---

- [ ] **Step 7: Run full frontend test suite**

Run: `cd ui && pnpm test -- --run`

Expected: All tests PASS.

---

- [ ] **Step 8: Commit distance changes**

```
git add ui/src/lib/constants.ts ui/src/lib/distance.ts ui/src/lib/distance.test.ts ui/src/lib/components/MySchedule.svelte
git commit -m "feat: display distance in feet with color-coded thresholds

Convert formatDistance from meters/km to rounded feet.
Add distanceStyle for green (<600ft) / orange (<1200ft) / dark-red-bold (>=1200ft).
Apply color styling in MySchedule distance line."
```

---

## Task 2: Map Utilities — Coordinates, Act Lookup, Countdown Color

**Files:**
- Modify: `ui/src/lib/constants.ts`
- Create: `ui/src/lib/map-utils.ts`
- Create: `ui/src/lib/map-utils.test.ts`

### Context

Three independent utilities needed by the map view:

1. **`latLngToPercent`** — converts stage lat/lng to CSS percentage positions on the
   static map image. Uses a `MAP_BOUNDS` constant (north/south/east/west of the image).
   Linear interpolation is accurate at this scale (~1.2 km).

2. **`stageStatusAt`** / **`allStageStatuses`** — given a list of acts and a time (in
   minutes since midnight), determines the current act and next upcoming act for each
   stage, along with remaining-time fractions for countdown color.

3. **`countdownColor`** — interpolates between gray (`#999999`, fraction=0) and dark
   green (`#1a7a4a`, fraction=1). Used for both current-act-remaining and next-act-approaching.

Also: `parseTimeToMinutes` (parses `"HH:MM"` → minutes) and `formatTimeDisplay`
(minutes → `"2:30 PM"` display string).

---

- [ ] **Step 1: Add map bounds constant**

In `ui/src/lib/constants.ts`, add after the `DISTANCE_COLORS` block:

```typescript
// Map view — bounds must match the static image in ui/static/fqf-map.png
// Computed for center 29.95626,-90.06250 zoom 16, 900x750px
export const MAP_BOUNDS = {
    north: 29.9635,
    south: 29.9490,
    east: -90.0530,
    west: -90.0720
} as const;

export const MAX_LOOKAHEAD_MINUTES = 60;
```

---

- [ ] **Step 2: Write failing tests for map utilities**

Create `ui/src/lib/map-utils.test.ts`:

```typescript
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
        const center = latLngToPercent(29.95626, -90.06250);
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
        const pos = latLngToPercent(29.95107, -90.06280);
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
        ['Stage B', { lat: 29.960, lng: -90.058 }],
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
```

---

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd ui && pnpm test -- --run src/lib/map-utils.test.ts`

Expected: FAIL — module `$lib/map-utils` does not exist.

---

- [ ] **Step 4: Implement map-utils.ts**

Create `ui/src/lib/map-utils.ts`:

```typescript
/**
 * Map view utilities: coordinate conversion, act-at-time lookup,
 * countdown color interpolation, and time formatting.
 */

import type { ActSummary } from '$lib/types';
import { MAP_BOUNDS, MAX_LOOKAHEAD_MINUTES } from '$lib/constants';

// Countdown color endpoints: gray (inactive) ↔ dark green (active)
export const COUNTDOWN_GRAY = '#999999';
export const COUNTDOWN_GREEN = '#1a7a4a';

const HEX_BASE = 16;
const RGB_SHIFT_R = 16;
const RGB_SHIFT_G = 8;
const RGB_MASK = 0xff;
const HEX_PREFIX_OFFSET = 1;
const MINUTES_PER_HOUR = 60;
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
export function latLngToPercent(
    lat: number,
    lng: number
): { x: number; y: number } {
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
    const currentDuration = current ? currentEnd - currentStart : 1;
    const currentFractionRemaining = current
        ? currentMinutesRemaining / currentDuration
        : 0;

    const nextMinutesUntil = next
        ? parseTimeToMinutes(next.start) - timeMinutes
        : 0;
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
    return [...byStage.entries()].map(([stage, stageActs]) =>
        stageStatusAt(stageActs, stage, timeMinutes)
    );
}

// ── Countdown color interpolation ───────────────────────────────────────

function hexToRgb(hex: string): [number, number, number] {
    const n = parseInt(hex.slice(HEX_PREFIX_OFFSET), HEX_BASE);
    return [
        (n >> RGB_SHIFT_R) & RGB_MASK,
        (n >> RGB_SHIFT_G) & RGB_MASK,
        n & RGB_MASK
    ];
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
```

---

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd ui && pnpm test -- --run src/lib/map-utils.test.ts`

Expected: All tests PASS.

---

- [ ] **Step 6: Run full test suite**

Run: `cd ui && pnpm test -- --run`

Expected: All tests PASS (both distance.test.ts and map-utils.test.ts).

---

- [ ] **Step 7: Commit map utilities**

```
git add ui/src/lib/constants.ts ui/src/lib/map-utils.ts ui/src/lib/map-utils.test.ts
git commit -m "feat: add map coordinate, act-lookup, and countdown color utilities

latLngToPercent converts stage GPS to CSS% positions on static map.
stageStatusAt/allStageStatuses compute current+next act per stage at a time.
countdownColor interpolates gray↔green for time-remaining indicators."
```

---

## Task 3: Static Map Image

**Files:**
- Create: `ui/static/fqf-map.png`

### Context

The map view needs a background image of the French Quarter covering all 19 stages
plus the Mississippi River. The image is downloaded once and served as a static asset.

Stage bounding box:
- Lat: 29.95107 (Fish Fry, south) to 29.96145 (Entergy, north) — ~1160m
- Lng: -90.06850 (Jazz Playhouse, west) to -90.05650 (PanAm, east) — ~1160m

Map image must cover `MAP_BOUNDS` (defined in Task 2):
- North: 29.9635, South: 29.9490, East: -90.0530, West: -90.0720

Target size: ~900x750px. The river should be visible at the south edge.

---

- [ ] **Step 1: Download map image**

**Option A — Python script (recommended, reproducible):**

```bash
pip install staticmap Pillow
```

Create and run a temporary script:

```python
# scripts/download_map.py
from staticmap import StaticMap

MAP_WIDTH = 900
MAP_HEIGHT = 750
MAP_CENTER_LNG = -90.06250
MAP_CENTER_LAT = 29.95626
MAP_ZOOM = 16
TILE_URL = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'

m = StaticMap(MAP_WIDTH, MAP_HEIGHT, url_template=TILE_URL)
image = m.render(zoom=MAP_ZOOM, center=[MAP_CENTER_LNG, MAP_CENTER_LAT])
image.save('ui/static/fqf-map.png')
print(f'Saved fqf-map.png ({MAP_WIDTH}x{MAP_HEIGHT})')
```

**Option B — Manual download:**

1. Open https://www.openstreetmap.org/#map=16/29.95626/-90.06250
2. Click "Share" (right sidebar) → "Image" tab
3. Set dimensions to 900x750, check the preview covers all stages and river
4. Download and save to `ui/static/fqf-map.png`

---

- [ ] **Step 2: Verify image dimensions**

```bash
file ui/static/fqf-map.png
# Should show: PNG image data, 900 x 750 (approximately)
```

If dimensions differ significantly from 900x750, the `MAP_BOUNDS` constants
may need adjustment. See calibration step below.

---

- [ ] **Step 3: Calibrate bounds (visual check)**

Start the dev server and temporarily add two test markers at Fish Fry and Entergy
positions to verify they land on the correct map locations. If they're offset,
adjust `MAP_BOUNDS` in `constants.ts` until they align.

Fish Fry expected position: ~48% from left, ~86% from top (south-center).
Entergy expected position: ~72% from left, ~14% from top (north-east area).

---

- [ ] **Step 4: Commit map image**

```
git add ui/static/fqf-map.png
git commit -m "asset: add static OpenStreetMap image for festival map view

900x750 image covering the French Quarter festival area including
the Mississippi River. Source: OpenStreetMap tiles at zoom 16."
```

---

## Task 4: MapView and StageMarker Components

**Files:**
- Modify: `ui/src/lib/types.ts`
- Create: `ui/src/lib/components/StageMarker.svelte`
- Create: `ui/src/lib/components/MapView.svelte`
- Modify: `ui/src/routes/+page.svelte`
- Modify: `ui/src/app.css`

### Context

The map view is a new tab showing the static map image with CSS-positioned
stage markers. A time scrubber (range input) lets the user pick any time
during the festival day. Each marker shows abbreviated stage name, current
act name with a countdown dot, and next act with an approaching dot.

The markers use `position: absolute` with `left`/`top` percentages computed
by `latLngToPercent`. The `transform: translate(-50%, -50%)` centers markers
on their stage point.

The time scrubber range is 11:00 AM to 10:00 PM (matching `GRID_START_HOUR`
and `GRID_END_HOUR`). Default time is 12:00 PM for pre-festival previewing.

---

- [ ] **Step 1: Add 'map' to ViewMode type**

In `ui/src/lib/types.ts`, update the `ViewMode` type:

```typescript
export type ViewMode = 'grid' | 'mobile' | 'my-schedule' | 'merge' | 'map';
```

---

- [ ] **Step 2: Create StageMarker component**

Create `ui/src/lib/components/StageMarker.svelte`:

```svelte
<script lang="ts">
    import type { StageStatus } from '$lib/map-utils';
    import { countdownColor } from '$lib/map-utils';
    import { shortenStageName } from '$lib/distance';

    interface Props {
        status: StageStatus;
        style: string;
    }

    let { status, style }: Props = $props();

    const stageAbbrev = $derived(shortenStageName(status.stage));

    const currentColor = $derived(
        status.current ? countdownColor(status.currentFractionRemaining) : null
    );
    const nextColor = $derived(
        status.next ? countdownColor(status.nextFractionApproaching) : null
    );
</script>

<div class="absolute -translate-x-1/2 -translate-y-full" {style}>
    <div class="fqf-map-marker" class:fqf-map-marker-idle={!status.current && !status.next}>
        <div
            class="text-[9px] font-bold truncate"
            style="color: var(--mg-purple-deep); max-width: 120px;"
        >
            {stageAbbrev}
        </div>

        {#if status.current}
            <div class="flex items-center gap-1">
                <span
                    class="inline-block w-2 h-2 rounded-full shrink-0"
                    style="background: {currentColor};"
                ></span>
                <span class="text-[8px] truncate" style="max-width: 90px;">
                    {status.current.name}
                </span>
                <span class="text-[8px] opacity-60 shrink-0">
                    {status.currentMinutesRemaining}m
                </span>
            </div>
        {/if}

        {#if status.next}
            <div class="flex items-center gap-1">
                <span
                    class="inline-block w-2 h-2 rounded-full shrink-0"
                    style="background: {nextColor};"
                ></span>
                <span class="text-[8px] truncate opacity-60" style="max-width: 90px;">
                    {status.next.name}
                </span>
                <span class="text-[8px] opacity-40 shrink-0">
                    in {status.nextMinutesUntil}m
                </span>
            </div>
        {/if}

        {#if !status.current && !status.next}
            <div class="text-[10px] opacity-30">idle</div>
        {/if}
    </div>

    <!-- Pin point connecting marker to map location -->
    <div class="fqf-map-pin"></div>
</div>
```

---

- [ ] **Step 3: Add map marker CSS**

In `ui/src/app.css`, add at the end:

```css
/* ── Map view markers ───────────────────────────────────────────────────── */
.fqf-map-marker {
    background: rgba(255, 253, 247, 0.92);
    border: 1px solid rgba(74, 26, 107, 0.25);
    border-radius: 0.375rem;
    padding: 0.2rem 0.4rem;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
    max-width: 150px;
    white-space: nowrap;
    pointer-events: auto;
}

.fqf-map-marker-idle {
    opacity: 0.5;
}

.fqf-map-pin {
    width: 2px;
    height: 8px;
    background: rgba(74, 26, 107, 0.4);
    margin: 0 auto;
}

/* ── Map time scrubber ──────────────────────────────────────────────────── */
.fqf-time-scrubber {
    background-color: rgba(255, 253, 247, 0.95);
    border-bottom: 1px solid rgba(74, 26, 107, 0.12);
}

.fqf-time-scrubber input[type='range'] {
    accent-color: var(--mg-purple);
}
```

---

- [ ] **Step 4: Create MapView component**

Create `ui/src/lib/components/MapView.svelte`:

```svelte
<script lang="ts">
    import type { ActSummary } from '$lib/types';
    import { GRID_START_HOUR, GRID_END_HOUR } from '$lib/constants';
    import {
        latLngToPercent,
        allStageStatuses,
        formatTimeDisplay
    } from '$lib/map-utils';
    import StageMarker from '$lib/components/StageMarker.svelte';

    interface Props {
        acts: ActSummary[];
        stageLocations: Map<string, { lat: number; lng: number }>;
    }

    let { acts, stageLocations }: Props = $props();

    const MINUTES_PER_HOUR = 60;
    const SCRUBBER_START = GRID_START_HOUR * MINUTES_PER_HOUR;
    const SCRUBBER_END = GRID_END_HOUR * MINUTES_PER_HOUR;
    const DEFAULT_HOUR = 12;
    const DEFAULT_TIME = DEFAULT_HOUR * MINUTES_PER_HOUR;

    let currentMinutes = $state(DEFAULT_TIME);

    const statuses = $derived(allStageStatuses(acts, stageLocations, currentMinutes));
    const timeLabel = $derived(formatTimeDisplay(currentMinutes));
</script>

<div class="flex flex-col h-full overflow-hidden">
    <!-- Time scrubber -->
    <div class="fqf-time-scrubber flex items-center gap-3 px-4 py-2">
        <span
            class="text-sm font-semibold shrink-0"
            style="color: var(--mg-purple-deep); min-width: 5.5rem;"
        >
            {timeLabel}
        </span>
        <input
            type="range"
            min={SCRUBBER_START}
            max={SCRUBBER_END}
            step={1}
            bind:value={currentMinutes}
            class="flex-1"
            aria-label="Festival time"
        />
    </div>

    <!-- Map container -->
    <div class="flex-1 overflow-auto">
        <div class="relative mx-auto" style="max-width: 900px;">
            <img
                src="/fqf-map.png"
                alt="French Quarter Festival area map"
                class="w-full h-auto block"
                draggable="false"
            />

            <!-- Stage markers positioned by lat/lng -->
            {#each statuses as status (status.stage)}
                {@const loc = stageLocations.get(status.stage)}
                {#if loc}
                    {@const pos = latLngToPercent(loc.lat, loc.lng)}
                    <StageMarker
                        {status}
                        style="left: {pos.x}%; top: {pos.y}%;"
                    />
                {/if}
            {/each}
        </div>
    </div>
</div>
```

---

- [ ] **Step 5: Wire MapView into page routing**

In `ui/src/routes/+page.svelte`:

1. Add import (after the existing component imports, around line 11):

```typescript
import MapView from '$lib/components/MapView.svelte';
```

2. Add "Map" tab to `VIEW_TABS` array (insert as second entry, after 'grid'):

```typescript
const VIEW_TABS: { value: ViewMode; label: () => string }[] = [
    { value: 'grid', label: () => 'All Acts' },
    { value: 'map', label: () => 'Map' },
    { value: 'my-schedule', label: () => `My Schedule (${appState.picks.size})` },
    { value: 'merge', label: () => 'Merge' }
];
```

3. Update the FilterPanel visibility condition (around line 129).
   Hide FilterPanel for map mode — stage/genre filters don't apply to the map.

Old:
```svelte
{#if appState.viewMode !== 'my-schedule' && appState.viewMode !== 'merge'}
```

New:
```svelte
{#if appState.viewMode !== 'my-schedule' && appState.viewMode !== 'merge' && appState.viewMode !== 'map'}
```

4. Add MapView rendering in the view mode switch block (around line 134).
   Insert before the `{:else if appState.viewMode === 'merge'}` branch:

```svelte
{:else if appState.viewMode === 'map'}
    <MapView
        {acts}
        {stageLocations}
    />
```

Note: `acts` is the date-filtered list (loaded when viewMode is not 'my-schedule'),
which is exactly what the map needs — all acts for the selected day.

---

- [ ] **Step 6: Run full test suite and lint**

Run both in parallel:
```bash
cd ui && pnpm test -- --run
cd ui && pnpm run lint
```

Expected: All tests PASS, no lint errors.

Fix any lint issues (likely just formatting — run `cd ui && pnpm run format` if needed).

---

- [ ] **Step 7: Verify with dev server**

```bash
make dev
```

1. Open the app in a browser
2. Click the "Map" tab — verify the map image loads
3. Move the time scrubber — verify stage markers update
4. Check that markers appear at reasonable positions on the map
5. Verify Day Tabs are visible in map mode
6. Verify Filter Panel is NOT visible in map mode
7. Verify other tabs (All Acts, My Schedule, Merge) still work

---

- [ ] **Step 8: Commit map view feature**

```
git add ui/src/lib/types.ts ui/src/lib/components/StageMarker.svelte \
       ui/src/lib/components/MapView.svelte ui/src/routes/+page.svelte \
       ui/src/app.css
git commit -m "feat: add static map view with stage markers and time scrubber

New Map tab shows OpenStreetMap image with CSS-positioned stage markers.
Time scrubber (11AM-10PM) drives current/next act display per stage.
Countdown dots interpolate green↔gray based on time remaining/approaching."
```

---

## Calibration Notes

After Task 3 and Task 4 are complete, the `MAP_BOUNDS` constants may need
fine-tuning to match the actual downloaded image. The theoretical values
assume exact Mercator math at zoom 16 centered on 29.95626, -90.06250.

If markers appear offset from their true stage locations:

1. Pick two stages that are far apart and whose positions you can identify
   on the map (e.g., Fish Fry near the river, Entergy in the north).
2. Note what percent position they SHOULD be at (by visual inspection).
3. Back-compute the correct bounds:
   - `west = lng - x_pct / 100 * (east - west)` (solve for west)
   - Similar for north/south.
4. Update `MAP_BOUNDS` in `constants.ts` and re-run tests.

The `latLngToPercent` tests for Fish Fry (48.4%, 85.7%) and Entergy (72.4%, 14.1%)
encode the expected positions — update these if bounds change.

---

## Future Enhancements (not in scope)

- **Auto-advance**: During the actual festival (April 16-19), default the time scrubber
  to the real clock and auto-advance every 60 seconds.
- **Zoomed cluster views**: Breakout maps for the dense French Market / Dutch Alley area.
- **User picks overlay**: Draw lines connecting the user's picked acts in time order.
- **Marker interaction**: Click a marker to open the act detail modal.
- **GPS location**: Web apps can access GPS via the Geolocation API (`navigator.geolocation`).
  Could show a "You are here" dot on the map. Requires HTTPS and user permission.
