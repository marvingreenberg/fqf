# Share Flow Redesign + Quick Fixes

## Issues covered

- **#13** — View-only share route: fix login flow and back link
- **#14** — Shared schedule doesn't refresh when source changes
- **#15** — Schedule saves should batch: 4 changes or 5 seconds
- **#16** — Page refresh should reset to default view state

---

## Issue #13: Share link flow redesign

### Current behavior (broken)

1. `/fq2026?share=xxx` shows main identity gate with a "View" ghost button
2. Clicking "View" navigates to `/fq2026/{share_hash}`
3. Parent layout's identity gate overlays the view-only page

### New behavior

**Step 1: Redirect.** When arriving at `/fq2026?share=xxx` (logged out), the
main identity gate immediately redirects to `/fq2026/{share_hash}`. The
share_hash comes from validating the share param against the API. If invalid,
stay at `/fq2026` and show the standard gate with "(!) Share not found".

**Step 2: Share login pane.** At `/fq2026/{share_hash}`, a context-specific
login pane (NOT the main IdentityGate) shows three options:

```
If you have an existing schedule, load it
🪄 {name}'s schedule will be added as a share
[Button: Load Schedule]
[  enter your secret words  ]

Create a new schedule, to compare with {name}'s picks!
Give your schedule a name to share back
[Button: New Schedule]
Name: [                    ]

Just look at the shared schedule
[Button: See {name}'s schedule]
```

- **Load**: calls fuzzyLookup, confirms identity, calls addShareToSchedule,
  redirects to `/fq2026` with Share tab active
- **New**: requires name, creates schedule, calls addShareToSchedule,
  redirects to `/fq2026` with Share tab active
- **See**: dismisses login pane, shows read-only schedule at current URL

Name input only appears for New. Load uses the stored name. See needs no name.

**Step 3: Back link.** The view-only route header shows:
- "← Back to Start" (bolder, slightly larger than current) linking to `/fq2026`
- NOT "Back to my schedule" (user may not be logged in)

### Components

**New:** `ui/src/lib/components/ShareLoginPane.svelte`
- Context-specific login for the share route
- Props: `shareName: string`, `shareHash: string`
- On Load/New success: `goto('/fq2026')` with `appState.viewMode = 'share'`
- On See: sets a local `dismissed` flag, pane hides

**Modified:** `ui/src/routes/fq2026/+layout.svelte`
- When `pendingShareId` is set and user is NOT confirmed, redirect to
  `/fq2026/{share_hash}` instead of showing the main identity gate
- Need to resolve share_id to share_hash (they may be the same — check API)

**Modified:** `ui/src/routes/fq2026/[share_hash]/+layout.svelte`
- Back link text: "← Back to Start", styled bolder/larger
- No avatar menu (already the case)

**Modified:** `ui/src/routes/fq2026/[share_hash]/+page.svelte`
- Shows ShareLoginPane on load
- After "See" is clicked, hides pane, shows read-only schedule
- After "Load"/"New", redirects away (pane handles this)

### Backend

No backend changes needed. Existing endpoints cover everything:
- `GET /api/v1/schedule/by-share/{share_id}` — validates share, returns data
- `POST /api/v1/schedule/{token}/add-share` — adds share ref
- `POST /api/v1/schedule/fuzzy-lookup` — load flow
- `POST /api/v1/schedule` — new schedule flow

---

## Issue #14: Shared schedule refresh

Add a "Refresh" button to the Share tab (ShareView component).

- Button at the top of the share content area, next to the person toggles
- On click: re-fetch each shared schedule via `GET /api/v1/schedule/by-share/{id}`
- Show status briefly: "Updated!" (green) or "No changes" (grey) for 3 seconds
- Replace the acts data in `appState.sharedSchedules` with fresh data

No automatic background refresh (YAGNI for now).

### Components

**Modified:** `ui/src/lib/components/ShareView.svelte`
- Add refresh button with loading/status state
- Re-fetch all shared schedules, compare pick arrays, show status

---

## Issue #15: Save batching timing

Change `SAVE_AFTER_CHANGES` and `SAVE_DEBOUNCE_MS` in `stores.svelte.ts`:

- `SAVE_AFTER_CHANGES = 4` (unchanged)
- `SAVE_DEBOUNCE_MS = 5000` (was 10000)
- Also flush on view mode change (tab switch)

### Components

**Modified:** `ui/src/lib/stores.svelte.ts`
- Change `SAVE_DEBOUNCE_MS` from 10000 to 5000
- Add `flushSave()` call when `viewMode` changes (via a new `setViewMode` method
  that flushes before switching)

---

## Issue #16: Refresh resets to default state, but tab switching preserves state

Two distinct behaviors:

**Browser refresh (Cmd-R):** Resets ALL transient UI state to defaults:
- `viewMode` → `'grid'`
- `mobileSortMode` → `'by-time'`
- Map mode → default (Scroll Time at start of day)
- Filter panel → collapsed
- No open modals

**Tab switching (clicking All Acts / Map / My Schedule / Share):** Preserves
each view's internal state. E.g., if you set the map time scroller to 3pm,
switch to All Acts, then back to Map — the scroller is still at 3pm. This
is the natural SPA behavior since the component state lives in memory.

### Verification

Check `saveToStorage()` and `loadFromStorage()` — confirm they don't touch
`viewMode` or any transient view state. Only token/name/counter should be
persisted. If `viewMode` is persisted, remove it.

Verify that in-view state (map scroll time, filter selections, mobile sort
mode) is held in component-local `$state` or `appState` fields that are NOT
written to localStorage — so they survive tab switches but reset on page
reload.

---

## Implementation order

1. **#15** (save timing) — 1 line change, no dependencies
2. **#16** (refresh reset) — verification + possible 1 line fix
3. **#14** (refresh button) — small, independent component change
4. **#13** (share flow) — largest, depends on the others being stable

#15 and #16 can go on one branch. #14 on another. #13 on its own.
