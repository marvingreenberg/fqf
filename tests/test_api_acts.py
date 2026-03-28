"""Tests for act API endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from fqf.api.app import create_app

ACTS_URL = "/api/v1/acts"
EXPECTED_ACT_COUNT = 302
THU_DATE = "2026-04-16"
FISH_FRY_PARTIAL = "Fish Fry"
REBIRTH_SLUG = "rebirth-brass-band"
REBIRTH_NAME = "Rebirth Brass Band"
NONEXISTENT_SLUG = "nonexistent-band"


@pytest.fixture
def app():  # type: ignore[no-untyped-def]
    return create_app()


@pytest.fixture
async def client(app):  # type: ignore[no-untyped-def]
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


class TestListActs:
    @pytest.mark.asyncio
    async def test_returns_all_acts(self, client: AsyncClient) -> None:
        resp = await client.get(ACTS_URL)
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] == EXPECTED_ACT_COUNT
        assert len(data["acts"]) == EXPECTED_ACT_COUNT

    @pytest.mark.asyncio
    async def test_act_summary_shape(self, client: AsyncClient) -> None:
        resp = await client.get(ACTS_URL)
        act = resp.json()["acts"][0]
        assert "slug" in act
        assert "name" in act
        assert "stage" in act
        assert "date" in act
        assert "start" in act
        assert "end" in act
        assert "genre" in act
        # about should NOT be in summary
        assert "about" not in act

    @pytest.mark.asyncio
    async def test_filter_by_date(self, client: AsyncClient) -> None:
        resp = await client.get(ACTS_URL, params={"date": THU_DATE})
        assert resp.status_code == 200
        data = resp.json()
        assert all(a["date"] == THU_DATE for a in data["acts"])

    @pytest.mark.asyncio
    async def test_filter_by_stage(self, client: AsyncClient) -> None:
        resp = await client.get(ACTS_URL, params={"stage": FISH_FRY_PARTIAL})
        assert resp.status_code == 200
        data = resp.json()
        assert all(FISH_FRY_PARTIAL in a["stage"] for a in data["acts"])

    @pytest.mark.asyncio
    async def test_filter_by_stage_without_date_returns_all_matching(
        self, client: AsyncClient
    ) -> None:
        resp = await client.get(ACTS_URL, params={"stage": FISH_FRY_PARTIAL})
        data = resp.json()
        # Fish Fry acts span multiple days
        dates = {a["date"] for a in data["acts"]}
        assert len(dates) > 1

    @pytest.mark.asyncio
    async def test_search(self, client: AsyncClient) -> None:
        resp = await client.get(ACTS_URL, params={"q": "brass"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] > 0

    @pytest.mark.asyncio
    async def test_search_takes_precedence_over_date(self, client: AsyncClient) -> None:
        resp = await client.get(ACTS_URL, params={"q": "brass", "date": THU_DATE})
        data = resp.json()
        # search ignores date filter — results may span multiple days
        assert data["count"] > 0


class TestGetAct:
    @pytest.mark.asyncio
    async def test_found(self, client: AsyncClient) -> None:
        resp = await client.get(f"{ACTS_URL}/{REBIRTH_SLUG}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == REBIRTH_NAME
        assert "about" in data
        assert "about_source" in data

    @pytest.mark.asyncio
    async def test_detail_includes_summary_fields(self, client: AsyncClient) -> None:
        resp = await client.get(f"{ACTS_URL}/{REBIRTH_SLUG}")
        data = resp.json()
        for field in ("slug", "name", "stage", "date", "start", "end", "genre"):
            assert field in data

    @pytest.mark.asyncio
    async def test_not_found(self, client: AsyncClient) -> None:
        resp = await client.get(f"{ACTS_URL}/{NONEXISTENT_SLUG}")
        assert resp.status_code == 404
