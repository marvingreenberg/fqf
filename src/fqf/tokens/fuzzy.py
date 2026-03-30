"""Fuzzy resolution of raw word-triple input to canonical tokens."""

import re

from fqf.tokens.words import POOL_MUSIC, POOL_NOLA, POOL_PLACES

_ALL_POOLS: list[list[str]] = [POOL_PLACES, POOL_MUSIC, POOL_NOLA]

# Maximum Levenshtein distance allowed for a fuzzy correction
MAX_CORRECTION_DISTANCE = 1

_SPLIT_PATTERN = re.compile(r"[^a-zA-Z]+")


def _levenshtein(a: str, b: str) -> int:
    """Compute Levenshtein edit distance between two strings."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            curr[j] = min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = curr
    return prev[len(b)]


def normalize_triple(raw: str) -> list[str]:
    """Split on hyphens/spaces/non-alpha, lowercase, return list of words."""
    return [w.lower() for w in _SPLIT_PATTERN.split(raw) if w]


def find_closest_word(word: str, pools: list[list[str]]) -> tuple[str, int]:
    """Find the closest word across all pools.

    Returns (word, distance) where distance is the minimum Levenshtein distance found.
    Exact matches always return distance 0.
    """
    best_word = word
    best_dist = len(word) + 1  # worse than any real distance
    for pool in pools:
        for candidate in pool:
            dist = _levenshtein(word, candidate)
            if dist < best_dist:
                best_dist = dist
                best_word = candidate
    return best_word, best_dist


def fuzzy_resolve(raw: str) -> tuple[str, str | None]:
    """Resolve a raw triple input to a canonical token.

    Returns (resolved_token, suggestion_or_none).
    - If all words match exactly: (token, None)
    - If all words correct within MAX_CORRECTION_DISTANCE: (corrected_token, "Did you mean: ...")
    - If any word is too far from any pool word: raises ValueError
    """
    words = normalize_triple(raw)
    if len(words) != 3:
        raise ValueError(f"Expected 3 words, got {len(words)}: {raw!r}")

    corrected: list[str] = []
    corrections_made: list[str] = []

    for word in words:
        closest, dist = find_closest_word(word, _ALL_POOLS)
        if dist > MAX_CORRECTION_DISTANCE:
            raise ValueError(
                f"No pool word close enough to {word!r} (nearest: {closest!r}, dist={dist})"
            )
        corrected.append(closest)
        if dist > 0:
            corrections_made.append(f"{word!r} → {closest!r}")

    token = "-".join(sorted(corrected))
    if corrections_made:
        suggestion = "Did you mean: " + ", ".join(corrections_made)
        return token, suggestion
    return token, None
