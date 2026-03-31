"""Shared helper utilities for API route handlers."""

from fqf.api.schemas import ActSummary
from fqf.models import Act


def to_summary(act: Act) -> ActSummary:
    """Convert an Act model to its summary schema representation."""
    return ActSummary(
        slug=act.slug,
        name=act.name,
        stage=act.stage,
        date=act.date,
        start=act.start,
        end=act.end,
        genre=act.genre,
    )
