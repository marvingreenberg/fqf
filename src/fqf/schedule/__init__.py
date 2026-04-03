"""Schedule data and query functions."""

# Data source: src/fqf/data/fq2026_acts.yaml, loaded via fqf.schedule.loader.

from datetime import date, time

from fqf.models import STAGE_ORDER, Act
from fqf.schedule.loader import load_schedule

SCHEDULE: list[Act] = load_schedule()

_SLUG_INDEX: dict[str, Act] = {act.slug: act for act in SCHEDULE}


def at(query_date: date, query_time: time) -> list[Act]:
    """Return all acts playing at a given date and time."""
    fallback = len(STAGE_ORDER)
    return sorted(
        [a for a in SCHEDULE if a.date == query_date and a.start <= query_time < a.end],
        key=lambda a: STAGE_ORDER.get(a.stage, fallback),
    )


def search(query: str) -> list[Act]:
    """Case-insensitive substring search across act name, stage, and genre."""
    q = query.lower()
    return sorted(
        [
            a
            for a in SCHEDULE
            if q in a.name.lower() or q in a.stage.lower() or q in a.genre.lower()
        ],
        key=lambda a: (a.date, a.start),
    )


def on(query_date: date, stage: str | None = None) -> list[Act]:
    """Return all acts on a given date, optionally filtered by stage substring."""
    results = [a for a in SCHEDULE if a.date == query_date]
    if stage:
        results = [a for a in results if stage.lower() in a.stage.lower()]
    fallback = len(STAGE_ORDER)
    return sorted(results, key=lambda a: (STAGE_ORDER.get(a.stage, fallback), a.start))


def get_by_slug(slug: str) -> Act | None:
    """Return a single act by its slug, or None."""
    return _SLUG_INDEX.get(slug)
