"""Tests for database CRUD operations in fqf.db."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import fqf.db as db_module
from fqf.db import (
    close_pool,
    create_schedule,
    init_pool,
    load_multiple_schedules,
    load_schedule,
    save_picks,
)

FAKE_TOKEN = "tremé-jazz-laissez"
SAMPLE_PICKS = ["rebirth-brass-band", "trombone-shorty"]
ANOTHER_TOKEN = "bywater-funk-krewe"
ANOTHER_PICKS = ["dr-john"]


# ── Helpers ──────────────────────────────────────────────────────────────────


def _make_pool(*, fetchrow_result=None, fetch_result=None, execute_result="UPDATE 1"):
    """Build a minimal asyncpg pool mock with acquire() as async context manager."""
    conn = AsyncMock()
    conn.execute = AsyncMock(return_value=execute_result)
    conn.fetchrow = AsyncMock(return_value=fetchrow_result)
    conn.fetch = AsyncMock(return_value=fetch_result or [])

    pool = MagicMock()
    pool.close = AsyncMock()

    # acquire() must work as `async with pool.acquire() as conn`
    acquire_ctx = AsyncMock()
    acquire_ctx.__aenter__ = AsyncMock(return_value=conn)
    acquire_ctx.__aexit__ = AsyncMock(return_value=None)
    pool.acquire = MagicMock(return_value=acquire_ctx)

    return pool, conn


# ── init_pool / close_pool ────────────────────────────────────────────────────


class TestInitPool:
    @pytest.mark.asyncio
    async def test_skips_when_no_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DATABASE_URL", raising=False)
        db_module._pool = None
        await init_pool()
        assert db_module._pool is None

    @pytest.mark.asyncio
    async def test_creates_pool_and_table(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DATABASE_URL", "postgresql://fake/db")
        pool, conn = _make_pool()

        with patch("asyncpg.create_pool", new=AsyncMock(return_value=pool)):
            await init_pool()

        assert db_module._pool is pool
        conn.execute.assert_awaited_once()
        called_sql = conn.execute.await_args[0][0]
        assert "CREATE TABLE IF NOT EXISTS schedules" in called_sql

        # cleanup
        db_module._pool = None


class TestClosePool:
    @pytest.mark.asyncio
    async def test_closes_and_clears_pool(self) -> None:
        pool, _ = _make_pool()
        db_module._pool = pool
        await close_pool()
        pool.close.assert_awaited_once()
        assert db_module._pool is None

    @pytest.mark.asyncio
    async def test_noop_when_pool_is_none(self) -> None:
        db_module._pool = None
        await close_pool()  # should not raise


# ── create_schedule ───────────────────────────────────────────────────────────


class TestCreateSchedule:
    @pytest.mark.asyncio
    async def test_returns_token_and_inserts_row(self) -> None:
        pool, conn = _make_pool()
        db_module._pool = pool

        with patch("fqf.db.generate_token", return_value=FAKE_TOKEN):
            token = await create_schedule()

        assert token == FAKE_TOKEN
        conn.execute.assert_awaited_once()
        sql, arg = conn.execute.await_args[0]
        assert "INSERT INTO schedules" in sql
        assert arg == FAKE_TOKEN

        db_module._pool = None


# ── load_schedule ─────────────────────────────────────────────────────────────


class TestLoadSchedule:
    @pytest.mark.asyncio
    async def test_returns_picks_for_existing_token(self) -> None:
        row = {"picks": json.dumps(SAMPLE_PICKS)}
        pool, conn = _make_pool(fetchrow_result=row)
        db_module._pool = pool

        result = await load_schedule(FAKE_TOKEN)

        assert result == SAMPLE_PICKS
        conn.fetchrow.assert_awaited_once()
        db_module._pool = None

    @pytest.mark.asyncio
    async def test_returns_none_for_missing_token(self) -> None:
        pool, conn = _make_pool(fetchrow_result=None)
        db_module._pool = pool

        result = await load_schedule("no-such-token")

        assert result is None
        db_module._pool = None

    @pytest.mark.asyncio
    async def test_returns_empty_picks(self) -> None:
        row = {"picks": json.dumps([])}
        pool, conn = _make_pool(fetchrow_result=row)
        db_module._pool = pool

        result = await load_schedule(FAKE_TOKEN)

        assert result == []
        db_module._pool = None


# ── save_picks ────────────────────────────────────────────────────────────────


class TestSavePicks:
    @pytest.mark.asyncio
    async def test_returns_true_on_successful_update(self) -> None:
        pool, conn = _make_pool(execute_result="UPDATE 1")
        db_module._pool = pool

        result = await save_picks(FAKE_TOKEN, SAMPLE_PICKS)

        assert result is True
        conn.execute.assert_awaited_once()
        db_module._pool = None

    @pytest.mark.asyncio
    async def test_returns_false_when_token_not_found(self) -> None:
        pool, conn = _make_pool(execute_result="UPDATE 0")
        db_module._pool = pool

        result = await save_picks("ghost-token", SAMPLE_PICKS)

        assert result is False
        db_module._pool = None

    @pytest.mark.asyncio
    async def test_serializes_picks_as_json(self) -> None:
        pool, conn = _make_pool(execute_result="UPDATE 1")
        db_module._pool = pool

        await save_picks(FAKE_TOKEN, SAMPLE_PICKS)

        sql, picks_json, token = conn.execute.await_args[0]
        assert "UPDATE schedules" in sql
        assert json.loads(picks_json) == SAMPLE_PICKS
        assert token == FAKE_TOKEN
        db_module._pool = None


# ── load_multiple_schedules ───────────────────────────────────────────────────


class TestLoadMultipleSchedules:
    @pytest.mark.asyncio
    async def test_returns_dict_keyed_by_token(self) -> None:
        rows = [
            {"token": FAKE_TOKEN, "picks": json.dumps(SAMPLE_PICKS)},
            {"token": ANOTHER_TOKEN, "picks": json.dumps(ANOTHER_PICKS)},
        ]
        pool, conn = _make_pool(fetch_result=rows)
        db_module._pool = pool

        result = await load_multiple_schedules([FAKE_TOKEN, ANOTHER_TOKEN])

        assert result == {FAKE_TOKEN: SAMPLE_PICKS, ANOTHER_TOKEN: ANOTHER_PICKS}
        db_module._pool = None

    @pytest.mark.asyncio
    async def test_returns_empty_dict_for_no_matches(self) -> None:
        pool, conn = _make_pool(fetch_result=[])
        db_module._pool = pool

        result = await load_multiple_schedules(["nope-a", "nope-b"])

        assert result == {}
        db_module._pool = None
