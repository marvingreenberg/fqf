# FQF 2026 Code Review

Comprehensive review of the codebase as of v0.6.0 (April 2026).
Covers DRY, architecture, file hygiene, and speculative bigger-picture suggestions.

---

## 1. DRY & Reuse Opportunities

 * Let's definitely do all these. Except 1.5

### 1.1 The two schedule pages are ~80% identical

`ui/src/routes/fq2026/+page.svelte` (257 lines) and
`ui/src/routes/fq2026/[share_hash]/+page.svelte` (262 lines) duplicate:

- `actsCache` + `isCacheFresh()` + `loadActs()` + `loadAllActs()` (identical)
- `openDetail()` / `closeDetail()` (identical)
- `MOBILE_BREAKPOINT`, `CACHE_TTL_MS` (identical constants)
- The `$effect` for reloading acts on date/view change (structurally identical)
- The entire view-switcher template (grid/mobile/map/my-schedule dispatch)
- The `ActDetailModal` footer

The share page differs only in: read-only mode, no `FilterPanel`, no share tab,
a login pane overlay, and local `picks`/`selectedDate` state instead of `appState`.

**Suggestion:** Extract a `ScheduleShell.svelte` component that owns the
view-switching, acts caching, day tabs, detail modal, and responsive layout.
Both pages compose it with a `readOnly` prop and optional slot overrides.
This would cut ~200 lines of duplication and make future view changes
(new tab, new view mode) one edit instead of two.

### 1.2 Login/identity forms are duplicated

`IdentityGate.svelte` (193 lines) and `ShareLoginPane.svelte` (164 lines)
both implement token input, name input, create/load flows, fuzzy lookup display,
and error handling. The styling is different but the logic is the same.

**Suggestion:** Extract a `LoginForm.svelte` that handles the token/name input,
load-existing, create-new logic, and fuzzy suggestion display. `IdentityGate`
and `ShareLoginPane` become thin wrappers providing context (headings, share
prompt, dismiss behavior).

### 1.3 Fleur-de-lis toggle icon rendered in 3 places

`ActBlock.svelte`, `ActRow.svelte`, and `ActDetailModal.svelte` each render
the fleur icon with picked/unpicked styling and click handling. The SVG path
is already centralized in `constants.ts` (good), but the rendering+toggle
logic is tripled.

**Suggestion:** Extract a `FleurToggle.svelte` component (~20 lines).
Accepts `picked`, `readOnly`, `ontoggle` props. Reuse in all three.

### 1.4 Modal dialog pattern duplicated

`AvatarMenu`, `IdentityGate`, `ShareLoginPane`, and `ActDetailModal` all
build their own modal overlays (fixed inset-0, z-50, backdrop, card). Each
has its own escape-key handler and click-outside logic.

**Suggestion:** Extract a generic `Modal.svelte` wrapper (backdrop + dismiss
behavior + escape key + focus trap). Components pass content as children.

### 1.5 Backend types mirrored manually in frontend

Pydantic models in `src/fqf/api/schemas.py` and TypeScript interfaces in
`ui/src/lib/types.ts` are maintained by hand. They're in sync today, but
adding a field to one without the other is a latent failure mode.

**Suggestion (low priority):** Consider generating TypeScript types from the
OpenAPI spec that FastAPI produces automatically (`/openapi.json`). Tools
like `openapi-typescript` can do this as a build step. Not urgent for 16
types, but prevents drift as the API grows.

---

## 2. Architecture & Patterns

### 2.1 Static schedule data hardcoded in Python

* Yeah lets move this into a separate YAML file, named fq2026_acts.yaml
  Add a little metadata, like the event name French Quarter Fest, date 2026, April 16-19

  There is some possibility of doing JF2026 a few weeks later.

The enrichment is already complete -- its also in the day files.
So lets do another thing, and redo the research... And look at the existing BIO text.
If it comes primarily from a single source, like wwoz.org or offbeat.com or
an instagram page, put a footnote link after which pops up a link like "From wwoz.org"
that links to the (primary, most significant) source.  The same source can still be at one of the world url links (and those links are a good place to look when finding the source of the bio).  THAT url (primary source) is the value that should be in about_source.  Unless the info is really compiled from lots of different sources, in which, GENERATED is fine.

The 302 acts live as `Act(...)` literals across 5,815 lines of Python
(`schedule/thursday.py` through `sunday.py`). This is fine for a fixed
festival — the data doesn't change at runtime. But the enrichment task
(adding `genre`, `about`, `about_source` to every Act) means these files
will grow to ~10k+ lines of Python and every enrichment edit is a Python
source change + lint + commit.

**Observation, not recommendation:** For a one-year festival, this is
pragmatic and avoids a data migration layer. If you ever wanted to support
multiple years or let users contribute corrections, moving acts to a
data file (JSON/YAML) loaded at startup would make sense. But for FQF 2026,
keep it as-is.

### 2.2 In-memory rate limiting won't survive multi-instance

`rate_limit.py` uses module-level dicts keyed by IP. Cloud Run is configured
for 0-3 instances. With >1 instance, each has its own rate-limit state, so
a client hitting different instances gets 2-3x the intended budget.

**Risk assessment:** Low. This is a festival schedule app, not a banking API.
The rate limits are generous (60/min), and Cloud Run sticky sessions help.
If abuse becomes real, a Redis sidecar or Cloud Run min-instances=1 would fix
it.

**Not worth the complexity now.**

### 2.3 CORS allows only localhost origins

* 👍🏻

`app.py` line 19: `CORS_ALLOW_ORIGINS = ["http://localhost:5173", "http://localhost:8000"]`

The production deployment at `festschedule.org` works because the SPA and API
are same-origin (both served from the same container). But if you ever split
them or add a CDN, this would silently break. Consider adding the production
origin for defense-in-depth:

```python
CORS_ALLOW_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8000",
    "https://festschedule.org",
]
```

### 2.4 CLI entrypoint registered but module doesn't exist

* 👍🏻 Clean this up -- remove

`pyproject.toml` declares `fqf = "fqf.cli:main"` but there's no `cli.py`
in `src/fqf/`. This means `pip install -e .` creates a broken `fqf` console
script. Either create the module or remove the entry point.

### 2.5 AppState is a god object (manageable, but watch it)

`stores.svelte.ts` at 220 lines houses identity, picks, view mode, map state,
filter state, save debouncing, and shared schedule management. It's well-organized
with clear method boundaries, but it's the single mutation point for everything.

**Not a problem yet.** If you add offline mode (save queuing, network detection)
as described in `docs/TODO-offline-mode.md`, it would push this past 300 lines.
At that point, consider splitting into focused stores: `identity.svelte.ts`,
`schedule.svelte.ts`, `view.svelte.ts`. They can reference each other via imports
without becoming circular.

### 2.6 No error handling for failed API saves

* 👍🏻

`AppState._flushSave()` calls `savePicks()` but doesn't catch errors. If the
API is unreachable, the save silently fails and `_unsavedChanges` resets to 0.
The user has no indication their picks weren't saved.

**Suggestion:** Catch errors, keep `_unsavedChanges` nonzero on failure, and
retry on the next pick toggle. An optional "save failed" indicator in the header
would complete the picture. This is directly on the path to the offline mode work
in `TODO-offline-mode.md`.

### 2.7 SPA fallback serves index.html for all unknown paths

The catch-all `spa_fallback` in `app.py` returns `index.html` for every
non-file, non-API path. This means 404s for genuinely bad URLs
(`/fq2026/nonexistent/path/foo`) return 200 + the SPA shell. Standard behavior
for SPAs, but consider returning a proper 404 for paths that clearly don't
match any route pattern (anything outside `/`, `/fq2026`, `/fq2026/<hash>`).

---

## 3. Files: Cleanup & Consolidation

### 3.1 README.md is empty

* 👍🏻

The file exists but contains nothing. This is the first thing anyone sees on
GitHub. Suggest populating with at minimum: project description, live URL
(`festschedule.org`), setup instructions (`make setup && make dev`), and a
screenshot.

### 3.2 brainstorm.md is mostly implemented

The ideas in `brainstorm.md` have largely been built:
- Google Maps links -- implemented in `ActDetailModal`
- Distance between picks -- implemented in `MySchedule` + `distance.ts`
- Interactive map view -- implemented as `MapView.svelte`
- Proximity warnings -- partially, via conflict colors in the grid

The unimplemented items (heat map, walking route planner, nearby-stages
suggestions) could move to GitHub issues. Once that's done, `brainstorm.md`
is historical and could be deleted or moved to `docs/`.

* Let's just delete it.

### 3.3 login-use-cases.md reads like scratch notes

`docs/login-use-cases.md` is an informal spec with raw thoughts, not a
polished doc. The login flows it describes are all implemented. It could
either be cleaned up into a proper reference or deleted since the code is
the source of truth.

* delete

### 3.4 feat/ directory is empty

`feat/` exists with no contents. If it was staging for a feature branch
workflow, it's no longer serving a purpose. Delete it.

*delete

### 3.5 docs/superpowers/ is agent scaffolding

The `plans/` and `specs/` directories under `docs/superpowers/` are
implementation plans generated during development. They're historical
records of how the code was built, not ongoing documentation. Consider:
- Keep if you find them useful as decision records
- Move to a `docs/archive/` if they clutter the active docs
- Delete if the commit history captures the same information

* delete

### 3.6 RELEASE_PROCESS.md could be in the Makefile or README

The release process is 5 steps: test, lint, tag, deploy, verify. This is
already mostly encoded in Makefile targets. The doc adds value for the
Dependabot review and hotfix instructions, but consider whether it belongs
inline in the README under a "Release" heading rather than a separate file.
Your call — it's a question of how many docs files you want to maintain.

* delete. move minimized content into bottom section of README

### 3.7 DomainMapping.md is infrastructure runbook — fine as-is

The domain setup doc has the exact `gcloud` commands used. This is valuable
for disaster recovery or replication. Keep it.

---

## 4. Testing Gaps

### 4.1 Frontend state and API untested

* 👍🏻

The Svelte utility modules have solid test coverage (`conflict.test.ts`,
`distance.test.ts`, `map-utils.test.ts`, `emoji-mapper.test.ts` — 61 tests
total). But `stores.svelte.ts` and `api.ts` have zero tests.

`AppState` has complex logic: debounced saving, pick toggling with Set
immutability, shared schedule management, localStorage persistence.
These are all testable in isolation with `vitest` — no component rendering
needed.

`api.ts` could use a few smoke tests with `msw` (Mock Service Worker) to
verify request shapes and error paths.

### 4.2 No Playwright E2E tests in the repo

* Add basic E2E tests, as suggested, with playwright

The Makefile has `make e2e` and a Playwright config exists, but I didn't
find any actual E2E test files. Critical flows worth covering:
- Create schedule -> pick acts -> reload -> picks persist
- Share link flow (generate, open, view)
- Fuzzy token login with typo correction


### 4.3 Backend test overlap

`test_tokens.py` (74 lines) and `test_tokens_new.py` (243 lines) cover
overlapping territory — the "new" file was likely added when deterministic
tokens and fuzzy resolution came in. Consider merging them into a single
`test_tokens.py`.

* 👍🏻

---

## 5. Minor Issues

### 5.1 `mobile` is a ViewMode but never set by user

* What this said, but rename "grid" to "all-acts"

`ViewMode = 'grid' | 'mobile' | 'my-schedule' | 'share' | 'map'` includes
`'mobile'`, but the view tabs only offer `grid`, `map`, `my-schedule`, and
`share`. The `mobile` mode is implicitly triggered by `isMobile` in the
template. This works but is confusing — the type suggests `mobile` is a
user-selectable mode. Consider removing it from the type and keeping the
mobile/desktop switch as a rendering concern only.

### 5.2 Zod is a dependency but never used

* cleanup

`package.json` lists `zod@3.25.76` as a dependency and CLAUDE.md mentions
"Zod for client-side validation." But there are no Zod schemas in the
codebase — `ui/src/lib/schema.ts` doesn't exist. Either add validation
where it matters (form inputs, API response shapes) or remove the dependency.

### 5.3 Word pools in tokens/words.py have issues

* I'd love to get 100,100,100  adverb, verb, noun or adjective, adjective, noun
that are ALL new orleans, music, festival related, like "wildly dancing krewe".  Or
monty python related, to keep things a little wacky. The nouns can include animals
that might not exactly be NO/MP related (iguana, giraffe) if they are not boring animals
- e.g. lion, cow, chicken, bear...

I think that means POOLS get renamed POOL1, POOL2, POOL3.  For backward compat, the
code should accept previously generated/saved triples.

`POOL_NOLA` appears to have grown beyond its intended 100 items — it contains
generic material words (nails, rivets, screws, bolts, washers, springs, gears,
wheels, axles, bearings...) and animal taxonomies (salamander, newt, frog, toad...)
that have nothing to do with New Orleans culture. This looks like an AI
generation artifact that wasn't trimmed. The token doc says 100 words, but
the actual list is much longer. The extra words don't break anything (more
combinations), but they dilute the NOLA flavor of the tokens. Trimming to
curated NOLA-relevant terms would improve the user experience.

Also: `POOL_MUSIC` has duplicate entries (`syncopated` appears twice, `soulful`
twice, `strutting` twice, `wailing` twice, `swinging` twice). The
`validate_word_pools()` function checks for Levenshtein distance but not exact
duplicates.

### 5.4 `click` is a core dependency but no CLI exists

* clean up

`click>=8.1` is in `[project.dependencies]` and there's a console script
`fqf = "fqf.cli:main"` in `pyproject.toml`, but no `cli.py` module exists.
This means `click` is a dead dependency in production. Either build the CLI
or remove both the dependency and the entry point.

### 5.5 `FilterPanel` not available on share page

* That's intentional.  I would like to add an indicator "Hides (n) selections"
  when the filter is active and has hidden selected acts, and also add
  checkboxes Show All [] Show Selected [] (but only when something is filtered, and when
  a filter hides a selection (including maybe))

The share view page doesn't include `FilterPanel`, so viewers of a shared
schedule can't filter by genre or stage. Intentional? If the schedule has
50+ picks across 4 days, filtering would be useful.

---

## 6. Speculative / Big-Picture

These are larger questions that may not be worth acting on now but are worth
thinking about.

### 6.1 Should the schedule data be a database instead of Python literals?

**Current:** 302 acts are Python dataclass literals compiled into the package.
Every change is a code change.

**Alternative:** Store acts in Firestore alongside schedules. The backend
loads them once at startup. Enrichment happens via a script or admin UI.

**Trade-offs:**
- Pro: Enrichment doesn't require code changes, deploys, or lint passes
- Pro: Enables multi-year support (FQF 2027, Jazz Fest, etc.)
- Pro: Community corrections without code access
- Con: Adds a data seeding step to deployment
- Con: Loses type safety and compile-time validation of act data
- Con: More complexity for a single-year festival app

**Verdict:** Not worth it for FQF 2026 alone. Worth doing if you want to
reuse this for other festivals or future years.

### 6.2 Would a different frontend framework make more sense?

The SvelteKit choice is solid — Svelte 5 runes are expressive, the bundle
is small, and the static adapter makes deployment simple. The main friction
points are ecosystem-related (fewer UI component libraries than React/Vue,
Skeleton UI v4 is still maturing).

If starting from scratch, the main alternative would be Next.js + React.
But the app is working, the code is clean, and migrating would cost weeks
for marginal benefit. **Stay with SvelteKit.**

### 6.3 PWA / offline-first

* Lets do this, with offline mode.  After everything else.

`docs/TODO-offline-mode.md` outlines a localStorage caching approach. Given
that the festival is outdoors with unreliable cell coverage, this is probably
the highest-impact feature not yet built. The current architecture supports
it well — act data is static, picks are a simple set, and the debounced
save model already handles temporary disconnects.

A service worker approach (mentioned as "not in scope") would actually be
straightforward with SvelteKit's `@sveltejs/adapter-static` output — you'd
just add a `service-worker.ts` with cache-first for static assets and
network-first for API calls. Worth considering before April 16.

### 6.4 Consider dropping Skeleton UI

* Lets discuss, after other defined tasks are completed.

Looking at the component usage, most of the UI is built with custom
`fqf-*` CSS classes and Tailwind utilities. Skeleton UI provides the
`AppBar` and some button styles, but most components are custom. The
framework adds bundle weight and constrains the Tailwind version.

If the custom styling trend continues, consider replacing Skeleton with
plain Tailwind + a few headless components (e.g., Melt UI or Bits UI for
accessibility primitives like dialogs and menus). This would simplify the
CSS stack and remove the Skeleton theming indirection.

### 6.5 Multi-festival generalization

* Lets do whatever config is needed to minimally support this generalization.

The app has clean separation between data (schedule modules) and logic
(API, UI). If you wanted to support Jazzfest, Voodoo Fest, or other
festivals, the main abstractions that would need to change are:

- Stage constants and locations → loaded from config/DB per festival
- Date constants → festival metadata
- Route prefix (`/fq2026`) → dynamic per festival
- Color theme → configurable

The codebase is closer to this than it might seem. The main blocker is the
hardcoded schedule data, per 6.1 above.

---
