"""Stage-related API endpoints."""

from fastapi import APIRouter

from fqf.api.schemas import StageInfo, StageListResponse
from fqf.models import ALL_STAGES, STAGE_LOCATIONS, STAGE_ORDER

router = APIRouter(prefix="/api/v1/stages", tags=["stages"])


@router.get("", response_model=StageListResponse)
async def list_stages() -> StageListResponse:
    """List all stages with geographic coordinates in geographic order."""
    stages = [
        StageInfo(
            name=stage,
            lat=STAGE_LOCATIONS[stage].lat,
            lng=STAGE_LOCATIONS[stage].lng,
            order=STAGE_ORDER[stage],
        )
        for stage in ALL_STAGES
    ]
    return StageListResponse(stages=stages, count=len(stages))
