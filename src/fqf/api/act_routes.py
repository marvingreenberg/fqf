"""Act-related API endpoints."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from fqf.api.schemas import ActDetail, ActListResponse, ActSummary
from fqf.models import Act
from fqf.schedule import SCHEDULE, get_by_slug, on, search

router = APIRouter(prefix="/api/v1/acts", tags=["acts"])

NOT_FOUND_DETAIL = "Act not found"


def _to_summary(act: Act) -> ActSummary:
    return ActSummary(
        slug=act.slug,
        name=act.name,
        stage=act.stage,
        date=act.date,
        start=act.start,
        end=act.end,
        genre=act.genre,
    )


def _to_detail(act: Act) -> ActDetail:
    return ActDetail(
        slug=act.slug,
        name=act.name,
        stage=act.stage,
        date=act.date,
        start=act.start,
        end=act.end,
        genre=act.genre,
        about=act.about,
        about_source=act.about_source,
    )


def _filter_by_stage(acts: list[Act], stage: str) -> list[Act]:
    return [a for a in acts if stage.lower() in a.stage.lower()]


@router.get("", response_model=ActListResponse)
async def list_acts(
    date: date | None = Query(None, alias="date"),
    stage: str | None = Query(None),
    q: str | None = Query(None),
) -> ActListResponse:
    """List acts with optional filtering by date, stage, or search query."""
    if q:
        results = search(q)
    elif date:
        results = on(date, stage=stage)
    else:
        all_acts = sorted(SCHEDULE, key=lambda a: (a.date, a.start))
        results = _filter_by_stage(all_acts, stage) if stage else all_acts
    summaries = [_to_summary(a) for a in results]
    return ActListResponse(acts=summaries, count=len(summaries))


@router.get("/{slug}", response_model=ActDetail)
async def get_act(slug: str) -> ActDetail:
    """Get full act detail by slug."""
    act = get_by_slug(slug)
    if act is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    return _to_detail(act)
