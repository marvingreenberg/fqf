"""Tests for schedule persistence API endpoints."""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from fqf.api.app import create_app

SCHEDULE_URL = "/api/v1/schedule"
MERGE_URL = "/api/v1/schedule/merge"
FUZZY_LOOKUP_URL = "/api/v1/schedule/fuzzy-lookup"

FAKE_TOKEN = "tremé-jazz-laissez"
OTHER_TOKEN = "bywater-funk-krewe"
SHARE_ID = "abcd1234"

# Real slugs from SCHEDULE so _slug_to_summary can resolve them
REAL_SLUG_1 = "kermit-ruffins-the-barbecue-swingers"
REAL_SLUG_2 = "rebirth-brass-band"
UNKNOWN_SLUG = "not-a-real-act"

SAMPLE_PICKS = [REAL_SLUG_1, REAL_SLUG_2]
ONE_UNKNOWN_PICK = [REAL_SLUG_1, UNKNOWN_SLUG]
SAMPLE_NAME = "My FQF Weekend"

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


SAMPLE_SHARE_RAW = [{"share_id": SHARE_ID, "name": "Friend"}]


class TestLoadSchedule:
    @pytest.mark.asyncio
    async def test_returns_200_with_picks_acts_and_name(self, client: AsyncClient) -> None:
        with patch(
            f"{DB_MODULE}.load_schedule",
            new=AsyncMock(return_value=(SAMPLE_PICKS, SAMPLE_NAME, [], "")),
        ):
            resp = await client.get(f"{SCHEDULE_URL}/{FAKE_TOKEN}")

        assert resp.status_code == 200
        data = resp.json()
        assert data["token"] == FAKE_TOKEN
        assert data["name"] == SAMPLE_NAME
        assert data["picks"] == SAMPLE_PICKS
        assert len(data["acts"]) == len(SAMPLE_PICKS)

    @pytest.mark.asyncio
    async def test_returns_shares_in_response(self, client: AsyncClient) -> None:
        with patch(
            f"{DB_MODULE}.load_schedule",
            new=AsyncMock(return_value=(SAMPLE_PICKS, SAMPLE_NAME, SAMPLE_SHARE_RAW, "")),
        ):
            resp = await client.get(f"{SCHEDULE_URL}/{FAKE_TOKEN}")

        data = resp.json()
        assert data["shares"] == [{"share_id": SHARE_ID, "name": "Friend"}]

    @pytest.mark.asyncio
    async def test_unknown_slugs_omitted_from_acts(self, client: AsyncClient) -> None:
        with patch(
            f"{DB_MODULE}.load_schedule",
            new=AsyncMock(return_value=(ONE_UNKNOWN_PICK, "", [], "")),
        ):
            resp = await client.get(f"{SCHEDULE_URL}/{FAKE_TOKEN}")

        data = resp.json()
        assert len(data["picks"]) == 2
        assert len(data["acts"]) == 1

    @pytest.mark.asyncio
    async def test_act_summary_shape(self, client: AsyncClient) -> None:
        with patch(
            f"{DB_MODULE}.load_schedule",
            new=AsyncMock(return_value=(SAMPLE_PICKS, "", [], "")),
        ):
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
        with patch(f"{DB_MODULE}.load_schedule", new=AsyncMock(return_value=([], "", [], ""))):
            resp = await client.get(f"{SCHEDULE_URL}/{FAKE_TOKEN}")
        data = resp.json()
        assert data["picks"] == []
        assert data["acts"] == []
        assert data["shares"] == []


# ── PUT /api/v1/schedule/{token} ──────────────────────────────────────────────


class TestSaveSchedule:
    @pytest.mark.asyncio
    async def test_returns_200_with_updated_picks(self, client: AsyncClient) -> None:
        with (
            patch(f"{DB_MODULE}.save_picks", new=AsyncMock(return_value=True)),
            patch(
                f"{DB_MODULE}.load_schedule",
                new=AsyncMock(return_value=(SAMPLE_PICKS, "", [], "")),
            ),
        ):
            resp = await client.put(f"{SCHEDULE_URL}/{FAKE_TOKEN}", json={"picks": SAMPLE_PICKS})

        assert resp.status_code == 200
        data = resp.json()
        assert data["token"] == FAKE_TOKEN
        assert data["picks"] == SAMPLE_PICKS
        assert len(data["acts"]) == len(SAMPLE_PICKS)

    @pytest.mark.asyncio
    async def test_name_field_in_body_is_passed_to_save_picks(self, client: AsyncClient) -> None:
        mock_save = AsyncMock(return_value=True)
        mock_load = AsyncMock(return_value=(SAMPLE_PICKS, SAMPLE_NAME, [], ""))
        with (
            patch(f"{DB_MODULE}.save_picks", new=mock_save),
            patch(f"{DB_MODULE}.load_schedule", new=mock_load),
        ):
            resp = await client.put(
                f"{SCHEDULE_URL}/{FAKE_TOKEN}",
                json={"picks": SAMPLE_PICKS, "name": SAMPLE_NAME},
            )

        assert resp.status_code == 200
        mock_save.assert_awaited_once_with(FAKE_TOKEN, SAMPLE_PICKS, SAMPLE_NAME)
        assert resp.json()["name"] == SAMPLE_NAME

    @pytest.mark.asyncio
    async def test_returns_404_when_token_not_found(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.save_picks", new=AsyncMock(return_value=False)):
            resp = await client.put(f"{SCHEDULE_URL}/{FAKE_TOKEN}", json={"picks": SAMPLE_PICKS})
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_unknown_slugs_omitted_from_acts(self, client: AsyncClient) -> None:
        with (
            patch(f"{DB_MODULE}.save_picks", new=AsyncMock(return_value=True)),
            patch(
                f"{DB_MODULE}.load_schedule",
                new=AsyncMock(return_value=(ONE_UNKNOWN_PICK, "", [], "")),
            ),
        ):
            resp = await client.put(
                f"{SCHEDULE_URL}/{FAKE_TOKEN}", json={"picks": ONE_UNKNOWN_PICK}
            )
        data = resp.json()
        assert len(data["picks"]) == 2
        assert len(data["acts"]) == 1


# ── POST /api/v1/schedule/{token}/share ───────────────────────────────────────


class TestShareSchedule:
    @pytest.mark.asyncio
    async def test_returns_200_with_share_id_and_url(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.create_share_id", new=AsyncMock(return_value=SHARE_ID)):
            resp = await client.post(f"{SCHEDULE_URL}/{FAKE_TOKEN}/share")

        assert resp.status_code == 200
        data = resp.json()
        assert data["share_id"] == SHARE_ID
        assert SHARE_ID in data["share_url"]

    @pytest.mark.asyncio
    async def test_returns_404_when_token_not_found(self, client: AsyncClient) -> None:
        with patch(
            f"{DB_MODULE}.create_share_id", new=AsyncMock(side_effect=KeyError("not found"))
        ):
            resp = await client.post(f"{SCHEDULE_URL}/{FAKE_TOKEN}/share")

        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_share_url_contains_share_path(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.create_share_id", new=AsyncMock(return_value=SHARE_ID)):
            resp = await client.post(f"{SCHEDULE_URL}/{FAKE_TOKEN}/share")

        data = resp.json()
        assert "/s/" in data["share_url"]


# ── GET /api/v1/schedule/by-share/{share_id} ─────────────────────────────────


class TestLoadByShare:
    @pytest.mark.asyncio
    async def test_returns_200_with_picks_and_name(self, client: AsyncClient) -> None:
        load_result = (FAKE_TOKEN, SAMPLE_PICKS, SAMPLE_NAME)
        with patch(f"{DB_MODULE}.load_schedule_by_share", new=AsyncMock(return_value=load_result)):
            resp = await client.get(f"{SCHEDULE_URL}/by-share/{SHARE_ID}")

        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == SAMPLE_NAME
        assert data["picks"] == SAMPLE_PICKS
        assert len(data["acts"]) == len(SAMPLE_PICKS)

    @pytest.mark.asyncio
    async def test_does_not_expose_token(self, client: AsyncClient) -> None:
        load_result = (FAKE_TOKEN, SAMPLE_PICKS, SAMPLE_NAME)
        with patch(f"{DB_MODULE}.load_schedule_by_share", new=AsyncMock(return_value=load_result)):
            resp = await client.get(f"{SCHEDULE_URL}/by-share/{SHARE_ID}")

        assert "token" not in resp.json()

    @pytest.mark.asyncio
    async def test_returns_404_when_share_id_not_found(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.load_schedule_by_share", new=AsyncMock(return_value=None)):
            resp = await client.get(f"{SCHEDULE_URL}/by-share/{SHARE_ID}")

        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_unknown_slugs_omitted_from_acts(self, client: AsyncClient) -> None:
        load_result = (FAKE_TOKEN, ONE_UNKNOWN_PICK, "")
        with patch(f"{DB_MODULE}.load_schedule_by_share", new=AsyncMock(return_value=load_result)):
            resp = await client.get(f"{SCHEDULE_URL}/by-share/{SHARE_ID}")

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


# ── POST /api/v1/schedule/{token}/add-share ───────────────────────────────────


class TestAddShare:
    @pytest.mark.asyncio
    async def test_returns_200_with_updated_shares(self, client: AsyncClient) -> None:
        loaded = (SAMPLE_PICKS, SAMPLE_NAME, SAMPLE_SHARE_RAW, "")
        with (
            patch(f"{DB_MODULE}.add_share_to_schedule", new=AsyncMock(return_value=True)),
            patch(f"{DB_MODULE}.load_schedule", new=AsyncMock(return_value=loaded)),
        ):
            resp = await client.post(
                f"{SCHEDULE_URL}/{FAKE_TOKEN}/add-share",
                json={"share_id": SHARE_ID, "name": "Friend"},
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["shares"] == [{"share_id": SHARE_ID, "name": "Friend"}]

    @pytest.mark.asyncio
    async def test_returns_404_when_token_not_found(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.add_share_to_schedule", new=AsyncMock(return_value=False)):
            resp = await client.post(
                f"{SCHEDULE_URL}/{FAKE_TOKEN}/add-share",
                json={"share_id": SHARE_ID, "name": "Friend"},
            )
        assert resp.status_code == 404


# ── DELETE /api/v1/schedule/{token}/remove-share/{share_id} ──────────────────


class TestRemoveShare:
    @pytest.mark.asyncio
    async def test_returns_200_with_share_removed(self, client: AsyncClient) -> None:
        loaded = (SAMPLE_PICKS, SAMPLE_NAME, [], "")
        with (
            patch(f"{DB_MODULE}.remove_share_from_schedule", new=AsyncMock(return_value=True)),
            patch(f"{DB_MODULE}.load_schedule", new=AsyncMock(return_value=loaded)),
        ):
            resp = await client.delete(f"{SCHEDULE_URL}/{FAKE_TOKEN}/remove-share/{SHARE_ID}")

        assert resp.status_code == 200
        assert resp.json()["shares"] == []

    @pytest.mark.asyncio
    async def test_returns_404_when_token_not_found(self, client: AsyncClient) -> None:
        with patch(f"{DB_MODULE}.remove_share_from_schedule", new=AsyncMock(return_value=False)):
            resp = await client.delete(f"{SCHEDULE_URL}/{FAKE_TOKEN}/remove-share/{SHARE_ID}")
        assert resp.status_code == 404


# ── POST /api/v1/schedule/fuzzy-lookup ───────────────────────────────────────

# Valid pool words for a resolvable triple
FUZZY_EXACT_TRIPLE = "treme-funky-crawfish"
FUZZY_SORTED_TOKEN = "crawfish-funky-treme"
FUZZY_TYPO_TRIPLE = "treme-funku-crawfish"  # "funku" → "funky"
FUZZY_OWNER_NAME = "Jazz Fan"

# A triple that's valid words but no schedule stored under that token
FUZZY_VALID_BUT_MISSING = "treme-jazzy-beignet"
FUZZY_SORTED_MISSING = "beignet-jazzy-treme"

# A triple with a word that can't be matched
FUZZY_BAD_WORD_TRIPLE = "treme-zzzzzzz-crawfish"


FUZZY_MODULE = "fqf.tokens.fuzzy"


class TestFuzzyLookup:
    @pytest.mark.asyncio
    async def test_exact_match_found(self, client: AsyncClient) -> None:
        """Exact triple that resolves to an existing schedule."""
        schedule_data = (SAMPLE_PICKS, FUZZY_OWNER_NAME, [], "")
        with patch(f"{DB_MODULE}.load_schedule", new=AsyncMock(return_value=schedule_data)):
            resp = await client.post(FUZZY_LOOKUP_URL, json={"raw_triple": FUZZY_EXACT_TRIPLE})

        assert resp.status_code == 200
        data = resp.json()
        assert data["found"] is True
        assert data["corrected"] is False
        assert data["name"] == FUZZY_OWNER_NAME
        assert data["token"] in (FUZZY_EXACT_TRIPLE, FUZZY_SORTED_TOKEN)

    @pytest.mark.asyncio
    async def test_typo_corrected_and_found(self, client: AsyncClient) -> None:
        """Triple with 1-char typo gets corrected and schedule is found."""
        schedule_data = (SAMPLE_PICKS, FUZZY_OWNER_NAME, [], "")
        # as_entered (corrected to treme-funky-crawfish) is found on first try
        with patch(f"{DB_MODULE}.load_schedule", new=AsyncMock(return_value=schedule_data)):
            resp = await client.post(FUZZY_LOOKUP_URL, json={"raw_triple": FUZZY_TYPO_TRIPLE})

        assert resp.status_code == 200
        data = resp.json()
        assert data["found"] is True
        assert data["corrected"] is True
        assert data["name"] == FUZZY_OWNER_NAME

    @pytest.mark.asyncio
    async def test_valid_words_but_schedule_not_found(self, client: AsyncClient) -> None:
        """Valid pool words but no schedule stored under that token."""
        with patch(f"{DB_MODULE}.load_schedule", new=AsyncMock(return_value=None)):
            resp = await client.post(FUZZY_LOOKUP_URL, json={"raw_triple": FUZZY_VALID_BUT_MISSING})

        assert resp.status_code == 200
        data = resp.json()
        assert data["found"] is False
        assert data["name"] == ""
        assert data["token"] in (FUZZY_VALID_BUT_MISSING, FUZZY_SORTED_MISSING)

    @pytest.mark.asyncio
    async def test_unresolvable_word_returns_400(self, client: AsyncClient) -> None:
        """Word with edit distance > 1 from all pool words returns 400."""
        resp = await client.post(FUZZY_LOOKUP_URL, json={"raw_triple": FUZZY_BAD_WORD_TRIPLE})
        assert resp.status_code == 400

    @pytest.mark.asyncio
    async def test_response_shape(self, client: AsyncClient) -> None:
        """Response always has all required fields."""
        with patch(f"{DB_MODULE}.load_schedule", new=AsyncMock(return_value=None)):
            resp = await client.post(FUZZY_LOOKUP_URL, json={"raw_triple": FUZZY_VALID_BUT_MISSING})

        assert resp.status_code == 200
        data = resp.json()
        for field in ("token", "corrected", "suggestion", "name", "found"):
            assert field in data
