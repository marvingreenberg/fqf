# FQF 2026 Schedule Builder — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a full-stack festival schedule builder that lets users browse 302 acts across 4 days, pick favorites, detect time conflicts, and share/merge schedules using memorable NOLA-themed tokens.

**Architecture:** Python/FastAPI backend serving a static SvelteKit frontend from a single container. Schedule data is compiled into the Python package (static, not in database). User picks are persisted in Neon serverless Postgres, keyed by three-word tokens. The API follows a lightweight-list / detailed-single pattern for act data.

**Tech Stack:** Python 3.10+, FastAPI, Pydantic v2, asyncpg, Neon Postgres, SvelteKit (Svelte 5 runes), Skeleton UI v4, Zod, Docker, GitHub Actions, Cloud Run.

---

## File Structure

### Backend (`src/fqf/`)

| File | Responsibility |
|------|---------------|
| `src/fqf/__init__.py` | Package init |
| `src/fqf/models.py` | `Act` dataclass, `Genre`/`AboutSource` enums, stage/date/time constants |
| `src/fqf/slugify.py` | Deterministic slug generation from act names |
| `src/fqf/schedule/__init__.py` | Combined `SCHEDULE` list, query functions (`at`, `search`, `on`, `get_by_slug`) |
| `src/fqf/schedule/thursday.py` | Thursday act data |
| `src/fqf/schedule/friday.py` | Friday act data |
| `src/fqf/schedule/saturday.py` | Saturday act data |
| `src/fqf/schedule/sunday.py` | Sunday act data |
| `src/fqf/tokens/words.py` | NOLA-themed word pools (~50 words × 3 pools) |
| `src/fqf/tokens/generator.py` | `generate_token()`, `validate_token_format()` |
| `src/fqf/db.py` | Neon connection pool, schedule CRUD operations |
| `src/fqf/api/app.py` | FastAPI app factory, CORS, lifespan, static mount |
| `src/fqf/api/act_routes.py` | `GET /api/v1/acts`, `GET /api/v1/acts/{slug}` |
| `src/fqf/api/schedule_routes.py` | Schedule CRUD + merge endpoints |
| `src/fqf/api/schemas.py` | Pydantic request/response models |
| `src/fqf/cli.py` | Click CLI entry point |

### Frontend (`ui/`)

| File | Responsibility |
|------|---------------|
| `ui/src/lib/types.ts` | TypeScript interfaces matching backend Pydantic models |
| `ui/src/lib/api.ts` | Typed fetch wrapper for all API endpoints |
| `ui/src/lib/stores.svelte.ts` | App-wide reactive state (selected day, picks, token, filters) |
| `ui/src/lib/conflict.ts` | Overlap calculation, conflict level assignment |
| `ui/src/lib/emoji-mapper.ts` | Deterministic token → emoji mapping for merge view |
| `ui/src/lib/constants.ts` | Grid sizing, color values, breakpoints |
| `ui/src/lib/components/DayTabs.svelte` | Day selector tabs (Thu/Fri/Sat/Sun) |
| `ui/src/lib/components/ScheduleGrid.svelte` | Desktop grid: stages as columns, time as vertical axis |
| `ui/src/lib/components/ActBlock.svelte` | Positioned act block with conflict coloring |
| `ui/src/lib/components/ActDetail.svelte` | Act bio panel (fetched on demand via slug) |
| `ui/src/lib/components/MobileSchedule.svelte` | Single-column mobile layout (by-time or by-stage) |
| `ui/src/lib/components/MySchedule.svelte` | Filtered view of picked acts only |
| `ui/src/lib/components/MergeView.svelte` | Multi-token merged schedule with emoji badges |
| `ui/src/lib/components/TokenDialog.svelte` | Create/load schedule modal |
| `ui/src/lib/components/FilterPanel.svelte` | Genre + stage filter checkboxes (stub) |
| `ui/src/routes/+layout.svelte` | App shell: AppBar, navigation, token display |
| `ui/src/routes/+page.svelte` | Main page: grid/mobile/my-schedule/merge view switching |

### Tests

| File | Covers |
|------|--------|
| `tests/conftest.py` | Shared fixtures (sample acts, test client) |
| `tests/test_models.py` | Act dataclass, enums, constants |
| `tests/test_slugify.py` | Slug generation edge cases |
| `tests/test_schedule.py` | Query functions: `at`, `search`, `on`, `get_by_slug` |
| `tests/test_tokens.py` | Token generation, format validation |
| `tests/test_db.py` | Database CRUD (mocked connection) |
| `tests/test_api_acts.py` | Act endpoint integration tests |
| `tests/test_api_schedules.py` | Schedule endpoint integration tests |
| `ui/src/lib/conflict.test.ts` | Overlap calculation + color assignment |
| `ui/src/lib/emoji-mapper.test.ts` | Token-to-emoji determinism |

### Infrastructure

| File | Responsibility |
|------|---------------|
| `pyproject.toml` | Python build config, tool settings, dependencies |
| `Makefile` | Standardized build/test/lint/deploy targets |
| `.gitignore` | Ignore patterns for Python, Node, Docker, IDE |
| `Dockerfile` | Multi-stage build (node → python → runtime) |
| `.github/workflows/ci.yml` | Test + lint on push/PR |
| `.github/workflows/deploy.yml` | Build image + deploy on version tags |

---

## Phase 1: Foundation

### Task 1: Project Scaffolding

**Files:**
- Create: `.gitignore`
- Create: `pyproject.toml`
- Create: `Makefile`
- Create: `src/fqf/__init__.py`

- [ ] **Step 1: Create `.gitignore`**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
.eggs/
*.egg
.venv/
.mypy_cache/
.pytest_cache/
htmlcov/
.coverage
.coverage.*

# Node / Frontend
node_modules/
ui/build/
ui/.svelte-kit/
.pnpm-store/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Docker
.docker/

# OS
.DS_Store
Thumbs.db

# Project
.multiline/
.htmlcov/
```

- [ ] **Step 2: Create `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=64", "wheel", "setuptools-scm>=8"]
build-backend = "setuptools.build_meta"

[project]
name = "fqf2026"
dynamic = ["version"]
description = "French Quarter Festival 2026 Schedule Builder"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.115",
    "uvicorn[standard]>=0.30",
    "asyncpg>=0.30",
    "click>=8.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "pytest-asyncio>=0.24",
    "httpx>=0.27",
    "black>=24.0",
    "isort>=5.13",
    "mypy>=1.11",
]

[project.scripts]
fqf = "fqf.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
fqf = ["static/**/*"]

[tool.setuptools_scm]
version_scheme = "guess-next-dev"
local_scheme = "node-and-date"

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
```

- [ ] **Step 3: Create `Makefile`**

```makefile
.PHONY: help setup setup-api setup-ui build build-api build-ui test test-api test-ui \
        lint lint-api lint-ui format format-api format-ui dev clean \
        build-image docker-run deploy e2e

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Setup ──────────────────────────────────────────────────────────────
setup: setup-api setup-ui ## Install all dependencies

setup-api: ## Install Python dependencies
	uv venv
	uv sync --all-extras

setup-ui: ## Install frontend dependencies
	pnpm --dir ui install

# ── Build ──────────────────────────────────────────────────────────────
build: build-api build-ui ## Build all packages

build-api: ## Build Python package
	uv build

build-ui: ## Build SvelteKit frontend
	pnpm --dir ui build

# ── Test ───────────────────────────────────────────────────────────────
test: test-api test-ui ## Run all tests

test-api: ## Run Python tests with coverage
	uv run pytest

test-ui: ## Run frontend unit tests
	pnpm --dir ui test

# ── Lint ───────────────────────────────────────────────────────────────
lint: lint-api lint-ui ## Run all linters

lint-api: ## Lint Python code
	uv run black --check src tests
	uv run isort --check src tests
	uv run mypy src

lint-ui: ## Lint frontend code
	pnpm --dir ui lint

# ── Format ─────────────────────────────────────────────────────────────
format: format-api format-ui ## Format all code

format-api: ## Format Python code
	uv run black src tests
	uv run isort src tests

format-ui: ## Format frontend code
	pnpm --dir ui format

# ── Dev ────────────────────────────────────────────────────────────────
dev: ## Start dev servers
	uv run uvicorn fqf.api.app:create_app --factory --reload --port 8000 &
	pnpm --dir ui dev --open

# ── Docker ─────────────────────────────────────────────────────────────
build-image: ## Build Docker image locally
	docker buildx build -t fqf:local .

docker-run: build-image ## Build and run Docker image
	docker run --rm -p 8000:8000 --env-file .env fqf:local

# ── Deploy ─────────────────────────────────────────────────────────────
deploy: ## Build, push, deploy to Cloud Run
	@echo "Deploy target — configure per environment"

# ── E2E ────────────────────────────────────────────────────────────────
e2e: ## Run E2E tests
	pnpm --dir ui exec playwright test

# ── Clean ──────────────────────────────────────────────────────────────
clean: ## Remove build artifacts
	rm -rf dist/ build/ *.egg-info .mypy_cache .pytest_cache htmlcov .coverage
	rm -rf ui/build ui/.svelte-kit
```

- [ ] **Step 4: Create package init**

```python
# src/fqf/__init__.py
"""French Quarter Festival 2026 Schedule Builder."""
```

Also create empty `__init__.py` files for subpackages:
- `src/fqf/schedule/__init__.py` (will be populated in Task 3)
- `src/fqf/tokens/__init__.py`
- `src/fqf/api/__init__.py`
- `tests/__init__.py`

- [ ] **Step 5: Verify setup**

Run: `uv venv && uv sync --all-extras`
Expected: Virtual environment created, all dependencies installed.

Run: `uv run python -c "import fqf; print('ok')"`
Expected: `ok`

- [ ] **Step 6: Commit**

```
feat: project scaffolding with pyproject.toml, Makefile, gitignore
```

---

### Task 2: Core Data Model

**Files:**
- Create: `src/fqf/slugify.py`
- Create: `src/fqf/models.py`
- Create: `tests/test_slugify.py`
- Create: `tests/test_models.py`

- [ ] **Step 1: Write slugify tests**

```python
# tests/test_slugify.py
"""Tests for deterministic slug generation."""

from fqf.slugify import slugify


class TestSlugify:
    def test_simple_name(self) -> None:
        assert slugify("Rebirth Brass Band") == "rebirth-brass-band"

    def test_ampersand(self) -> None:
        assert slugify("Kermit Ruffins & the Barbecue Swingers") == (
            "kermit-ruffins-the-barbecue-swingers"
        )

    def test_apostrophe(self) -> None:
        assert slugify("George Porter Jr & Runnin' Pardners") == (
            "george-porter-jr-runnin-pardners"
        )

    def test_unicode_accent(self) -> None:
        assert slugify("Arsène Delay & Charlie Wooton") == (
            "arsene-delay-charlie-wooton"
        )

    def test_unicode_special(self) -> None:
        assert slugify("Fermín Ceballos + Merengue4FOUR") == (
            "fermin-ceballos-merengue4four"
        )

    def test_parentheses(self) -> None:
        assert slugify("Sir Chantz Powell & The Sound Of Funk (S.O.F.)") == (
            "sir-chantz-powell-the-sound-of-funk-s-o-f"
        )

    def test_quotes(self) -> None:
        assert slugify("John 'Papa' Gros") == "john-papa-gros"

    def test_featuring(self) -> None:
        assert slugify("Stanton Moore featuring Joe Ashlar and Danny Abel") == (
            "stanton-moore-featuring-joe-ashlar-and-danny-abel"
        )

    def test_numeric_prefix(self) -> None:
        assert slugify("504 Millz") == "504-millz"

    def test_deterministic(self) -> None:
        name = "The Dirty Dozen Brass Band"
        assert slugify(name) == slugify(name)

    def test_ecirb_muller(self) -> None:
        assert slugify("Ecirb Müller's Twisted Dixie") == (
            "ecirb-mullers-twisted-dixie"
        )

    def test_presents_in_name(self) -> None:
        assert slugify("Ovi-G presents 'Xtra Cash!'") == (
            "ovi-g-presents-xtra-cash"
        )
```

- [ ] **Step 2: Run slugify tests — verify they fail**

Run: `uv run pytest tests/test_slugify.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'fqf.slugify'`

- [ ] **Step 3: Implement slugify**

```python
# src/fqf/slugify.py
"""Deterministic slug generation for act names."""

import re
import unicodedata


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug.

    Normalizes unicode, lowercases, replaces non-alphanumeric
    characters with hyphens, and strips leading/trailing hyphens.
    """
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text
```

- [ ] **Step 4: Run slugify tests — verify they pass**

Run: `uv run pytest tests/test_slugify.py -v`
Expected: All 12 tests PASS.

- [ ] **Step 5: Write model tests**

```python
# tests/test_models.py
"""Tests for data models, enums, and constants."""

from datetime import date, time

from fqf.models import (
    Act, Genre, AboutSource,
    THU, FRI, SAT, SUN, FESTIVAL_DATES,
    ABITA, NEWORLEANS, ALL_STAGES,
    t,
)


class TestGenreEnum:
    def test_all_genres_have_string_values(self) -> None:
        for genre in Genre:
            assert isinstance(genre.value, str)
            assert len(genre.value) > 0

    def test_specific_values(self) -> None:
        assert Genre.BRASS_BAND == "Brass Band"
        assert Genre.JAZZ_TRADITIONAL == "Jazz (Traditional)"
        assert Genre.RNB_SOUL == "R&B / Soul"
        assert Genre.UNKNOWN == "Unknown"

    def test_genre_count(self) -> None:
        EXPECTED_GENRE_COUNT = 18  # 17 defined + Unknown
        assert len(Genre) == EXPECTED_GENRE_COUNT


class TestAboutSource:
    def test_values(self) -> None:
        assert AboutSource.RESEARCHED == "researched"
        assert AboutSource.GENERATED == "generated"
        assert AboutSource.NONE == ""


class TestDateConstants:
    def test_festival_dates(self) -> None:
        assert THU == date(2026, 4, 16)
        assert FRI == date(2026, 4, 17)
        assert SAT == date(2026, 4, 18)
        assert SUN == date(2026, 4, 19)

    def test_festival_dates_list(self) -> None:
        assert FESTIVAL_DATES == [THU, FRI, SAT, SUN]


class TestTimeHelper:
    def test_basic(self) -> None:
        assert t(14, 30) == time(14, 30)

    def test_zero_minutes(self) -> None:
        assert t(11, 0) == time(11, 0)


class TestStageConstants:
    def test_stage_count(self) -> None:
        EXPECTED_STAGE_COUNT = 19
        assert len(ALL_STAGES) == EXPECTED_STAGE_COUNT

    def test_no_duplicates(self) -> None:
        assert len(ALL_STAGES) == len(set(ALL_STAGES))


class TestAct:
    def test_basic_creation(self) -> None:
        act = Act("Rebirth Brass Band", ABITA, THU, t(17, 0), t(18, 20))
        assert act.name == "Rebirth Brass Band"
        assert act.stage == ABITA
        assert act.date == THU
        assert act.start == t(17, 0)
        assert act.end == t(18, 20)

    def test_slug_computed(self) -> None:
        act = Act("Rebirth Brass Band", ABITA, THU, t(17, 0), t(18, 20))
        assert act.slug == "rebirth-brass-band"

    def test_default_genre(self) -> None:
        act = Act("Test", ABITA, THU, t(11, 0), t(12, 0))
        assert act.genre == Genre.UNKNOWN

    def test_default_about(self) -> None:
        act = Act("Test", ABITA, THU, t(11, 0), t(12, 0))
        assert act.about == ""
        assert act.about_source == AboutSource.NONE

    def test_enriched_act(self) -> None:
        act = Act(
            "Rebirth Brass Band", ABITA, THU, t(17, 0), t(18, 20),
            genre=Genre.BRASS_BAND,
            about="One of the greatest brass bands in New Orleans history.",
            about_source=AboutSource.RESEARCHED,
        )
        assert act.genre == Genre.BRASS_BAND
        assert act.about_source == AboutSource.RESEARCHED

    def test_frozen(self) -> None:
        act = Act("Test", ABITA, THU, t(11, 0), t(12, 0))
        try:
            act.name = "Changed"  # type: ignore[misc]
            assert False, "Should have raised FrozenInstanceError"
        except AttributeError:
            pass

    def test_str(self) -> None:
        act = Act("Rebirth Brass Band", ABITA, THU, t(17, 0), t(18, 20))
        result = str(act)
        assert "Rebirth Brass Band" in result
        assert ABITA in result
```

- [ ] **Step 6: Run model tests — verify they fail**

Run: `uv run pytest tests/test_models.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'fqf.models'`

- [ ] **Step 7: Implement models**

```python
# src/fqf/models.py
"""Data models, enums, and constants for FQF 2026."""

from dataclasses import dataclass, field
from datetime import date, time
from enum import StrEnum

from fqf.slugify import slugify


class Genre(StrEnum):
    """Controlled vocabulary for act genres."""

    BRASS_BAND = "Brass Band"
    JAZZ_TRADITIONAL = "Jazz (Traditional)"
    JAZZ_CONTEMPORARY = "Jazz (Contemporary)"
    ZYDECO = "Zydeco"
    CAJUN = "Cajun"
    RNB_SOUL = "R&B / Soul"
    BLUES = "Blues"
    FUNK = "Funk"
    ROCK = "Rock"
    WORLD = "World"
    LATIN = "Latin"
    REGGAE = "Reggae"
    GOSPEL = "Gospel"
    SINGER_SONGWRITER = "Singer-Songwriter"
    ELECTRONIC_DJ = "Electronic / DJ"
    INDIAN_MARDI_GRAS = "Indian Mardi Gras"
    MIXED_ECLECTIC = "Mixed / Eclectic"
    UNKNOWN = "Unknown"


class AboutSource(StrEnum):
    """How the act bio was obtained."""

    RESEARCHED = "researched"
    GENERATED = "generated"
    NONE = ""


# ── Date constants ─────────────────────────────────────────────────────
THU = date(2026, 4, 16)
FRI = date(2026, 4, 17)
SAT = date(2026, 4, 18)
SUN = date(2026, 4, 19)

FESTIVAL_DATES = [THU, FRI, SAT, SUN]

# ── Stage constants ────────────────────────────────────────────────────
ABITA = "Abita Beer Stage"
NEWORLEANS = "NewOrleans.com Stage"
TROPICAL = "Tropical Isle Hand Grenade Stage"
JACKDANIELS = "Jack Daniel's Stage"
WILLOW = "Willow Dispensary Stage"
LOYOLA = "Loyola Esplanade in the Shade Stage"
FISHFRY = "Louisiana Fish Fry Stage"
ENTERGY = "Entergy Songwriter Stage"
PANAMLIFE = "Pan-American Life Insurance Group Stage"
JAZZPLAYHOUSE = "Jazz Playhouse at the Royal Sonesta"
FRENCHMARKET = "French Market Traditional Jazz Stage"
DUTCHALLEY = "French Market Dutch Alley Stage"
HOUSEOFBLUES = "House of Blues Voodoo Garden Stage"
JAZZPARK = "New Orleans Jazz National Historical Park Stage"
SCHOOLHOUSE = "Ernie's Schoolhouse Stage"
HANCOCK = "Hancock Whitney Stage"
OMNI = "Omni Royal Orleans Stage"
KREWE = "KREWE Eyewear Stage"
CAFEBEIGNET = "Cafe Beignet Stage"

ALL_STAGES = [
    ABITA, NEWORLEANS, TROPICAL, JACKDANIELS, WILLOW, LOYOLA,
    FISHFRY, ENTERGY, PANAMLIFE, JAZZPLAYHOUSE, FRENCHMARKET,
    DUTCHALLEY, HOUSEOFBLUES, JAZZPARK, SCHOOLHOUSE, HANCOCK,
    OMNI, KREWE, CAFEBEIGNET,
]


def t(h: int, m: int) -> time:
    """Shorthand for time(h, m)."""
    return time(h, m)


@dataclass(frozen=True)
class Act:
    """A single performance at the festival."""

    name: str
    stage: str
    date: date
    start: time
    end: time
    genre: str = Genre.UNKNOWN
    about: str = ""
    about_source: str = AboutSource.NONE
    slug: str = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "slug", slugify(self.name))

    def __str__(self) -> str:
        return (
            f"{self.name:<60} | {self.stage:<45} | "
            f"{self.date.strftime('%a %b %d')} | "
            f"{self.start.strftime('%-I:%M %p')} - {self.end.strftime('%-I:%M %p')}"
        )
```

- [ ] **Step 8: Run all tests — verify they pass**

Run: `uv run pytest tests/test_slugify.py tests/test_models.py -v`
Expected: All tests PASS.

- [ ] **Step 9: Commit**

```
feat: core data model with Act, Genre, AboutSource, slugify
```

---

### Task 3: Schedule Data Migration

**Files:**
- Create: `src/fqf/schedule/thursday.py`
- Create: `src/fqf/schedule/friday.py`
- Create: `src/fqf/schedule/saturday.py`
- Create: `src/fqf/schedule/sunday.py`
- Modify: `src/fqf/schedule/__init__.py`
- Create: `tests/test_schedule.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: Write schedule query tests**

```python
# tests/conftest.py
"""Shared test fixtures."""

import pytest
from datetime import time

from fqf.models import Act, Genre, AboutSource, ABITA, NEWORLEANS, TROPICAL, THU, FRI, t


@pytest.fixture
def sample_acts() -> list[Act]:
    """A small set of acts for unit testing."""
    return [
        Act("Alpha Band", ABITA, THU, t(11, 0), t(12, 0)),
        Act("Beta Brass", NEWORLEANS, THU, t(11, 30), t(12, 30)),
        Act("Gamma Jazz", TROPICAL, THU, t(14, 0), t(15, 0), genre=Genre.JAZZ_TRADITIONAL),
        Act("Delta Blues", ABITA, FRI, t(11, 0), t(12, 0), genre=Genre.BLUES),
    ]
```

```python
# tests/test_schedule.py
"""Tests for schedule query functions."""

from datetime import date, time

from fqf.models import (
    THU, FRI, SAT, SUN, ABITA, NEWORLEANS, TROPICAL,
    FISHFRY, JACKDANIELS, Genre, t,
)
from fqf.schedule import SCHEDULE, at, search, on, get_by_slug


class TestScheduleData:
    def test_total_act_count(self) -> None:
        EXPECTED_ACT_COUNT = 302
        assert len(SCHEDULE) == EXPECTED_ACT_COUNT

    def test_all_dates_are_festival_dates(self) -> None:
        valid_dates = {THU, FRI, SAT, SUN}
        for act in SCHEDULE:
            assert act.date in valid_dates, f"{act.name} has invalid date {act.date}"

    def test_start_before_end(self) -> None:
        for act in SCHEDULE:
            assert act.start < act.end, f"{act.name} starts at {act.start} but ends at {act.end}"

    def test_all_slugs_unique(self) -> None:
        slugs = [act.slug for act in SCHEDULE]
        duplicates = [s for s in slugs if slugs.count(s) > 1]
        assert len(slugs) == len(set(slugs)), f"Duplicate slugs: {set(duplicates)}"

    def test_known_act_exists(self) -> None:
        names = [act.name for act in SCHEDULE]
        assert "Rebirth Brass Band" in names
        assert "The Soul Rebels" in names
        assert "Tuba Skinny" in names


class TestAt:
    def test_returns_acts_at_time(self) -> None:
        results = at(FRI, t(14, 0))
        assert len(results) > 0
        for act in results:
            assert act.date == FRI
            assert act.start <= t(14, 0) < act.end

    def test_no_results_outside_hours(self) -> None:
        results = at(THU, t(6, 0))
        assert results == []

    def test_sorted_by_stage(self) -> None:
        results = at(SAT, t(14, 0))
        stages = [act.stage for act in results]
        assert stages == sorted(stages)


class TestSearch:
    def test_search_by_name(self) -> None:
        results = search("Rebirth")
        assert any(a.name == "Rebirth Brass Band" for a in results)

    def test_search_by_stage(self) -> None:
        results = search("Fish Fry")
        assert all(FISHFRY.lower() in a.stage.lower() for a in results)

    def test_search_case_insensitive(self) -> None:
        assert search("rebirth") == search("REBIRTH")

    def test_search_no_results(self) -> None:
        assert search("zzzznonexistent") == []

    def test_sorted_by_date_time(self) -> None:
        results = search("brass")
        for i in range(len(results) - 1):
            assert (results[i].date, results[i].start) <= (
                results[i + 1].date, results[i + 1].start
            )


class TestOn:
    def test_all_acts_on_day(self) -> None:
        results = on(SAT)
        assert len(results) > 0
        assert all(a.date == SAT for a in results)

    def test_filter_by_stage(self) -> None:
        results = on(THU, stage="Jack Daniel")
        assert all(JACKDANIELS.lower() in a.stage.lower() for a in results)

    def test_sorted_by_stage_then_time(self) -> None:
        results = on(FRI)
        for i in range(len(results) - 1):
            assert (results[i].stage, results[i].start) <= (
                results[i + 1].stage, results[i + 1].start
            )


class TestGetBySlug:
    def test_found(self) -> None:
        act = get_by_slug("rebirth-brass-band")
        assert act is not None
        assert act.name == "Rebirth Brass Band"

    def test_not_found(self) -> None:
        assert get_by_slug("nonexistent-band") is None
```

- [ ] **Step 2: Run schedule tests — verify they fail**

Run: `uv run pytest tests/test_schedule.py -v`
Expected: FAIL — `ImportError: cannot import name 'SCHEDULE' from 'fqf.schedule'`

- [ ] **Step 3: Migrate schedule data into day files**

Each day file follows this pattern. The data comes directly from the existing `fqf2026.py`, with the date comment headers corrected (Thursday is April 16, not 17, etc.).

```python
# src/fqf/schedule/thursday.py
"""Thursday April 16, 2026 — FQF schedule data."""

from fqf.models import (
    Act, THU, t,
    ABITA, NEWORLEANS, TROPICAL, JACKDANIELS, WILLOW,
    FISHFRY, PANAMLIFE, HOUSEOFBLUES,
)

THURSDAY_ACTS: list[Act] = [
    Act("Seguenon Kone featuring Ivorie Spectacle", ABITA, THU, t(11, 30), t(12, 30)),
    Act("The Quickening",                           ABITA, THU, t(12, 50), t(13, 50)),
    # ... all Thursday acts from fqf2026.py, using the same constants ...
    Act("Julian Primeaux",                          HOUSEOFBLUES, THU, t(19, 30), t(21, 30)),
]
```

Repeat for `friday.py` (FRI acts), `saturday.py` (SAT acts), `sunday.py` (SUN acts). Each file imports only the stage constants and date constant it needs.

**Critical:** Fix the date comments. The existing file says "THURSDAY April 17" but THU is April 16. The correct headers are:
- Thursday April 16
- Friday April 17
- Saturday April 18
- Sunday April 19

- [ ] **Step 4: Implement schedule query module**

```python
# src/fqf/schedule/__init__.py
"""Schedule data and query functions."""

from datetime import date, time

from fqf.models import Act
from fqf.schedule.thursday import THURSDAY_ACTS
from fqf.schedule.friday import FRIDAY_ACTS
from fqf.schedule.saturday import SATURDAY_ACTS
from fqf.schedule.sunday import SUNDAY_ACTS

SCHEDULE: list[Act] = THURSDAY_ACTS + FRIDAY_ACTS + SATURDAY_ACTS + SUNDAY_ACTS

_SLUG_INDEX: dict[str, Act] = {act.slug: act for act in SCHEDULE}


def at(query_date: date, query_time: time) -> list[Act]:
    """Return all acts playing at a given date and time."""
    return sorted(
        [a for a in SCHEDULE if a.date == query_date and a.start <= query_time < a.end],
        key=lambda a: a.stage,
    )


def search(query: str) -> list[Act]:
    """Case-insensitive substring search across act name, stage, and genre."""
    q = query.lower()
    return sorted(
        [
            a for a in SCHEDULE
            if q in a.name.lower() or q in a.stage.lower() or q in a.genre.lower()
        ],
        key=lambda a: (a.date, a.start),
    )


def on(query_date: date, stage: str | None = None) -> list[Act]:
    """Return all acts on a given date, optionally filtered by stage substring."""
    results = [a for a in SCHEDULE if a.date == query_date]
    if stage:
        results = [a for a in results if stage.lower() in a.stage.lower()]
    return sorted(results, key=lambda a: (a.stage, a.start))


def get_by_slug(slug: str) -> Act | None:
    """Return a single act by its slug, or None."""
    return _SLUG_INDEX.get(slug)
```

- [ ] **Step 5: Run all tests — verify they pass**

Run: `uv run pytest tests/ -v`
Expected: All tests PASS. Specifically verify `test_total_act_count` confirms 302 and `test_all_slugs_unique` passes.

- [ ] **Step 6: Remove the original `fqf2026.py`**

The module is now fully replaced by `src/fqf/`. Delete `fqf2026.py` from the project root.

- [ ] **Step 7: Commit**

```
feat: migrate schedule data into src/fqf package, split by day

Restructured fqf2026.py into a proper Python package with:
- Act dataclass enhanced with slug, genre, about fields
- Schedule data split into per-day modules
- Query API (at, search, on) preserved with identical signatures
- New get_by_slug query for API lookups
```

---

## Phase 2: Backend Services

### Task 4: Token Generation

**Files:**
- Create: `src/fqf/tokens/words.py`
- Create: `src/fqf/tokens/generator.py`
- Create: `tests/test_tokens.py`

- [ ] **Step 1: Write token tests**

```python
# tests/test_tokens.py
"""Tests for NOLA-themed token generation."""

import re

from fqf.tokens.generator import generate_token, validate_token_format
from fqf.tokens.words import POOL_PLACES, POOL_MUSIC, POOL_NOLA


EXPECTED_MIN_POOL_SIZE = 40
TOKEN_PATTERN = re.compile(r"^[a-z]+-[a-z]+-[a-z]+$")


class TestWordPools:
    def test_places_pool_size(self) -> None:
        assert len(POOL_PLACES) >= EXPECTED_MIN_POOL_SIZE

    def test_music_pool_size(self) -> None:
        assert len(POOL_MUSIC) >= EXPECTED_MIN_POOL_SIZE

    def test_nola_pool_size(self) -> None:
        assert len(POOL_NOLA) >= EXPECTED_MIN_POOL_SIZE

    def test_no_duplicates_within_pools(self) -> None:
        for pool in [POOL_PLACES, POOL_MUSIC, POOL_NOLA]:
            assert len(pool) == len(set(pool))

    def test_all_lowercase_alpha(self) -> None:
        for pool in [POOL_PLACES, POOL_MUSIC, POOL_NOLA]:
            for word in pool:
                assert word == word.lower(), f"Word not lowercase: {word}"
                assert word.isalpha(), f"Word has non-alpha chars: {word}"


class TestGenerateToken:
    def test_format_three_words(self) -> None:
        token = generate_token()
        parts = token.split("-")
        assert len(parts) == 3

    def test_matches_pattern(self) -> None:
        token = generate_token()
        assert TOKEN_PATTERN.match(token), f"Token doesn't match pattern: {token}"

    def test_uniqueness_over_many_generations(self) -> None:
        GENERATION_COUNT = 200
        tokens = {generate_token() for _ in range(GENERATION_COUNT)}
        # With ~50^3 = 125k combos, 200 should all be unique
        assert len(tokens) == GENERATION_COUNT

    def test_words_from_pools(self) -> None:
        token = generate_token()
        parts = token.split("-")
        assert parts[0] in POOL_PLACES
        assert parts[1] in POOL_MUSIC
        assert parts[2] in POOL_NOLA


class TestValidateTokenFormat:
    def test_valid(self) -> None:
        assert validate_token_format("treme-funky-crawfish") is True

    def test_too_few_words(self) -> None:
        assert validate_token_format("treme-funky") is False

    def test_too_many_words(self) -> None:
        assert validate_token_format("treme-funky-crawfish-extra") is False

    def test_empty(self) -> None:
        assert validate_token_format("") is False

    def test_uppercase_rejected(self) -> None:
        assert validate_token_format("Treme-Funky-Crawfish") is False

    def test_numbers_rejected(self) -> None:
        assert validate_token_format("treme-funky-504") is False
```

- [ ] **Step 2: Run token tests — verify they fail**

Run: `uv run pytest tests/test_tokens.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement word pools**

```python
# src/fqf/tokens/words.py
"""NOLA-themed word pools for token generation.

Three pools of ~50 words each, yielding ~125,000 unique combinations.
Format: <place>-<music-adjective>-<nola-noun>
Example: "treme-funky-crawfish", "marigny-brassy-beignet"
"""

POOL_PLACES: list[str] = [
    "treme", "marigny", "bywater", "frenchmen", "bourbon",
    "magazine", "congo", "decatur", "rampart", "esplanade",
    "chartres", "dauphine", "royal", "canal", "basin",
    "gentilly", "algiers", "uptown", "midcity", "lakeside",
    "bayou", "warehouse", "garden", "irish", "seventh",
    "backatown", "hollygrove", "broadmoor", "carrollton", "fontaine",
    "pirate", "jackson", "dumaine", "iberville", "gravier",
    "perdido", "poydras", "calliope", "melpomene", "terpsichore",
    "coliseum", "annunciation", "tchoupitoulas", "constance", "laurel",
    "octavia", "napoleon", "valence", "cadiz", "milan",
]

POOL_MUSIC: list[str] = [
    "funky", "jazzy", "stomping", "swinging", "rolling",
    "syncopated", "groovy", "soulful", "brassy", "bluesy",
    "bouncing", "strutting", "riffing", "sliding", "honking",
    "wailing", "crooning", "belting", "grooving", "shuffling",
    "clapping", "tapping", "rumbling", "humming", "howling",
    "singing", "drumming", "strumming", "picking", "blowing",
    "marching", "dancing", "prancing", "stepping", "twirling",
    "bopping", "jamming", "vamping", "comping", "soloing",
    "mellow", "brisk", "lively", "fiery", "smooth",
    "snappy", "peppy", "bold", "sweet", "wild",
]

POOL_NOLA: list[str] = [
    "crawfish", "beignet", "gumbo", "praline", "flambeaux",
    "parasol", "pelican", "magnolia", "streetcar", "shotgun",
    "kingcake", "hurricane", "sazerac", "roux", "andouille",
    "boudin", "etouffee", "tabasco", "oyster", "shrimp",
    "trumpet", "trombone", "tuba", "washboard", "snaredrum",
    "accordion", "fiddle", "tambourine", "cowbell", "saxophone",
    "po boy", "muffuletta", "jambalaya", "bisque", "grillades",
    "doubloon", "krewe", "lagniappe", "fais", "pirogue",
    "nutria", "heron", "egret", "ibis", "alligator",
    "cypress", "moss", "levee", "floodwall", "crescent",
]
```

Wait — the test checks `word.isalpha()` but "po boy" has a space. And the token format is "word-word-word" where hyphens separate the three pools. If pool words contain spaces, the token format breaks. Let me fix the pool to use only single words (no spaces).

Let me revise `POOL_NOLA` to remove multi-word entries:

```python
POOL_NOLA: list[str] = [
    "crawfish", "beignet", "gumbo", "praline", "flambeaux",
    "parasol", "pelican", "magnolia", "streetcar", "shotgun",
    "kingcake", "hurricane", "sazerac", "roux", "andouille",
    "boudin", "etouffee", "tabasco", "oyster", "shrimp",
    "trumpet", "trombone", "tuba", "washboard", "snaredrum",
    "accordion", "fiddle", "tambourine", "cowbell", "saxophone",
    "muffuletta", "jambalaya", "bisque", "grillades", "chicory",
    "doubloon", "krewe", "lagniappe", "pirogue", "zydeco",
    "nutria", "heron", "egret", "ibis", "alligator",
    "cypress", "moss", "levee", "crescent", "voodoo",
]
```

OK let me include the corrected version in the plan.

- [ ] **Step 4: Implement token generator**

```python
# src/fqf/tokens/generator.py
"""Generate and validate NOLA-themed schedule tokens."""

import re
import secrets

from fqf.tokens.words import POOL_PLACES, POOL_MUSIC, POOL_NOLA

TOKEN_WORD_COUNT = 3
_TOKEN_PATTERN = re.compile(r"^[a-z]+-[a-z]+-[a-z]+$")


def generate_token() -> str:
    """Generate a random three-word NOLA-themed token.

    Format: <place>-<music-adjective>-<nola-noun>
    Example: "treme-funky-crawfish"
    """
    place = secrets.choice(POOL_PLACES)
    music = secrets.choice(POOL_MUSIC)
    nola = secrets.choice(POOL_NOLA)
    return f"{place}-{music}-{nola}"


def validate_token_format(token: str) -> bool:
    """Check if a string matches the expected token format."""
    if not _TOKEN_PATTERN.match(token):
        return False
    parts = token.split("-")
    return len(parts) == TOKEN_WORD_COUNT
```

- [ ] **Step 5: Run token tests — verify they pass**

Run: `uv run pytest tests/test_tokens.py -v`
Expected: All tests PASS.

- [ ] **Step 6: Commit**

```
feat: NOLA-themed token generation for schedule identification
```

---

### Task 5: FastAPI App + Act Endpoints

**Files:**
- Create: `src/fqf/api/schemas.py`
- Create: `src/fqf/api/app.py`
- Create: `src/fqf/api/act_routes.py`
- Create: `tests/test_api_acts.py`

- [ ] **Step 1: Write act endpoint tests**

```python
# tests/test_api_acts.py
"""Tests for act API endpoints."""

import pytest
from httpx import AsyncClient, ASGITransport

from fqf.api.app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


class TestListActs:
    @pytest.mark.asyncio
    async def test_returns_all_acts(self, client: AsyncClient) -> None:
        resp = await client.get("/api/v1/acts")
        assert resp.status_code == 200
        data = resp.json()
        EXPECTED_ACT_COUNT = 302
        assert data["count"] == EXPECTED_ACT_COUNT
        assert len(data["acts"]) == EXPECTED_ACT_COUNT

    @pytest.mark.asyncio
    async def test_act_summary_shape(self, client: AsyncClient) -> None:
        resp = await client.get("/api/v1/acts")
        act = resp.json()["acts"][0]
        assert "slug" in act
        assert "name" in act
        assert "stage" in act
        assert "date" in act
        assert "start" in act
        assert "end" in act
        assert "genre" in act
        # about should NOT be in summary
        assert "about" not in act

    @pytest.mark.asyncio
    async def test_filter_by_date(self, client: AsyncClient) -> None:
        resp = await client.get("/api/v1/acts", params={"date": "2026-04-16"})
        assert resp.status_code == 200
        data = resp.json()
        assert all(a["date"] == "2026-04-16" for a in data["acts"])

    @pytest.mark.asyncio
    async def test_filter_by_stage(self, client: AsyncClient) -> None:
        resp = await client.get("/api/v1/acts", params={"stage": "Fish Fry"})
        assert resp.status_code == 200
        data = resp.json()
        assert all("Fish Fry" in a["stage"] for a in data["acts"])

    @pytest.mark.asyncio
    async def test_search(self, client: AsyncClient) -> None:
        resp = await client.get("/api/v1/acts", params={"q": "brass"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] > 0


class TestGetAct:
    @pytest.mark.asyncio
    async def test_found(self, client: AsyncClient) -> None:
        resp = await client.get("/api/v1/acts/rebirth-brass-band")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Rebirth Brass Band"
        assert "about" in data
        assert "about_source" in data

    @pytest.mark.asyncio
    async def test_not_found(self, client: AsyncClient) -> None:
        resp = await client.get("/api/v1/acts/nonexistent-band")
        assert resp.status_code == 404
```

- [ ] **Step 2: Run act endpoint tests — verify they fail**

Run: `uv run pytest tests/test_api_acts.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement Pydantic schemas**

```python
# src/fqf/api/schemas.py
"""Pydantic request/response models for the API."""

from datetime import date, time

from pydantic import BaseModel, field_serializer


class ActSummary(BaseModel):
    """Lightweight act representation for list endpoints."""

    slug: str
    name: str
    stage: str
    date: date
    start: time
    end: time
    genre: str

    @field_serializer("start", "end")
    @classmethod
    def serialize_time(cls, v: time) -> str:
        return v.strftime("%H:%M")


class ActDetail(ActSummary):
    """Full act representation including bio."""

    about: str
    about_source: str


class ActListResponse(BaseModel):
    """Response for list/search endpoints."""

    acts: list[ActSummary]
    count: int


class ScheduleUpdate(BaseModel):
    """Request body for saving picks."""

    picks: list[str]


class TokenResponse(BaseModel):
    """Response when creating a new schedule."""

    token: str


class ScheduleResponse(BaseModel):
    """Response for loading a schedule."""

    token: str
    picks: list[str]
    acts: list[ActSummary]


class MergeEntry(BaseModel):
    """One person's picks in a merge response."""

    token: str
    picks: list[str]


class MergeResponse(BaseModel):
    """Response for merge endpoint."""

    schedules: list[MergeEntry]
    acts: list[ActSummary]
```

- [ ] **Step 4: Implement act routes**

```python
# src/fqf/api/act_routes.py
"""Act-related API endpoints."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from fqf.api.schemas import ActDetail, ActListResponse, ActSummary
from fqf.models import Act
from fqf.schedule import SCHEDULE, get_by_slug, search, on

router = APIRouter(prefix="/api/v1/acts", tags=["acts"])

NOT_FOUND_DETAIL = "Act not found"


def _to_summary(act: Act) -> ActSummary:
    return ActSummary(
        slug=act.slug, name=act.name, stage=act.stage,
        date=act.date, start=act.start, end=act.end, genre=act.genre,
    )


def _to_detail(act: Act) -> ActDetail:
    return ActDetail(
        slug=act.slug, name=act.name, stage=act.stage,
        date=act.date, start=act.start, end=act.end, genre=act.genre,
        about=act.about, about_source=act.about_source,
    )


@router.get("", response_model=ActListResponse)
async def list_acts(
    date: date | None = Query(None, alias="date"),
    stage: str | None = Query(None),
    q: str | None = Query(None),
) -> ActListResponse:
    """List acts with optional filtering."""
    if q:
        results = search(q)
    elif date:
        results = on(date, stage=stage)
    else:
        results = on(date, stage=stage) if stage else sorted(SCHEDULE, key=lambda a: (a.date, a.start))
    summaries = [_to_summary(a) for a in results]
    return ActListResponse(acts=summaries, count=len(summaries))


@router.get("/{slug}", response_model=ActDetail)
async def get_act(slug: str) -> ActDetail:
    """Get full act detail by slug."""
    act = get_by_slug(slug)
    if act is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    return _to_detail(act)
```

- [ ] **Step 5: Implement FastAPI app factory**

```python
# src/fqf/api/app.py
"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fqf.api.act_routes import router as act_router

API_TITLE = "FQF 2026 Schedule Builder"
CORS_ALLOW_ORIGINS = ["http://localhost:5173", "http://localhost:8000"]


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title=API_TITLE)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(act_router)

    return app
```

- [ ] **Step 6: Run act endpoint tests — verify they pass**

Run: `uv run pytest tests/test_api_acts.py -v`
Expected: All tests PASS.

- [ ] **Step 7: Commit**

```
feat: FastAPI app with act list/detail endpoints
```

---

### Task 6: Database + Schedule Persistence Endpoints

**Files:**
- Create: `src/fqf/db.py`
- Create: `src/fqf/api/schedule_routes.py`
- Modify: `src/fqf/api/app.py`
- Create: `tests/test_db.py`
- Create: `tests/test_api_schedules.py`

- [ ] **Step 1: Write database layer tests**

```python
# tests/test_db.py
"""Tests for database operations (mocked connection)."""

from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from fqf.db import create_schedule, load_schedule, save_picks, load_multiple_schedules


@pytest.fixture
def mock_pool():
    pool = AsyncMock()
    conn = AsyncMock()
    pool.acquire.return_value.__aenter__ = AsyncMock(return_value=conn)
    pool.acquire.return_value.__aexit__ = AsyncMock(return_value=False)
    return pool, conn


class TestCreateSchedule:
    @pytest.mark.asyncio
    async def test_inserts_and_returns_token(self, mock_pool) -> None:
        pool, conn = mock_pool
        conn.execute = AsyncMock()
        with patch("fqf.db._pool", pool):
            token = await create_schedule()
        assert isinstance(token, str)
        assert len(token.split("-")) == 3
        conn.execute.assert_called_once()


class TestLoadSchedule:
    @pytest.mark.asyncio
    async def test_returns_picks(self, mock_pool) -> None:
        pool, conn = mock_pool
        conn.fetchrow = AsyncMock(return_value={"picks": ["rebirth-brass-band"]})
        with patch("fqf.db._pool", pool):
            result = await load_schedule("treme-funky-crawfish")
        assert result == ["rebirth-brass-band"]

    @pytest.mark.asyncio
    async def test_returns_none_when_not_found(self, mock_pool) -> None:
        pool, conn = mock_pool
        conn.fetchrow = AsyncMock(return_value=None)
        with patch("fqf.db._pool", pool):
            result = await load_schedule("nonexistent-token-here")
        assert result is None


class TestSavePicks:
    @pytest.mark.asyncio
    async def test_updates_picks(self, mock_pool) -> None:
        pool, conn = mock_pool
        conn.execute = AsyncMock(return_value="UPDATE 1")
        with patch("fqf.db._pool", pool):
            success = await save_picks("treme-funky-crawfish", ["rebirth-brass-band"])
        assert success is True

    @pytest.mark.asyncio
    async def test_returns_false_when_not_found(self, mock_pool) -> None:
        pool, conn = mock_pool
        conn.execute = AsyncMock(return_value="UPDATE 0")
        with patch("fqf.db._pool", pool):
            success = await save_picks("nonexistent-token-here", ["some-slug"])
        assert success is False


class TestLoadMultipleSchedules:
    @pytest.mark.asyncio
    async def test_returns_map(self, mock_pool) -> None:
        pool, conn = mock_pool
        conn.fetch = AsyncMock(return_value=[
            {"token": "token-one-here", "picks": ["slug-a"]},
            {"token": "token-two-here", "picks": ["slug-b"]},
        ])
        with patch("fqf.db._pool", pool):
            result = await load_multiple_schedules(["token-one-here", "token-two-here"])
        assert result["token-one-here"] == ["slug-a"]
        assert result["token-two-here"] == ["slug-b"]
```

- [ ] **Step 2: Run db tests — verify they fail**

Run: `uv run pytest tests/test_db.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement database layer**

```python
# src/fqf/db.py
"""Neon Postgres connection and schedule CRUD operations."""

import json
import os

import asyncpg

from fqf.tokens.generator import generate_token

DATABASE_URL_ENV = "DATABASE_URL"
MIN_POOL_SIZE = 1
MAX_POOL_SIZE = 5

_pool: asyncpg.Pool | None = None

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS schedules (
    token TEXT PRIMARY KEY,
    picks JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

INSERT_SCHEDULE_SQL = """
INSERT INTO schedules (token, picks) VALUES ($1, '[]'::jsonb);
"""

SELECT_SCHEDULE_SQL = """
SELECT picks FROM schedules WHERE token = $1;
"""

UPDATE_PICKS_SQL = """
UPDATE schedules SET picks = $1::jsonb, updated_at = NOW() WHERE token = $2;
"""

SELECT_MULTIPLE_SQL = """
SELECT token, picks FROM schedules WHERE token = ANY($1);
"""


async def init_pool() -> None:
    """Initialize the connection pool. Call once at app startup."""
    global _pool
    database_url = os.environ.get(DATABASE_URL_ENV, "")
    if not database_url:
        return
    _pool = await asyncpg.create_pool(
        database_url, min_size=MIN_POOL_SIZE, max_size=MAX_POOL_SIZE,
    )
    async with _pool.acquire() as conn:
        await conn.execute(CREATE_TABLE_SQL)


async def close_pool() -> None:
    """Close the connection pool. Call once at app shutdown."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


async def create_schedule() -> str:
    """Generate a new token and create an empty schedule row."""
    assert _pool is not None
    token = generate_token()
    async with _pool.acquire() as conn:
        await conn.execute(INSERT_SCHEDULE_SQL, token)
    return token


async def load_schedule(token: str) -> list[str] | None:
    """Load picks for a token. Returns None if token doesn't exist."""
    assert _pool is not None
    async with _pool.acquire() as conn:
        row = await conn.fetchrow(SELECT_SCHEDULE_SQL, token)
    if row is None:
        return None
    return json.loads(row["picks"])


async def save_picks(token: str, picks: list[str]) -> bool:
    """Update picks for an existing token. Returns False if token not found."""
    assert _pool is not None
    async with _pool.acquire() as conn:
        result = await conn.execute(UPDATE_PICKS_SQL, json.dumps(picks), token)
    return result == "UPDATE 1"


async def load_multiple_schedules(tokens: list[str]) -> dict[str, list[str]]:
    """Load picks for multiple tokens at once."""
    assert _pool is not None
    async with _pool.acquire() as conn:
        rows = await conn.fetch(SELECT_MULTIPLE_SQL, tokens)
    return {row["token"]: json.loads(row["picks"]) for row in rows}
```

- [ ] **Step 4: Run db tests — verify they pass**

Run: `uv run pytest tests/test_db.py -v`
Expected: All tests PASS.

- [ ] **Step 5: Write schedule endpoint tests**

```python
# tests/test_api_schedules.py
"""Tests for schedule API endpoints."""

from unittest.mock import AsyncMock, patch
import pytest
from httpx import AsyncClient, ASGITransport

from fqf.api.app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


class TestCreateSchedule:
    @pytest.mark.asyncio
    async def test_returns_token(self, client: AsyncClient) -> None:
        with patch("fqf.api.schedule_routes.create_schedule", new_callable=AsyncMock) as mock:
            mock.return_value = "treme-funky-crawfish"
            resp = await client.post("/api/v1/schedule")
        assert resp.status_code == 201
        assert resp.json()["token"] == "treme-funky-crawfish"


class TestLoadSchedule:
    @pytest.mark.asyncio
    async def test_found(self, client: AsyncClient) -> None:
        with patch("fqf.api.schedule_routes.load_schedule", new_callable=AsyncMock) as mock:
            mock.return_value = ["rebirth-brass-band"]
            resp = await client.get("/api/v1/schedule/treme-funky-crawfish")
        assert resp.status_code == 200
        data = resp.json()
        assert data["token"] == "treme-funky-crawfish"
        assert "rebirth-brass-band" in data["picks"]
        assert len(data["acts"]) == 1

    @pytest.mark.asyncio
    async def test_not_found(self, client: AsyncClient) -> None:
        with patch("fqf.api.schedule_routes.load_schedule", new_callable=AsyncMock) as mock:
            mock.return_value = None
            resp = await client.get("/api/v1/schedule/nonexistent-token-here")
        assert resp.status_code == 404


class TestSavePicks:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient) -> None:
        with patch("fqf.api.schedule_routes.save_picks", new_callable=AsyncMock) as mock:
            mock.return_value = True
            resp = await client.put(
                "/api/v1/schedule/treme-funky-crawfish",
                json={"picks": ["rebirth-brass-band"]},
            )
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_not_found(self, client: AsyncClient) -> None:
        with patch("fqf.api.schedule_routes.save_picks", new_callable=AsyncMock) as mock:
            mock.return_value = False
            resp = await client.put(
                "/api/v1/schedule/nonexistent-token-here",
                json={"picks": ["some-slug"]},
            )
        assert resp.status_code == 404


MAX_MERGE_TOKENS = 5


class TestMergeSchedules:
    @pytest.mark.asyncio
    async def test_merge_two(self, client: AsyncClient) -> None:
        with patch(
            "fqf.api.schedule_routes.load_multiple_schedules", new_callable=AsyncMock
        ) as mock:
            mock.return_value = {
                "token-one-here": ["rebirth-brass-band"],
                "token-two-here": ["rebirth-brass-band", "tuba-skinny"],
            }
            resp = await client.get(
                "/api/v1/schedule/merge",
                params={"tokens": "token-one-here,token-two-here"},
            )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["schedules"]) == 2
        # Union of all picks
        slugs = {a["slug"] for a in data["acts"]}
        assert "rebirth-brass-band" in slugs
        assert "tuba-skinny" in slugs

    @pytest.mark.asyncio
    async def test_too_many_tokens(self, client: AsyncClient) -> None:
        tokens = ",".join(f"token-{i}-here" for i in range(MAX_MERGE_TOKENS + 1))
        resp = await client.get("/api/v1/schedule/merge", params={"tokens": tokens})
        assert resp.status_code == 400
```

- [ ] **Step 6: Implement schedule routes**

```python
# src/fqf/api/schedule_routes.py
"""Schedule persistence API endpoints."""

from fastapi import APIRouter, HTTPException, Query

from fqf.api.schemas import (
    ActSummary, MergeEntry, MergeResponse,
    ScheduleResponse, ScheduleUpdate, TokenResponse,
)
from fqf.db import create_schedule, load_schedule, save_picks, load_multiple_schedules
from fqf.schedule import get_by_slug

router = APIRouter(prefix="/api/v1/schedule", tags=["schedule"])

NOT_FOUND_DETAIL = "Schedule not found"
TOO_MANY_TOKENS_DETAIL = "Too many tokens"
MAX_MERGE_TOKENS = 5


def _slug_to_summary(slug: str) -> ActSummary | None:
    act = get_by_slug(slug)
    if act is None:
        return None
    return ActSummary(
        slug=act.slug, name=act.name, stage=act.stage,
        date=act.date, start=act.start, end=act.end, genre=act.genre,
    )


@router.post("", response_model=TokenResponse, status_code=201)
async def create() -> TokenResponse:
    """Generate a new schedule with a NOLA-themed token."""
    token = await create_schedule()
    return TokenResponse(token=token)


@router.get("/{token}", response_model=ScheduleResponse)
async def load(token: str) -> ScheduleResponse:
    """Load a schedule by its token."""
    picks = await load_schedule(token)
    if picks is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    acts = [s for slug in picks if (s := _slug_to_summary(slug)) is not None]
    return ScheduleResponse(token=token, picks=picks, acts=acts)


@router.put("/{token}", response_model=ScheduleResponse)
async def save(token: str, body: ScheduleUpdate) -> ScheduleResponse:
    """Save picks for an existing schedule."""
    success = await save_picks(token, body.picks)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    acts = [s for slug in body.picks if (s := _slug_to_summary(slug)) is not None]
    return ScheduleResponse(token=token, picks=body.picks, acts=acts)


@router.get("/merge", response_model=MergeResponse)
async def merge(tokens: str = Query(..., description="Comma-separated tokens")) -> MergeResponse:
    """Merge multiple schedules for comparison."""
    token_list = [t.strip() for t in tokens.split(",") if t.strip()]
    if len(token_list) > MAX_MERGE_TOKENS:
        raise HTTPException(status_code=400, detail=TOO_MANY_TOKENS_DETAIL)

    schedules_map = await load_multiple_schedules(token_list)
    entries = [
        MergeEntry(token=tok, picks=schedules_map.get(tok, []))
        for tok in token_list
    ]

    all_slugs = {slug for picks in schedules_map.values() for slug in picks}
    acts = [s for slug in all_slugs if (s := _slug_to_summary(slug)) is not None]

    return MergeResponse(schedules=entries, acts=acts)
```

- [ ] **Step 7: Update app factory to include schedule routes and lifespan**

```python
# src/fqf/api/app.py
"""FastAPI application factory."""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fqf.api.act_routes import router as act_router
from fqf.api.schedule_routes import router as schedule_router
from fqf.db import init_pool, close_pool

API_TITLE = "FQF 2026 Schedule Builder"
CORS_ALLOW_ORIGINS = ["http://localhost:5173", "http://localhost:8000"]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize and tear down the database pool."""
    await init_pool()
    yield
    await close_pool()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title=API_TITLE, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(act_router)
    app.include_router(schedule_router)

    return app
```

**Note:** The route `/api/v1/schedule/merge` must be registered before `/api/v1/schedule/{token}`, or FastAPI will try to match "merge" as a token. The `merge` endpoint is defined first in `schedule_routes.py`, but verify this works in testing. If there's a conflict, move the merge endpoint to a separate path like `/api/v1/merge`.

- [ ] **Step 8: Run all tests — verify they pass**

Run: `uv run pytest tests/ -v`
Expected: All tests PASS.

- [ ] **Step 9: Commit**

```
feat: database layer and schedule persistence API endpoints
```

---

## Phase 3: Frontend Foundation

### Task 7: SvelteKit Scaffolding

**Files:**
- Create: `ui/package.json`
- Create: `ui/svelte.config.js`
- Create: `ui/vite.config.ts`
- Create: `ui/tsconfig.json`
- Create: `ui/src/app.html`
- Create: `ui/src/app.css`

- [ ] **Step 1: Initialize SvelteKit project**

Run from project root:
```bash
pnpm create svelte@latest ui --template skeleton --types typescript
```

Select: Skeleton project, TypeScript, no additional options.

- [ ] **Step 2: Install dependencies**

```bash
pnpm --dir ui install
pnpm --dir ui add -D @sveltejs/adapter-static
pnpm --dir ui add @skeletonlabs/skeleton @skeletonlabs/tw-plugin
pnpm --dir ui add -D tailwindcss postcss autoprefixer
pnpm --dir ui add -D vitest @testing-library/svelte jsdom
pnpm --dir ui add -D playwright @playwright/test
pnpm --dir ui add zod
pnpm --dir ui add chart.js
```

- [ ] **Step 3: Configure adapter-static**

```javascript
// ui/svelte.config.js
import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    preprocess: vitePreprocess(),
    kit: {
        adapter: adapter({
            pages: 'build',
            assets: 'build',
            fallback: 'index.html',
            precompress: false,
            strict: true
        })
    }
};

export default config;
```

- [ ] **Step 4: Configure Vite with API proxy for dev**

```typescript
// ui/vite.config.ts
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
    plugins: [sveltekit()],
    server: {
        proxy: {
            '/api': 'http://localhost:8000'
        }
    },
    test: {
        include: ['src/**/*.test.ts'],
        environment: 'jsdom'
    }
});
```

- [ ] **Step 5: Set up Skeleton UI and Tailwind**

Follow the Skeleton v4 installation guide. Create `tailwind.config.ts` with the Skeleton plugin, set up the theme, and import Skeleton styles in `app.css`.

- [ ] **Step 6: Create app shell layout**

```svelte
<!-- ui/src/routes/+layout.svelte -->
<script lang="ts">
    import { AppBar } from '@skeletonlabs/skeleton';
    import '../app.css';

    let { children } = $props();
</script>

<div class="min-h-screen flex flex-col">
    <AppBar>
        <svelte:fragment slot="lead">
            <strong class="text-xl">FQF 2026</strong>
        </svelte:fragment>
        <svelte:fragment slot="trail">
            <span class="text-sm opacity-75">French Quarter Fest Schedule Builder</span>
        </svelte:fragment>
    </AppBar>

    <main class="flex-1">
        {@render children()}
    </main>
</div>
```

- [ ] **Step 7: Verify dev server starts**

Run: `pnpm --dir ui dev`
Expected: SvelteKit dev server starts on port 5173, shows the app shell.

- [ ] **Step 8: Commit**

```
feat: SvelteKit scaffolding with Skeleton UI and adapter-static
```

---

### Task 8: Types, API Client, and Stores

**Files:**
- Create: `ui/src/lib/types.ts`
- Create: `ui/src/lib/api.ts`
- Create: `ui/src/lib/stores.svelte.ts`
- Create: `ui/src/lib/constants.ts`

- [ ] **Step 1: Define TypeScript interfaces**

```typescript
// ui/src/lib/types.ts

export interface ActSummary {
    slug: string;
    name: string;
    stage: string;
    date: string;      // "YYYY-MM-DD"
    start: string;     // "HH:MM"
    end: string;       // "HH:MM"
    genre: string;
}

export interface ActDetail extends ActSummary {
    about: string;
    about_source: string;
}

export interface ActListResponse {
    acts: ActSummary[];
    count: number;
}

export interface ScheduleResponse {
    token: string;
    picks: string[];
    acts: ActSummary[];
}

export interface ScheduleUpdate {
    picks: string[];
}

export interface TokenResponse {
    token: string;
}

export interface MergeEntry {
    token: string;
    picks: string[];
}

export interface MergeResponse {
    schedules: MergeEntry[];
    acts: ActSummary[];
}

export type ConflictLevel = 'none' | 'yellow' | 'red';

export type ViewMode = 'grid' | 'mobile' | 'my-schedule' | 'merge';

export type MobileSortMode = 'by-time' | 'by-stage';

export const FESTIVAL_DATES = ['2026-04-16', '2026-04-17', '2026-04-18', '2026-04-19'] as const;

export const DAY_LABELS: Record<string, string> = {
    '2026-04-16': 'Thu 16',
    '2026-04-17': 'Fri 17',
    '2026-04-18': 'Sat 18',
    '2026-04-19': 'Sun 19',
};
```

- [ ] **Step 2: Implement API client**

```typescript
// ui/src/lib/api.ts

import type {
    ActListResponse, ActDetail, ScheduleResponse,
    ScheduleUpdate, TokenResponse, MergeResponse,
} from '$lib/types';

const BASE = '/api/v1';

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
    const resp = await fetch(url, init);
    if (!resp.ok) {
        throw new Error(`API error: ${resp.status} ${resp.statusText}`);
    }
    return resp.json() as Promise<T>;
}

export async function listActs(params?: {
    date?: string; stage?: string; q?: string;
}): Promise<ActListResponse> {
    const query = new URLSearchParams();
    if (params?.date) query.set('date', params.date);
    if (params?.stage) query.set('stage', params.stage);
    if (params?.q) query.set('q', params.q);
    const qs = query.toString();
    return fetchJson<ActListResponse>(`${BASE}/acts${qs ? `?${qs}` : ''}`);
}

export async function getAct(slug: string): Promise<ActDetail> {
    return fetchJson<ActDetail>(`${BASE}/acts/${slug}`);
}

export async function createSchedule(): Promise<TokenResponse> {
    return fetchJson<TokenResponse>(`${BASE}/schedule`, { method: 'POST' });
}

export async function loadSchedule(token: string): Promise<ScheduleResponse> {
    return fetchJson<ScheduleResponse>(`${BASE}/schedule/${token}`);
}

export async function savePicks(token: string, picks: string[]): Promise<ScheduleResponse> {
    const body: ScheduleUpdate = { picks };
    return fetchJson<ScheduleResponse>(`${BASE}/schedule/${token}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });
}

export async function mergeSchedules(tokens: string[]): Promise<MergeResponse> {
    return fetchJson<MergeResponse>(
        `${BASE}/schedule/merge?tokens=${tokens.join(',')}`
    );
}
```

- [ ] **Step 3: Implement reactive stores**

```typescript
// ui/src/lib/stores.svelte.ts

import type { ActSummary, ViewMode, MobileSortMode } from '$lib/types';
import { FESTIVAL_DATES } from '$lib/types';

class AppState {
    selectedDate = $state<string>(FESTIVAL_DATES[0]);
    viewMode = $state<ViewMode>('grid');
    mobileSortMode = $state<MobileSortMode>('by-time');
    token = $state<string | null>(null);
    picks = $state<Set<string>>(new Set());
    acts = $state<ActSummary[]>([]);
    loading = $state<boolean>(false);

    get picksArray(): string[] {
        return [...this.picks];
    }

    togglePick(slug: string): void {
        const next = new Set(this.picks);
        if (next.has(slug)) {
            next.delete(slug);
        } else {
            next.add(slug);
        }
        this.picks = next;
    }

    isPicked(slug: string): boolean {
        return this.picks.has(slug);
    }

    clearPicks(): void {
        this.picks = new Set();
    }
}

export const appState = new AppState();
```

- [ ] **Step 4: Define constants**

```typescript
// ui/src/lib/constants.ts

export const PIXELS_PER_MINUTE = 2;
export const GRID_START_HOUR = 11;
export const GRID_END_HOUR = 22;
export const GRID_COLUMN_MIN_WIDTH = 140;

export const CONFLICT_THRESHOLD = 0.30;

export const CONFLICT_COLORS = {
    none: '#22c55e',    // green-500
    yellow: '#eab308',  // yellow-500
    red: '#ef4444',     // red-500
} as const;

export const MAX_MERGE_TOKENS = 5;
```

- [ ] **Step 5: Commit**

```
feat: frontend types, API client, reactive stores, constants
```

---

### Task 9: Conflict Calculation

**Files:**
- Create: `ui/src/lib/conflict.ts`
- Create: `ui/src/lib/conflict.test.ts`

- [ ] **Step 1: Write conflict tests**

```typescript
// ui/src/lib/conflict.test.ts

import { describe, it, expect } from 'vitest';
import {
    timeToMinutes, calculateOverlapRatio, getConflictLevel,
    getWorstConflict,
} from '$lib/conflict';
import type { ActSummary } from '$lib/types';

describe('timeToMinutes', () => {
    it('converts HH:MM to minutes since midnight', () => {
        expect(timeToMinutes('14:30')).toBe(870);
    });

    it('handles midnight', () => {
        expect(timeToMinutes('00:00')).toBe(0);
    });

    it('handles 11 AM', () => {
        expect(timeToMinutes('11:00')).toBe(660);
    });
});

describe('calculateOverlapRatio', () => {
    it('returns 0 for non-overlapping acts', () => {
        // Act 1: 11:00-12:00, Act 2: 13:00-14:00
        expect(calculateOverlapRatio(660, 720, 780, 840)).toBe(0);
    });

    it('calculates partial overlap', () => {
        // Act 1: 14:00-15:00 (840-900), Act 2: 14:30-15:30 (870-930)
        // overlap = min(900,930) - 870 = 30, span = max(900,930) - 840 = 90
        const ratio = calculateOverlapRatio(840, 900, 870, 930);
        expect(ratio).toBeCloseTo(30 / 90);
    });

    it('handles containment correctly', () => {
        // Act 1: 14:00-16:00 (840-960), Act 2: 14:30-15:00 (870-900)
        // overlap = min(960,900) - 870 = 30, span = max(960,900) - 840 = 120
        const ratio = calculateOverlapRatio(840, 960, 870, 900);
        expect(ratio).toBeCloseTo(30 / 120);
    });

    it('handles reversed order (s2 < s1)', () => {
        // Same as partial overlap but args reversed
        const ratio = calculateOverlapRatio(870, 930, 840, 900);
        expect(ratio).toBeCloseTo(30 / 90);
    });

    it('returns 0 for adjacent acts (no gap, no overlap)', () => {
        // Act 1: 14:00-15:00, Act 2: 15:00-16:00
        expect(calculateOverlapRatio(840, 900, 900, 960)).toBe(0);
    });
});

describe('getConflictLevel', () => {
    it('returns none for 0', () => {
        expect(getConflictLevel(0)).toBe('none');
    });

    it('returns yellow for small overlap', () => {
        expect(getConflictLevel(0.15)).toBe('yellow');
    });

    it('returns red at threshold', () => {
        expect(getConflictLevel(0.30)).toBe('red');
    });

    it('returns red above threshold', () => {
        expect(getConflictLevel(0.75)).toBe('red');
    });
});

function makeAct(start: string, end: string, slug: string = 'test'): ActSummary {
    return { slug, name: 'Test', stage: 'Stage', date: '2026-04-16', start, end, genre: 'Unknown' };
}

describe('getWorstConflict', () => {
    it('returns none when no other picks', () => {
        const act = makeAct('14:00', '15:00', 'a');
        expect(getWorstConflict(act, [], new Set(['a']))).toBe('none');
    });

    it('returns none when no overlap', () => {
        const act = makeAct('14:00', '15:00', 'a');
        const allActs = [act, makeAct('16:00', '17:00', 'b')];
        expect(getWorstConflict(act, allActs, new Set(['a', 'b']))).toBe('none');
    });

    it('returns worst conflict level among all picked acts', () => {
        const act = makeAct('14:00', '15:00', 'a');
        const b = makeAct('14:50', '15:50', 'b'); // small overlap
        const c = makeAct('14:10', '15:30', 'c'); // big overlap
        const allActs = [act, b, c];
        expect(getWorstConflict(act, allActs, new Set(['a', 'b', 'c']))).toBe('red');
    });

    it('ignores acts on different dates', () => {
        const act = makeAct('14:00', '15:00', 'a');
        const other = { ...makeAct('14:00', '15:00', 'b'), date: '2026-04-17' };
        expect(getWorstConflict(act, [act, other], new Set(['a', 'b']))).toBe('none');
    });
});
```

- [ ] **Step 2: Run conflict tests — verify they fail**

Run: `pnpm --dir ui test -- --run src/lib/conflict.test.ts`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement conflict calculation**

```typescript
// ui/src/lib/conflict.ts

import type { ActSummary, ConflictLevel } from '$lib/types';
import { CONFLICT_THRESHOLD } from '$lib/constants';

export function timeToMinutes(time: string): number {
    const [h, m] = time.split(':').map(Number);
    return h * 60 + m;
}

export function calculateOverlapRatio(
    s1: number, e1: number, s2: number, e2: number,
): number {
    // Normalize so s1 <= s2
    if (s1 > s2) {
        [s1, e1, s2, e2] = [s2, e2, s1, e1];
    }
    const overlap = Math.max(0, Math.min(e1, e2) - s2);
    if (overlap === 0) return 0;
    const totalSpan = Math.max(e1, e2) - s1;
    return overlap / totalSpan;
}

export function getConflictLevel(ratio: number): ConflictLevel {
    if (ratio === 0) return 'none';
    if (ratio < CONFLICT_THRESHOLD) return 'yellow';
    return 'red';
}

const CONFLICT_SEVERITY: Record<ConflictLevel, number> = {
    none: 0,
    yellow: 1,
    red: 2,
};

export function getWorstConflict(
    act: ActSummary,
    allActs: ActSummary[],
    picks: Set<string>,
): ConflictLevel {
    let worst: ConflictLevel = 'none';
    const s1 = timeToMinutes(act.start);
    const e1 = timeToMinutes(act.end);

    for (const other of allActs) {
        if (other.slug === act.slug) continue;
        if (!picks.has(other.slug)) continue;
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

- [ ] **Step 4: Run conflict tests — verify they pass**

Run: `pnpm --dir ui test -- --run src/lib/conflict.test.ts`
Expected: All tests PASS.

- [ ] **Step 5: Commit**

```
feat: conflict detection with overlap ratio and severity levels
```

---

## Phase 4: Frontend Views

### Task 10: Grid View (Desktop)

**Files:**
- Create: `ui/src/lib/components/DayTabs.svelte`
- Create: `ui/src/lib/components/ScheduleGrid.svelte`
- Create: `ui/src/lib/components/ActBlock.svelte`
- Modify: `ui/src/routes/+page.svelte`

- [ ] **Step 1: Implement DayTabs**

```svelte
<!-- ui/src/lib/components/DayTabs.svelte -->
<script lang="ts">
    import { FESTIVAL_DATES, DAY_LABELS } from '$lib/types';

    let { selectedDate = $bindable() }: { selectedDate: string } = $props();
</script>

<div class="flex gap-1 p-2 bg-surface-200-700-token rounded-lg">
    {#each FESTIVAL_DATES as d}
        <button
            class="btn px-6 py-2 text-lg font-semibold transition-colors"
            class:variant-filled-primary={selectedDate === d}
            class:variant-ghost={selectedDate !== d}
            onclick={() => (selectedDate = d)}
        >
            {DAY_LABELS[d]}
        </button>
    {/each}
</div>
```

- [ ] **Step 2: Implement ActBlock**

```svelte
<!-- ui/src/lib/components/ActBlock.svelte -->
<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';
    import { CONFLICT_COLORS } from '$lib/constants';

    let {
        act,
        top,
        height,
        isPicked,
        conflictLevel,
        onToggle,
        onDetail,
    }: {
        act: ActSummary;
        top: number;
        height: number;
        isPicked: boolean;
        conflictLevel: ConflictLevel;
        onToggle: () => void;
        onDetail: () => void;
    } = $props();

    let borderColor = $derived(
        isPicked ? CONFLICT_COLORS[conflictLevel] : 'transparent'
    );
</script>

<div
    class="absolute left-0 right-0 mx-1 rounded-md border-2 overflow-hidden cursor-pointer
           bg-surface-100-800-token hover:bg-surface-200-700-token transition-colors text-xs"
    style="top: {top}px; height: {height}px; border-color: {borderColor};"
    role="button"
    tabindex="0"
    onclick={onDetail}
    onkeydown={(e) => e.key === 'Enter' && onDetail()}
>
    <div class="p-1 h-full flex flex-col">
        <div class="flex items-start gap-1">
            <input
                type="checkbox"
                checked={isPicked}
                class="mt-0.5 shrink-0"
                onclick|stopPropagation={onToggle}
            />
            <span class="font-semibold leading-tight line-clamp-2">{act.name}</span>
        </div>
        {#if height > 50}
            <span class="opacity-60 mt-auto">
                {act.start}–{act.end}
            </span>
        {/if}
    </div>
</div>
```

- [ ] **Step 3: Implement ScheduleGrid**

```svelte
<!-- ui/src/lib/components/ScheduleGrid.svelte -->
<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';
    import { PIXELS_PER_MINUTE, GRID_START_HOUR, GRID_END_HOUR } from '$lib/constants';
    import { timeToMinutes, getWorstConflict } from '$lib/conflict';
    import ActBlock from './ActBlock.svelte';

    let {
        acts,
        picks,
        onTogglePick,
        onActDetail,
    }: {
        acts: ActSummary[];
        picks: Set<string>;
        onTogglePick: (slug: string) => void;
        onActDetail: (slug: string) => void;
    } = $props();

    const MINUTES_PER_HOUR = 60;
    const gridStartMinutes = GRID_START_HOUR * MINUTES_PER_HOUR;
    const gridEndMinutes = GRID_END_HOUR * MINUTES_PER_HOUR;
    const gridHeight = (gridEndMinutes - gridStartMinutes) * PIXELS_PER_MINUTE;

    let stages = $derived.by(() => {
        const seen = new Set<string>();
        const ordered: string[] = [];
        for (const act of acts) {
            if (!seen.has(act.stage)) {
                seen.add(act.stage);
                ordered.push(act.stage);
            }
        }
        return ordered;
    });

    let actsByStage = $derived.by(() => {
        const map = new Map<string, ActSummary[]>();
        for (const act of acts) {
            const list = map.get(act.stage) ?? [];
            list.push(act);
            map.set(act.stage, list);
        }
        return map;
    });

    function actTop(act: ActSummary): number {
        return (timeToMinutes(act.start) - gridStartMinutes) * PIXELS_PER_MINUTE;
    }

    function actHeight(act: ActSummary): number {
        return (timeToMinutes(act.end) - timeToMinutes(act.start)) * PIXELS_PER_MINUTE;
    }

    function conflictFor(act: ActSummary): ConflictLevel {
        if (!picks.has(act.slug)) return 'none';
        return getWorstConflict(act, acts, picks);
    }

    const HALF_HOUR_MINUTES = 30;
    let timeLabels = $derived.by(() => {
        const labels: { minutes: number; label: string }[] = [];
        for (let m = gridStartMinutes; m < gridEndMinutes; m += HALF_HOUR_MINUTES) {
            const h = Math.floor(m / MINUTES_PER_HOUR);
            const mm = m % MINUTES_PER_HOUR;
            const suffix = h >= 12 ? 'PM' : 'AM';
            const h12 = h > 12 ? h - 12 : h === 0 ? 12 : h;
            labels.push({
                minutes: m,
                label: mm === 0 ? `${h12} ${suffix}` : `${h12}:${String(mm).padStart(2, '0')}`,
            });
        }
        return labels;
    });
</script>

<div class="flex overflow-x-auto">
    <!-- Time labels column -->
    <div class="sticky left-0 z-10 bg-surface-50-900-token w-16 shrink-0 relative"
         style="height: {gridHeight}px;">
        {#each timeLabels as { minutes, label }}
            <div
                class="absolute text-xs text-right pr-2 opacity-60 w-full"
                style="top: {(minutes - gridStartMinutes) * PIXELS_PER_MINUTE}px;"
            >
                {label}
            </div>
        {/each}
    </div>

    <!-- Stage columns -->
    {#each stages as stage}
        <div class="flex flex-col shrink-0" style="min-width: 140px; width: 140px;">
            <!-- Stage header -->
            <div class="sticky top-0 z-20 bg-primary-500 text-white text-xs font-bold
                        p-1 text-center h-16 flex items-center justify-center">
                {stage}
            </div>
            <!-- Act blocks -->
            <div class="relative bg-surface-50-900-token border-r border-surface-300-600-token"
                 style="height: {gridHeight}px;">
                {#each actsByStage.get(stage) ?? [] as act (act.slug)}
                    <ActBlock
                        {act}
                        top={actTop(act)}
                        height={actHeight(act)}
                        isPicked={picks.has(act.slug)}
                        conflictLevel={conflictFor(act)}
                        onToggle={() => onTogglePick(act.slug)}
                        onDetail={() => onActDetail(act.slug)}
                    />
                {/each}
            </div>
        </div>
    {/each}
</div>
```

- [ ] **Step 4: Wire up the main page**

```svelte
<!-- ui/src/routes/+page.svelte -->
<script lang="ts">
    import { onMount } from 'svelte';
    import DayTabs from '$lib/components/DayTabs.svelte';
    import ScheduleGrid from '$lib/components/ScheduleGrid.svelte';
    import { appState } from '$lib/stores.svelte';
    import { listActs, getAct } from '$lib/api';
    import type { ActSummary, ActDetail } from '$lib/types';

    let acts = $state<ActSummary[]>([]);
    let selectedActDetail = $state<ActDetail | null>(null);
    let showDetail = $state(false);

    async function loadActs() {
        appState.loading = true;
        try {
            const resp = await listActs({ date: appState.selectedDate });
            acts = resp.acts;
        } finally {
            appState.loading = false;
        }
    }

    async function handleActDetail(slug: string) {
        selectedActDetail = await getAct(slug);
        showDetail = true;
    }

    function handleTogglePick(slug: string) {
        appState.togglePick(slug);
    }

    onMount(() => { loadActs(); });

    $effect(() => {
        // Re-fetch when day changes
        appState.selectedDate;
        loadActs();
    });
</script>

<div class="p-4 space-y-4">
    <DayTabs bind:selectedDate={appState.selectedDate} />

    {#if appState.loading}
        <div class="text-center p-8">Loading...</div>
    {:else}
        <ScheduleGrid
            {acts}
            picks={appState.picks}
            onTogglePick={handleTogglePick}
            onActDetail={handleActDetail}
        />
    {/if}
</div>

{#if showDetail && selectedActDetail}
    <!-- Act detail overlay — implemented in Task 11 -->
    <div class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
         onclick={() => (showDetail = false)}
         role="dialog">
        <div class="card p-6 max-w-lg w-full max-h-[80vh] overflow-y-auto"
             onclick|stopPropagation>
            <h2 class="h3 mb-2">{selectedActDetail.name}</h2>
            <span class="badge variant-filled-primary">{selectedActDetail.genre}</span>
            <p class="mt-4 whitespace-pre-line">{selectedActDetail.about || 'No bio available yet.'}</p>
            <div class="mt-4 text-sm opacity-60">
                {selectedActDetail.stage} &middot;
                {selectedActDetail.start}–{selectedActDetail.end}
            </div>
            <button class="btn variant-ghost mt-4" onclick={() => (showDetail = false)}>Close</button>
        </div>
    </div>
{/if}
```

- [ ] **Step 5: Verify grid renders**

Run: Start both backend and frontend dev servers.
- Backend: `uv run uvicorn fqf.api.app:create_app --factory --reload --port 8000`
- Frontend: `pnpm --dir ui dev`

Navigate to `http://localhost:5173`. Verify:
- Day tabs are visible and clickable
- Grid shows stages as columns with act blocks positioned by time
- Clicking a checkbox toggles pick state
- Clicking an act name opens the detail overlay

- [ ] **Step 6: Commit**

```
feat: desktop schedule grid with day tabs and act blocks
```

---

### Task 11: Mobile View

**Files:**
- Create: `ui/src/lib/components/MobileSchedule.svelte`
- Modify: `ui/src/routes/+page.svelte`

- [ ] **Step 1: Implement MobileSchedule component**

```svelte
<!-- ui/src/lib/components/MobileSchedule.svelte -->
<script lang="ts">
    import type { ActSummary, ConflictLevel, MobileSortMode } from '$lib/types';
    import { getWorstConflict } from '$lib/conflict';
    import { CONFLICT_COLORS } from '$lib/constants';

    let {
        acts,
        picks,
        sortMode,
        onTogglePick,
        onActDetail,
    }: {
        acts: ActSummary[];
        picks: Set<string>;
        sortMode: MobileSortMode;
        onTogglePick: (slug: string) => void;
        onActDetail: (slug: string) => void;
    } = $props();

    type GroupedActs = { label: string; acts: ActSummary[] }[];

    let grouped = $derived.by((): GroupedActs => {
        if (sortMode === 'by-stage') {
            const map = new Map<string, ActSummary[]>();
            for (const act of acts) {
                const list = map.get(act.stage) ?? [];
                list.push(act);
                map.set(act.stage, list);
            }
            return [...map.entries()].map(([stage, stageActs]) => ({
                label: stage,
                acts: stageActs.sort((a, b) => a.start.localeCompare(b.start)),
            }));
        }
        // by-time: group by half-hour slots
        const SLOT_MINUTES = 30;
        const MINUTES_PER_HOUR = 60;
        const sorted = [...acts].sort((a, b) => a.start.localeCompare(b.start));
        const map = new Map<string, ActSummary[]>();
        for (const act of sorted) {
            const [h, m] = act.start.split(':').map(Number);
            const slot = Math.floor((h * MINUTES_PER_HOUR + m) / SLOT_MINUTES) * SLOT_MINUTES;
            const slotH = Math.floor(slot / MINUTES_PER_HOUR);
            const slotM = slot % MINUTES_PER_HOUR;
            const suffix = slotH >= 12 ? 'PM' : 'AM';
            const h12 = slotH > 12 ? slotH - 12 : slotH;
            const label = `${h12}:${String(slotM).padStart(2, '0')} ${suffix}`;
            const list = map.get(label) ?? [];
            list.push(act);
            map.set(label, list);
        }
        return [...map.entries()].map(([label, slotActs]) => ({ label, acts: slotActs }));
    });

    function conflictFor(act: ActSummary): ConflictLevel {
        if (!picks.has(act.slug)) return 'none';
        return getWorstConflict(act, acts, picks);
    }

    function borderStyle(act: ActSummary): string {
        const level = conflictFor(act);
        if (!picks.has(act.slug)) return 'border-transparent';
        return `border-color: ${CONFLICT_COLORS[level]}`;
    }
</script>

<div class="space-y-6">
    {#each grouped as group}
        <div>
            <h3 class="h4 sticky top-0 bg-surface-50-900-token py-2 z-10 border-b border-surface-300-600-token">
                {group.label}
            </h3>
            <div class="space-y-2 mt-2">
                {#each group.acts as act (act.slug)}
                    <div
                        class="card p-3 border-l-4 flex items-start gap-3"
                        style={borderStyle(act)}
                    >
                        <input
                            type="checkbox"
                            checked={picks.has(act.slug)}
                            class="mt-1 shrink-0"
                            onchange={() => onTogglePick(act.slug)}
                        />
                        <div class="flex-1 min-w-0">
                            <button
                                class="font-semibold text-left hover:underline"
                                onclick={() => onActDetail(act.slug)}
                            >
                                {act.name}
                            </button>
                            <div class="text-sm opacity-70">
                                {act.stage}
                            </div>
                            <div class="text-sm opacity-50">
                                {act.start}–{act.end} &middot; {act.genre}
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    {/each}
</div>
```

- [ ] **Step 2: Add responsive view switching to main page**

Update `+page.svelte` to detect screen width and switch between grid and mobile views. Add a sort mode toggle for mobile.

```svelte
<!-- Add to +page.svelte <script> -->
    import MobileSchedule from '$lib/components/MobileSchedule.svelte';

    const MOBILE_BREAKPOINT = 768;
    let innerWidth = $state(0);
    let isMobile = $derived(innerWidth < MOBILE_BREAKPOINT);
```

```svelte
<!-- Add to +page.svelte template -->
<svelte:window bind:innerWidth />

<!-- Replace the grid section with: -->
{#if appState.loading}
    <div class="text-center p-8">Loading...</div>
{:else if isMobile}
    <div class="flex gap-2 mb-4">
        <button
            class="btn btn-sm"
            class:variant-filled-primary={appState.mobileSortMode === 'by-time'}
            class:variant-ghost={appState.mobileSortMode !== 'by-time'}
            onclick={() => (appState.mobileSortMode = 'by-time')}
        >By Time</button>
        <button
            class="btn btn-sm"
            class:variant-filled-primary={appState.mobileSortMode === 'by-stage'}
            class:variant-ghost={appState.mobileSortMode !== 'by-stage'}
            onclick={() => (appState.mobileSortMode = 'by-stage')}
        >By Stage</button>
    </div>
    <MobileSchedule
        {acts}
        picks={appState.picks}
        sortMode={appState.mobileSortMode}
        onTogglePick={handleTogglePick}
        onActDetail={handleActDetail}
    />
{:else}
    <ScheduleGrid ... />
{/if}
```

- [ ] **Step 3: Test on mobile viewport**

Open browser dev tools, toggle device toolbar (responsive mode). Verify:
- Below 768px, the mobile list view appears
- By-time and by-stage toggles work
- Checkboxes toggle with conflict colors
- Act names open the detail overlay

- [ ] **Step 4: Commit**

```
feat: responsive mobile schedule view with time/stage sort modes
```

---

### Task 12: Selection + Token Flow

**Files:**
- Create: `ui/src/lib/components/TokenDialog.svelte`
- Modify: `ui/src/lib/stores.svelte.ts`
- Modify: `ui/src/routes/+layout.svelte`

- [ ] **Step 1: Implement TokenDialog**

```svelte
<!-- ui/src/lib/components/TokenDialog.svelte -->
<script lang="ts">
    import { createSchedule, loadSchedule, savePicks } from '$lib/api';
    import { appState } from '$lib/stores.svelte';

    let {
        open = $bindable(),
    }: {
        open: boolean;
    } = $props();

    let mode = $state<'choose' | 'create' | 'load'>('choose');
    let inputToken = $state('');
    let error = $state('');
    let loading = $state(false);
    let newToken = $state('');

    async function handleCreate() {
        loading = true;
        error = '';
        try {
            const resp = await createSchedule();
            newToken = resp.token;
            appState.token = resp.token;
            appState.clearPicks();
            mode = 'create';
        } catch (e) {
            error = 'Failed to create schedule. Try again.';
        } finally {
            loading = false;
        }
    }

    async function handleLoad() {
        if (!inputToken.trim()) return;
        loading = true;
        error = '';
        try {
            const resp = await loadSchedule(inputToken.trim());
            appState.token = resp.token;
            appState.picks = new Set(resp.picks);
            open = false;
        } catch {
            error = 'Schedule not found. Check your secret words.';
        } finally {
            loading = false;
        }
    }

    function handleClose() {
        open = false;
        mode = 'choose';
        error = '';
        inputToken = '';
        newToken = '';
    }
</script>

{#if open}
    <div class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
         onclick={handleClose}
         role="dialog">
        <div class="card p-6 max-w-md w-full space-y-4"
             onclick|stopPropagation>

            {#if mode === 'choose'}
                <h2 class="h3">Your Schedule</h2>
                <p class="opacity-70">Create a new schedule or load an existing one with your secret words.</p>
                <div class="flex flex-col gap-3">
                    <button class="btn variant-filled-primary" onclick={handleCreate} disabled={loading}>
                        New Schedule
                    </button>
                    <button class="btn variant-ghost" onclick={() => (mode = 'load')}>
                        I Have Secret Words
                    </button>
                </div>

            {:else if mode === 'create'}
                <h2 class="h3">Your Secret Words</h2>
                <p>Remember these words to access your schedule later:</p>
                <div class="text-2xl font-bold text-center p-4 bg-primary-500/10 rounded-lg">
                    {newToken}
                </div>
                <p class="text-sm opacity-60">
                    Anyone with these words can view and edit this schedule.
                </p>
                <button class="btn variant-filled-primary w-full" onclick={handleClose}>
                    Got It
                </button>

            {:else}
                <h2 class="h3">Enter Your Secret Words</h2>
                <input
                    type="text"
                    class="input"
                    placeholder="e.g. treme-funky-crawfish"
                    bind:value={inputToken}
                    onkeydown={(e) => e.key === 'Enter' && handleLoad()}
                />
                {#if error}
                    <p class="text-error-500 text-sm">{error}</p>
                {/if}
                <div class="flex gap-2">
                    <button class="btn variant-ghost" onclick={() => (mode = 'choose')}>Back</button>
                    <button class="btn variant-filled-primary flex-1" onclick={handleLoad} disabled={loading}>
                        Load Schedule
                    </button>
                </div>
            {/if}
        </div>
    </div>
{/if}
```

- [ ] **Step 2: Add auto-save to stores**

Extend `AppState` in `stores.svelte.ts` to debounce-save picks when they change:

```typescript
// Add to stores.svelte.ts AppState class

    private _saveTimeout: ReturnType<typeof setTimeout> | null = null;
    private SAVE_DEBOUNCE_MS = 1000;

    scheduleSave(): void {
        if (!this.token) return;
        if (this._saveTimeout) clearTimeout(this._saveTimeout);
        this._saveTimeout = setTimeout(async () => {
            if (this.token) {
                const { savePicks } = await import('$lib/api');
                await savePicks(this.token, this.picksArray);
            }
        }, this.SAVE_DEBOUNCE_MS);
    }

    // Update togglePick to trigger save
    togglePick(slug: string): void {
        const next = new Set(this.picks);
        if (next.has(slug)) {
            next.delete(slug);
        } else {
            next.add(slug);
        }
        this.picks = next;
        this.scheduleSave();
    }
```

- [ ] **Step 3: Add token display and dialog trigger to layout**

Update `+layout.svelte` to show the current token in the AppBar and a button to open the TokenDialog:

```svelte
<!-- Add to +layout.svelte -->
<script lang="ts">
    import TokenDialog from '$lib/components/TokenDialog.svelte';
    import { appState } from '$lib/stores.svelte';

    let showTokenDialog = $state(false);
</script>

<!-- In AppBar trail slot -->
<svelte:fragment slot="trail">
    {#if appState.token}
        <span class="badge variant-soft-primary">{appState.token}</span>
    {/if}
    <button class="btn btn-sm variant-ghost" onclick={() => (showTokenDialog = true)}>
        {appState.token ? 'Switch' : 'My Schedule'}
    </button>
</svelte:fragment>

<!-- After the main content -->
<TokenDialog bind:open={showTokenDialog} />
```

- [ ] **Step 4: Verify token flow end-to-end**

This requires a running Neon database. Set `DATABASE_URL` in a `.env` file and start the backend with it loaded. Verify:
1. Click "My Schedule" → dialog opens
2. Click "New Schedule" → three-word token appears
3. Close dialog, select some acts, wait 1 second
4. Refresh page, re-enter the token → picks are restored

- [ ] **Step 5: Commit**

```
feat: token-based schedule persistence with auto-save
```

---

### Task 13: My Schedule View

**Files:**
- Create: `ui/src/lib/components/MySchedule.svelte`
- Modify: `ui/src/routes/+page.svelte`

- [ ] **Step 1: Implement MySchedule component**

```svelte
<!-- ui/src/lib/components/MySchedule.svelte -->
<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';
    import { DAY_LABELS } from '$lib/types';
    import { getWorstConflict } from '$lib/conflict';
    import { CONFLICT_COLORS } from '$lib/constants';

    let {
        allActs,
        picks,
        onTogglePick,
        onActDetail,
    }: {
        allActs: ActSummary[];
        picks: Set<string>;
        onTogglePick: (slug: string) => void;
        onActDetail: (slug: string) => void;
    } = $props();

    let pickedActs = $derived(
        allActs
            .filter((a) => picks.has(a.slug))
            .sort((a, b) => a.date.localeCompare(b.date) || a.start.localeCompare(b.start))
    );

    type DayGroup = { date: string; label: string; acts: ActSummary[] };

    let grouped = $derived.by((): DayGroup[] => {
        const map = new Map<string, ActSummary[]>();
        for (const act of pickedActs) {
            const list = map.get(act.date) ?? [];
            list.push(act);
            map.set(act.date, list);
        }
        return [...map.entries()].map(([date, acts]) => ({
            date,
            label: DAY_LABELS[date] ?? date,
            acts,
        }));
    });

    function conflictFor(act: ActSummary): ConflictLevel {
        return getWorstConflict(act, allActs, picks);
    }
</script>

{#if pickedActs.length === 0}
    <div class="text-center p-12 opacity-60">
        <p class="text-lg">No acts selected yet.</p>
        <p>Switch to the grid view and check off acts you want to see.</p>
    </div>
{:else}
    <div class="space-y-6">
        {#each grouped as group}
            <div>
                <h3 class="h3 mb-3">{group.label}</h3>
                <div class="space-y-2">
                    {#each group.acts as act (act.slug)}
                        {@const level = conflictFor(act)}
                        <div
                            class="card p-3 border-l-4 flex items-start gap-3"
                            style="border-color: {CONFLICT_COLORS[level]};"
                        >
                            <input
                                type="checkbox"
                                checked={true}
                                class="mt-1 shrink-0"
                                onchange={() => onTogglePick(act.slug)}
                            />
                            <div class="flex-1 min-w-0">
                                <button class="font-semibold text-left hover:underline"
                                        onclick={() => onActDetail(act.slug)}>
                                    {act.name}
                                </button>
                                <div class="text-sm opacity-70">{act.stage}</div>
                                <div class="text-sm opacity-50">
                                    {act.start}–{act.end} &middot; {act.genre}
                                </div>
                            </div>
                            {#if level !== 'none'}
                                <span class="badge text-xs"
                                      style="background-color: {CONFLICT_COLORS[level]}; color: white;">
                                    conflict
                                </span>
                            {/if}
                        </div>
                    {/each}
                </div>
            </div>
        {/each}
    </div>
{/if}
```

- [ ] **Step 2: Add view mode tabs to main page**

Update `+page.svelte` to include a view mode selector (Grid / My Schedule / Merge) above the day tabs:

```svelte
<!-- Add view mode selector -->
<div class="flex gap-2">
    <button class="btn btn-sm"
            class:variant-filled-primary={appState.viewMode === 'grid'}
            class:variant-ghost={appState.viewMode !== 'grid'}
            onclick={() => (appState.viewMode = 'grid')}>
        All Acts
    </button>
    <button class="btn btn-sm"
            class:variant-filled-primary={appState.viewMode === 'my-schedule'}
            class:variant-ghost={appState.viewMode !== 'my-schedule'}
            onclick={() => (appState.viewMode = 'my-schedule')}>
        My Schedule ({appState.picks.size})
    </button>
    <button class="btn btn-sm"
            class:variant-filled-primary={appState.viewMode === 'merge'}
            class:variant-ghost={appState.viewMode !== 'merge'}
            onclick={() => (appState.viewMode = 'merge')}>
        Merge
    </button>
</div>

<!-- Conditional rendering based on viewMode -->
{#if appState.viewMode === 'my-schedule'}
    <MySchedule
        {allActs}
        picks={appState.picks}
        onTogglePick={handleTogglePick}
        onActDetail={handleActDetail}
    />
{:else if appState.viewMode === 'merge'}
    <!-- Merge view — Task 14 -->
{:else}
    <!-- Grid or Mobile view -->
{/if}
```

**Note:** The My Schedule view needs acts for ALL days (not just the selected day). Load all acts when switching to this view, or maintain a full-schedule cache.

- [ ] **Step 3: Verify My Schedule view**

Verify:
- Selecting acts in grid view, then switching to My Schedule shows them grouped by day
- Conflict badges appear when overlapping acts are picked
- Unchecking an act in My Schedule removes it from picks

- [ ] **Step 4: Commit**

```
feat: my-schedule view with conflict indicators
```

---

### Task 14: Merge View

**Files:**
- Create: `ui/src/lib/emoji-mapper.ts`
- Create: `ui/src/lib/emoji-mapper.test.ts`
- Create: `ui/src/lib/components/MergeView.svelte`
- Modify: `ui/src/routes/+page.svelte`

- [ ] **Step 1: Write emoji mapper tests**

```typescript
// ui/src/lib/emoji-mapper.test.ts

import { describe, it, expect } from 'vitest';
import { assignEmojis } from '$lib/emoji-mapper';

describe('assignEmojis', () => {
    it('assigns unique emojis to each token', () => {
        const result = assignEmojis(['token-a', 'token-b']);
        const emojis = Object.values(result);
        expect(new Set(emojis).size).toBe(2);
    });

    it('is deterministic for same set of tokens', () => {
        const a = assignEmojis(['token-a', 'token-b']);
        const b = assignEmojis(['token-a', 'token-b']);
        expect(a).toEqual(b);
    });

    it('is deterministic regardless of input order', () => {
        const a = assignEmojis(['token-a', 'token-b']);
        const b = assignEmojis(['token-b', 'token-a']);
        expect(a).toEqual(b);
    });

    it('handles up to 5 tokens', () => {
        const tokens = ['a', 'b', 'c', 'd', 'e'];
        const result = assignEmojis(tokens);
        expect(Object.keys(result).length).toBe(5);
        expect(new Set(Object.values(result)).size).toBe(5);
    });
});
```

- [ ] **Step 2: Implement emoji mapper**

```typescript
// ui/src/lib/emoji-mapper.ts

const MERGE_EMOJIS = ['🐊', '🎺', '🦞', '⚜️', '🎭', '🌶️', '🥁', '🦜'] as const;

export function assignEmojis(tokens: string[]): Record<string, string> {
    const sorted = [...tokens].sort();
    const result: Record<string, string> = {};
    for (let i = 0; i < sorted.length; i++) {
        result[sorted[i]] = MERGE_EMOJIS[i % MERGE_EMOJIS.length];
    }
    return result;
}
```

- [ ] **Step 3: Run emoji mapper tests — verify they pass**

Run: `pnpm --dir ui test -- --run src/lib/emoji-mapper.test.ts`
Expected: All tests PASS.

- [ ] **Step 4: Implement MergeView component**

```svelte
<!-- ui/src/lib/components/MergeView.svelte -->
<script lang="ts">
    import type { ActSummary, ConflictLevel, MergeEntry } from '$lib/types';
    import { DAY_LABELS } from '$lib/types';
    import { mergeSchedules } from '$lib/api';
    import { assignEmojis } from '$lib/emoji-mapper';
    import { getWorstConflict } from '$lib/conflict';
    import { CONFLICT_COLORS, MAX_MERGE_TOKENS } from '$lib/constants';
    import { appState } from '$lib/stores.svelte';

    let tokenInput = $state('');
    let mergeTokens = $state<string[]>([]);
    let schedules = $state<MergeEntry[]>([]);
    let mergedActs = $state<ActSummary[]>([]);
    let emojiMap = $state<Record<string, string>>({});
    let error = $state('');
    let loading = $state(false);

    // Auto-include current user's token
    $effect(() => {
        if (appState.token && !mergeTokens.includes(appState.token)) {
            mergeTokens = [appState.token, ...mergeTokens];
        }
    });

    async function addToken() {
        const token = tokenInput.trim();
        if (!token) return;
        if (mergeTokens.includes(token)) {
            error = 'Token already added.';
            return;
        }
        if (mergeTokens.length >= MAX_MERGE_TOKENS) {
            error = `Maximum ${MAX_MERGE_TOKENS} schedules.`;
            return;
        }
        mergeTokens = [...mergeTokens, token];
        tokenInput = '';
        error = '';
        await loadMerge();
    }

    function removeToken(token: string) {
        mergeTokens = mergeTokens.filter((t) => t !== token);
        if (mergeTokens.length > 0) loadMerge();
        else { schedules = []; mergedActs = []; }
    }

    async function loadMerge() {
        if (mergeTokens.length === 0) return;
        loading = true;
        try {
            const resp = await mergeSchedules(mergeTokens);
            schedules = resp.schedules;
            mergedActs = resp.acts;
            emojiMap = assignEmojis(mergeTokens);
        } catch {
            error = 'Failed to load schedules.';
        } finally {
            loading = false;
        }
    }

    let allPicks = $derived(
        new Set(schedules.flatMap((s) => s.picks))
    );

    function pickersFor(slug: string): string[] {
        return schedules
            .filter((s) => s.picks.includes(slug))
            .map((s) => emojiMap[s.token] ?? '?');
    }

    let sortedActs = $derived(
        [...mergedActs].sort((a, b) =>
            a.date.localeCompare(b.date) || a.start.localeCompare(b.start)
        )
    );

    type DayGroup = { date: string; label: string; acts: ActSummary[] };

    let grouped = $derived.by((): DayGroup[] => {
        const map = new Map<string, ActSummary[]>();
        for (const act of sortedActs) {
            const list = map.get(act.date) ?? [];
            list.push(act);
            map.set(act.date, list);
        }
        return [...map.entries()].map(([date, acts]) => ({
            date,
            label: DAY_LABELS[date] ?? date,
            acts,
        }));
    });

    function conflictFor(act: ActSummary): ConflictLevel {
        return getWorstConflict(act, mergedActs, allPicks);
    }
</script>

<div class="space-y-4">
    <!-- Token management -->
    <div class="card p-4 space-y-3">
        <h3 class="h4">Merge Schedules</h3>
        <div class="flex flex-wrap gap-2">
            {#each mergeTokens as token}
                <span class="badge variant-soft-primary flex items-center gap-1">
                    {emojiMap[token] ?? ''} {token}
                    <button class="ml-1 opacity-60 hover:opacity-100" onclick={() => removeToken(token)}>×</button>
                </span>
            {/each}
        </div>
        <div class="flex gap-2">
            <input
                type="text"
                class="input flex-1"
                placeholder="Enter a friend's secret words"
                bind:value={tokenInput}
                onkeydown={(e) => e.key === 'Enter' && addToken()}
            />
            <button class="btn variant-filled-primary" onclick={addToken} disabled={loading}>
                Add
            </button>
        </div>
        {#if error}
            <p class="text-error-500 text-sm">{error}</p>
        {/if}
    </div>

    <!-- Merged schedule display -->
    {#if loading}
        <div class="text-center p-8">Loading...</div>
    {:else if sortedActs.length === 0}
        <p class="text-center opacity-60 p-8">Add schedule tokens above to see merged picks.</p>
    {:else}
        <div class="space-y-6">
            {#each grouped as group}
                <div>
                    <h3 class="h3 mb-3">{group.label}</h3>
                    <div class="space-y-2">
                        {#each group.acts as act (act.slug)}
                            {@const level = conflictFor(act)}
                            {@const pickers = pickersFor(act.slug)}
                            <div
                                class="card p-3 border-l-4 flex items-start gap-3"
                                style="border-color: {CONFLICT_COLORS[level]};"
                            >
                                <div class="flex-1 min-w-0">
                                    <div class="flex items-center gap-2">
                                        <span class="font-semibold">{act.name}</span>
                                        <span class="text-lg">{pickers.join(' ')}</span>
                                    </div>
                                    <div class="text-sm opacity-70">{act.stage}</div>
                                    <div class="text-sm opacity-50">
                                        {act.start}–{act.end} &middot; {act.genre}
                                    </div>
                                </div>
                                {#if level !== 'none'}
                                    <span class="badge text-xs"
                                          style="background-color: {CONFLICT_COLORS[level]}; color: white;">
                                        conflict
                                    </span>
                                {/if}
                            </div>
                        {/each}
                    </div>
                </div>
            {/each}
        </div>

        <!-- Legend -->
        <div class="card p-3 flex flex-wrap gap-4 text-sm">
            {#each schedules as s}
                <span>{emojiMap[s.token]} {s.token}</span>
            {/each}
        </div>
    {/if}
</div>
```

- [ ] **Step 5: Wire merge view into main page**

Update the `+page.svelte` merge section to render the `MergeView` component.

- [ ] **Step 6: Verify merge flow**

Create two schedules with different tokens, pick different acts in each. Enter both tokens in the merge view. Verify:
- Both tokens appear with unique emojis
- All picked acts from both schedules appear
- Emoji badges show who picked what
- Conflict coloring reflects the union of all picks

- [ ] **Step 7: Commit**

```
feat: merge view with emoji badges for multi-schedule comparison
```

---

### Task 15: Filter Stubs

**Files:**
- Create: `ui/src/lib/components/FilterPanel.svelte`
- Modify: `ui/src/lib/stores.svelte.ts`
- Modify: `ui/src/routes/+page.svelte`

- [ ] **Step 1: Add filter state to stores**

```typescript
// Add to stores.svelte.ts AppState class

    hiddenGenres = $state<Set<string>>(new Set());
    hiddenStages = $state<Set<string>>(new Set());
    showAll = $state<boolean>(false);

    toggleGenre(genre: string): void {
        const next = new Set(this.hiddenGenres);
        if (next.has(genre)) next.delete(genre);
        else next.add(genre);
        this.hiddenGenres = next;
    }

    toggleStage(stage: string): void {
        const next = new Set(this.hiddenStages);
        if (next.has(stage)) next.delete(stage);
        else next.add(stage);
        this.hiddenStages = next;
    }

    isActVisible(act: { genre: string; stage: string }): boolean {
        if (this.showAll) return true;
        if (this.hiddenGenres.has(act.genre)) return false;
        if (this.hiddenStages.has(act.stage)) return false;
        return true;
    }
```

- [ ] **Step 2: Implement FilterPanel**

```svelte
<!-- ui/src/lib/components/FilterPanel.svelte -->
<script lang="ts">
    import { appState } from '$lib/stores.svelte';

    let { genres, stages }: { genres: string[]; stages: string[] } = $props();

    let showFilters = $state(false);
</script>

<div class="card p-3">
    <div class="flex items-center justify-between">
        <button class="btn btn-sm variant-ghost" onclick={() => (showFilters = !showFilters)}>
            Filters {showFilters ? '▲' : '▼'}
        </button>
        <label class="flex items-center gap-2 text-sm">
            <input type="checkbox" bind:checked={appState.showAll} />
            Show All
        </label>
    </div>

    {#if showFilters}
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
            <div>
                <h4 class="font-semibold text-sm mb-2">Genres</h4>
                <div class="space-y-1 max-h-48 overflow-y-auto">
                    {#each genres as genre}
                        <label class="flex items-center gap-2 text-sm">
                            <input
                                type="checkbox"
                                checked={!appState.hiddenGenres.has(genre)}
                                onchange={() => appState.toggleGenre(genre)}
                            />
                            {genre}
                        </label>
                    {/each}
                </div>
            </div>
            <div>
                <h4 class="font-semibold text-sm mb-2">Stages</h4>
                <div class="space-y-1 max-h-48 overflow-y-auto">
                    {#each stages as stage}
                        <label class="flex items-center gap-2 text-sm">
                            <input
                                type="checkbox"
                                checked={!appState.hiddenStages.has(stage)}
                                onchange={() => appState.toggleStage(stage)}
                            />
                            {stage}
                        </label>
                    {/each}
                </div>
            </div>
        </div>
    {/if}
</div>
```

- [ ] **Step 3: Wire filter panel into page and apply filtering**

Add `FilterPanel` above the grid. Filter the acts passed to the grid/mobile/my-schedule components using `appState.isActVisible()`.

**Note:** The filter is purely client-side — it hides/shows acts already loaded. No API changes needed. The "Show All" checkbox temporarily bypasses all filters.

- [ ] **Step 4: Commit**

```
feat: filter panel stubs for genre and stage filtering
```

---

## Phase 5: Infrastructure

### Task 16: Docker

**Files:**
- Create: `Dockerfile`

- [ ] **Step 1: Create multi-stage Dockerfile**

```dockerfile
# ── Stage 1: Build frontend ──────────────────────────────────────────
FROM node:22-slim AS frontend

WORKDIR /app/ui
RUN corepack enable && corepack prepare pnpm@latest --activate

COPY ui/package.json ui/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY ui/ ./
RUN pnpm build

# ── Stage 2: Build backend + bundle ──────────────────────────────────
FROM python:3.11-slim AS backend

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./
COPY src/ ./src/

# Copy built frontend into static directory
COPY --from=frontend /app/ui/build ./src/fqf/static/

RUN uv pip install --system .

EXPOSE 8000

CMD ["uvicorn", "fqf.api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 2: Update app.py to serve static files**

Add a static file mount to `create_app()` in `src/fqf/api/app.py`:

```python
import importlib.resources
from pathlib import Path
from fastapi.staticfiles import StaticFiles

# Inside create_app(), after router includes:
static_dir = Path(__file__).parent.parent / "static"
if static_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
```

**Note:** The static mount must be the LAST mount, after all API routers, because it catches all remaining paths.

- [ ] **Step 3: Verify Docker build**

Run: `make build-image`
Expected: Image builds successfully.

Run: `docker run --rm -p 8000:8000 -e DATABASE_URL=<neon-url> fqf:local`
Expected: App serves both API and frontend on port 8000.

- [ ] **Step 4: Commit**

```
feat: multi-stage Dockerfile serving API and static frontend
```

---

### Task 17: CI/CD

**Files:**
- Create: `.github/workflows/ci.yml`
- Create: `.github/workflows/deploy.yml`

- [ ] **Step 1: Create CI workflow**

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_call:

jobs:
  test-api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --all-extras --frozen
      - run: uv run pytest

  test-ui:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm
          cache-dependency-path: ui/pnpm-lock.yaml
      - run: pnpm --dir ui install --frozen-lockfile
      - run: pnpm --dir ui test

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --all-extras --frozen
      - run: uv run black --check src tests
      - run: uv run isort --check src tests
      - run: uv run mypy src
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm
          cache-dependency-path: ui/pnpm-lock.yaml
      - run: pnpm --dir ui install --frozen-lockfile
      - run: pnpm --dir ui lint
```

- [ ] **Step 2: Create deploy workflow**

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    tags: ['v*']

jobs:
  ci:
    uses: ./.github/workflows/ci.yml

  deploy:
    needs: ci
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Extract version
        id: version
        run: echo "version=${GITHUB_REF_NAME#v}" >> $GITHUB_OUTPUT

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GHCR_PAT }}

      - name: Login to GCP Artifact Registry
        uses: docker/login-action@v3
        with:
          registry: us-docker.pkg.dev
          username: _json_key
          password: ${{ secrets.GCP_SA_KEY }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ steps.version.outputs.version }}
            ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Deploy to Cloud Run
        uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      - name: Deploy service
        run: |
          gcloud run deploy fqf \
            --image ghcr.io/${{ github.repository }}:${{ steps.version.outputs.version }} \
            --region us-central1 \
            --project ${{ secrets.GCP_PROJECT }} \
            --memory 512Mi \
            --cpu 1 \
            --min-instances 0 \
            --max-instances 3 \
            --port 8000 \
            --allow-unauthenticated \
            --set-env-vars "DATABASE_URL=${{ secrets.DATABASE_URL }}"
```

- [ ] **Step 3: Commit**

```
feat: GitHub Actions CI/CD workflows for test, lint, and deploy
```

---

## Post-Implementation: Enrichment

After all the above tasks are complete and the full stack is working, the **artist enrichment** effort can begin as a separate workstream. It involves:

1. Adding `genre` and `about` values to each Act in the schedule data files
2. Following the research strategy in CLAUDE.md (WWOZ first, then other sources)
3. Working through acts in batches (by stage or by day)
4. Lower priority for Schoolhouse Stage (school groups) and some HOB Voodoo Garden acts
5. Using `about_source = AboutSource.GENERATED` for acts with no research sources

This is intentionally excluded from this plan because it's a long-running research task, not a code architecture task.

---

## Date Corrections

The existing `fqf2026.py` has incorrect date comments. The correct festival dates are:

| Day | Date | Existing Comment | Correct Comment |
|-----|------|-----------------|-----------------|
| Thursday | April 16 | "THURSDAY April 17" | "Thursday April 16" |
| Friday | April 17 | "FRIDAY April 18" | "Friday April 17" |
| Saturday | April 18 | "SATURDAY April 19" | "Saturday April 18" |
| Sunday | April 19 | "SUNDAY April 20" | "Sunday April 19" |

The date constants (`THU`, `FRI`, `SAT`, `SUN`) are already correct. Only the comments need fixing during the migration in Task 3.
