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


class ActListResponse(BaseModel):
    """Response for list/search endpoints."""

    acts: list[ActSummary]
    count: int


class ScheduleUpdate(BaseModel):
    """Request body for saving picks."""

    picks: list[str]


class TokenResponse(BaseModel):
    """Response when creating a new schedule."""

    token: str


class ScheduleResponse(BaseModel):
    """Response for loading a schedule."""

    token: str
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
