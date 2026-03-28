"""Schedule persistence API endpoints."""

from fastapi import APIRouter, HTTPException, Query, Request

from fqf.api.schemas import (
    ActSummary,
    MergeEntry,
    MergeResponse,
    ScheduleResponse,
    ScheduleUpdate,
    SharedScheduleResponse,
    ShareResponse,
    TokenResponse,
)
from fqf.db import (
    create_schedule,
    create_share_id,
    load_multiple_schedules,
    load_schedule,
    load_schedule_by_share,
    save_picks,
)
from fqf.schedule import get_by_slug

router = APIRouter(prefix="/api/v1/schedule", tags=["schedule"])

NOT_FOUND_DETAIL = "Schedule not found"
TOO_MANY_TOKENS_DETAIL = "Too many tokens"
MAX_MERGE_TOKENS = 5

SHARE_PATH_PREFIX = "/s"


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


# IMPORTANT: /merge and /by-share/... must be defined before /{token} to avoid
# those literal path segments being captured as a token parameter.
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


@router.get("/by-share/{share_id}", response_model=SharedScheduleResponse)
async def load_by_share(share_id: str) -> SharedScheduleResponse:
    """Load a read-only schedule view by its share_id."""
    result = await load_schedule_by_share(share_id)
    if result is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    _token, picks, name = result
    acts = [s for slug in picks if (s := _slug_to_summary(slug)) is not None]
    return SharedScheduleResponse(name=name, picks=picks, acts=acts)


@router.post("", response_model=TokenResponse, status_code=201)
async def create() -> TokenResponse:
    """Generate a new schedule with a NOLA-themed token."""
    token = await create_schedule()
    return TokenResponse(token=token)


@router.post("/{token}/share", response_model=ShareResponse)
async def share(token: str, request: Request) -> ShareResponse:
    """Generate (or retrieve) a share_id for a schedule."""
    try:
        share_id = await create_share_id(token)
    except KeyError:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    base_url = str(request.base_url).rstrip("/")
    share_url = f"{base_url}{SHARE_PATH_PREFIX}/{share_id}"
    return ShareResponse(share_id=share_id, share_url=share_url)


@router.get("/{token}", response_model=ScheduleResponse)
async def load(token: str) -> ScheduleResponse:
    """Load a schedule by its token."""
    result = await load_schedule(token)
    if result is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    picks, name = result
    acts = [s for slug in picks if (s := _slug_to_summary(slug)) is not None]
    return ScheduleResponse(token=token, name=name, picks=picks, acts=acts)


@router.put("/{token}", response_model=ScheduleResponse)
async def save(token: str, body: ScheduleUpdate) -> ScheduleResponse:
    """Save picks (and optionally name) for an existing schedule."""
    success = await save_picks(token, body.picks, body.name)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    # Re-fetch name so the response reflects any update
    result = await load_schedule(token)
    name = result[1] if result is not None else (body.name or "")
    acts = [s for slug in body.picks if (s := _slug_to_summary(slug)) is not None]
    return ScheduleResponse(token=token, name=name, picks=body.picks, acts=acts)
