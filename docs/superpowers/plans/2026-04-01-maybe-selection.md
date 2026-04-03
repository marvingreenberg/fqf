# "Maybe" Selection State Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a third selection state ("maybe") alongside picked/unpicked, represented by a `?` icon, stored as `?slug` in the picks array for backward compatibility.

**Architecture:** Picks remain a `Set<string>` but entries can be `"slug"` (picked) or `"?slug"` (maybe). Helper functions abstract the prefix logic. A new SVG question mark icon appears alongside the fleur-de-lis in all interactive views. Maybe acts appear on My Schedule maps with borrowed counters but don't generate conflicts or path arrows. In the Share view, each user's emoji circle gains a small fleur/? sub-indicator when that user has the act picked or maybe'd.

**Tech Stack:** SvelteKit, Svelte 5 runes, TypeScript, existing conflict/map-utils modules

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `ui/src/lib/constants.ts` | Modify | Add `MAYBE_PREFIX`, `QUESTION_PATH` SVG, `MAYBE_GRADIENT_BG` |
| `ui/src/lib/picks.ts` | Create | Pure helper functions: `isPicked`, `isMaybe`, `isSelected`, `bareSlug`, `togglePick`, `toggleMaybe` |
| `ui/src/lib/stores.svelte.ts` | Modify | Use picks.ts helpers; add `toggleMaybe`; update `isPicked`/add `isMaybe`/`isSelected` |
| `ui/src/lib/conflict.ts` | Modify | Filter out `?`-prefixed slugs in `getWorstConflict` |
| `ui/src/lib/map-utils.ts` | Modify | Update `pickedActsForDay`, `buildScheduleMarkers`, `buildPathArrows` for maybe acts |
| `ui/src/lib/components/PickButtons.svelte` | Create | Shared fleur + `?` button pair (interactive) |
| `ui/src/lib/components/ActRow.svelte` | Modify | Replace inline fleur with `PickButtons` |
| `ui/src/lib/components/ActBlock.svelte` | Modify | Replace inline fleur with `PickButtons`; add gradient background for maybe |
| `ui/src/lib/components/ActDetailModal.svelte` | Modify | Replace inline fleur with `PickButtons` |
| `ui/src/lib/components/MapActLabel.svelte` | Modify | Accept `isMaybe` prop; show `?` icon instead of fleur when maybe |
| `ui/src/lib/components/StageMarker.svelte` | Modify | Pass `isMaybe` to MapActLabel |
| `ui/src/lib/components/MapView.svelte` | Modify | Handle maybe acts in My Schedule (counter logic, no arrows); pass `isMaybe` |
| `ui/src/lib/components/ShareView.svelte` | Modify | Add fleur/? sub-indicator on emoji circles |
| `ui/src/lib/components/MobileSchedule.svelte` | Modify | Maybe acts appear, no conflict badges |
| `ui/src/lib/components/MySchedule.svelte` | Modify | Maybe acts appear, no conflict badges |
| `ui/src/app.css` | Modify | Add `.fqf-act-block.maybe` gradient style; `.fqf-emoji-sub-indicator` styles |
| `tests/` | Modify/Create | Tests for picks.ts, updated conflict.ts tests, updated map-utils tests |

---

### Task 1: Core picks helper module

**Files:**
- Create: `ui/src/lib/picks.ts`
- Create: `ui/src/lib/picks.test.ts`

This module provides pure functions that abstract the `?` prefix convention. Every other module imports from here instead of inspecting prefixes directly.

- [ ] **Step 1: Write failing tests for picks helpers**

```typescript
// ui/src/lib/picks.test.ts
import { describe, it, expect } from 'vitest';
import {
    MAYBE_PREFIX,
    bareSlug,
    isPicked,
    isMaybe,
    isSelected,
    togglePick,
    toggleMaybe
} from '$lib/picks';

describe('bareSlug', () => {
    it('strips ? prefix', () => {
        expect(bareSlug('?foo')).toBe('foo');
    });
    it('returns bare slug unchanged', () => {
        expect(bareSlug('foo')).toBe('foo');
    });
});

describe('isPicked', () => {
    it('returns true for bare slug in set', () => {
        expect(isPicked('foo', new Set(['foo']))).toBe(true);
    });
    it('returns false for ?-prefixed slug in set', () => {
        expect(isPicked('foo', new Set(['?foo']))).toBe(false);
    });
    it('returns false for missing slug', () => {
        expect(isPicked('foo', new Set())).toBe(false);
    });
});

describe('isMaybe', () => {
    it('returns true for ?-prefixed slug in set', () => {
        expect(isMaybe('foo', new Set(['?foo']))).toBe(true);
    });
    it('returns false for bare slug in set', () => {
        expect(isMaybe('foo', new Set(['foo']))).toBe(false);
    });
});

describe('isSelected', () => {
    it('returns true for picked', () => {
        expect(isSelected('foo', new Set(['foo']))).toBe(true);
    });
    it('returns true for maybe', () => {
        expect(isSelected('foo', new Set(['?foo']))).toBe(true);
    });
    it('returns false for neither', () => {
        expect(isSelected('foo', new Set())).toBe(false);
    });
});

describe('togglePick', () => {
    it('unpicked → picked', () => {
        const picks = new Set<string>();
        const next = togglePick('foo', picks);
        expect(next.has('foo')).toBe(true);
        expect(next.has('?foo')).toBe(false);
    });
    it('picked → unpicked', () => {
        const picks = new Set(['foo']);
        const next = togglePick('foo', picks);
        expect(next.has('foo')).toBe(false);
    });
    it('maybe → picked (clears maybe)', () => {
        const picks = new Set(['?foo']);
        const next = togglePick('foo', picks);
        expect(next.has('foo')).toBe(true);
        expect(next.has('?foo')).toBe(false);
    });
});

describe('toggleMaybe', () => {
    it('unpicked → maybe', () => {
        const picks = new Set<string>();
        const next = toggleMaybe('foo', picks);
        expect(next.has('?foo')).toBe(true);
        expect(next.has('foo')).toBe(false);
    });
    it('maybe → unpicked', () => {
        const picks = new Set(['?foo']);
        const next = toggleMaybe('foo', picks);
        expect(next.has('?foo')).toBe(false);
    });
    it('picked → maybe (clears pick)', () => {
        const picks = new Set(['foo']);
        const next = toggleMaybe('foo', picks);
        expect(next.has('?foo')).toBe(true);
        expect(next.has('foo')).toBe(false);
    });
});
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `do_cmd -d ui -- pnpm vitest run src/lib/picks.test.ts`
Expected: FAIL — module not found

- [ ] **Step 3: Implement picks.ts**

```typescript
// ui/src/lib/picks.ts
export const MAYBE_PREFIX = '?';

/** Strip the maybe prefix if present; always returns a bare slug. */
export function bareSlug(entry: string): string {
    return entry.startsWith(MAYBE_PREFIX) ? entry.slice(MAYBE_PREFIX.length) : entry;
}

/** True if the act is definitively picked (not maybe). */
export function isPicked(slug: string, picks: Set<string>): boolean {
    return picks.has(slug);
}

/** True if the act is in the maybe state. */
export function isMaybe(slug: string, picks: Set<string>): boolean {
    return picks.has(MAYBE_PREFIX + slug);
}

/** True if the act is picked or maybe. */
export function isSelected(slug: string, picks: Set<string>): boolean {
    return isPicked(slug, picks) || isMaybe(slug, picks);
}

/**
 * Toggle the picked state for an act. Returns a new Set.
 * Unpicked → picked. Picked → unpicked. Maybe → picked.
 */
export function togglePick(slug: string, picks: Set<string>): Set<string> {
    const next = new Set(picks);
    const maybeKey = MAYBE_PREFIX + slug;
    if (next.has(slug)) {
        next.delete(slug);
    } else {
        next.delete(maybeKey);
        next.add(slug);
    }
    return next;
}

/**
 * Toggle the maybe state for an act. Returns a new Set.
 * Unpicked → maybe. Maybe → unpicked. Picked → maybe.
 */
export function toggleMaybe(slug: string, picks: Set<string>): Set<string> {
    const next = new Set(picks);
    const maybeKey = MAYBE_PREFIX + slug;
    if (next.has(maybeKey)) {
        next.delete(maybeKey);
    } else {
        next.delete(slug);
        next.add(maybeKey);
    }
    return next;
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `do_cmd -d ui -- pnpm vitest run src/lib/picks.test.ts`
Expected: All PASS

- [ ] **Step 5: Commit**

```
feat: add picks helper module with maybe state support
```

---

### Task 2: Question mark SVG and constants

**Files:**
- Modify: `ui/src/lib/constants.ts`

- [ ] **Step 1: Add constants**

Add to `ui/src/lib/constants.ts`:

```typescript
// Question mark SVG path — 16x16 viewBox, matches fleur dimensions
// Unfilled circle with ? inside
export const QUESTION_PATH =
    'M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8S12.42 0 8 0ZM8 14.5C4.42 14.5 1.5 11.58 1.5 8S4.42 1.5 8 1.5 14.5 4.42 14.5 8 11.58 14.5 8 14.5ZM8.8 11h-1.6v-1.6h1.6V11ZM10.72 6.94c-.18.32-.52.68-1.02 1.08-.34.27-.55.49-.64.66-.09.17-.13.41-.13.72H7.37c0-.52.08-.92.25-1.19.17-.27.49-.58.97-.93.37-.27.62-.51.74-.71.12-.2.18-.43.18-.68 0-.32-.11-.58-.34-.78-.23-.2-.54-.3-.94-.3-.4 0-.72.1-.96.31-.24.21-.37.5-.39.87H5.28c.03-.75.29-1.33.79-1.75.5-.42 1.14-.63 1.93-.63.82 0 1.48.2 1.96.6.48.4.72.93.72 1.59 0 .4-.11.76-.33 1.08l.37-.01Z';

// Maybe selection gradient for desktop grid blocks
export const MAYBE_GRADIENT = 'linear-gradient(to right, rgba(34,197,94,0.2), rgba(200,200,200,0.2))';
```

- [ ] **Step 2: Build to verify no errors**

Run: `do_cmd -d ui -- pnpm build`
Expected: success

- [ ] **Step 3: Commit**

```
feat: add question mark SVG path and maybe gradient constants
```

---

### Task 3: Update conflict system to ignore maybe acts

**Files:**
- Modify: `ui/src/lib/conflict.ts`
- Modify: `ui/src/lib/conflict.test.ts`

Maybe acts (`?slug`) should never participate in conflict detection.

- [ ] **Step 1: Write failing test**

Add to `ui/src/lib/conflict.test.ts`:

```typescript
describe('getWorstConflict with maybe picks', () => {
    it('ignores maybe-prefixed picks in conflict calculation', () => {
        const act1: ActSummary = { slug: 'a', name: 'A', stage: 'S1', date: '2026-04-16', start: '11:00', end: '12:00', genre: 'Jazz' };
        const act2: ActSummary = { slug: 'b', name: 'B', stage: 'S2', date: '2026-04-16', start: '11:30', end: '12:30', genre: 'Jazz' };
        // act2 is a maybe — should not cause conflict for act1
        const picks = new Set(['a', '?b']);
        expect(getWorstConflict(act1, [act1, act2], picks)).toBe('none');
    });

    it('ignores maybe-prefixed act as the subject', () => {
        const act1: ActSummary = { slug: 'a', name: 'A', stage: 'S1', date: '2026-04-16', start: '11:00', end: '12:00', genre: 'Jazz' };
        const act2: ActSummary = { slug: 'b', name: 'B', stage: 'S2', date: '2026-04-16', start: '11:30', end: '12:30', genre: 'Jazz' };
        const picks = new Set(['?a', 'b']);
        // ?a is maybe, so it has no conflicts
        expect(getWorstConflict(act1, [act1, act2], picks)).toBe('none');
    });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `do_cmd -d ui -- pnpm vitest run src/lib/conflict.test.ts`
Expected: FAIL — maybe picks still count as conflicts

- [ ] **Step 3: Update getWorstConflict**

In `ui/src/lib/conflict.ts`, modify `getWorstConflict`:

```typescript
import { isPicked, MAYBE_PREFIX } from '$lib/picks';

export function getWorstConflict(
    act: ActSummary,
    allActs: ActSummary[],
    picks: Set<string>
): ConflictLevel {
    // Maybe acts never have conflicts
    if (!isPicked(act.slug, picks)) return 'none';

    let worst: ConflictLevel = 'none';
    const s1 = timeToMinutes(act.start);
    const e1 = timeToMinutes(act.end);

    for (const other of allActs) {
        if (other.slug === act.slug) continue;
        // Only definite picks cause conflicts (not ?-prefixed)
        if (!isPicked(other.slug, picks)) continue;
        if (other.date !== act.date) continue;

        const s2 = timeToMinutes(other.start);
        const e2 = timeToMinutes(other.end);
        const ratio = calculateOverlapRatio(s1, e1, s2, e2);
        const level = getConflictLevel(ratio);

        if (CONFLICT_SEVERITY[level] > CONFLICT_SEVERITY[worst]) {
            worst = level;
        }
        if (worst === 'red') break;
    }

    return worst;
}
```

The key change: replace `picks.has(other.slug)` with `isPicked(other.slug, picks)` which only matches bare slugs, not `?`-prefixed ones. And guard the subject act similarly.

- [ ] **Step 4: Run tests to verify they pass**

Run: `do_cmd -d ui -- pnpm vitest run src/lib/conflict.test.ts`
Expected: All PASS

- [ ] **Step 5: Commit**

```
feat: exclude maybe acts from conflict detection
```

---

### Task 4: Update stores to support maybe

**Files:**
- Modify: `ui/src/lib/stores.svelte.ts`

- [ ] **Step 1: Add toggleMaybe and update helpers**

```typescript
import {
    isPicked as _isPicked,
    isMaybe as _isMaybe,
    isSelected as _isSelected,
    togglePick as _togglePick,
    toggleMaybe as _toggleMaybe
} from '$lib/picks';

// In AppState class:

togglePick(slug: string): void {
    this.picks = _togglePick(slug, this.picks);
    this.scheduleSave();
}

toggleMaybe(slug: string): void {
    this.picks = _toggleMaybe(slug, this.picks);
    this.scheduleSave();
}

isPicked(slug: string): boolean {
    return _isPicked(slug, this.picks);
}

isMaybe(slug: string): boolean {
    return _isMaybe(slug, this.picks);
}

isSelected(slug: string): boolean {
    return _isSelected(slug, this.picks);
}
```

- [ ] **Step 2: Update picks count in tab label**

In `ui/src/routes/fq2026/+page.svelte`, the "My Schedule" tab label uses `appState.picks.size`. This now counts both picked and maybe entries. This is correct per requirement ("just the total count").

- [ ] **Step 3: Build and run tests**

Run: `do_cmd -d ui -- pnpm build && do_cmd -d ui -- pnpm vitest run`
Expected: Build success, all tests pass

- [ ] **Step 4: Commit**

```
feat: add toggleMaybe and selection helpers to app state
```

---

### Task 5: PickButtons shared component

**Files:**
- Create: `ui/src/lib/components/PickButtons.svelte`

A shared component rendering the fleur and `?` buttons side by side. Used by ActRow, ActBlock, and ActDetailModal.

- [ ] **Step 1: Create PickButtons.svelte**

```svelte
<script lang="ts">
    import { FLEUR_PATH, QUESTION_PATH, PICKED_FLEUR_FILL } from '$lib/constants';

    const FLEUR_VIEWBOX = '0 0 16 16';
    const UNPICKED_STROKE = 'rgba(74, 26, 107, 0.3)';
    const UNPICKED_STROKE_WIDTH = 0.75;
    const MAYBE_FILL = PICKED_FLEUR_FILL; // same green for both states

    interface Props {
        isPicked: boolean;
        isMaybe: boolean;
        size?: number;
        onTogglePick: () => void;
        onToggleMaybe: () => void;
        ariaName?: string;
    }

    let {
        isPicked,
        isMaybe,
        size = 14,
        onTogglePick,
        onToggleMaybe,
        ariaName = 'act'
    }: Props = $props();

    const containerSize = $derived(`${size / 14}rem`);
</script>

<div class="flex items-center gap-0.5 shrink-0">
    <button
        class="fqf-fleur"
        style="width: {containerSize}; height: {containerSize};"
        onclick={(e) => {
            e.stopPropagation();
            onTogglePick();
        }}
        aria-label={isPicked ? `Remove ${ariaName} from picks` : `Add ${ariaName} to picks`}
    >
        <svg
            viewBox={FLEUR_VIEWBOX}
            width={size}
            height={size}
            fill={isPicked ? PICKED_FLEUR_FILL : 'none'}
            stroke={isPicked ? 'none' : UNPICKED_STROKE}
            stroke-width={isPicked ? 0 : UNPICKED_STROKE_WIDTH}
        >
            <path d={FLEUR_PATH} />
        </svg>
    </button>
    <button
        class="fqf-fleur"
        style="width: {containerSize}; height: {containerSize};"
        onclick={(e) => {
            e.stopPropagation();
            onToggleMaybe();
        }}
        aria-label={isMaybe ? `Remove ${ariaName} from maybes` : `Mark ${ariaName} as maybe`}
    >
        <svg
            viewBox={FLEUR_VIEWBOX}
            width={size}
            height={size}
            fill={isMaybe ? MAYBE_FILL : 'none'}
            stroke={isMaybe ? 'none' : UNPICKED_STROKE}
            stroke-width={isMaybe ? 0 : UNPICKED_STROKE_WIDTH}
        >
            <path d={QUESTION_PATH} />
        </svg>
    </button>
</div>
```

- [ ] **Step 2: Build to verify**

Run: `do_cmd -d ui -- pnpm build`
Expected: success

- [ ] **Step 3: Commit**

```
feat: add PickButtons component with fleur and question mark
```

---

### Task 6: Replace inline fleur in ActRow, ActBlock, ActDetailModal

**Files:**
- Modify: `ui/src/lib/components/ActRow.svelte`
- Modify: `ui/src/lib/components/ActBlock.svelte`
- Modify: `ui/src/lib/components/ActDetailModal.svelte`
- Modify: `ui/src/app.css`

Each component currently has inline fleur SVG rendering. Replace with `PickButtons`. Add `isMaybe` and `onToggleMaybe` props. For ActBlock, add the maybe gradient background.

- [ ] **Step 1: Update ActRow**

Add props `isMaybe: boolean` and `onToggleMaybe: (slug: string) => void`. Replace the inline fleur button block with:

```svelte
{#if !readOnly}
    <PickButtons
        {isPicked}
        {isMaybe}
        size={18}
        onTogglePick={() => onTogglePick(act.slug)}
        onToggleMaybe={() => onToggleMaybe(act.slug)}
        ariaName={act.name}
    />
{/if}
```

- [ ] **Step 2: Update ActBlock**

Add props `isMaybe: boolean` and `onToggleMaybe: () => void`. Replace inline fleur with:

```svelte
{#if !readOnly}
    <PickButtons
        {isPicked}
        {isMaybe}
        size={14}
        onTogglePick={() => onToggle()}
        onToggleMaybe={() => onToggleMaybe()}
        ariaName={act.name}
    />
{/if}
```

Update `blockClass` to include maybe state:

```typescript
const blockClass = $derived.by(() => {
    let cls = 'fqf-act-block';
    if (isPicked) cls += ' picked';
    else if (isMaybe) cls += ' maybe';
    return cls;
});
```

Add CSS in `ui/src/app.css`:

```css
.fqf-act-block.maybe {
    background: linear-gradient(to right, rgba(34, 197, 94, 0.2), rgba(200, 200, 200, 0.2));
    border-color: var(--mg-green-deep);
    border-width: 1.5px;
}
```

- [ ] **Step 3: Update ActDetailModal**

Add `isMaybe: boolean` and `onToggleMaybe?: () => void` props. Replace inline fleur with `PickButtons` (size=20).

- [ ] **Step 4: Update callers**

In all parent components that render ActRow, ActBlock, ActDetailModal:

- `ScheduleGrid.svelte`: pass `isMaybe={appState.isMaybe(act.slug)}` and `onToggleMaybe={() => appState.toggleMaybe(act.slug)}` to ActBlock
- `MobileSchedule.svelte`: pass `isMaybe` and `onToggleMaybe` to ActRow
- `MySchedule.svelte`: pass `isMaybe` and `onToggleMaybe` to ActRow
- `ShareView.svelte`: pass `isMaybe={appState.isMaybe(act.slug)}` and `onToggleMaybe` to ActRow
- `+page.svelte` (main): pass `isMaybe` and `onToggleMaybe` to ActDetailModal
- `+page.svelte` (share): pass `isMaybe={false}` and no-op `onToggleMaybe` to ActDetailModal (readOnly)

- [ ] **Step 5: Build and lint**

Run: `do_cmd -d ui -- pnpm build && do_cmd -d ui -- pnpm lint`
Expected: success

- [ ] **Step 6: Commit**

```
feat: replace inline fleur with PickButtons in all act views
```

---

### Task 7: Map view — maybe acts with question mark icon

**Files:**
- Modify: `ui/src/lib/components/MapActLabel.svelte`
- Modify: `ui/src/lib/components/StageMarker.svelte`
- Modify: `ui/src/lib/components/MapView.svelte`

- [ ] **Step 1: Update MapActLabel to show ? for maybe acts**

Add `isMaybe?: boolean` prop (default false). When true, render `QUESTION_PATH` instead of `FLEUR_PATH`:

```svelte
import { FLEUR_PATH, QUESTION_PATH } from '$lib/constants';

const iconPath = $derived(isMaybe ? QUESTION_PATH : FLEUR_PATH);
```

Use `iconPath` in the SVG `<path d={iconPath} ... />`.

- [ ] **Step 2: Update StageMarker**

Already computes `isPicked`. Add `isMaybeAct` derived:

```typescript
import { isMaybe as _isMaybe } from '$lib/picks';
const isMaybeAct = $derived(displayAct ? _isMaybe(displayAct.slug, picks) : false);
```

For fleur fill: maybe acts get green (same as picked). Pass `isMaybe={isMaybeAct}` to MapActLabel.

For conflict: maybe acts never show conflict borders (borderStyle stays empty).

- [ ] **Step 3: Update MapView My Schedule section**

Pass `isMaybe` to MapActLabel in the My Schedule markers:

```svelte
{@const actIsMaybe = isMaybe(marker.act.slug, picks)}
<MapActLabel
    ...
    isMaybe={actIsMaybe}
    isPicked={!actIsMaybe}
    ...
/>
```

- [ ] **Step 4: Build and lint**

Run: `do_cmd -d ui -- pnpm build && do_cmd -d ui -- pnpm lint`
Expected: success

- [ ] **Step 5: Commit**

```
feat: show question mark icon for maybe acts on map
```

---

### Task 8: Map My Schedule — maybe counter logic and no arrows

**Files:**
- Modify: `ui/src/lib/map-utils.ts`
- Modify: `ui/src/lib/map-utils.test.ts`

Maybe acts appear in My Schedule but:
1. Their counter borrows from the nearest overlapping picked act, or prev_picked + 1 if no overlap
2. The counter does not advance — next picked act gets its natural number
3. No path arrows are drawn to/from maybe acts

- [ ] **Step 1: Write failing tests**

Add to `ui/src/lib/map-utils.test.ts`:

```typescript
describe('buildScheduleMarkers with maybe acts', () => {
    it('assigns borrowed counter to maybe act overlapping a picked act', () => {
        // picked act #1 at 11:00-12:00, maybe at 11:30-12:30, picked #2 at 13:00-14:00
        const acts = [
            { slug: 'a', start: '11:00', end: '12:00', stage: 'S1', ... },
            { slug: 'b', start: '11:30', end: '12:30', stage: 'S2', ... },
            { slug: 'c', start: '13:00', end: '14:00', stage: 'S1', ... },
        ];
        const picks = new Set(['a', '?b', 'c']);
        const markers = buildScheduleMarkers(acts, stageLocations, picks);
        // a → order 1, b (maybe) → order 1 (borrows from a), c → order 2
        expect(markers[0].order).toBe(1); // a
        expect(markers[1].order).toBe(1); // b (maybe, overlaps a)
        expect(markers[2].order).toBe(2); // c
    });

    it('assigns prev+1 counter to maybe act with no overlap', () => {
        const acts = [
            { slug: 'a', start: '11:00', end: '12:00', stage: 'S1', ... },
            { slug: 'b', start: '14:00', end: '15:00', stage: 'S2', ... },
            { slug: 'c', start: '16:00', end: '17:00', stage: 'S1', ... },
        ];
        const picks = new Set(['a', '?b', 'c']);
        const markers = buildScheduleMarkers(acts, stageLocations, picks);
        // a → 1, b (maybe, no overlap) → 2, c → 2 (counter didn't advance)
        expect(markers[0].order).toBe(1);
        expect(markers[1].order).toBe(2);
        expect(markers[2].order).toBe(2);
    });
});

describe('buildPathArrows with maybe acts', () => {
    it('skips maybe acts in arrow path', () => {
        const acts = [
            { slug: 'a', start: '11:00', end: '12:00', stage: 'S1', ... },
            { slug: 'b', start: '12:30', end: '13:30', stage: 'S2', ... }, // maybe
            { slug: 'c', start: '14:00', end: '15:00', stage: 'S3', ... },
        ];
        const picks = new Set(['a', '?b', 'c']);
        const arrows = buildPathArrows(acts, stageLocations, picks);
        // Arrow from a→c, skipping maybe b
        expect(arrows.length).toBe(1); // or 0 if distance < threshold
    });
});
```

(Fill in full ActSummary fields with date/genre as needed.)

- [ ] **Step 2: Run tests to verify they fail**

Run: `do_cmd -d ui -- pnpm vitest run src/lib/map-utils.test.ts`
Expected: FAIL

- [ ] **Step 3: Update pickedActsForDay**

`pickedActsForDay` currently filters on `picks.has(a.slug)`. Update to include both picked and maybe acts:

```typescript
import { isSelected, bareSlug, isPicked as _isPicked, isMaybe as _isMaybe } from '$lib/picks';

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
```

- [ ] **Step 4: Update buildScheduleMarkers**

Pass `picks` as a parameter. Compute counter for maybe acts:

```typescript
export function buildScheduleMarkers(
    orderedActs: ActSummary[],
    stageLocations: Map<string, { lat: number; lng: number }>,
    picks: Set<string>
): ScheduleMarker[] {
    const stageCounts = new Map<string, number>();
    let pickedCounter = 0;

    return orderedActs
        .map((act) => {
            const loc = stageLocations.get(act.stage);
            if (!loc) return null;
            const actIsMaybe = _isMaybe(act.slug, picks);
            const conflict = actIsMaybe ? 'none' as ConflictLevel : computeConflictForAct(act, orderedActs, picks);
            const offset = stageCounts.get(act.stage) ?? 0;
            stageCounts.set(act.stage, offset + 1);

            let order: number;
            if (actIsMaybe) {
                // Borrow counter from nearest overlapping picked act
                const overlapping = findOverlappingPickedAct(act, orderedActs, picks);
                order = overlapping !== null ? overlapping : pickedCounter + 1;
                // Don't increment pickedCounter
            } else {
                pickedCounter++;
                order = pickedCounter;
            }

            return {
                act,
                order,
                conflict,
                pos: latLngToPercent(loc.lat, loc.lng),
                isFirst: pickedCounter === 1 && !actIsMaybe,
                stageOffset: offset,
                isMaybe: actIsMaybe
            };
        })
        .filter((m): m is ScheduleMarker => m !== null);
}

/** Find the counter of the first picked act that overlaps this act. */
function findOverlappingPickedAct(
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
```

Add `isMaybe: boolean` to the `ScheduleMarker` interface.

- [ ] **Step 5: Update buildPathArrows**

Only draw arrows between consecutive *picked* (non-maybe) acts:

```typescript
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
```

- [ ] **Step 6: Update MapView.svelte calls**

Pass `picks` to `buildScheduleMarkers` and `buildPathArrows`:

```typescript
const scheduleMarkers = $derived(
    appState.mapMode === 'my-schedule' ? buildScheduleMarkers(orderedPicks, stageLocations, picks) : []
);
const pathArrows = $derived(
    appState.mapMode === 'my-schedule' && appState.mapShowPaths
        ? buildPathArrows(orderedPicks, stageLocations, picks)
        : []
);
```

- [ ] **Step 7: Run tests**

Run: `do_cmd -d ui -- pnpm vitest run`
Expected: All PASS

- [ ] **Step 8: Commit**

```
feat: maybe counter logic and skip arrows for maybe acts
```

---

### Task 9: Share view — fleur/? sub-indicators on emoji circles

**Files:**
- Modify: `ui/src/lib/components/ShareView.svelte`
- Modify: `ui/src/app.css`

In the share view, each user's emoji circle should show a small fleur or `?` sub-indicator when that user has an act picked or maybe'd. The indicators are slightly smaller font in slightly larger circles.

- [ ] **Step 1: Update ShareView emoji rendering**

In the `{#snippet extra()}` block that renders picker emoji circles, add a sub-indicator:

```svelte
{#each pickers as id (id)}
    {@const entry = allEntries.find((e) => e.id === id)}
    {@const entryPicks = entry ? (entry.id === appState.token ? appState.picks : new Set(appState.sharedSchedules.find(s => s.share_id === entry.id)?.picks ?? [])) : new Set<string>()}
    {@const pickedByEntry = isPicked(act.slug, entryPicks)}
    {@const maybeByEntry = isMaybe(act.slug, entryPicks)}
    <span
        class="fqf-emoji-circle fqf-emoji-circle-with-sub {badgeClass(id)}"
        title={entry?.label ?? id}
    >
        {emojiMap[id] ?? '?'}
        {#if pickedByEntry}
            <span class="fqf-emoji-sub-indicator">
                <svg viewBox="0 0 16 16" width="8" height="8" fill="#22c55e">
                    <path d={FLEUR_PATH} />
                </svg>
            </span>
        {:else if maybeByEntry}
            <span class="fqf-emoji-sub-indicator">
                <svg viewBox="0 0 16 16" width="8" height="8" fill="#22c55e">
                    <path d={QUESTION_PATH} />
                </svg>
            </span>
        {/if}
    </span>
{/each}
```

- [ ] **Step 2: Add CSS for sub-indicator**

```css
.fqf-emoji-circle-with-sub {
    position: relative;
}

.fqf-emoji-sub-indicator {
    position: absolute;
    bottom: -2px;
    right: -2px;
    background: white;
    border-radius: 9999px;
    padding: 1px;
    line-height: 0;
}
```

- [ ] **Step 3: Handle ?-prefixed slugs in ShareView pickersBySlug**

The `pickersBySlug` map needs to resolve bare slugs from `?`-prefixed entries:

```typescript
import { bareSlug, isPicked, isMaybe } from '$lib/picks';

const pickersBySlug = $derived.by(() => {
    const map = new Map<string, string[]>();
    for (const entry of activeEntries) {
        for (const rawSlug of entry.picks) {
            const slug = bareSlug(rawSlug);
            if (!map.has(slug)) map.set(slug, []);
            map.get(slug)!.push(entry.id);
        }
    }
    return map;
});
```

Similarly update `allPickSlugs` to use `bareSlug`:

```typescript
const allPickSlugs = $derived.by(() => {
    const union = new Set<string>();
    for (const entry of activeEntries) {
        for (const rawSlug of entry.picks) union.add(bareSlug(rawSlug));
    }
    return union;
});
```

- [ ] **Step 4: Build, lint, test**

Run: `do_cmd -d ui -- pnpm build && do_cmd -d ui -- pnpm lint && do_cmd -d ui -- pnpm vitest run`
Expected: All pass

- [ ] **Step 5: Commit**

```
feat: add fleur/? sub-indicators on share view emoji circles
```

---

### Task 10: MobileSchedule and MySchedule — maybe acts visible

**Files:**
- Modify: `ui/src/lib/components/MobileSchedule.svelte`
- Modify: `ui/src/lib/components/MySchedule.svelte`

Maybe acts should appear in these views but never show conflict badges.

- [ ] **Step 1: Update MobileSchedule**

Import picks helpers. When computing `conflictColor`, return `'transparent'` for maybe acts. Pass `isMaybe` and `onToggleMaybe` through to ActRow.

For act filtering: currently shows all acts. The conflict color check already uses `isPicked` — just ensure it returns transparent for maybe:

```typescript
function conflictColor(act: ActSummary): string {
    if (!_isPicked(act.slug, picks)) return 'transparent';
    // ... existing logic
}
```

- [ ] **Step 2: Update MySchedule**

Similar changes. Maybe acts appear in the list but with `conflictColor = 'transparent'` and no distance annotations.

The `orderedPicks` filter needs to include both picked and maybe:

```typescript
import { isSelected } from '$lib/picks';

const orderedPicks = $derived(
    allActs.filter((a) => isSelected(a.slug, picks) && a.date === selectedDate)
);
```

- [ ] **Step 3: Build, lint, test**

Run: `do_cmd -d ui -- pnpm build && do_cmd -d ui -- pnpm lint && do_cmd -d ui -- pnpm vitest run`
Expected: All pass

- [ ] **Step 4: Commit**

```
feat: show maybe acts in mobile and my schedule views
```

---

### Task 11: Full integration test and final cleanup

**Files:**
- All modified files

- [ ] **Step 1: Run full test suite**

```bash
do_cmd -d ui -- pnpm vitest run
do_cmd -p .,dev -- python -m pytest tests/ --tb=short -q
```

- [ ] **Step 2: Run full lint**

```bash
do_cmd -d ui -- pnpm lint
do_cmd -p .,dev -- make lint-api
```

- [ ] **Step 3: Manual verification checklist**

- Toggle fleur → act goes green, ? deselects
- Toggle ? → act gets gradient (grid), ? deselects fleur
- Maybe acts on map show green ? icon
- My Schedule map: maybe acts appear with borrowed counters
- No arrows to/from maybe acts
- No conflict badges for maybe acts in any view
- Share view: emoji circles show sub-indicators
- Save/reload: ?-prefixed slugs persist correctly
- Existing schedules (no ? entries) work unchanged

- [ ] **Step 4: Commit**

```
chore: integration test and cleanup for maybe selection feature
```

---

Plan complete and saved to `docs/superpowers/plans/2026-04-01-maybe-selection.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?