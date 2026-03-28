"""Schedule persistence API endpoints."""

from fastapi import APIRouter, HTTPException, Query

from fqf.api.schemas import (
    ActSummary,
    MergeEntry,
    MergeResponse,
    ScheduleResponse,
    ScheduleUpdate,
    TokenResponse,
)
from fqf.db import create_schedule, load_multiple_schedules, load_schedule, save_picks
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
        slug=act.slug,
        name=act.name,
        stage=act.stage,
        date=act.date,
        start=act.start,
        end=act.end,
        genre=act.genre,
    )


# IMPORTANT: /merge must be defined before /{token} to avoid "merge" being
# captured as a token path parameter.
@router.get("/merge", response_model=MergeResponse)
async def merge(tokens: str = Query(..., description="Comma-separated tokens")) -> MergeResponse:
    """Merge multiple schedules for comparison."""
    token_list = [t.strip() for t in tokens.split(",") if t.strip()]
    if len(token_list) > MAX_MERGE_TOKENS:
        raise HTTPException(status_code=400, detail=TOO_MANY_TOKENS_DETAIL)

    schedules_map = await load_multiple_schedules(token_list)
    entries = [MergeEntry(token=tok, picks=schedules_map.get(tok, [])) for tok in token_list]

    all_slugs = {slug for picks in schedules_map.values() for slug in picks}
    acts = [s for slug in all_slugs if (s := _slug_to_summary(slug)) is not None]

    return MergeResponse(schedules=entries, acts=acts)


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
