"""Schedule data and query functions."""

from datetime import date, time

from fqf.models import Act
from fqf.schedule.friday import FRIDAY_ACTS
from fqf.schedule.saturday import SATURDAY_ACTS
from fqf.schedule.sunday import SUNDAY_ACTS
from fqf.schedule.thursday import THURSDAY_ACTS

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
    return sorted(results, key=lambda a: (a.stage, a.start))


def get_by_slug(slug: str) -> Act | None:
    """Return a single act by its slug, or None."""
    return _SLUG_INDEX.get(slug)
