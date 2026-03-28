"""Generate and validate NOLA-themed schedule tokens."""

import re
import secrets

from fqf.tokens.words import POOL_MUSIC, POOL_NOLA, POOL_PLACES

TOKEN_WORD_COUNT = 3
_TOKEN_PATTERN = re.compile(r"^[a-z]+-[a-z]+-[a-z]+$")


def generate_token() -> str:
    """Generate a random three-word NOLA-themed token."""
    place = secrets.choice(POOL_PLACES)
    music = secrets.choice(POOL_MUSIC)
    nola = secrets.choice(POOL_NOLA)
    return f"{place}-{music}-{nola}"


def validate_token_format(token: str) -> bool:
    """Check if a string matches the expected token format."""
    if not _TOKEN_PATTERN.match(token):
        return False
    parts = token.split("-")
    return len(parts) == TOKEN_WORD_COUNT
