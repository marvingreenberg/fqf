# Identity, Security & Login Redesign

## Purpose

Redesign the identity system to be more robust against abuse, more forgiving
for users, and deterministic per device. Replace the current random token
generation with fingerprint-derived tokens, add rate limiting, and make
triple entry tolerant of typos and ordering.

## Login Use Cases

Six cases defined in `docs/login-use-cases.md`. Summary:

### Case 1: Fresh visit, no stored triple
Show two buttons:
- **Load schedule** — italic "Load existing schedule if you have one"
  - Text input below, grey placeholder "use your secret words"
- **New Schedule**

### Case 2: Fresh visit with valid `?share=xxxxx`
Same as Case 1 plus:
- **New Schedule** italic "Create a schedule to allow comparing with {name}"
- **View {name}'s schedule?** italic "view only, no changes can be made"
  - View-only navigates to `/fqf2026/{share_hash}` — shows the other person's
    schedule in All Acts / My Schedule / Map tabs. No share tab, no editing.

### Case 3: Fresh visit with invalid `?share=xxxxx`
Same as Case 1 with dark orange italic message: "(!) Share not found"

### Case 4: Returning visit, stored triple
- **Load schedule** — text input pre-filled with stored triple (black text)
  - italic "Load existing schedule, or enter new one"
- **New Schedule** — generates fingerprint + incremented counter

### Case 5: Returning visit with valid `?share=xxxxx`
Skip login entirely. Add share to shares list, go to share tab.

### Case 6: Returning visit with invalid `?share=xxxxx`
Same as Case 4 with dark orange italic message: "(!) Share not found"

## Name Field

Name is **required** for both Load and New. Prompt: "ANY name! Fred, BooBoo —
just for sharing your schedule". This name is stored with the schedule and
shown in share views.

## Deterministic Token Generation

### Fingerprint
Use canvas fingerprinting to derive a device-specific hash:
1. Draw text + shapes on a hidden canvas element
2. Extract pixel data via `toDataURL()`
3. Hash with SHA-256 → `fingerprint_hash`

**Stability check**: draw canvas twice in same session, compare hashes.
If they differ (Brave, Tor), fall back to random generation.

### Token derivation (server-side)
- Client sends `POST /api/v1/schedule` with body:
  `{ fingerprint_hash: string, counter: number, name: string }`
- Server uses `SHA256(fingerprint_hash + counter)` to seed deterministic
  selection from word pools — no server secret needed since the fingerprint
  is already unpredictable
- Same inputs → same token, always
- New tokens stored with words sorted alphabetically
- Server stores the token in Firestore (existing flow)

### Counter
- Stored in localStorage alongside the triple
- Starts at 0 for first schedule on a device
- Incremented when user explicitly creates a "New Schedule" on a device
  that already has one
- Persists across "clear" (logout) — only reset by full localStorage wipe

### Rate limiting
- Max 5 schedules per fingerprint hash (counter 0-4)
- Backend rejects `counter >= 5` with 429
- Also rate limit by IP: max 10 create requests per hour (via middleware)
- Rate limit on load endpoint: max 30 requests per minute per IP

## Fuzzy Triple Matching

When a user enters their triple, normalize before lookup:

1. **Case insensitive**: lowercase everything
2. **Separator agnostic**: split on hyphens, spaces, or any non-alpha character
3. **Order agnostic**: try the entered order first, then try sorted
   alphabetically. Two lookups max, not all permutations. New schedules
   store tokens with words sorted. Legacy tokens (unsorted) are found
   by the first lookup.
4. **Typo correction**: for each entered word, if it doesn't exactly match
   any word in any pool, find the closest match by Levenshtein distance
   - With ~100 words per pool (~300 total), this is trivial to compute
   - Accept corrections with distance ≤ 1 (one character off)
   - Show the user: "Did you mean: berthe-funky-gazebo?" with the corrected
     triple, and auto-fill it. User confirms.
   - Distance > 1: show error, don't guess

### Pool matching for fuzzy lookup
Each entered word is checked against all three pools to find the best
match. With only 300 total words and distance ≤ 1, ambiguity is unlikely.

**Validation**: on startup or in tests, verify no two words across all
three pools have Levenshtein distance ≤ 1 from each other. If any do,
rename one. This guarantees unambiguous correction.

## View-Only Mode (Case 2)

New SvelteKit route: `/fq2026/[share_hash]/+page.svelte`
- Fetches schedule via `GET /api/v1/schedule/by-share/{share_hash}`
- Reuses existing components: `ScheduleGrid`, `MobileSchedule`, `MySchedule`,
  `MapView`, `DayTabs`, `FilterPanel`
- All picks are the shared person's picks (read-only)
- Fleur-de-lis hidden or greyed out (no toggling)
- No share tab, no identity gate
- Header shows "{name}'s schedule" with a "Stop viewing {name}" link
  back to `/fq2026`
- URL stays as `/fq2026/{share_hash}` (distinct from the main app URL)

## Storage

| Key | Storage | Contents |
|-----|---------|----------|
| `fqf_identity` | localStorage | `{ token, name, counter }` |
| `fqf_fingerprint_counter` | localStorage | counter (persists across clear) |
| Acts cache | localStorage | per-date act lists (see offline-mode TODO) |
| Picks cache | localStorage | current picks array (see offline-mode TODO) |

"Clear" (logout) removes `fqf_identity` but NOT `fqf_fingerprint_counter`.

## Backend Changes

### New/modified endpoints
- `POST /api/v1/schedule` — accept `fingerprint_hash` and `counter` in body;
  use HMAC for deterministic token derivation
- `POST /api/v1/schedule/fuzzy-lookup` — accept raw triple string, return
  corrected triple + schedule if found, or suggestions if close match
- Rate limiting middleware on all endpoints (IP-based)
- Per-fingerprint rate limiting on create endpoint

### Word pool validation
- On module load, verify no two words across all pools have Levenshtein
  distance ≤ 1. Raise error if violated.

## Frontend Changes

### New files
- `ui/src/lib/fingerprint.ts` — canvas fingerprinting + stability check
- `ui/src/routes/fq2026/[share_hash]/+page.svelte` — view-only route

### Modified files
- `IdentityGate.svelte` — redesigned per login use cases
- `stores.svelte.ts` — counter persistence, fingerprint storage
- `api.ts` — updated createSchedule with fingerprint/counter, fuzzy lookup

## Testing

### Backend (unit)
- Deterministic derivation: same inputs → same token (synthetic hashes)
- Different inputs → different tokens (10,000 synthetic hashes, all unique)
- Fuzzy matching: exact match, 1-char typo correction, rejection at distance 2
- Word pool validation: no close-distance collisions across pools
- Rate limiting: verify 429 after threshold

### Frontend (Playwright E2E)
- Canvas fingerprint: Chromium vs WebKit produce different hashes
  (verifies function is not trivially broken)
- Login flow: all 6 use cases
- View-only mode: share link renders read-only schedule

## Not in scope
- Cross-device identity linking
- Service Worker / PWA
- OAuth or external auth providers
