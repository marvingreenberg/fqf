"""Tests for stage API endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from fqf.api.app import create_app
from fqf.models import ALL_STAGES

STAGES_URL = "/api/v1/stages"
EXPECTED_STAGE_COUNT = 19
MIN_LAT = 29.94
MAX_LAT = 29.97
MIN_LNG = -90.08
MAX_LNG = -90.05


@pytest.fixture
def app():  # type: ignore[no-untyped-def]
    return create_app()


@pytest.fixture
async def client(app):  # type: ignore[no-untyped-def]
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


class TestListStages:
    @pytest.mark.asyncio
    async def test_returns_all_stages(self, client: AsyncClient) -> None:
        resp = await client.get(STAGES_URL)
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] == EXPECTED_STAGE_COUNT
        assert len(data["stages"]) == EXPECTED_STAGE_COUNT

    @pytest.mark.asyncio
    async def test_stage_shape(self, client: AsyncClient) -> None:
        resp = await client.get(STAGES_URL)
        stage = resp.json()["stages"][0]
        assert "name" in stage
        assert "lat" in stage
        assert "lng" in stage
        assert "order" in stage

    @pytest.mark.asyncio
    async def test_stage_names_match_constants(self, client: AsyncClient) -> None:
        resp = await client.get(STAGES_URL)
        api_names = {s["name"] for s in resp.json()["stages"]}
        assert api_names == set(ALL_STAGES)

    @pytest.mark.asyncio
    async def test_stages_in_geographic_order(self, client: AsyncClient) -> None:
        resp = await client.get(STAGES_URL)
        stages = resp.json()["stages"]
        orders = [s["order"] for s in stages]
        assert orders == sorted(orders)
        latitudes = [s["lat"] for s in stages]
        assert latitudes == sorted(latitudes)

    @pytest.mark.asyncio
    async def test_coordinates_in_new_orleans(self, client: AsyncClient) -> None:
        resp = await client.get(STAGES_URL)
        for stage in resp.json()["stages"]:
            assert MIN_LAT <= stage["lat"] <= MAX_LAT, f"{stage['name']} lat out of range"
            assert MIN_LNG <= stage["lng"] <= MAX_LNG, f"{stage['name']} lng out of range"
