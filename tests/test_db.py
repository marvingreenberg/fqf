"""Tests for database CRUD operations in fqf.db."""

from unittest.mock import MagicMock, patch

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


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def reset_db_state():
    """Reset module-level db state before each test."""
    db_module._db = None
    db_module._memory_store = None
    yield
    db_module._db = None
    db_module._memory_store = None


def _make_firestore_doc(*, exists: bool, data: dict | None = None) -> MagicMock:
    doc = MagicMock()
    doc.exists = exists
    doc.to_dict = MagicMock(return_value=data)
    return doc


def _make_firestore_client(*, get_doc: MagicMock | None = None) -> MagicMock:
    """Build a minimal Firestore client mock."""
    client = MagicMock()
    doc_ref = MagicMock()
    collection = MagicMock(return_value=MagicMock())
    client.collection = collection

    if get_doc is not None:
        client.collection.return_value.document.return_value.get.return_value = get_doc
        client.collection.return_value.document.return_value.set = MagicMock()
        client.collection.return_value.document.return_value.update = MagicMock()

    return client


# ── init_pool / close_pool ────────────────────────────────────────────────────


class TestInitPool:
    @pytest.mark.asyncio
    async def test_uses_memory_when_no_env_vars(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(db_module.FIRESTORE_EMULATOR_HOST_ENV, raising=False)
        monkeypatch.delenv(db_module.GCP_PROJECT_ENV, raising=False)

        # Prevent default credentials from succeeding
        with patch("google.cloud.firestore.Client", side_effect=Exception("no creds")):
            await init_pool()

        assert db_module._db is None
        assert db_module._memory_store == {}

    @pytest.mark.asyncio
    async def test_connects_to_emulator_when_env_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(db_module.FIRESTORE_EMULATOR_HOST_ENV, "localhost:8081")
        monkeypatch.delenv(db_module.GCP_PROJECT_ENV, raising=False)

        fake_client = MagicMock()
        with patch("google.cloud.firestore.Client", return_value=fake_client) as mock_client:
            await init_pool()

        mock_client.assert_called_once_with(project=db_module.FALLBACK_PROJECT_ID)
        assert db_module._db is fake_client
        assert db_module._memory_store is None

    @pytest.mark.asyncio
    async def test_connects_with_gcp_project(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(db_module.FIRESTORE_EMULATOR_HOST_ENV, raising=False)
        monkeypatch.setenv(db_module.GCP_PROJECT_ENV, "my-gcp-project")

        fake_client = MagicMock()
        with patch("google.cloud.firestore.Client", return_value=fake_client) as mock_client:
            await init_pool()

        mock_client.assert_called_once_with(project="my-gcp-project")
        assert db_module._db is fake_client

    @pytest.mark.asyncio
    async def test_connects_with_default_credentials(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(db_module.FIRESTORE_EMULATOR_HOST_ENV, raising=False)
        monkeypatch.delenv(db_module.GCP_PROJECT_ENV, raising=False)

        fake_client = MagicMock()
        with patch("google.cloud.firestore.Client", return_value=fake_client):
            await init_pool()

        assert db_module._db is fake_client
        assert db_module._memory_store is None

    @pytest.mark.asyncio
    async def test_emulator_uses_gcp_project_when_set(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv(db_module.FIRESTORE_EMULATOR_HOST_ENV, "localhost:8081")
        monkeypatch.setenv(db_module.GCP_PROJECT_ENV, "my-project")

        fake_client = MagicMock()
        with patch("google.cloud.firestore.Client", return_value=fake_client) as mock_client:
            await init_pool()

        mock_client.assert_called_once_with(project="my-project")


class TestClosePool:
    @pytest.mark.asyncio
    async def test_closes_and_clears_db(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client
        await close_pool()
        fake_client.close.assert_called_once()
        assert db_module._db is None

    @pytest.mark.asyncio
    async def test_clears_memory_store(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: SAMPLE_PICKS}
        await close_pool()
        assert db_module._memory_store is None

    @pytest.mark.asyncio
    async def test_noop_when_nothing_initialized(self) -> None:
        await close_pool()  # should not raise


# ── In-memory path (no mocking needed) ───────────────────────────────────────


class TestInMemoryCreateSchedule:
    @pytest.mark.asyncio
    async def test_returns_token_and_stores_empty_picks(self) -> None:
        db_module._memory_store = {}
        with patch("fqf.db.generate_token", return_value=FAKE_TOKEN):
            token = await create_schedule()
        assert token == FAKE_TOKEN
        assert db_module._memory_store[FAKE_TOKEN] == []

    @pytest.mark.asyncio
    async def test_multiple_tokens_are_independent(self) -> None:
        db_module._memory_store = {}
        with patch("fqf.db.generate_token", side_effect=[FAKE_TOKEN, ANOTHER_TOKEN]):
            t1 = await create_schedule()
            t2 = await create_schedule()
        assert t1 != t2
        assert FAKE_TOKEN in db_module._memory_store
        assert ANOTHER_TOKEN in db_module._memory_store


class TestInMemoryLoadSchedule:
    @pytest.mark.asyncio
    async def test_returns_picks_for_existing_token(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: list(SAMPLE_PICKS)}
        result = await load_schedule(FAKE_TOKEN)
        assert result == SAMPLE_PICKS

    @pytest.mark.asyncio
    async def test_returns_none_for_missing_token(self) -> None:
        db_module._memory_store = {}
        result = await load_schedule("no-such-token")
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_empty_list_for_empty_picks(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: []}
        result = await load_schedule(FAKE_TOKEN)
        assert result == []

    @pytest.mark.asyncio
    async def test_returns_copy_not_reference(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: list(SAMPLE_PICKS)}
        result = await load_schedule(FAKE_TOKEN)
        assert result is not None
        result.append("mutated")
        assert db_module._memory_store[FAKE_TOKEN] == SAMPLE_PICKS


class TestInMemorySavePicks:
    @pytest.mark.asyncio
    async def test_returns_true_on_update(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: []}
        result = await save_picks(FAKE_TOKEN, SAMPLE_PICKS)
        assert result is True
        assert db_module._memory_store[FAKE_TOKEN] == SAMPLE_PICKS

    @pytest.mark.asyncio
    async def test_returns_false_for_missing_token(self) -> None:
        db_module._memory_store = {}
        result = await save_picks("ghost-token", SAMPLE_PICKS)
        assert result is False

    @pytest.mark.asyncio
    async def test_stores_copy_not_reference(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: []}
        picks = list(SAMPLE_PICKS)
        await save_picks(FAKE_TOKEN, picks)
        picks.append("mutated")
        assert db_module._memory_store[FAKE_TOKEN] == SAMPLE_PICKS


class TestInMemoryLoadMultipleSchedules:
    @pytest.mark.asyncio
    async def test_returns_dict_keyed_by_token(self) -> None:
        db_module._memory_store = {
            FAKE_TOKEN: list(SAMPLE_PICKS),
            ANOTHER_TOKEN: list(ANOTHER_PICKS),
        }
        result = await load_multiple_schedules([FAKE_TOKEN, ANOTHER_TOKEN])
        assert result == {FAKE_TOKEN: SAMPLE_PICKS, ANOTHER_TOKEN: ANOTHER_PICKS}

    @pytest.mark.asyncio
    async def test_skips_missing_tokens(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: list(SAMPLE_PICKS)}
        result = await load_multiple_schedules([FAKE_TOKEN, "nope"])
        assert result == {FAKE_TOKEN: SAMPLE_PICKS}

    @pytest.mark.asyncio
    async def test_returns_empty_dict_for_no_matches(self) -> None:
        db_module._memory_store = {}
        result = await load_multiple_schedules(["nope-a", "nope-b"])
        assert result == {}


# ── Firestore path (mock the client) ─────────────────────────────────────────


class TestFirestoreCreateSchedule:
    @pytest.mark.asyncio
    async def test_calls_set_on_new_doc(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        with patch("fqf.db.generate_token", return_value=FAKE_TOKEN):
            token = await create_schedule()

        assert token == FAKE_TOKEN
        fake_client.collection.assert_called_with(db_module.SCHEDULES_COLLECTION)
        fake_client.collection().document.assert_called_with(FAKE_TOKEN)
        fake_client.collection().document().set.assert_called_once_with({db_module.PICKS_FIELD: []})


class TestFirestoreLoadSchedule:
    @pytest.mark.asyncio
    async def test_returns_picks_for_existing_token(self) -> None:
        doc = _make_firestore_doc(exists=True, data={db_module.PICKS_FIELD: list(SAMPLE_PICKS)})
        fake_client = MagicMock()
        fake_client.collection().document().get.return_value = doc
        db_module._db = fake_client

        result = await load_schedule(FAKE_TOKEN)
        assert result == SAMPLE_PICKS

    @pytest.mark.asyncio
    async def test_returns_none_for_missing_doc(self) -> None:
        doc = _make_firestore_doc(exists=False)
        fake_client = MagicMock()
        fake_client.collection().document().get.return_value = doc
        db_module._db = fake_client

        result = await load_schedule("no-such-token")
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_empty_list_when_picks_absent(self) -> None:
        doc = _make_firestore_doc(exists=True, data={})
        fake_client = MagicMock()
        fake_client.collection().document().get.return_value = doc
        db_module._db = fake_client

        result = await load_schedule(FAKE_TOKEN)
        assert result == []

    @pytest.mark.asyncio
    async def test_returns_empty_list_when_data_is_none(self) -> None:
        doc = _make_firestore_doc(exists=True, data=None)
        fake_client = MagicMock()
        fake_client.collection().document().get.return_value = doc
        db_module._db = fake_client

        result = await load_schedule(FAKE_TOKEN)
        assert result == []


class TestFirestoreSavePicks:
    @pytest.mark.asyncio
    async def test_returns_true_and_calls_update(self) -> None:
        doc = _make_firestore_doc(exists=True, data={db_module.PICKS_FIELD: []})
        doc_ref = MagicMock()
        doc_ref.get.return_value = doc
        fake_client = MagicMock()
        fake_client.collection().document.return_value = doc_ref
        db_module._db = fake_client

        result = await save_picks(FAKE_TOKEN, SAMPLE_PICKS)

        assert result is True
        doc_ref.update.assert_called_once_with({db_module.PICKS_FIELD: list(SAMPLE_PICKS)})

    @pytest.mark.asyncio
    async def test_returns_false_for_missing_doc(self) -> None:
        doc = _make_firestore_doc(exists=False)
        doc_ref = MagicMock()
        doc_ref.get.return_value = doc
        fake_client = MagicMock()
        fake_client.collection().document.return_value = doc_ref
        db_module._db = fake_client

        result = await save_picks("ghost-token", SAMPLE_PICKS)

        assert result is False
        doc_ref.update.assert_not_called()


class TestFirestoreLoadMultipleSchedules:
    @pytest.mark.asyncio
    async def test_returns_dict_for_existing_tokens(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        docs = {
            FAKE_TOKEN: _make_firestore_doc(
                exists=True, data={db_module.PICKS_FIELD: list(SAMPLE_PICKS)}
            ),
            ANOTHER_TOKEN: _make_firestore_doc(
                exists=True, data={db_module.PICKS_FIELD: list(ANOTHER_PICKS)}
            ),
        }

        def make_doc_ref(token: str) -> MagicMock:
            doc_ref = MagicMock()
            doc_ref.get.return_value = docs[token]
            return doc_ref

        fake_client.collection().document.side_effect = make_doc_ref

        result = await load_multiple_schedules([FAKE_TOKEN, ANOTHER_TOKEN])
        assert result == {FAKE_TOKEN: SAMPLE_PICKS, ANOTHER_TOKEN: ANOTHER_PICKS}

    @pytest.mark.asyncio
    async def test_skips_missing_tokens(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        missing_doc = _make_firestore_doc(exists=False)
        fake_client.collection().document().get.return_value = missing_doc

        result = await load_multiple_schedules(["nope-a"])
        assert result == {}

    @pytest.mark.asyncio
    async def test_returns_empty_dict_for_empty_token_list(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        result = await load_multiple_schedules([])
        assert result == {}
        fake_client.collection.assert_not_called()
