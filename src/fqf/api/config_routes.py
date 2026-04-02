"""Festival configuration API endpoint."""

from fastapi import APIRouter

from fqf.api.schemas import FestivalConfigResponse
from fqf.festival_config import (
    DAY_LABELS,
    FESTIVAL_DATES,
    FESTIVAL_NAME,
    FESTIVAL_SHORT_NAME,
    FESTIVAL_YEAR,
)

router = APIRouter(prefix="/api/v1/config", tags=["config"])


@router.get("", response_model=FestivalConfigResponse)
async def get_config() -> FestivalConfigResponse:
    """Return festival metadata for the currently configured festival."""
    return FestivalConfigResponse(
        name=FESTIVAL_NAME,
        short_name=FESTIVAL_SHORT_NAME,
        year=FESTIVAL_YEAR,
        dates=[d.isoformat() for d in FESTIVAL_DATES],
        day_labels=DAY_LABELS,
    )
