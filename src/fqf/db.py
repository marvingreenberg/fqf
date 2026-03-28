"""Neon Postgres connection and schedule CRUD operations.

When DATABASE_URL is not set, falls back to in-memory storage for local dev.
"""

import json
import logging
import os

import asyncpg  # type: ignore[import-untyped]

from fqf.tokens.generator import generate_token

DATABASE_URL_ENV = "DATABASE_URL"
MIN_POOL_SIZE = 1
MAX_POOL_SIZE = 5

logger = logging.getLogger(__name__)

_pool: asyncpg.Pool | None = None

# In-memory fallback for local dev (no DATABASE_URL)
_memory_store: dict[str, list[str]] | None = None

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS schedules (
    token TEXT PRIMARY KEY,
    picks JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

INSERT_SCHEDULE_SQL = """
INSERT INTO schedules (token, picks) VALUES ($1, '[]'::jsonb);
"""

SELECT_SCHEDULE_SQL = """
SELECT picks FROM schedules WHERE token = $1;
"""

UPDATE_PICKS_SQL = """
UPDATE schedules SET picks = $1::jsonb, updated_at = NOW() WHERE token = $2;
"""

SELECT_MULTIPLE_SQL = """
SELECT token, picks FROM schedules WHERE token = ANY($1);
"""


def _using_memory() -> bool:
    return _memory_store is not None


async def init_pool() -> None:
    """Initialize the connection pool, or fall back to in-memory storage."""
    global _pool, _memory_store
    database_url = os.environ.get(DATABASE_URL_ENV, "")
    if not database_url:
        logger.info("No DATABASE_URL set — using in-memory schedule storage")
        _memory_store = {}
        return
    _pool = await asyncpg.create_pool(database_url, min_size=MIN_POOL_SIZE, max_size=MAX_POOL_SIZE)
    async with _pool.acquire() as conn:
        await conn.execute(CREATE_TABLE_SQL)


async def close_pool() -> None:
    """Close the connection pool. Call once at app shutdown."""
    global _pool, _memory_store
    if _pool:
        await _pool.close()
        _pool = None
    _memory_store = None


async def create_schedule() -> str:
    """Generate a new token and create an empty schedule row."""
    token = generate_token()
    if _using_memory():
        assert _memory_store is not None
        _memory_store[token] = []
        return token
    assert _pool is not None
    async with _pool.acquire() as conn:
        await conn.execute(INSERT_SCHEDULE_SQL, token)
    return token


async def load_schedule(token: str) -> list[str] | None:
    """Load picks for a token. Returns None if token doesn't exist."""
    if _using_memory():
        assert _memory_store is not None
        if token not in _memory_store:
            return None
        return list(_memory_store[token])
    assert _pool is not None
    async with _pool.acquire() as conn:
        row = await conn.fetchrow(SELECT_SCHEDULE_SQL, token)
    if row is None:
        return None
    return json.loads(row["picks"])  # type: ignore[no-any-return]


async def save_picks(token: str, picks: list[str]) -> bool:
    """Update picks for an existing token. Returns False if token not found."""
    if _using_memory():
        assert _memory_store is not None
        if token not in _memory_store:
            return False
        _memory_store[token] = list(picks)
        return True
    assert _pool is not None
    async with _pool.acquire() as conn:
        result = await conn.execute(UPDATE_PICKS_SQL, json.dumps(picks), token)
    return bool(result == "UPDATE 1")


async def load_multiple_schedules(tokens: list[str]) -> dict[str, list[str]]:
    """Load picks for multiple tokens at once."""
    if _using_memory():
        assert _memory_store is not None
        return {t: list(_memory_store[t]) for t in tokens if t in _memory_store}
    assert _pool is not None
    async with _pool.acquire() as conn:
        rows = await conn.fetch(SELECT_MULTIPLE_SQL, tokens)
    return {row["token"]: json.loads(row["picks"]) for row in rows}
