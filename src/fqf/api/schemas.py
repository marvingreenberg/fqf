"""Pydantic request/response models for the API."""

from datetime import date, time

from pydantic import BaseModel, field_serializer


class ActSummary(BaseModel):
    """Lightweight act representation for list endpoints."""

    slug: str
    name: str
    stage: str
    date: date
    start: time
    end: time
    genre: str

    @field_serializer("start", "end")
    @classmethod
    def serialize_time(cls, v: time) -> str:
        return v.strftime("%H:%M")


class ActDetail(ActSummary):
    """Full act representation including bio."""

    about: str
    about_source: str
    websites: list[str]


class ActListResponse(BaseModel):
    """Response for list/search endpoints."""

    acts: list[ActSummary]
    count: int


class StageInfo(BaseModel):
    """Stage with geographic coordinates."""

    name: str
    lat: float
    lng: float
    order: int


class StageListResponse(BaseModel):
    """Response for stages endpoint."""

    stages: list[StageInfo]
    count: int


class ShareRef(BaseModel):
    """A persisted reference to a shared schedule."""

    share_id: str
    name: str


class ScheduleUpdate(BaseModel):
    """Request body for saving picks."""

    picks: list[str]
    name: str | None = None


class AddShareRequest(BaseModel):
    """Request body for adding a share reference."""

    share_id: str
    name: str


class CreateScheduleRequest(BaseModel):
    """Request body for creating a new schedule."""

    name: str
    fingerprint_hash: str | None = None
    counter: int = 0


class FuzzyLookupRequest(BaseModel):
    """Request body for fuzzy triple lookup."""

    raw_triple: str


class FuzzyLookupResponse(BaseModel):
    """Response for fuzzy lookup endpoint."""

    token: str
    suggestion: str | None = None


class TokenResponse(BaseModel):
    """Response when creating a new schedule."""

    token: str


class ScheduleResponse(BaseModel):
    """Response for loading a schedule."""

    token: str
    name: str
    picks: list[str]
    acts: list[ActSummary]
    shares: list[ShareRef] = []
    share_id: str = ""


class ShareResponse(BaseModel):
    """Response when generating a share link."""

    share_id: str
    share_url: str


class SharedScheduleResponse(BaseModel):
    """Read-only schedule view accessed via share link."""

    name: str
    picks: list[str]
    acts: list[ActSummary]


class MergeEntry(BaseModel):
    """One person's picks in a merge response."""

    token: str
    picks: list[str]


class MergeResponse(BaseModel):
    """Response for merge endpoint."""

    schedules: list[MergeEntry]
    acts: list[ActSummary]
