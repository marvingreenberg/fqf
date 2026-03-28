"""Tests for database CRUD operations in fqf.db."""

from unittest.mock import MagicMock, patch

import pytest

import fqf.db as db_module
from fqf.db import (
    MAX_RETRY_ATTEMPTS,
    NAME_FIELD,
    PICKS_FIELD,
    SHARE_ID_FIELD,
    SHARES_FIELD,
    add_share_to_schedule,
    close_pool,
    create_schedule,
    create_share_id,
    init_pool,
    load_multiple_schedules,
    load_schedule,
    load_schedule_by_share,
    remove_share_from_schedule,
    save_picks,
)

FAKE_TOKEN = "tremé-jazz-laissez"
SAMPLE_PICKS = ["rebirth-brass-band", "trombone-shorty"]
ANOTHER_TOKEN = "bywater-funk-krewe"
ANOTHER_PICKS = ["dr-john"]
SAMPLE_NAME = "My FQF Weekend"
SHARE_ID = "abcd1234"


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def reset_db_state():
    """Reset module-level db state before each test."""
    db_module._db = None
    db_module._memory_store = None
    yield
    db_module._db = None
    db_module._memory_store = None


def _mem_doc(
    picks: list[str],
    name: str = "",
    share_id: str = "",
    shares: list[dict] | None = None,
) -> dict:
    return {
        PICKS_FIELD: picks,
        NAME_FIELD: name,
        SHARE_ID_FIELD: share_id,
        SHARES_FIELD: shares if shares is not None else [],
    }


def _make_firestore_doc(*, exists: bool, data: dict | None = None) -> MagicMock:
    doc = MagicMock()
    doc.exists = exists
    doc.to_dict = MagicMock(return_value=data)
    return doc


def _make_firestore_client(*, get_doc: MagicMock | None = None) -> MagicMock:
    """Build a minimal Firestore client mock."""
    client = MagicMock()
    client.collection = MagicMock(return_value=MagicMock())

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
        db_module._memory_store = {FAKE_TOKEN: _mem_doc(list(SAMPLE_PICKS))}
        await close_pool()
        assert db_module._memory_store is None

    @pytest.mark.asyncio
    async def test_noop_when_nothing_initialized(self) -> None:
        await close_pool()  # should not raise


# ── In-memory path ────────────────────────────────────────────────────────────


class TestInMemoryCreateSchedule:
    @pytest.mark.asyncio
    async def test_returns_token_and_stores_empty_picks(self) -> None:
        db_module._memory_store = {}
        with patch("fqf.db.generate_token", return_value=FAKE_TOKEN):
            token = await create_schedule()
        assert token == FAKE_TOKEN
        assert db_module._memory_store[FAKE_TOKEN][PICKS_FIELD] == []

    @pytest.mark.asyncio
    async def test_stores_name_when_provided(self) -> None:
        db_module._memory_store = {}
        with patch("fqf.db.generate_token", return_value=FAKE_TOKEN):
            token = await create_schedule(name=SAMPLE_NAME)
        assert db_module._memory_store[token][NAME_FIELD] == SAMPLE_NAME

    @pytest.mark.asyncio
    async def test_name_defaults_to_empty_string(self) -> None:
        db_module._memory_store = {}
        with patch("fqf.db.generate_token", return_value=FAKE_TOKEN):
            token = await create_schedule()
        assert db_module._memory_store[token][NAME_FIELD] == ""

    @pytest.mark.asyncio
    async def test_multiple_tokens_are_independent(self) -> None:
        db_module._memory_store = {}
        with patch("fqf.db.generate_token", side_effect=[FAKE_TOKEN, ANOTHER_TOKEN]):
            t1 = await create_schedule()
            t2 = await create_schedule()
        assert t1 != t2
        assert FAKE_TOKEN in db_module._memory_store
        assert ANOTHER_TOKEN in db_module._memory_store

    @pytest.mark.asyncio
    async def test_retries_on_collision_and_succeeds(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc([])}
        with patch("fqf.db.generate_token", side_effect=[FAKE_TOKEN, ANOTHER_TOKEN]):
            token = await create_schedule()
        assert token == ANOTHER_TOKEN
        assert ANOTHER_TOKEN in db_module._memory_store

    @pytest.mark.asyncio
    async def test_raises_after_max_retries_exhausted(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc([])}
        collision_tokens = [FAKE_TOKEN] * MAX_RETRY_ATTEMPTS
        with patch("fqf.db.generate_token", side_effect=collision_tokens):
            with pytest.raises(RuntimeError, match="unique schedule token"):
                await create_schedule()


class TestInMemoryLoadSchedule:
    @pytest.mark.asyncio
    async def test_returns_picks_and_name_for_existing_token(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc(list(SAMPLE_PICKS), name=SAMPLE_NAME)}
        result = await load_schedule(FAKE_TOKEN)
        assert result == (SAMPLE_PICKS, SAMPLE_NAME, [])

    @pytest.mark.asyncio
    async def test_returns_none_for_missing_token(self) -> None:
        db_module._memory_store = {}
        result = await load_schedule("no-such-token")
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_empty_picks_and_empty_name_for_blank_doc(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc([])}
        result = await load_schedule(FAKE_TOKEN)
        assert result == ([], "", [])

    @pytest.mark.asyncio
    async def test_returns_shares_when_present(self) -> None:
        share_entry = {SHARE_ID_FIELD: SHARE_ID, NAME_FIELD: "Friend"}
        db_module._memory_store = {
            FAKE_TOKEN: _mem_doc(list(SAMPLE_PICKS), shares=[share_entry])
        }
        result = await load_schedule(FAKE_TOKEN)
        assert result is not None
        picks, name, shares = result
        assert shares == [share_entry]

    @pytest.mark.asyncio
    async def test_returns_copy_not_reference(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc(list(SAMPLE_PICKS))}
        result = await load_schedule(FAKE_TOKEN)
        assert result is not None
        picks, _, _shares = result
        picks.append("mutated")
        assert db_module._memory_store[FAKE_TOKEN][PICKS_FIELD] == SAMPLE_PICKS


class TestInMemorySavePicks:
    @pytest.mark.asyncio
    async def test_returns_true_on_update(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc([])}
        result = await save_picks(FAKE_TOKEN, SAMPLE_PICKS)
        assert result is True
        assert db_module._memory_store[FAKE_TOKEN][PICKS_FIELD] == SAMPLE_PICKS

    @pytest.mark.asyncio
    async def test_updates_name_when_provided(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc([], name="")}
        await save_picks(FAKE_TOKEN, SAMPLE_PICKS, name=SAMPLE_NAME)
        assert db_module._memory_store[FAKE_TOKEN][NAME_FIELD] == SAMPLE_NAME

    @pytest.mark.asyncio
    async def test_does_not_touch_name_when_none(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc([], name=SAMPLE_NAME)}
        await save_picks(FAKE_TOKEN, SAMPLE_PICKS, name=None)
        assert db_module._memory_store[FAKE_TOKEN][NAME_FIELD] == SAMPLE_NAME

    @pytest.mark.asyncio
    async def test_returns_false_for_missing_token(self) -> None:
        db_module._memory_store = {}
        result = await save_picks("ghost-token", SAMPLE_PICKS)
        assert result is False

    @pytest.mark.asyncio
    async def test_stores_copy_not_reference(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc([])}
        picks = list(SAMPLE_PICKS)
        await save_picks(FAKE_TOKEN, picks)
        picks.append("mutated")
        assert db_module._memory_store[FAKE_TOKEN][PICKS_FIELD] == SAMPLE_PICKS


class TestInMemoryLoadMultipleSchedules:
    @pytest.mark.asyncio
    async def test_returns_dict_keyed_by_token(self) -> None:
        db_module._memory_store = {
            FAKE_TOKEN: _mem_doc(list(SAMPLE_PICKS)),
            ANOTHER_TOKEN: _mem_doc(list(ANOTHER_PICKS)),
        }
        result = await load_multiple_schedules([FAKE_TOKEN, ANOTHER_TOKEN])
        assert result == {FAKE_TOKEN: SAMPLE_PICKS, ANOTHER_TOKEN: ANOTHER_PICKS}

    @pytest.mark.asyncio
    async def test_skips_missing_tokens(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc(list(SAMPLE_PICKS))}
        result = await load_multiple_schedules([FAKE_TOKEN, "nope"])
        assert result == {FAKE_TOKEN: SAMPLE_PICKS}

    @pytest.mark.asyncio
    async def test_returns_empty_dict_for_no_matches(self) -> None:
        db_module._memory_store = {}
        result = await load_multiple_schedules(["nope-a", "nope-b"])
        assert result == {}


# ── In-memory: create_share_id ────────────────────────────────────────────────


class TestInMemoryCreateShareId:
    @pytest.mark.asyncio
    async def test_generates_and_stores_share_id(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc([])}
        share_id = await create_share_id(FAKE_TOKEN)
        assert share_id == db_module._memory_store[FAKE_TOKEN][SHARE_ID_FIELD]
        assert len(share_id) == 8  # 4 bytes → 8 hex chars

    @pytest.mark.asyncio
    async def test_returns_existing_share_id_on_second_call(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc([], share_id=SHARE_ID)}
        share_id = await create_share_id(FAKE_TOKEN)
        assert share_id == SHARE_ID

    @pytest.mark.asyncio
    async def test_raises_key_error_for_missing_token(self) -> None:
        db_module._memory_store = {}
        with pytest.raises(KeyError):
            await create_share_id("no-such-token")


# ── In-memory: load_schedule_by_share ────────────────────────────────────────


class TestInMemoryLoadScheduleByShare:
    @pytest.mark.asyncio
    async def test_returns_token_picks_name_when_found(self) -> None:
        db_module._memory_store = {
            FAKE_TOKEN: _mem_doc(list(SAMPLE_PICKS), name=SAMPLE_NAME, share_id=SHARE_ID)
        }
        result = await load_schedule_by_share(SHARE_ID)
        assert result == (FAKE_TOKEN, SAMPLE_PICKS, SAMPLE_NAME)

    @pytest.mark.asyncio
    async def test_returns_none_when_not_found(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc(list(SAMPLE_PICKS))}
        result = await load_schedule_by_share("deadbeef")
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_for_empty_store(self) -> None:
        db_module._memory_store = {}
        result = await load_schedule_by_share(SHARE_ID)
        assert result is None


# ── Firestore path ────────────────────────────────────────────────────────────


class TestFirestoreCreateSchedule:
    @pytest.mark.asyncio
    async def test_calls_set_on_new_doc(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        existing_doc = _make_firestore_doc(exists=False)
        fake_client.collection().document().get.return_value = existing_doc

        with patch("fqf.db.generate_token", return_value=FAKE_TOKEN):
            token = await create_schedule()

        assert token == FAKE_TOKEN
        expected = {PICKS_FIELD: [], NAME_FIELD: "", SHARE_ID_FIELD: "", SHARES_FIELD: []}
        fake_client.collection().document().set.assert_called_once_with(expected)

    @pytest.mark.asyncio
    async def test_stores_name_field(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        existing_doc = _make_firestore_doc(exists=False)
        fake_client.collection().document().get.return_value = existing_doc

        with patch("fqf.db.generate_token", return_value=FAKE_TOKEN):
            await create_schedule(name=SAMPLE_NAME)

        expected = {PICKS_FIELD: [], NAME_FIELD: SAMPLE_NAME, SHARE_ID_FIELD: "", SHARES_FIELD: []}
        fake_client.collection().document().set.assert_called_once_with(expected)

    @pytest.mark.asyncio
    async def test_retries_on_collision_and_succeeds(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        collision_doc = _make_firestore_doc(exists=True)
        new_doc = _make_firestore_doc(exists=False)

        doc_ref_collision = MagicMock()
        doc_ref_collision.get.return_value = collision_doc
        doc_ref_new = MagicMock()
        doc_ref_new.get.return_value = new_doc

        fake_client.collection().document.side_effect = [doc_ref_collision, doc_ref_new]

        with patch("fqf.db.generate_token", side_effect=[FAKE_TOKEN, ANOTHER_TOKEN]):
            token = await create_schedule()

        assert token == ANOTHER_TOKEN
        expected = {PICKS_FIELD: [], NAME_FIELD: "", SHARE_ID_FIELD: "", SHARES_FIELD: []}
        doc_ref_new.set.assert_called_once_with(expected)

    @pytest.mark.asyncio
    async def test_raises_after_max_retries_exhausted(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        collision_doc = _make_firestore_doc(exists=True)
        fake_client.collection().document().get.return_value = collision_doc

        collision_tokens = [FAKE_TOKEN] * MAX_RETRY_ATTEMPTS
        with patch("fqf.db.generate_token", side_effect=collision_tokens):
            with pytest.raises(RuntimeError, match="unique schedule token"):
                await create_schedule()


class TestFirestoreLoadSchedule:
    @pytest.mark.asyncio
    async def test_returns_picks_and_name_for_existing_token(self) -> None:
        data = {PICKS_FIELD: list(SAMPLE_PICKS), NAME_FIELD: SAMPLE_NAME}
        doc = _make_firestore_doc(exists=True, data=data)
        fake_client = MagicMock()
        fake_client.collection().document().get.return_value = doc
        db_module._db = fake_client

        result = await load_schedule(FAKE_TOKEN)
        assert result == (SAMPLE_PICKS, SAMPLE_NAME, [])

    @pytest.mark.asyncio
    async def test_returns_shares_when_present(self) -> None:
        share_entry = {SHARE_ID_FIELD: SHARE_ID, NAME_FIELD: "Friend"}
        data = {PICKS_FIELD: list(SAMPLE_PICKS), NAME_FIELD: SAMPLE_NAME, SHARES_FIELD: [share_entry]}
        doc = _make_firestore_doc(exists=True, data=data)
        fake_client = MagicMock()
        fake_client.collection().document().get.return_value = doc
        db_module._db = fake_client

        result = await load_schedule(FAKE_TOKEN)
        assert result is not None
        picks, name, shares = result
        assert shares == [share_entry]

    @pytest.mark.asyncio
    async def test_returns_none_for_missing_doc(self) -> None:
        doc = _make_firestore_doc(exists=False)
        fake_client = MagicMock()
        fake_client.collection().document().get.return_value = doc
        db_module._db = fake_client

        result = await load_schedule("no-such-token")
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_empty_picks_when_picks_absent(self) -> None:
        doc = _make_firestore_doc(exists=True, data={})
        fake_client = MagicMock()
        fake_client.collection().document().get.return_value = doc
        db_module._db = fake_client

        result = await load_schedule(FAKE_TOKEN)
        assert result == ([], "", [])

    @pytest.mark.asyncio
    async def test_returns_empty_when_data_is_none(self) -> None:
        doc = _make_firestore_doc(exists=True, data=None)
        fake_client = MagicMock()
        fake_client.collection().document().get.return_value = doc
        db_module._db = fake_client

        result = await load_schedule(FAKE_TOKEN)
        assert result == ([], "", [])


class TestFirestoreSavePicks:
    @pytest.mark.asyncio
    async def test_returns_true_and_calls_update(self) -> None:
        doc = _make_firestore_doc(exists=True, data={PICKS_FIELD: []})
        doc_ref = MagicMock()
        doc_ref.get.return_value = doc
        fake_client = MagicMock()
        fake_client.collection().document.return_value = doc_ref
        db_module._db = fake_client

        result = await save_picks(FAKE_TOKEN, SAMPLE_PICKS)

        assert result is True
        doc_ref.update.assert_called_once_with({PICKS_FIELD: list(SAMPLE_PICKS)})

    @pytest.mark.asyncio
    async def test_includes_name_in_update_when_provided(self) -> None:
        doc = _make_firestore_doc(exists=True, data={PICKS_FIELD: []})
        doc_ref = MagicMock()
        doc_ref.get.return_value = doc
        fake_client = MagicMock()
        fake_client.collection().document.return_value = doc_ref
        db_module._db = fake_client

        await save_picks(FAKE_TOKEN, SAMPLE_PICKS, name=SAMPLE_NAME)

        doc_ref.update.assert_called_once_with(
            {PICKS_FIELD: list(SAMPLE_PICKS), NAME_FIELD: SAMPLE_NAME}
        )

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
            FAKE_TOKEN: _make_firestore_doc(exists=True, data={PICKS_FIELD: list(SAMPLE_PICKS)}),
            ANOTHER_TOKEN: _make_firestore_doc(
                exists=True, data={PICKS_FIELD: list(ANOTHER_PICKS)}
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


# ── Firestore: create_share_id ────────────────────────────────────────────────


class TestFirestoreCreateShareId:
    @pytest.mark.asyncio
    async def test_generates_and_stores_share_id(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        doc_data = {PICKS_FIELD: [], NAME_FIELD: "", SHARE_ID_FIELD: ""}
        doc = _make_firestore_doc(exists=True, data=doc_data)
        doc_ref = MagicMock()
        doc_ref.get.return_value = doc
        fake_client.collection().document.return_value = doc_ref

        with patch("fqf.db.secrets.token_hex", return_value=SHARE_ID):
            share_id = await create_share_id(FAKE_TOKEN)

        assert share_id == SHARE_ID
        doc_ref.update.assert_called_once_with({SHARE_ID_FIELD: SHARE_ID})

    @pytest.mark.asyncio
    async def test_returns_existing_share_id_without_update(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        doc_data = {PICKS_FIELD: [], NAME_FIELD: "", SHARE_ID_FIELD: SHARE_ID}
        doc = _make_firestore_doc(exists=True, data=doc_data)
        doc_ref = MagicMock()
        doc_ref.get.return_value = doc
        fake_client.collection().document.return_value = doc_ref

        share_id = await create_share_id(FAKE_TOKEN)

        assert share_id == SHARE_ID
        doc_ref.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_key_error_for_missing_doc(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        doc = _make_firestore_doc(exists=False)
        doc_ref = MagicMock()
        doc_ref.get.return_value = doc
        fake_client.collection().document.return_value = doc_ref

        with pytest.raises(KeyError):
            await create_share_id("no-such-token")


# ── Firestore: load_schedule_by_share ────────────────────────────────────────


class TestFirestoreLoadScheduleByShare:
    @pytest.mark.asyncio
    async def test_returns_token_picks_name_when_found(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        doc = _make_firestore_doc(
            exists=True,
            data={PICKS_FIELD: list(SAMPLE_PICKS), NAME_FIELD: SAMPLE_NAME},
        )
        doc.id = FAKE_TOKEN
        fake_client.collection().where().limit().get.return_value = [doc]

        result = await load_schedule_by_share(SHARE_ID)
        assert result == (FAKE_TOKEN, SAMPLE_PICKS, SAMPLE_NAME)

    @pytest.mark.asyncio
    async def test_returns_none_when_query_empty(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        fake_client.collection().where().limit().get.return_value = []

        result = await load_schedule_by_share("deadbeef")
        assert result is None


# ── In-memory: add_share_to_schedule ─────────────────────────────────────────


SHARE_NAME = "Friend"


class TestInMemoryAddShareToSchedule:
    @pytest.mark.asyncio
    async def test_adds_share_and_returns_true(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc([])}
        result = await add_share_to_schedule(FAKE_TOKEN, SHARE_ID, SHARE_NAME)
        assert result is True
        shares = db_module._memory_store[FAKE_TOKEN][SHARES_FIELD]
        assert shares == [{SHARE_ID_FIELD: SHARE_ID, NAME_FIELD: SHARE_NAME}]

    @pytest.mark.asyncio
    async def test_deduplicates_by_share_id(self) -> None:
        existing = [{SHARE_ID_FIELD: SHARE_ID, NAME_FIELD: SHARE_NAME}]
        db_module._memory_store = {FAKE_TOKEN: _mem_doc([], shares=existing)}
        await add_share_to_schedule(FAKE_TOKEN, SHARE_ID, SHARE_NAME)
        assert len(db_module._memory_store[FAKE_TOKEN][SHARES_FIELD]) == 1

    @pytest.mark.asyncio
    async def test_returns_false_for_missing_token(self) -> None:
        db_module._memory_store = {}
        result = await add_share_to_schedule("ghost-token", SHARE_ID, SHARE_NAME)
        assert result is False


# ── In-memory: remove_share_from_schedule ────────────────────────────────────


class TestInMemoryRemoveShareFromSchedule:
    @pytest.mark.asyncio
    async def test_removes_share_and_returns_true(self) -> None:
        existing = [{SHARE_ID_FIELD: SHARE_ID, NAME_FIELD: SHARE_NAME}]
        db_module._memory_store = {FAKE_TOKEN: _mem_doc([], shares=existing)}
        result = await remove_share_from_schedule(FAKE_TOKEN, SHARE_ID)
        assert result is True
        assert db_module._memory_store[FAKE_TOKEN][SHARES_FIELD] == []

    @pytest.mark.asyncio
    async def test_noop_when_share_id_not_present(self) -> None:
        db_module._memory_store = {FAKE_TOKEN: _mem_doc([])}
        result = await remove_share_from_schedule(FAKE_TOKEN, "not-there")
        assert result is True
        assert db_module._memory_store[FAKE_TOKEN][SHARES_FIELD] == []

    @pytest.mark.asyncio
    async def test_returns_false_for_missing_token(self) -> None:
        db_module._memory_store = {}
        result = await remove_share_from_schedule("ghost-token", SHARE_ID)
        assert result is False


# ── Firestore: add_share_to_schedule ─────────────────────────────────────────


class TestFirestoreAddShareToSchedule:
    @pytest.mark.asyncio
    async def test_adds_share_and_updates_doc(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        doc_data = {PICKS_FIELD: [], NAME_FIELD: "", SHARES_FIELD: []}
        doc = _make_firestore_doc(exists=True, data=doc_data)
        doc_ref = MagicMock()
        doc_ref.get.return_value = doc
        fake_client.collection().document.return_value = doc_ref

        result = await add_share_to_schedule(FAKE_TOKEN, SHARE_ID, SHARE_NAME)

        assert result is True
        expected_shares = [{SHARE_ID_FIELD: SHARE_ID, NAME_FIELD: SHARE_NAME}]
        doc_ref.update.assert_called_once_with({SHARES_FIELD: expected_shares})

    @pytest.mark.asyncio
    async def test_does_not_update_when_share_already_exists(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        existing = [{SHARE_ID_FIELD: SHARE_ID, NAME_FIELD: SHARE_NAME}]
        doc_data = {PICKS_FIELD: [], NAME_FIELD: "", SHARES_FIELD: existing}
        doc = _make_firestore_doc(exists=True, data=doc_data)
        doc_ref = MagicMock()
        doc_ref.get.return_value = doc
        fake_client.collection().document.return_value = doc_ref

        result = await add_share_to_schedule(FAKE_TOKEN, SHARE_ID, SHARE_NAME)

        assert result is True
        doc_ref.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_returns_false_for_missing_doc(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        doc = _make_firestore_doc(exists=False)
        doc_ref = MagicMock()
        doc_ref.get.return_value = doc
        fake_client.collection().document.return_value = doc_ref

        result = await add_share_to_schedule("ghost-token", SHARE_ID, SHARE_NAME)
        assert result is False


# ── Firestore: remove_share_from_schedule ────────────────────────────────────


class TestFirestoreRemoveShareFromSchedule:
    @pytest.mark.asyncio
    async def test_removes_share_and_updates_doc(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        existing = [{SHARE_ID_FIELD: SHARE_ID, NAME_FIELD: SHARE_NAME}]
        doc_data = {PICKS_FIELD: [], NAME_FIELD: "", SHARES_FIELD: existing}
        doc = _make_firestore_doc(exists=True, data=doc_data)
        doc_ref = MagicMock()
        doc_ref.get.return_value = doc
        fake_client.collection().document.return_value = doc_ref

        result = await remove_share_from_schedule(FAKE_TOKEN, SHARE_ID)

        assert result is True
        doc_ref.update.assert_called_once_with({SHARES_FIELD: []})

    @pytest.mark.asyncio
    async def test_returns_false_for_missing_doc(self) -> None:
        fake_client = MagicMock()
        db_module._db = fake_client

        doc = _make_firestore_doc(exists=False)
        doc_ref = MagicMock()
        doc_ref.get.return_value = doc
        fake_client.collection().document.return_value = doc_ref

        result = await remove_share_from_schedule("ghost-token", SHARE_ID)
        assert result is False
