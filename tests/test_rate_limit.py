"""Tests for in-memory rate limiting."""

import time
from collections import deque
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

import fqf.api.rate_limit as rl_module
from fqf.api.rate_limit import (
    CREATES_PER_HOUR,
    HTTP_TOO_MANY_REQUESTS,
    MINUTE_WINDOW,
    RATE_LIMIT_DETAIL_CREATE,
    RATE_LIMIT_DETAIL_GLOBAL,
    REQUESTS_PER_MINUTE,
    check_create_rate,
    check_global_rate,
    create_rate_limit_dependency,
    global_rate_limit_dependency,
)

TEST_IP = "192.168.1.100"
OTHER_IP = "10.0.0.1"


@pytest.fixture(autouse=True)
def reset_rate_limit_state() -> None:  # type: ignore[return]
    """Clear rate-limit windows before each test."""
    rl_module._create_windows.clear()
    rl_module._global_windows.clear()
    yield
    rl_module._create_windows.clear()
    rl_module._global_windows.clear()


class TestCheckGlobalRate:
    def test_allows_requests_under_limit(self) -> None:
        for _ in range(REQUESTS_PER_MINUTE - 1):
            check_global_rate(TEST_IP)  # should not raise

    def test_raises_429_at_limit(self) -> None:
        for _ in range(REQUESTS_PER_MINUTE):
            check_global_rate(TEST_IP)
        with pytest.raises(HTTPException) as exc_info:
            check_global_rate(TEST_IP)
        assert exc_info.value.status_code == HTTP_TOO_MANY_REQUESTS
        assert exc_info.value.detail == RATE_LIMIT_DETAIL_GLOBAL

    def test_different_ips_tracked_independently(self) -> None:
        for _ in range(REQUESTS_PER_MINUTE):
            check_global_rate(TEST_IP)
        # Different IP should not be affected
        check_global_rate(OTHER_IP)  # should not raise

    def test_old_timestamps_evicted(self) -> None:
        now = time.time()
        # Fill the window with timestamps older than MINUTE_WINDOW
        old_time = now - MINUTE_WINDOW - 1
        rl_module._global_windows[TEST_IP] = deque([old_time] * REQUESTS_PER_MINUTE)
        # Should allow a new request since old ones are expired
        check_global_rate(TEST_IP)  # should not raise


class TestCheckCreateRate:
    def test_allows_creates_under_limit(self) -> None:
        for _ in range(CREATES_PER_HOUR - 1):
            check_create_rate(TEST_IP)  # should not raise

    def test_raises_429_at_create_limit(self) -> None:
        for _ in range(CREATES_PER_HOUR):
            check_create_rate(TEST_IP)
        with pytest.raises(HTTPException) as exc_info:
            check_create_rate(TEST_IP)
        assert exc_info.value.status_code == HTTP_TOO_MANY_REQUESTS
        assert exc_info.value.detail == RATE_LIMIT_DETAIL_CREATE

    def test_different_ips_tracked_independently(self) -> None:
        for _ in range(CREATES_PER_HOUR):
            check_create_rate(TEST_IP)
        check_create_rate(OTHER_IP)  # should not raise


class TestClientIpExtraction:
    def _make_request(
        self,
        client_host: str | None = "127.0.0.1",
        forwarded_for: str | None = None,
    ) -> MagicMock:
        request = MagicMock()
        request.client = MagicMock(host=client_host) if client_host else None
        headers = {}
        if forwarded_for:
            headers["x-forwarded-for"] = forwarded_for
        request.headers = headers
        return request

    @pytest.mark.asyncio
    async def test_global_uses_client_host(self) -> None:
        request = self._make_request(client_host=TEST_IP)
        await global_rate_limit_dependency(request)
        assert TEST_IP in rl_module._global_windows

    @pytest.mark.asyncio
    async def test_global_uses_forwarded_for(self) -> None:
        request = self._make_request(client_host="10.0.0.1", forwarded_for=f"{TEST_IP}, 10.0.0.1")
        await global_rate_limit_dependency(request)
        assert TEST_IP in rl_module._global_windows

    @pytest.mark.asyncio
    async def test_create_dependency_checks_both_limits(self) -> None:
        request = self._make_request(client_host=TEST_IP)
        await create_rate_limit_dependency(request)
        assert TEST_IP in rl_module._global_windows
        assert TEST_IP in rl_module._create_windows

    @pytest.mark.asyncio
    async def test_no_client_falls_back_to_unknown(self) -> None:
        request = self._make_request(client_host=None)
        await global_rate_limit_dependency(request)
        assert "unknown" in rl_module._global_windows
