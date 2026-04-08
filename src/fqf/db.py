"""Firestore-backed schedule persistence.

Uses Google Cloud Firestore for storage. Automatically connects to the local
emulator when FIRESTORE_EMULATOR_HOST is set. Falls back to in-memory storage
when neither Firestore nor emulator is available.
"""

import logging
import os
import secrets
from typing import Any

from fqf.tokens.generator import generate_token, generate_token_deterministic

logger = logging.getLogger(__name__)

FIRESTORE_EMULATOR_HOST_ENV = "FIRESTORE_EMULATOR_HOST"
GCP_PROJECT_ENV = "GCP_PROJECT"
FALLBACK_PROJECT_ID = "fqf2026-local"
SCHEDULES_COLLECTION = "schedules"
PICKS_FIELD = "picks"
NAME_FIELD = "name"
SHARE_ID_FIELD = "share_id"
SHARES_FIELD = "shares"
SHARE_ID_BYTES = 4
MAX_RETRY_ATTEMPTS = 10

# Firestore client (lazy init). Typed as Any — the SDK's base class returns
# DocumentSnapshot | Awaitable[DocumentSnapshot] from .get(), but the sync
# client always returns DocumentSnapshot; Any avoids spurious union-attr errors.
_db: Any = None
# In-memory fallback: maps token -> {"picks": [...], "name": "...", "share_id": "...", "shares": [...]}
_memory_store: dict[str, dict[str, Any]] | None = None


def _using_memory() -> bool:
    return _memory_store is not None


async def init_pool() -> None:
    """Initialize Firestore client or fall back to in-memory."""
    global _db, _memory_store

    emulator_host = os.environ.get(FIRESTORE_EMULATOR_HOST_ENV)
    gcp_project = os.environ.get(GCP_PROJECT_ENV, "")

    if emulator_host:
        from google.cloud import firestore

        project_id = gcp_project or FALLBACK_PROJECT_ID
        logger.info(
            "Connecting to Firestore emulator at %s (project: %s)", emulator_host, project_id
        )
        _db = firestore.Client(project=project_id)
        return

    if gcp_project:
        from google.cloud import firestore

        logger.info("Connecting to Firestore (project: %s)", gcp_project)
        _db = firestore.Client(project=gcp_project)
        return

    # Try default credentials (Cloud Run injects these automatically)
    try:
        from google.cloud import firestore

        _db = firestore.Client()
        logger.info("Connected to Firestore with default credentials")
        return
    except Exception:
        pass

    logger.info("No Firestore available — using in-memory schedule storage")
    _memory_store = {}


async def close_pool() -> None:
    """Clean up resources."""
    global _db, _memory_store
    if _db is not None:
        _db.close()
        _db = None
    _memory_store = None


async def create_schedule(
    name: str = "", fingerprint_hash: str | None = None, counter: int = 0
) -> str:
    """Generate a unique token and create an empty schedule document.

    If fingerprint_hash is provided, generates a deterministic token via
    generate_token_deterministic(). If that token already exists (same device,
    same counter), returns the existing token — idempotent for the same input.
    Falls back to random generation when fingerprint_hash is None.
    Retries up to MAX_RETRY_ATTEMPTS times on token collision before raising
    (random path only; deterministic path never increments the counter).
    """
    if fingerprint_hash is not None:
        token = generate_token_deterministic(fingerprint_hash, counter)
        if _using_memory():
            assert _memory_store is not None
            if token not in _memory_store:
                _memory_store[token] = {
                    PICKS_FIELD: [],
                    NAME_FIELD: name,
                    SHARE_ID_FIELD: "",
                    SHARES_FIELD: [],
                }
            return token
        else:
            assert _db is not None
            doc_ref = _db.collection(SCHEDULES_COLLECTION).document(token)
            if not doc_ref.get().exists:
                doc_ref.set(
                    {PICKS_FIELD: [], NAME_FIELD: name, SHARE_ID_FIELD: "", SHARES_FIELD: []}
                )
            return token

    for attempt in range(MAX_RETRY_ATTEMPTS):
        token = generate_token()
        if _using_memory():
            assert _memory_store is not None
            if token not in _memory_store:
                _memory_store[token] = {
                    PICKS_FIELD: [],
                    NAME_FIELD: name,
                    SHARE_ID_FIELD: "",
                    SHARES_FIELD: [],
                }
                return token
        else:
            assert _db is not None
            doc_ref = _db.collection(SCHEDULES_COLLECTION).document(token)
            if not doc_ref.get().exists:
                doc_ref.set(
                    {PICKS_FIELD: [], NAME_FIELD: name, SHARE_ID_FIELD: "", SHARES_FIELD: []}
                )
                return token
        logger.warning("Token collision on attempt %d: %s", attempt + 1, token)

    raise RuntimeError(
        f"Failed to generate a unique schedule token after {MAX_RETRY_ATTEMPTS} attempts"
    )


async def load_schedule(
    token: str,
) -> tuple[list[str], str, list[dict[str, str]], str] | None:
    """Load picks, name, shares, and share_id for a token.

    Returns (picks, name, shares, share_id) or None if token doesn't exist.
    """
    if _using_memory():
        assert _memory_store is not None
        if token not in _memory_store:
            return None
        doc = _memory_store[token]
        shares: list[dict[str, str]] = list(doc.get(SHARES_FIELD, []))
        own_share_id: str = str(doc.get(SHARE_ID_FIELD, ""))
        return list(doc[PICKS_FIELD]), doc.get(NAME_FIELD, ""), shares, own_share_id
    assert _db is not None
    doc = _db.collection(SCHEDULES_COLLECTION).document(token).get()
    if not doc.exists:
        return None
    data = doc.to_dict()
    if not data:
        return [], "", [], ""
    fs_shares: list[dict[str, str]] = list(data.get(SHARES_FIELD, []))
    fs_share_id: str = str(data.get(SHARE_ID_FIELD, ""))
    return list(data.get(PICKS_FIELD, [])), data.get(NAME_FIELD, ""), fs_shares, fs_share_id


async def save_picks(token: str, picks: list[str], name: str | None = None) -> bool:
    """Update picks (and optionally name) for an existing token. Returns False if not found."""
    if _using_memory():
        assert _memory_store is not None
        if token not in _memory_store:
            return False
        _memory_store[token][PICKS_FIELD] = list(picks)
        if name is not None:
            _memory_store[token][NAME_FIELD] = name
        return True
    assert _db is not None
    doc_ref = _db.collection(SCHEDULES_COLLECTION).document(token)
    doc = doc_ref.get()
    if not doc.exists:
        return False
    update: dict[str, Any] = {PICKS_FIELD: list(picks)}
    if name is not None:
        update[NAME_FIELD] = name
    doc_ref.update(update)
    return True


async def create_share_id(token: str) -> str:
    """Generate and store a share_id for a schedule, returning the existing one if present."""
    if _using_memory():
        assert _memory_store is not None
        if token not in _memory_store:
            raise KeyError(f"Token not found: {token}")
        existing: str = str(_memory_store[token].get(SHARE_ID_FIELD, ""))
        if existing:
            return existing
        share_id = secrets.token_hex(SHARE_ID_BYTES)
        _memory_store[token][SHARE_ID_FIELD] = share_id
        return share_id
    assert _db is not None
    doc_ref = _db.collection(SCHEDULES_COLLECTION).document(token)
    doc = doc_ref.get()
    if not doc.exists:
        raise KeyError(f"Token not found: {token}")
    data = doc.to_dict() or {}
    fs_existing: str = str(data.get(SHARE_ID_FIELD, ""))
    if fs_existing:
        return fs_existing
    share_id = secrets.token_hex(SHARE_ID_BYTES)
    doc_ref.update({SHARE_ID_FIELD: share_id})
    return share_id


async def load_schedule_by_share(share_id: str) -> tuple[str, list[str], str] | None:
    """Look up a schedule by share_id. Returns (token, picks, name) or None if not found."""
    if _using_memory():
        assert _memory_store is not None
        for token, doc in _memory_store.items():
            if doc.get(SHARE_ID_FIELD) == share_id:
                return token, list(doc[PICKS_FIELD]), doc.get(NAME_FIELD, "")
        return None
    assert _db is not None
    results = (
        _db.collection(SCHEDULES_COLLECTION).where(SHARE_ID_FIELD, "==", share_id).limit(1).get()
    )
    for doc in results:
        data = doc.to_dict() or {}
        name: str = str(data.get(NAME_FIELD, ""))
        return doc.id, list(data.get(PICKS_FIELD, [])), name
    return None


async def add_share_to_schedule(token: str, share_id: str, share_name: str) -> bool:
    """Add a share reference to a user's schedule. Deduplicates by share_id.

    Returns False if token not found.
    """
    if _using_memory():
        assert _memory_store is not None
        if token not in _memory_store:
            return False
        existing: list[dict[str, str]] = _memory_store[token].setdefault(SHARES_FIELD, [])
        if not any(s[SHARE_ID_FIELD] == share_id for s in existing):
            existing.append({SHARE_ID_FIELD: share_id, NAME_FIELD: share_name})
        return True
    assert _db is not None
    doc_ref = _db.collection(SCHEDULES_COLLECTION).document(token)
    doc = doc_ref.get()
    if not doc.exists:
        return False
    data = doc.to_dict() or {}
    fs_shares: list[dict[str, str]] = list(data.get(SHARES_FIELD, []))
    if not any(s[SHARE_ID_FIELD] == share_id for s in fs_shares):
        fs_shares.append({SHARE_ID_FIELD: share_id, NAME_FIELD: share_name})
        doc_ref.update({SHARES_FIELD: fs_shares})
    return True


async def remove_share_from_schedule(token: str, share_id: str) -> bool:
    """Remove a share reference from a user's schedule.

    Returns False if token not found.
    """
    if _using_memory():
        assert _memory_store is not None
        if token not in _memory_store:
            return False
        existing = _memory_store[token].get(SHARES_FIELD, [])
        _memory_store[token][SHARES_FIELD] = [s for s in existing if s[SHARE_ID_FIELD] != share_id]
        return True
    assert _db is not None
    doc_ref = _db.collection(SCHEDULES_COLLECTION).document(token)
    doc = doc_ref.get()
    if not doc.exists:
        return False
    data = doc.to_dict() or {}
    fs_shares: list[dict[str, str]] = list(data.get(SHARES_FIELD, []))
    updated = [s for s in fs_shares if s[SHARE_ID_FIELD] != share_id]
    doc_ref.update({SHARES_FIELD: updated})
    return True


async def has_share_in_schedule(target_share_id: str, check_share_id: str) -> bool | None:
    """Check if check_share_id is in the shares list of the schedule identified by target_share_id.

    Returns True if present, False if not present, None if target not found.
    """
    if _using_memory():
        assert _memory_store is not None
        for _token, doc in _memory_store.items():
            if doc.get(SHARE_ID_FIELD) == target_share_id:
                shares: list[dict[str, str]] = doc.get(SHARES_FIELD, [])
                return any(s[SHARE_ID_FIELD] == check_share_id for s in shares)
        return None
    assert _db is not None
    results = (
        _db.collection(SCHEDULES_COLLECTION)
        .where(SHARE_ID_FIELD, "==", target_share_id)
        .limit(1)
        .get()
    )
    for doc in results:
        data = doc.to_dict() or {}
        fs_shares: list[dict[str, str]] = list(data.get(SHARES_FIELD, []))
        return any(s[SHARE_ID_FIELD] == check_share_id for s in fs_shares)
    return None


async def delete_schedule(token: str) -> bool:
    """Delete a schedule entirely. Returns False if token not found."""
    if _using_memory():
        assert _memory_store is not None
        if token not in _memory_store:
            return False
        del _memory_store[token]
        return True
    assert _db is not None
    doc_ref = _db.collection(SCHEDULES_COLLECTION).document(token)
    if not doc_ref.get().exists:
        return False
    doc_ref.delete()
    return True
