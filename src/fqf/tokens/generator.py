"""Generate and validate NOLA-themed schedule tokens."""

import hashlib
import re
import secrets

from fqf.tokens.words import POOL_MUSIC, POOL_NOLA, POOL_PLACES

TOKEN_WORD_COUNT = 3
_TOKEN_PATTERN = re.compile(r"^[a-z]+-[a-z]+-[a-z]+$")

# Byte slice sizes for extracting pool indices from a SHA-256 digest
_HASH_SLICE_SIZE = 4

# Separator inserted between fingerprint_hash and counter in the SHA-256 input,
# preventing collisions like (fp="a", counter=12) == (fp="a1", counter=2).
FINGERPRINT_HASH_SEPARATOR = ":"


def generate_token() -> str:
    """Generate a random three-word NOLA-themed token (words in sorted order)."""
    place = secrets.choice(POOL_PLACES)
    music = secrets.choice(POOL_MUSIC)
    nola = secrets.choice(POOL_NOLA)
    return "-".join(sorted([place, music, nola]))


def generate_token_deterministic(fingerprint_hash: str, counter: int) -> str:
    """Generate a deterministic token from a fingerprint hash and counter.

    Uses SHA256(fingerprint_hash + ":" + str(counter)) to seed word selection.
    Words are sorted alphabetically in the resulting token.
    """
    seed = f"{fingerprint_hash}{FINGERPRINT_HASH_SEPARATOR}{counter}"
    digest = hashlib.sha256(seed.encode()).digest()
    place_idx = int.from_bytes(digest[0:_HASH_SLICE_SIZE], "big") % len(POOL_PLACES)
    music_idx = int.from_bytes(digest[_HASH_SLICE_SIZE : _HASH_SLICE_SIZE * 2], "big") % len(
        POOL_MUSIC
    )
    nola_idx = int.from_bytes(digest[_HASH_SLICE_SIZE * 2 : _HASH_SLICE_SIZE * 3], "big") % len(
        POOL_NOLA
    )
    words = sorted([POOL_PLACES[place_idx], POOL_MUSIC[music_idx], POOL_NOLA[nola_idx]])
    return "-".join(words)


def validate_token_format(token: str) -> bool:
    """Check if a string matches the expected token format."""
    if not _TOKEN_PATTERN.match(token):
        return False
    parts = token.split("-")
    return len(parts) == TOKEN_WORD_COUNT
