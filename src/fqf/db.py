"""Neon Postgres connection and schedule CRUD operations."""

import json
import os

import asyncpg  # type: ignore[import-untyped]

from fqf.tokens.generator import generate_token

DATABASE_URL_ENV = "DATABASE_URL"
MIN_POOL_SIZE = 1
MAX_POOL_SIZE = 5

_pool: asyncpg.Pool | None = None

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


async def init_pool() -> None:
    """Initialize the connection pool. Call once at app startup."""
    global _pool
    database_url = os.environ.get(DATABASE_URL_ENV, "")
    if not database_url:
        return
    _pool = await asyncpg.create_pool(database_url, min_size=MIN_POOL_SIZE, max_size=MAX_POOL_SIZE)
    async with _pool.acquire() as conn:
        await conn.execute(CREATE_TABLE_SQL)


async def close_pool() -> None:
    """Close the connection pool. Call once at app shutdown."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


async def create_schedule() -> str:
    """Generate a new token and create an empty schedule row."""
    assert _pool is not None
    token = generate_token()
    async with _pool.acquire() as conn:
        await conn.execute(INSERT_SCHEDULE_SQL, token)
    return token


async def load_schedule(token: str) -> list[str] | None:
    """Load picks for a token. Returns None if token doesn't exist."""
    assert _pool is not None
    async with _pool.acquire() as conn:
        row = await conn.fetchrow(SELECT_SCHEDULE_SQL, token)
    if row is None:
        return None
    return json.loads(row["picks"])  # type: ignore[no-any-return]


async def save_picks(token: str, picks: list[str]) -> bool:
    """Update picks for an existing token. Returns False if token not found."""
    assert _pool is not None
    async with _pool.acquire() as conn:
        result = await conn.execute(UPDATE_PICKS_SQL, json.dumps(picks), token)
    return bool(result == "UPDATE 1")


async def load_multiple_schedules(tokens: list[str]) -> dict[str, list[str]]:
    """Load picks for multiple tokens at once."""
    assert _pool is not None
    async with _pool.acquire() as conn:
        rows = await conn.fetch(SELECT_MULTIPLE_SQL, tokens)
    return {row["token"]: json.loads(row["picks"]) for row in rows}
