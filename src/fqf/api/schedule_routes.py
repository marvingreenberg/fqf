"""Schedule persistence API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from fqf.api.rate_limit import (
    check_create_ip_limit,
    check_fingerprint_limit,
    check_general_limit,
    check_load_limit,
)
from fqf.api.schemas import (
    ActSummary,
    AddShareRequest,
    CreateScheduleRequest,
    FuzzyLookupRequest,
    FuzzyLookupResponse,
    MergeEntry,
    MergeResponse,
    ScheduleResponse,
    ScheduleUpdate,
    SharedScheduleResponse,
    ShareRef,
    ShareResponse,
    TokenResponse,
)
from fqf.db import (
    add_share_to_schedule,
    create_schedule,
    create_share_id,
    load_multiple_schedules,
    load_schedule,
    load_schedule_by_share,
    remove_share_from_schedule,
    save_picks,
)
from fqf.schedule import get_by_slug
from fqf.tokens.fuzzy import fuzzy_resolve_triple

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


FUZZY_LOOKUP_PATH = "/fuzzy-lookup"
INVALID_TRIPLE_DETAIL = "Invalid triple"


# IMPORTANT: /merge, /by-share/..., and /fuzzy-lookup must be defined before /{token} to avoid
# those literal path segments being captured as a token parameter.
@router.get("/merge", response_model=MergeResponse, dependencies=[Depends(check_general_limit)])
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


@router.get(
    "/by-share/{share_id}",
    response_model=SharedScheduleResponse,
    dependencies=[Depends(check_general_limit)],
)
async def load_by_share(share_id: str) -> SharedScheduleResponse:
    """Load a read-only schedule view by its share_id."""
    result = await load_schedule_by_share(share_id)
    if result is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    _token, picks, name = result
    acts = [s for slug in picks if (s := _slug_to_summary(slug)) is not None]
    return SharedScheduleResponse(name=name, picks=picks, acts=acts)


@router.post(
    "",
    response_model=TokenResponse,
    status_code=201,
    dependencies=[Depends(check_create_ip_limit)],
)
async def create(body: CreateScheduleRequest) -> TokenResponse:
    """Generate a new schedule with a NOLA-themed token."""
    check_fingerprint_limit(body.counter)
    token = await create_schedule()
    return TokenResponse(token=token)


@router.post(
    "/{token}/share", response_model=ShareResponse, dependencies=[Depends(check_general_limit)]
)
async def share(token: str, request: Request) -> ShareResponse:
    """Generate (or retrieve) a share_id for a schedule."""
    try:
        share_id = await create_share_id(token)
    except KeyError:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    base_url = str(request.base_url).rstrip("/")
    share_url = f"{base_url}{SHARE_PATH_PREFIX}/{share_id}"
    return ShareResponse(share_id=share_id, share_url=share_url)


@router.post(
    FUZZY_LOOKUP_PATH,
    response_model=FuzzyLookupResponse,
    dependencies=[Depends(check_load_limit)],
)
async def fuzzy_lookup(body: FuzzyLookupRequest) -> FuzzyLookupResponse:
    """Resolve a fuzzy triple string to a schedule token, correcting minor typos."""
    try:
        as_entered, sorted_token, was_corrected = fuzzy_resolve_triple(body.raw_triple)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    result = await load_schedule(as_entered)
    if result is not None:
        token = as_entered
        name = result[1]
        return FuzzyLookupResponse(
            token=token, corrected=was_corrected, suggestion=as_entered, name=name, found=True
        )

    result = await load_schedule(sorted_token)
    if result is not None:
        name = result[1]
        return FuzzyLookupResponse(
            token=sorted_token,
            corrected=was_corrected,
            suggestion=sorted_token,
            name=name,
            found=True,
        )

    return FuzzyLookupResponse(
        token=sorted_token,
        corrected=was_corrected,
        suggestion=sorted_token,
        name="",
        found=False,
    )


@router.get("/{token}", response_model=ScheduleResponse, dependencies=[Depends(check_load_limit)])
async def load(token: str) -> ScheduleResponse:
    """Load a schedule by its token."""
    result = await load_schedule(token)
    if result is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    picks, name, raw_shares, own_share_id = result
    acts = [s for slug in picks if (s := _slug_to_summary(slug)) is not None]
    shares = [ShareRef(share_id=s["share_id"], name=s["name"]) for s in raw_shares]
    return ScheduleResponse(
        token=token, name=name, picks=picks, acts=acts, shares=shares, share_id=own_share_id
    )


@router.put(
    "/{token}", response_model=ScheduleResponse, dependencies=[Depends(check_general_limit)]
)
async def save(token: str, body: ScheduleUpdate) -> ScheduleResponse:
    """Save picks (and optionally name) for an existing schedule."""
    success = await save_picks(token, body.picks, body.name)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    # Re-fetch to reflect any update and include shares
    result = await load_schedule(token)
    name = result[1] if result is not None else (body.name or "")
    raw_shares = result[2] if result is not None else []
    own_share_id = result[3] if result is not None else ""
    acts = [s for slug in body.picks if (s := _slug_to_summary(slug)) is not None]
    shares = [ShareRef(share_id=s["share_id"], name=s["name"]) for s in raw_shares]
    return ScheduleResponse(
        token=token, name=name, picks=body.picks, acts=acts, shares=shares, share_id=own_share_id
    )


@router.post(
    "/{token}/add-share",
    response_model=ScheduleResponse,
    dependencies=[Depends(check_general_limit)],
)
async def add_share(token: str, body: AddShareRequest) -> ScheduleResponse:
    """Add a share reference to the user's schedule."""
    success = await add_share_to_schedule(token, body.share_id, body.name)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    result = await load_schedule(token)
    if result is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    picks, name, raw_shares, own_share_id = result
    acts = [s for slug in picks if (s := _slug_to_summary(slug)) is not None]
    shares = [ShareRef(share_id=s["share_id"], name=s["name"]) for s in raw_shares]
    return ScheduleResponse(
        token=token, name=name, picks=picks, acts=acts, shares=shares, share_id=own_share_id
    )


@router.delete(
    "/{token}/remove-share/{share_id}",
    response_model=ScheduleResponse,
    dependencies=[Depends(check_general_limit)],
)
async def remove_share(token: str, share_id: str) -> ScheduleResponse:
    """Remove a share reference from the user's schedule."""
    success = await remove_share_from_schedule(token, share_id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    result = await load_schedule(token)
    if result is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    picks, name, raw_shares, own_share_id = result
    acts = [s for slug in picks if (s := _slug_to_summary(slug)) is not None]
    shares = [ShareRef(share_id=s["share_id"], name=s["name"]) for s in raw_shares]
    return ScheduleResponse(
        token=token, name=name, picks=picks, acts=acts, shares=shares, share_id=own_share_id
    )
