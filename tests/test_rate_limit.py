"""Tests for in-memory rate limiting."""

import os
import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException
from httpx import ASGITransport, AsyncClient

from fqf.api.app import create_app
from fqf.api.rate_limit import (
    CREATE_MAX_PER_FINGERPRINT,
    CREATE_MAX_PER_HOUR,
    GENERAL_MAX_PER_MINUTE,
    LOAD_MAX_PER_MINUTE,
    RateLimiter,
    _client_ip,
    _limiter,
    check_fingerprint_limit,
)

SCHEDULE_URL = "/api/v1/schedule"
FAKE_TOKEN = "tremé-jazz-laissez"
DB_MODULE = "fqf.api.schedule_routes"


@pytest.fixture(autouse=True)
def reset_module_limiter() -> None:
    """Clear the module-level rate limiter state before each test.

    Prevents accumulated counts from one test affecting another when tests share
    the same in-process singleton.
    """
    _limiter._counters.clear()


# ── RateLimiter unit tests ───────────────────────────────────────────────────


class TestRateLimiterUnderLimit:
    def test_single_request_passes(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DISABLE_RATE_LIMIT", raising=False)
        limiter = RateLimiter()
        # Should not raise
        limiter.check("key1", max_requests=5, window_seconds=60)

    def test_requests_up_to_limit_all_pass(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DISABLE_RATE_LIMIT", raising=False)
        limiter = RateLimiter()
        for _ in range(CREATE_MAX_PER_HOUR):
            limiter.check("key2", max_requests=CREATE_MAX_PER_HOUR, window_seconds=3600)

    def test_request_exceeding_limit_raises_429(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DISABLE_RATE_LIMIT", raising=False)
        limiter = RateLimiter()
        for _ in range(LOAD_MAX_PER_MINUTE):
            limiter.check("key3", max_requests=LOAD_MAX_PER_MINUTE, window_seconds=60)
        with pytest.raises(HTTPException) as exc_info:
            limiter.check("key3", max_requests=LOAD_MAX_PER_MINUTE, window_seconds=60)
        assert exc_info.value.status_code == 429

    def test_different_keys_are_independent(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DISABLE_RATE_LIMIT", raising=False)
        limiter = RateLimiter()
        for _ in range(3):
            limiter.check("keyA", max_requests=3, window_seconds=60)
        # keyA is now exhausted
        with pytest.raises(HTTPException):
            limiter.check("keyA", max_requests=3, window_seconds=60)
        # keyB should still pass
        limiter.check("keyB", max_requests=3, window_seconds=60)


class TestRateLimiterWindowExpiry:
    def test_requests_allowed_again_after_window(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DISABLE_RATE_LIMIT", raising=False)
        limiter = RateLimiter()
        key = "expiry-key"
        window = 1  # 1-second window for fast test

        # Fill the window
        for _ in range(3):
            limiter.check(key, max_requests=3, window_seconds=window)

        # Exhausted — next request should fail
        with pytest.raises(HTTPException):
            limiter.check(key, max_requests=3, window_seconds=window)

        # Advance time past the window
        with patch("fqf.api.rate_limit.time.monotonic", return_value=time.monotonic() + 2):
            # Should pass again after the window expires
            limiter.check(key, max_requests=3, window_seconds=window)

    def test_old_timestamps_are_pruned(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DISABLE_RATE_LIMIT", raising=False)
        limiter = RateLimiter()
        key = "prune-key"

        # Make two requests in the distant past (simulated via monotonic patch)
        past = time.monotonic() - 120  # 2 minutes ago
        with patch("fqf.api.rate_limit.time.monotonic", return_value=past):
            limiter.check(key, max_requests=2, window_seconds=60)
            limiter.check(key, max_requests=2, window_seconds=60)

        # Now make a fresh request — old timestamps should be outside the 60s window
        limiter.check(key, max_requests=2, window_seconds=60)


class TestRateLimiterReset:
    def test_reset_clears_counter(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DISABLE_RATE_LIMIT", raising=False)
        limiter = RateLimiter()
        key = "reset-key"
        for _ in range(3):
            limiter.check(key, max_requests=3, window_seconds=60)
        with pytest.raises(HTTPException):
            limiter.check(key, max_requests=3, window_seconds=60)

        limiter.reset(key)
        # Should pass again after reset
        limiter.check(key, max_requests=3, window_seconds=60)


class TestRateLimiterDisabledViaEnv:
    def test_disabled_when_env_var_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DISABLE_RATE_LIMIT", "1")
        limiter = RateLimiter()
        # Should never raise regardless of count
        for _ in range(GENERAL_MAX_PER_MINUTE + 10):
            limiter.check("disabled-key", max_requests=1, window_seconds=60)

    def test_enabled_when_env_var_not_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DISABLE_RATE_LIMIT", raising=False)
        limiter = RateLimiter()
        with pytest.raises(HTTPException):
            for _ in range(100):
                limiter.check("enabled-key", max_requests=1, window_seconds=60)


# ── check_fingerprint_limit unit tests ───────────────────────────────────────


class TestFingerprintLimit:
    def test_counter_below_limit_passes(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DISABLE_RATE_LIMIT", raising=False)
        for counter in range(CREATE_MAX_PER_FINGERPRINT):
            check_fingerprint_limit(counter)  # Should not raise

    def test_counter_at_limit_raises_429(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DISABLE_RATE_LIMIT", raising=False)
        with pytest.raises(HTTPException) as exc_info:
            check_fingerprint_limit(CREATE_MAX_PER_FINGERPRINT)
        assert exc_info.value.status_code == 429

    def test_counter_above_limit_raises_429(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DISABLE_RATE_LIMIT", raising=False)
        with pytest.raises(HTTPException) as exc_info:
            check_fingerprint_limit(CREATE_MAX_PER_FINGERPRINT + 5)
        assert exc_info.value.status_code == 429

    def test_disabled_via_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DISABLE_RATE_LIMIT", "1")
        # Should not raise even above limit
        check_fingerprint_limit(CREATE_MAX_PER_FINGERPRINT + 99)


# ── _client_ip unit tests ─────────────────────────────────────────────────────


class TestClientIp:
    def test_extracts_forwarded_for_header(self) -> None:
        req = MagicMock()
        req.headers = {"X-Forwarded-For": "1.2.3.4, 10.0.0.1"}
        req.client = None
        assert _client_ip(req) == "1.2.3.4"

    def test_falls_back_to_client_host(self) -> None:
        req = MagicMock()
        req.headers = {}
        req.client = MagicMock(host="5.6.7.8")
        assert _client_ip(req) == "5.6.7.8"

    def test_returns_unknown_when_no_client(self) -> None:
        req = MagicMock()
        req.headers = {}
        req.client = None
        assert _client_ip(req) == "unknown"


# ── Integration tests via HTTP client ─────────────────────────────────────────


@pytest.fixture
def app():  # type: ignore[no-untyped-def]
    return create_app()


@pytest.fixture
async def client(app):  # type: ignore[no-untyped-def]
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


class TestCreateEndpointFingerprintRejection:
    @pytest.mark.asyncio
    async def test_counter_below_limit_allowed(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.create_schedule", new=AsyncMock(return_value=FAKE_TOKEN)):
            resp = await client.post(SCHEDULE_URL, json={"counter": 0})
        assert resp.status_code == 201

    @pytest.mark.asyncio
    async def test_counter_at_limit_rejected_with_429(
        self, client: AsyncClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("DISABLE_RATE_LIMIT", raising=False)
        resp = await client.post(SCHEDULE_URL, json={"counter": CREATE_MAX_PER_FINGERPRINT})
        assert resp.status_code == 429

    @pytest.mark.asyncio
    async def test_counter_above_limit_rejected_with_429(
        self, client: AsyncClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("DISABLE_RATE_LIMIT", raising=False)
        resp = await client.post(SCHEDULE_URL, json={"counter": CREATE_MAX_PER_FINGERPRINT + 10})
        assert resp.status_code == 429

    @pytest.mark.asyncio
    async def test_counter_defaults_to_zero_when_omitted(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.create_schedule", new=AsyncMock(return_value=FAKE_TOKEN)):
            resp = await client.post(SCHEDULE_URL, json={})
        assert resp.status_code == 201


class TestGeneralRateLimitMiddleware:
    @pytest.mark.asyncio
    async def test_rate_limit_disabled_allows_burst(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """With DISABLE_RATE_LIMIT=1, many rapid requests all succeed."""
        monkeypatch.setenv("DISABLE_RATE_LIMIT", "1")
        app = create_app()
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            for _ in range(GENERAL_MAX_PER_MINUTE + 5):
                resp = await c.get("/api/v1/acts")
                assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_ip_rate_limit_on_load_endpoint(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """After LOAD_MAX_PER_MINUTE requests, GET /{token} returns 429."""
        monkeypatch.delenv("DISABLE_RATE_LIMIT", raising=False)
        app = create_app()
        transport = ASGITransport(app=app)
        schedule_data = ([], "", [], "")
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            with patch(
                "fqf.api.schedule_routes.load_schedule",
                new=AsyncMock(return_value=schedule_data),
            ):
                statuses = []
                for _ in range(LOAD_MAX_PER_MINUTE + 1):
                    r = await c.get(f"{SCHEDULE_URL}/{FAKE_TOKEN}")
                    statuses.append(r.status_code)
        assert statuses[-1] == 429
        assert all(s == 200 for s in statuses[:LOAD_MAX_PER_MINUTE])
