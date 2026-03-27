# FQF 2026 Schedule Project

## Purpose
Personal schedule builder for French Quarter Festival 2026 (April 16–19, New Orleans).
The Python module `fqf2026.py` is the data layer. A UI will be built on top of it (format TBD).

## Data Source
Schedule scraped from https://frenchquarterfest.org/music/ on March 27, 2026.
Map reference: https://frenchquarterfest.org/map/ (PDF only, stage locations not yet encoded).

---

## Current Task: Artist Enrichment

Add `genre` and `about` fields to every `Act` in `SCHEDULE`.

### Fields to add to the `Act` dataclass

```python
genre: str        # controlled vocabulary term (see below)
about: str        # 4–10 line festival-guide summary
about_source: str # "researched" | "generated"
```

### Research strategy (in priority order)
1. `wwoz.org` — search artist name
2. `whereyat.com` — search artist name
3. Artist's own website or social media
4. General web search
5. If no usable source found: write a short genre-tagged placeholder,
   set `about_source = "generated"`

### Writing style for `about`
- Friendly festival-guide voice, not a Wikipedia stub
- 4–10 lines (aim for 5–7 for most acts)
- Lead with what makes them worth watching at a festival
- Mention New Orleans roots/connection where relevant
- Do not reproduce verbatim text from any source — paraphrase

### Multi-artist billings
Some act names combine multiple artists, e.g.:
- "Stanton Moore featuring Joe Ashlar and Danny Abel"
- "Yusa & Mahmoud Chouki"
- "Don Paul and Rivers Answer Moons"

Treat these as a single ensemble entry. Write one combined `about` covering
the collaboration. Individual artist bios are fine to draw on for context,
but the summary should describe them as a unit.

---

## Genre Vocabulary (controlled list)

Use exactly these strings to keep search/filter queries consistent:

| Genre string | Covers |
|---|---|
| `"Brass Band"` | New Orleans street brass, second line |
| `"Jazz (Traditional)"` | Trad jazz, Dixieland, swing |
| `"Jazz (Contemporary)"` | Modern jazz, fusion, post-bop |
| `"Zydeco"` | Zydeco |
| `"Cajun"` | Cajun, Creole folk |
| `"R&B / Soul"` | R&B, soul, Motown-influenced |
| `"Blues"` | Blues, blues-rock |
| `"Funk"` | Funk, P-funk influenced |
| `"Rock"` | Rock, indie rock |
| `"World"` | Afrobeat, Latin jazz, samba, Caribbean, global |
| `"Latin"` | Salsa, merengue, cumbia, son |
| `"Reggae"` | Reggae, dancehall |
| `"Gospel"` | Gospel, sacred |
| `"Singer-Songwriter"` | Acoustic, folk, Americana, country-adjacent |
| `"Electronic / DJ"` | DJ sets, electronic |
| `"Indian Mardi Gras"` | Mardi Gras Indians |
| `"Mixed / Eclectic"` | Acts that genuinely span 2+ genres |

If an act straddles two genres, pick the dominant one. Only use
`"Mixed / Eclectic"` when no single genre fits.

---

## Code Conventions

### Stage name constants (use these, never hardcode strings)
```python
ABITA         = "Abita Beer Stage"
NEWORLEANS    = "NewOrleans.com Stage"
TROPICAL      = "Tropical Isle Hand Grenade Stage"
JACKDANIELS   = "Jack Daniel's Stage"
WILLOW        = "Willow Dispensary Stage"
LOYOLA        = "Loyola Esplanade in the Shade Stage"
FISHFRY       = "Louisiana Fish Fry Stage"
ENTERGY       = "Entergy Songwriter Stage"
PANAMLIFE     = "Pan-American Life Insurance Group Stage"
JAZZPLAYHOUSE = "Jazz Playhouse at the Royal Sonesta"
FRENCHMARKET  = "French Market Traditional Jazz Stage"
DUTCHALLEY    = "French Market Dutch Alley Stage"
HOUSEOFBLUES  = "House of Blues Voodoo Garden Stage"
JAZZPARK      = "New Orleans Jazz National Historical Park Stage"
SCHOOLHOUSE   = "Ernie's Schoolhouse Stage"
HANCOCK       = "Hancock Whitney Stage"
OMNI          = "Omni Royal Orleans Stage"
KREWE         = "KREWE Eyewear Stage"
CAFEBEIGNET   = "Cafe Beignet Stage"
```

### Date and time constants
```python
THU = date(2026, 4, 16)   # Thursday
FRI = date(2026, 4, 17)   # Friday
SAT = date(2026, 4, 18)   # Saturday
SUN = date(2026, 4, 19)   # Sunday

t(h, m)  # shorthand for time(h, m), e.g. t(14, 30) = 2:30 PM
```

### Query API (do not break these signatures)
```python
at(query_date: date, query_time: time) -> list[Act]
search(query: str) -> list[Act]
on(query_date: date, stage: str | None = None) -> list[Act]
```

---

## Known Gaps / Deferred Work

- **Stage proximity**: physical distances between stages not yet encoded.
  Needed for conflict-flagging in the schedule builder UI.
  Source: https://frenchquarterfest.org/wp-content/uploads/2026/03/FQF-Map-v5.pdf
  (graphical PDF — will require manual interpretation)

- **UI format**: not yet decided. Candidates include a React artifact,
  standalone HTML file, or terminal UI.

- **Personal schedule storage**: no persistence layer yet.

- **Presenter/sponsor data**: stripped from data layer intentionally
  (e.g. "Airbnb presents Banu Gibson" — stored as just "Banu Gibson").

---

## Scale Notes
- 302 acts total across 4 days and up to 19 stages per day
- Ernie's Schoolhouse Stage is youth/school performers — lower research priority
- House of Blues Voodoo Garden Stage acts skew toward less-documented local artists
- Entergy Songwriter Stage is consistently solo singer-songwriter format

## Other

The Act dataclass needs the three new fields added before any enrichment starts — Claude Code should do that first, verify it doesn't break the query API, then work through enrichment in batches

The Schoolhouse Stage and some HOB Voodoo Garden acts are low-priority rabbit holes — use "generated" placeholders for school groups and move on

WWOZ in particular has good bios for the more established local acts — it's worth having Claude Code check there first before going to general web search


## Architecture

Full-stack application: Python/FastAPI backend + SvelteKit frontend, served from a single Docker container.
Deployed to Google Cloud Run via GitHub Actions.

### Backend (`src/fqf/`)
- **Python 3.10+**, FastAPI, Pydantic v2 models, click CLI
- API routes under `/api/v1/`
- `pyproject.toml` for all project config (build, lint, test, coverage)
- `uv` for dependency management and virtual environments
- `setuptools-scm` for git-tag-based versioning

### Frontend (`ui/`)
- **SvelteKit** with **Svelte 5 runes** (`$state`, `$derived`, `$effect`, `$props`, `$bindable`) -- NOT Svelte 4 syntax
- **Skeleton UI v4** component framework
- **Chart.js** for data visualization
- **Zod** for client-side validation (should mirror backend Pydantic constraints)
- Package manager: **pnpm** (version pinned in `package.json` via `packageManager` field)
- **Vite** dev server, **Vitest** for unit tests, **Playwright** for E2E

### Key Patterns
- `ui/src/lib/types.ts` -- TypeScript interfaces matching backend Pydantic models
- `ui/src/lib/schema.ts` -- Zod schemas for validation
- `ui/src/lib/stores.svelte.ts` -- Svelte 5 `$state()` stores with getter/setter `.value` pattern
- Component tests use `@testing-library/svelte` -- query by role/label, not DOM structure

## Development Workflow

### Makefile (standardized targets)

All projects use a Makefile with consistent target names:

| Target | Description |
|--------|-------------|
| `make help` | List all available targets |
| `make setup` | Install all dependencies (API + UI), configure Docker/GCP auth |
| `make build` | Build all packages |
| `make test` | Run all tests (API + UI) |
| `make dev` | Start API + UI dev servers with hot reload, open browser |
| `make lint` | Run all linters (API + UI) |
| `make format` | Auto-format all code (API + UI) |
| `make build-image` | Build Docker image locally via buildx |
| `make docker-run` | Build and run Docker image on port 8000 |
| `make deploy` | Build, push, deploy to Cloud Run |
| `make e2e` | Run E2E tests (starts backend, builds UI, runs Playwright) |
| `make clean` | Remove build artifacts |

Component-level targets follow the pattern `<target>-api` / `<target>-ui`:
- `setup-api`, `setup-ui`
- `build-api`, `build-ui`
- `test-api`, `test-ui`
- `lint-api`, `lint-ui`
- `format-api`, `format-ui`

### Linting

All changes must conform to lint/format rules. **Always run `make lint` before committing.**

**Backend** (`make lint-api`):
- `black` -- formatter (line-length 100)
- `isort` -- import sorting (profile: black)
- `mypy` -- strict type checking

**Frontend** (`make lint-ui`):
- `eslint` -- code quality
- `prettier` -- formatting

### Testing

**Backend**: `make test-api` runs `pytest` with coverage reporting
**Frontend unit**: `make test-ui` runs `vitest`
**Frontend E2E**: `make e2e` starts the backend, builds UI, runs Playwright

Coverage target: 85% minimum for lines and branches.

A feature or refactor is NOT complete until the test suite passes and coverage meets the threshold.

### Python Configuration (`pyproject.toml`)

All Python config lives in `pyproject.toml` -- no separate `setup.cfg`, `tox.ini`, etc.

```toml
[build-system]
requires = ["setuptools>=64", "wheel", "setuptools-scm>=8"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 100
target-version = ["py310"]

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.10"
strict = true

[tool.pytest.ini_options]
addopts = ["--cov=src/fqf", "--cov-report=html", "--cov-report=term"]
testpaths = ["tests"]

[tool.coverage.run]
source = ["src"]
omit = ["tests/*"]

[tool.setuptools_scm]
version_scheme = "guess-next-dev"
local_scheme = "node-and-date"
```

### Version Strategy

- Versions derived from git tags via `setuptools-scm`
- Tag format: `v<major>.<minor>.<patch>` (e.g., `v2.1.0`)
- Pre-release/dev builds get automatic suffixes from SCM
- Docker images tagged with: exact version, `latest`, and `v<major>` (for stable releases)
- Major-version Cloud Run services (`<service>-v<N>`) allow accessing any major version

## Docker

Single multi-stage Dockerfile:

1. **Stage 1 (frontend)**: `node:22-slim` -- pnpm install, SvelteKit build to static
2. **Stage 2 (backend)**: `python:3.11-slim` -- pip install backend, copy static assets into package
3. Serves both API and static frontend from a single `uvicorn` process on port 8000

The `pyproject.toml` must include `[tool.setuptools.package-data]` for `static/**/*` or the Docker build won't include frontend assets.

## CI/CD

### GitHub Actions

**CI** (`.github/workflows/ci.yml`): Runs on push/PR to main.
- Three parallel jobs: `test-api`, `test-ui`, `lint`
- Uses `actions/setup-python` + `astral-sh/setup-uv` for Python
- Uses `pnpm/action-setup` + `actions/setup-node` for frontend
- Lock files enforced: `uv sync --frozen`, `pnpm install --frozen-lockfile`

**Deploy** (`.github/workflows/deploy.yml`): Triggered by version tags (`v*`).
- Calls CI workflow first (`workflow_call`) -- tests must pass before deploy
- Builds multi-platform Docker image via `docker/build-push-action` with GHA cache
- Pushes to both GHCR and GCP Artifact Registry
- Deploys to Cloud Run with version-aware service naming:
  - `<service>` -- always points to latest deploy
  - `<service>-v<N>` -- stable major version endpoint
  - `<service>-v<N>-prev` -- previous stable version (for comparison/rollback)

### Required Secrets
- `GCP_SA_KEY` -- GCP service account JSON for Cloud Run deploys
- `GCP_PROJECT` -- GCP project ID
- `GHCR_PAT` -- GitHub Container Registry personal access token

## Deployment

- **Platform**: Google Cloud Run (managed, serverless)
- **Registry**: Dual-push to GHCR (`ghcr.io`) and GCP Artifact Registry
- **Resources**: 512Mi memory, 1 CPU, 0-3 instances, port 8000
- **Access**: `--allow-unauthenticated` (public)
- Local deploy: `make deploy` (requires `gcloud` auth + Docker login)
- Automated deploy: push a `v*` tag to trigger the deploy workflow

## UI Framework Rules

- Use **Svelte 5 runes** exclusively -- no Svelte 4 `$:` reactive statements, no `export let` for props
- Props: `let { foo = $bindable() }: { foo: Type } = $props()`
- Render delegation: `{#snippet name()}...{/snippet}` passed as props (type `Snippet`)
- Reactivity: `$derived()`, `$derived.by(() => { ... })`, `$effect()`
- State stores: `$state()` with getter/setter `.value` pattern in `.svelte.ts` files
- Component library: Skeleton UI v4 (AppBar, drawers, buttons, inputs)
- Static adapter (`@sveltejs/adapter-static`) -- output is pure static files served by the backend

## Git Workflow

1. **Branch**: `git checkout -b <feature-branch>` off main
2. **Implement**: Write code and tests
3. **Test**: `make test` + `make lint` must both pass
4. **Commit**: To the feature branch
5. **Merge**: Feature branch onto main
6. **Push**: Push main to origin
7. **Deploy**: Tag with `v<major>.<minor>.<patch>` and push tag

**Main is always deployable**: zero lint errors and zero test failures at all times. Never dismiss failures as pre-existing.
