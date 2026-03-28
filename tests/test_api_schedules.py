"""Tests for schedule persistence API endpoints."""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from fqf.api.app import create_app

SCHEDULE_URL = "/api/v1/schedule"
MERGE_URL = "/api/v1/schedule/merge"

FAKE_TOKEN = "tremé-jazz-laissez"
OTHER_TOKEN = "bywater-funk-krewe"

# Real slugs from SCHEDULE so _slug_to_summary can resolve them
REAL_SLUG_1 = "kermit-ruffins-the-barbecue-swingers"
REAL_SLUG_2 = "rebirth-brass-band"
UNKNOWN_SLUG = "not-a-real-act"

SAMPLE_PICKS = [REAL_SLUG_1, REAL_SLUG_2]
ONE_UNKNOWN_PICK = [REAL_SLUG_1, UNKNOWN_SLUG]

MAX_MERGE_TOKENS = 5
TOO_MANY_TOKENS = ",".join(f"tok-{i}" for i in range(MAX_MERGE_TOKENS + 1))

DB_MODULE = "fqf.api.schedule_routes"


# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def app():  # type: ignore[no-untyped-def]
    return create_app()


@pytest.fixture
async def client(app):  # type: ignore[no-untyped-def]
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


# ── POST /api/v1/schedule ─────────────────────────────────────────────────────


class TestCreateSchedule:
    @pytest.mark.asyncio
    async def test_returns_201_with_token(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.create_schedule", new=AsyncMock(return_value=FAKE_TOKEN)):
            resp = await client.post(SCHEDULE_URL)
        assert resp.status_code == 201
        assert resp.json() == {"token": FAKE_TOKEN}

    @pytest.mark.asyncio
    async def test_token_field_present(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.create_schedule", new=AsyncMock(return_value=FAKE_TOKEN)):
            resp = await client.post(SCHEDULE_URL)
        assert "token" in resp.json()


# ── GET /api/v1/schedule/{token} ──────────────────────────────────────────────


class TestLoadSchedule:
    @pytest.mark.asyncio
    async def test_returns_200_with_picks_and_acts(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.load_schedule", new=AsyncMock(return_value=SAMPLE_PICKS)):
            resp = await client.get(f"{SCHEDULE_URL}/{FAKE_TOKEN}")

        assert resp.status_code == 200
        data = resp.json()
        assert data["token"] == FAKE_TOKEN
        assert data["picks"] == SAMPLE_PICKS
        # Both slugs are real acts — acts list should have 2 entries
        assert len(data["acts"]) == len(SAMPLE_PICKS)

    @pytest.mark.asyncio
    async def test_unknown_slugs_omitted_from_acts(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.load_schedule", new=AsyncMock(return_value=ONE_UNKNOWN_PICK)):
            resp = await client.get(f"{SCHEDULE_URL}/{FAKE_TOKEN}")

        data = resp.json()
        # picks includes unknown slug, acts only has the resolvable one
        assert len(data["picks"]) == 2
        assert len(data["acts"]) == 1

    @pytest.mark.asyncio
    async def test_act_summary_shape(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.load_schedule", new=AsyncMock(return_value=SAMPLE_PICKS)):
            resp = await client.get(f"{SCHEDULE_URL}/{FAKE_TOKEN}")

        act = resp.json()["acts"][0]
        for field in ("slug", "name", "stage", "date", "start", "end", "genre"):
            assert field in act

    @pytest.mark.asyncio
    async def test_returns_404_for_unknown_token(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.load_schedule", new=AsyncMock(return_value=None)):
            resp = await client.get(f"{SCHEDULE_URL}/{FAKE_TOKEN}")
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_empty_picks_returns_empty_acts(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.load_schedule", new=AsyncMock(return_value=[])):
            resp = await client.get(f"{SCHEDULE_URL}/{FAKE_TOKEN}")
        data = resp.json()
        assert data["picks"] == []
        assert data["acts"] == []


# ── PUT /api/v1/schedule/{token} ──────────────────────────────────────────────


class TestSaveSchedule:
    @pytest.mark.asyncio
    async def test_returns_200_with_updated_picks(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.save_picks", new=AsyncMock(return_value=True)):
            resp = await client.put(f"{SCHEDULE_URL}/{FAKE_TOKEN}", json={"picks": SAMPLE_PICKS})

        assert resp.status_code == 200
        data = resp.json()
        assert data["token"] == FAKE_TOKEN
        assert data["picks"] == SAMPLE_PICKS
        assert len(data["acts"]) == len(SAMPLE_PICKS)

    @pytest.mark.asyncio
    async def test_returns_404_when_token_not_found(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.save_picks", new=AsyncMock(return_value=False)):
            resp = await client.put(f"{SCHEDULE_URL}/{FAKE_TOKEN}", json={"picks": SAMPLE_PICKS})
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_unknown_slugs_omitted_from_acts(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.save_picks", new=AsyncMock(return_value=True)):
            resp = await client.put(
                f"{SCHEDULE_URL}/{FAKE_TOKEN}", json={"picks": ONE_UNKNOWN_PICK}
            )
        data = resp.json()
        assert len(data["picks"]) == 2
        assert len(data["acts"]) == 1


# ── GET /api/v1/schedule/merge ────────────────────────────────────────────────


class TestMergeSchedules:
    @pytest.mark.asyncio
    async def test_returns_200_with_merged_schedules(self, client: AsyncClient) -> None:
        schedules_map = {
            FAKE_TOKEN: [REAL_SLUG_1],
            OTHER_TOKEN: [REAL_SLUG_2],
        }
        with patch(
            f"{DB_MODULE}.load_multiple_schedules", new=AsyncMock(return_value=schedules_map)
        ):
            resp = await client.get(MERGE_URL, params={"tokens": f"{FAKE_TOKEN},{OTHER_TOKEN}"})

        assert resp.status_code == 200
        data = resp.json()
        assert len(data["schedules"]) == 2
        assert len(data["acts"]) == 2

    @pytest.mark.asyncio
    async def test_missing_token_gets_empty_picks(self, client: AsyncClient) -> None:
        # Only FAKE_TOKEN in db; OTHER_TOKEN is absent
        schedules_map = {FAKE_TOKEN: [REAL_SLUG_1]}
        with patch(
            f"{DB_MODULE}.load_multiple_schedules", new=AsyncMock(return_value=schedules_map)
        ):
            resp = await client.get(MERGE_URL, params={"tokens": f"{FAKE_TOKEN},{OTHER_TOKEN}"})

        data = resp.json()
        assert len(data["schedules"]) == 2
        missing = next(s for s in data["schedules"] if s["token"] == OTHER_TOKEN)
        assert missing["picks"] == []

    @pytest.mark.asyncio
    async def test_returns_400_when_too_many_tokens(self, client: AsyncClient) -> None:
        resp = await client.get(MERGE_URL, params={"tokens": TOO_MANY_TOKENS})
        assert resp.status_code == 400

    @pytest.mark.asyncio
    async def test_schedule_entry_shape(self, client: AsyncClient) -> None:
        schedules_map = {FAKE_TOKEN: [REAL_SLUG_1]}
        with patch(
            f"{DB_MODULE}.load_multiple_schedules", new=AsyncMock(return_value=schedules_map)
        ):
            resp = await client.get(MERGE_URL, params={"tokens": FAKE_TOKEN})

        entry = resp.json()["schedules"][0]
        assert "token" in entry
        assert "picks" in entry

    @pytest.mark.asyncio
    async def test_empty_token_list_returns_empty(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.load_multiple_schedules", new=AsyncMock(return_value={})):
            resp = await client.get(MERGE_URL, params={"tokens": ""})

        assert resp.status_code == 200
        data = resp.json()
        assert data["schedules"] == []
        assert data["acts"] == []
