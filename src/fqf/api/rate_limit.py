"""In-memory rate limiting for the FQF API."""

import os
import time
from collections import defaultdict
from dataclasses import dataclass, field

from fastapi import HTTPException, Request

# Maximum schedule creates per IP per hour
CREATE_MAX_PER_HOUR = 10
# Maximum schedules per fingerprint (reject when counter >= this)
CREATE_MAX_PER_FINGERPRINT = 5
# Maximum load/fuzzy-lookup requests per IP per minute
LOAD_MAX_PER_MINUTE = 30
# General rate limit for all endpoints
GENERAL_MAX_PER_MINUTE = 60

_RATE_LIMIT_DISABLED_ENV = "DISABLE_RATE_LIMIT"
_TOO_MANY_REQUESTS_STATUS = 429
_RATE_LIMIT_DETAIL = "Too many requests"
_FINGERPRINT_LIMIT_DETAIL = "Schedule limit reached for this browser"

_SECONDS_PER_MINUTE = 60
_SECONDS_PER_HOUR = 3600


def _rate_limiting_enabled() -> bool:
    return os.environ.get(_RATE_LIMIT_DISABLED_ENV, "").lower() not in ("1", "true", "yes")


@dataclass
class _WindowCounter:
    """Sliding-window request counter for one key."""

    timestamps: list[float] = field(default_factory=list)

    def count_in_window(self, window_seconds: int, now: float) -> int:
        cutoff = now - window_seconds
        self.timestamps = [t for t in self.timestamps if t > cutoff]
        return len(self.timestamps)

    def record(self, now: float) -> None:
        self.timestamps.append(now)


class RateLimiter:
    """Thread-safe (asyncio-safe for single-process uvicorn) in-memory rate limiter.

    Tracks sliding-window request counts per key. Safe for concurrent async usage
    because CPython's GIL protects the dict operations; no explicit lock needed
    for single-process deployments.
    """

    def __init__(self) -> None:
        self._counters: dict[str, _WindowCounter] = defaultdict(_WindowCounter)

    def check(self, key: str, max_requests: int, window_seconds: int) -> None:
        """Raise HTTPException(429) if the key has exceeded max_requests in window_seconds.

        Records the current request if it is within the limit.
        """
        if not _rate_limiting_enabled():
            return
        now = time.monotonic()
        counter = self._counters[key]
        count = counter.count_in_window(window_seconds, now)
        if count >= max_requests:
            raise HTTPException(status_code=_TOO_MANY_REQUESTS_STATUS, detail=_RATE_LIMIT_DETAIL)
        counter.record(now)

    def reset(self, key: str) -> None:
        """Remove all recorded timestamps for a key (useful in tests)."""
        self._counters.pop(key, None)


# Module-level singleton — shared across all requests in one process
_limiter = RateLimiter()


def _client_ip(request: Request) -> str:
    """Extract the best-available client IP from the request."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For may be a comma-separated list; leftmost is the originating client
        return forwarded_for.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


async def check_create_ip_limit(request: Request) -> None:
    """Dependency: enforce CREATE_MAX_PER_HOUR creates per IP."""
    key = f"create:ip:{_client_ip(request)}"
    _limiter.check(key, CREATE_MAX_PER_HOUR, _SECONDS_PER_HOUR)


async def check_load_limit(request: Request) -> None:
    """Dependency: enforce LOAD_MAX_PER_MINUTE load/fuzzy-lookup requests per IP."""
    key = f"load:ip:{_client_ip(request)}"
    _limiter.check(key, LOAD_MAX_PER_MINUTE, _SECONDS_PER_MINUTE)


async def check_general_limit(request: Request) -> None:
    """Dependency: enforce GENERAL_MAX_PER_MINUTE requests per IP for all endpoints."""
    key = f"general:ip:{_client_ip(request)}"
    _limiter.check(key, GENERAL_MAX_PER_MINUTE, _SECONDS_PER_MINUTE)


def check_fingerprint_limit(counter: int) -> None:
    """Raise HTTPException(429) if a client-supplied counter has reached the per-fingerprint cap.

    The counter is provided by the client and represents how many schedules this browser
    fingerprint has already created. Reject before generating when counter >= CREATE_MAX_PER_FINGERPRINT.
    """
    if not _rate_limiting_enabled():
        return
    if counter >= CREATE_MAX_PER_FINGERPRINT:
        raise HTTPException(status_code=_TOO_MANY_REQUESTS_STATUS, detail=_FINGERPRINT_LIMIT_DETAIL)
