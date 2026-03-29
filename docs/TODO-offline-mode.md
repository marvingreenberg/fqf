# Offline Mode

## Goal

The app should work fully offline after the first load. Browsing acts, picking
favorites, viewing schedules, and switching tabs should never require a network
connection. Network is only needed for identity confirmation and syncing picks
to the backend.

## Current State

- Act data is static (compiled into the Python package, served as API responses)
- Picks are stored in `appState.picks` (in-memory Set) and saved to backend via
  debounced API call
- If the server is down after initial load, the app continues working but
  picks aren't persisted

## Planned Changes

### 1. Network status indicator

- Watch `navigator.onLine` and/or periodic health check (`GET /api/v1/acts?date=...`
  with short timeout)
- Show a small icon in the header when offline (e.g., a crossed-out cloud or
  wifi icon, in the Mardi Gras gold color)
- Hide the icon when online

### 2. Queue saves for when back online

- When `scheduleSave()` fires but network is unavailable, queue the save
- When network returns, flush the queue
- Use `window.addEventListener('online', flush)` to detect reconnection

### 3. LocalStorage cache for minimal required state

The following could be saved to localStorage so the app works even on a
completely fresh page load with no network:

- **Identity**: token + name (already saved as `fqf_identity`)
- **Picks**: array of act slugs (small — ~50 slugs max, a few KB)
- **Act data**: the full act list per day could be cached in localStorage
  after first fetch. The data is static and rarely changes (~302 acts,
  ~100KB as JSON). This would allow the grid to render without any API call.
- **Shared schedule refs**: already persisted in Firestore, but the local
  list of share_ids + names could be cached

With all of the above in localStorage, the app would:
1. Render instantly from cache on load
2. Attempt to sync with backend in the background
3. Show the offline icon if sync fails
4. Continue working fully — browsing, picking, tab switching
5. Sync picks when network returns

### 4. Cache invalidation

- Act data: cache with a long TTL (hours/days) since it's static. Could
  include a version/hash in the API response to detect changes.
- Picks: localStorage is the source of truth when offline; backend is the
  source of truth when online. On reconnect, the most recent write wins
  (last-write-wins, no merge needed since picks are a simple set).

## Not in scope

- Service Worker / PWA (would be the "real" solution for offline but adds
  significant complexity)
- Conflict resolution between devices (if picks changed on two devices
  while both were offline)
