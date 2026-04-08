"""Schedule persistence API endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from fqf.api.helpers import to_summary
from fqf.api.rate_limit import create_rate_limit_dependency, global_rate_limit_dependency
from fqf.api.schemas import (
    ActSummary,
    AddShareRequest,
    CreateScheduleRequest,
    FuzzyLookupRequest,
    FuzzyLookupResponse,
    ScheduleResponse,
    ScheduleUpdate,
    ShareBackRequest,
    ShareBackResponse,
    SharedScheduleResponse,
    ShareRef,
    ShareResponse,
    TokenResponse,
)
from fqf.db import (
    add_share_to_schedule,
    create_schedule,
    create_share_id,
    delete_schedule,
    has_share_in_schedule,
    load_schedule,
    load_schedule_by_share,
    remove_share_from_schedule,
    save_picks,
)
from fqf.schedule import get_by_slug
from fqf.tokens.fuzzy import fuzzy_resolve

router = APIRouter(prefix="/api/v1/schedule", tags=["schedule"])

NOT_FOUND_DETAIL = "Schedule not found"
FUZZY_NO_MATCH_DETAIL = "No matching token found"

SHARE_PATH_PREFIX = "/s"

_GlobalRateLimit = Annotated[None, Depends(global_rate_limit_dependency)]
_CreateRateLimit = Annotated[None, Depends(create_rate_limit_dependency)]


def _slug_to_summary(slug: str) -> ActSummary | None:
    act = get_by_slug(slug)
    return None if act is None else to_summary(act)


async def _build_schedule_response(token: str) -> ScheduleResponse:
    """Load a schedule by token and assemble the full ScheduleResponse.

    Raises HTTPException 404 if the token does not exist.
    """
    result = await load_schedule(token)
    if result is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    picks, name, raw_shares, own_share_id = result
    acts = [s for slug in picks if (s := _slug_to_summary(slug)) is not None]
    shares = [ShareRef(share_id=s["share_id"], name=s["name"]) for s in raw_shares]
    return ScheduleResponse(
        token=token, name=name, picks=picks, acts=acts, shares=shares, share_id=own_share_id
    )


# IMPORTANT: /fuzzy-lookup and /by-share/... must be defined before /{token}
# to avoid those literal path segments being captured as a token parameter.
@router.post("/fuzzy-lookup", response_model=FuzzyLookupResponse)
async def fuzzy_lookup(
    body: FuzzyLookupRequest,
    _rl: _GlobalRateLimit,
) -> FuzzyLookupResponse:
    """Resolve a fuzzy word triple to a canonical token.

    Tries exact match first, then 1-character corrections. Returns 404 if no
    pool word is close enough.
    """
    try:
        resolved_token, suggestion = fuzzy_resolve(body.raw_triple)
    except ValueError:
        raise HTTPException(status_code=404, detail=FUZZY_NO_MATCH_DETAIL)

    result = await load_schedule(resolved_token)
    if result is None:
        # Try sorted order — fuzzy_resolve already sorts, but raw input might be sorted differently
        raise HTTPException(status_code=404, detail=FUZZY_NO_MATCH_DETAIL)

    return FuzzyLookupResponse(token=resolved_token, suggestion=suggestion)


@router.get("/by-share/{share_id}", response_model=SharedScheduleResponse)
async def load_by_share(
    share_id: str,
    _rl: _GlobalRateLimit,
    check_share_id: str | None = Query(
        None, description="Check if this share_id is in target's shares"
    ),
) -> SharedScheduleResponse:
    """Load a read-only schedule view by its share_id."""
    result = await load_schedule_by_share(share_id)
    if result is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    _token, picks, name = result
    acts = [s for slug in picks if (s := _slug_to_summary(slug)) is not None]
    has_back: bool | None = None
    if check_share_id is not None:
        has_back = await has_share_in_schedule(share_id, check_share_id) or False
    return SharedScheduleResponse(name=name, picks=picks, acts=acts, has_back_share=has_back)


@router.post("/by-share/{share_id}/share-back", response_model=ShareBackResponse)
async def share_back(
    share_id: str, body: ShareBackRequest, _rl: _GlobalRateLimit
) -> ShareBackResponse:
    """Add the caller's share to another user's schedule, looked up by share_id."""
    result = await load_schedule_by_share(share_id)
    if result is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    target_token = result[0]
    already = await has_share_in_schedule(share_id, body.our_share_id)
    if already:
        return ShareBackResponse(already_shared=True)
    await add_share_to_schedule(target_token, body.our_share_id, body.our_name)
    return ShareBackResponse(already_shared=False)


@router.post("", response_model=TokenResponse, status_code=201)
async def create(body: CreateScheduleRequest, _rl: _CreateRateLimit) -> TokenResponse:
    """Generate a new schedule with a NOLA-themed token."""
    token = await create_schedule(
        name=body.name,
        fingerprint_hash=body.fingerprint_hash,
        counter=body.counter,
    )
    return TokenResponse(token=token)


@router.post("/{token}/share", response_model=ShareResponse)
async def share(token: str, request: Request, _rl: _GlobalRateLimit) -> ShareResponse:
    """Generate (or retrieve) a share_id for a schedule."""
    try:
        share_id = await create_share_id(token)
    except KeyError:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    base_url = str(request.base_url).rstrip("/")
    share_url = f"{base_url}{SHARE_PATH_PREFIX}/{share_id}"
    return ShareResponse(share_id=share_id, share_url=share_url)


@router.get("/{token}", response_model=ScheduleResponse)
async def load(token: str, _rl: _GlobalRateLimit) -> ScheduleResponse:
    """Load a schedule by its token."""
    return await _build_schedule_response(token)


@router.put("/{token}", response_model=ScheduleResponse)
async def save(token: str, body: ScheduleUpdate, _rl: _GlobalRateLimit) -> ScheduleResponse:
    """Save picks (and optionally name) for an existing schedule."""
    success = await save_picks(token, body.picks, body.name)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    return await _build_schedule_response(token)


@router.delete("/{token}", status_code=204)
async def delete(token: str, _rl: _GlobalRateLimit) -> None:
    """Delete a schedule and all its data."""
    removed = await delete_schedule(token)
    if not removed:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)


@router.post("/{token}/add-share", response_model=ScheduleResponse)
async def add_share(token: str, body: AddShareRequest, _rl: _GlobalRateLimit) -> ScheduleResponse:
    """Add a share reference to the user's schedule."""
    success = await add_share_to_schedule(token, body.share_id, body.name)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    return await _build_schedule_response(token)


@router.delete("/{token}/remove-share/{share_id}", response_model=ScheduleResponse)
async def remove_share(token: str, share_id: str, _rl: _GlobalRateLimit) -> ScheduleResponse:
    """Remove a share reference from the user's schedule."""
    success = await remove_share_from_schedule(token, share_id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL)
    return await _build_schedule_response(token)
