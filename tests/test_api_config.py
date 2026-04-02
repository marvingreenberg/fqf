"""Tests for the festival config API endpoint."""

import pytest
from httpx import ASGITransport, AsyncClient

from fqf.api.app import create_app
from fqf.festival_config import (
    DAY_LABELS,
    FESTIVAL_DATES,
    FESTIVAL_NAME,
    FESTIVAL_SHORT_NAME,
    FESTIVAL_YEAR,
)

CONFIG_URL = "/api/v1/config"


@pytest.fixture
def app():  # type: ignore[no-untyped-def]
    return create_app()


@pytest.fixture
async def client(app):  # type: ignore[no-untyped-def]
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


class TestGetConfig:
    @pytest.mark.asyncio
    async def test_returns_200(self, client: AsyncClient) -> None:
        resp = await client.get(CONFIG_URL)
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_response_shape(self, client: AsyncClient) -> None:
        data = (await client.get(CONFIG_URL)).json()
        assert "name" in data
        assert "short_name" in data
        assert "year" in data
        assert "dates" in data
        assert "day_labels" in data

    @pytest.mark.asyncio
    async def test_festival_name(self, client: AsyncClient) -> None:
        data = (await client.get(CONFIG_URL)).json()
        assert data["name"] == FESTIVAL_NAME
        assert data["short_name"] == FESTIVAL_SHORT_NAME

    @pytest.mark.asyncio
    async def test_festival_year(self, client: AsyncClient) -> None:
        data = (await client.get(CONFIG_URL)).json()
        assert data["year"] == FESTIVAL_YEAR

    @pytest.mark.asyncio
    async def test_dates_are_iso_strings(self, client: AsyncClient) -> None:
        data = (await client.get(CONFIG_URL)).json()
        expected = [d.isoformat() for d in FESTIVAL_DATES]
        assert data["dates"] == expected

    @pytest.mark.asyncio
    async def test_day_labels_match_config(self, client: AsyncClient) -> None:
        data = (await client.get(CONFIG_URL)).json()
        assert data["day_labels"] == DAY_LABELS

    @pytest.mark.asyncio
    async def test_dates_and_day_labels_keys_align(self, client: AsyncClient) -> None:
        data = (await client.get(CONFIG_URL)).json()
        assert set(data["dates"]) == set(data["day_labels"].keys())
