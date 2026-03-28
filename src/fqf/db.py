"""Firestore-backed schedule persistence.

Uses Google Cloud Firestore for storage. Automatically connects to the local
emulator when FIRESTORE_EMULATOR_HOST is set. Falls back to in-memory storage
when neither Firestore nor emulator is available.
"""

import logging
import os
from typing import Any

from fqf.tokens.generator import generate_token

logger = logging.getLogger(__name__)

FIRESTORE_EMULATOR_HOST_ENV = "FIRESTORE_EMULATOR_HOST"
GCP_PROJECT_ENV = "GCP_PROJECT"
FALLBACK_PROJECT_ID = "fqf-local"
SCHEDULES_COLLECTION = "schedules"
PICKS_FIELD = "picks"

# Firestore client (lazy init). Typed as Any — the SDK's base class returns
# DocumentSnapshot | Awaitable[DocumentSnapshot] from .get(), but the sync
# client always returns DocumentSnapshot; Any avoids spurious union-attr errors.
_db: Any = None
# In-memory fallback
_memory_store: dict[str, list[str]] | None = None


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


async def create_schedule() -> str:
    """Generate a new token and create an empty schedule document."""
    token = generate_token()
    if _using_memory():
        assert _memory_store is not None
        _memory_store[token] = []
        return token
    assert _db is not None
    _db.collection(SCHEDULES_COLLECTION).document(token).set({PICKS_FIELD: []})
    return token


async def load_schedule(token: str) -> list[str] | None:
    """Load picks for a token. Returns None if token doesn't exist."""
    if _using_memory():
        assert _memory_store is not None
        if token not in _memory_store:
            return None
        return list(_memory_store[token])
    assert _db is not None
    doc = _db.collection(SCHEDULES_COLLECTION).document(token).get()
    if not doc.exists:
        return None
    data = doc.to_dict()
    return list(data.get(PICKS_FIELD, [])) if data else []


async def save_picks(token: str, picks: list[str]) -> bool:
    """Update picks for an existing token. Returns False if token not found."""
    if _using_memory():
        assert _memory_store is not None
        if token not in _memory_store:
            return False
        _memory_store[token] = list(picks)
        return True
    assert _db is not None
    doc_ref = _db.collection(SCHEDULES_COLLECTION).document(token)
    doc = doc_ref.get()
    if not doc.exists:
        return False
    doc_ref.update({PICKS_FIELD: list(picks)})
    return True


async def load_multiple_schedules(tokens: list[str]) -> dict[str, list[str]]:
    """Load picks for multiple tokens at once."""
    if _using_memory():
        assert _memory_store is not None
        return {t: list(_memory_store[t]) for t in tokens if t in _memory_store}
    assert _db is not None
    result: dict[str, list[str]] = {}
    for token in tokens:
        doc = _db.collection(SCHEDULES_COLLECTION).document(token).get()
        if doc.exists:
            data = doc.to_dict()
            result[token] = list(data.get(PICKS_FIELD, [])) if data else []
    return result
