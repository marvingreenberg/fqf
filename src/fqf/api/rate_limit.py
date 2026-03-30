"""Simple in-memory sliding-window rate limiter for FastAPI endpoints."""

import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request

# Per-IP limits
CREATES_PER_HOUR = 10
REQUESTS_PER_MINUTE = 60

# Window durations in seconds
HOUR_WINDOW = 3600
MINUTE_WINDOW = 60

HTTP_TOO_MANY_REQUESTS = 429
RATE_LIMIT_DETAIL_CREATE = "Too many schedule creations. Try again later."
RATE_LIMIT_DETAIL_GLOBAL = "Too many requests. Try again later."

# Sliding-window deques: ip -> deque of timestamps (float, seconds since epoch)
_create_windows: dict[str, deque[float]] = defaultdict(deque)
_global_windows: dict[str, deque[float]] = defaultdict(deque)


def _evict_old(dq: deque[float], window: int, now: float) -> None:
    """Remove timestamps older than `window` seconds from the left of the deque."""
    cutoff = now - window
    while dq and dq[0] < cutoff:
        dq.popleft()


def check_create_rate(ip: str) -> None:
    """Raise 429 if this IP has exceeded the create-schedule rate limit."""
    now = time.time()
    dq = _create_windows[ip]
    _evict_old(dq, HOUR_WINDOW, now)
    if len(dq) >= CREATES_PER_HOUR:
        raise HTTPException(status_code=HTTP_TOO_MANY_REQUESTS, detail=RATE_LIMIT_DETAIL_CREATE)
    dq.append(now)


def check_global_rate(ip: str) -> None:
    """Raise 429 if this IP has exceeded the global per-minute rate limit."""
    now = time.time()
    dq = _global_windows[ip]
    _evict_old(dq, MINUTE_WINDOW, now)
    if len(dq) >= REQUESTS_PER_MINUTE:
        raise HTTPException(status_code=HTTP_TOO_MANY_REQUESTS, detail=RATE_LIMIT_DETAIL_GLOBAL)
    dq.append(now)


def _client_ip(request: Request) -> str:
    """Extract the client IP from the request, respecting X-Forwarded-For."""
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


async def global_rate_limit_dependency(request: Request) -> None:
    """FastAPI dependency: apply the global per-minute rate limit."""
    check_global_rate(_client_ip(request))


async def create_rate_limit_dependency(request: Request) -> None:
    """FastAPI dependency: apply both global and create-specific rate limits."""
    ip = _client_ip(request)
    check_global_rate(ip)
    check_create_rate(ip)
