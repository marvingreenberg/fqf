"""Fuzzy matching for NOLA-themed triple tokens."""

import re

from fqf.tokens.words import POOL_MUSIC, POOL_NOLA, POOL_PLACES, levenshtein_distance

_ALL_WORDS: list[str] = POOL_PLACES + POOL_MUSIC + POOL_NOLA

EXPECTED_WORD_COUNT = 3
MAX_CORRECTION_DISTANCE = 1

_SPLIT_PATTERN = re.compile(r"[^a-zA-Z]+")


def normalize_triple(raw: str) -> list[str]:
    """Split and lowercase a raw triple string into exactly 3 words.

    Splits on hyphens, spaces, or any non-alpha character.
    Raises ValueError if the result is not exactly 3 non-empty words.
    """
    words = [w for w in _SPLIT_PATTERN.split(raw.lower()) if w]
    if len(words) != EXPECTED_WORD_COUNT:
        raise ValueError(f"Expected {EXPECTED_WORD_COUNT} words, got {len(words)}: {raw!r}")
    return words


def correct_word(word: str) -> tuple[str, bool]:
    """Match a word to the closest pool word, correcting at most 1 edit.

    Returns (word, False) if exact match exists.
    Returns (closest_word, True) if closest match has distance <= 1.
    Raises ValueError if closest match has distance > 1.
    """
    if word in _ALL_WORDS:
        return word, False

    closest_word = min(_ALL_WORDS, key=lambda w: levenshtein_distance(word, w))
    distance = levenshtein_distance(word, closest_word)
    if distance <= MAX_CORRECTION_DISTANCE:
        return closest_word, True
    raise ValueError(
        f"Cannot match word {word!r}: closest is {closest_word!r} (distance {distance})"
    )


def fuzzy_resolve_triple(raw: str) -> tuple[str, str, bool]:
    """Resolve a raw triple string to canonical tokens.

    Returns (as_entered_token, sorted_token, was_corrected) where:
    - as_entered_token: corrected words joined with hyphens in input order
    - sorted_token: same words sorted alphabetically and joined with hyphens
    - was_corrected: True if any word required fuzzy correction

    Raises ValueError if the input doesn't have exactly 3 words or a word
    cannot be matched within 1 edit distance.
    """
    words = normalize_triple(raw)
    corrected_words = []
    any_corrected = False
    for word in words:
        resolved, was_corrected = correct_word(word)
        corrected_words.append(resolved)
        if was_corrected:
            any_corrected = True

    as_entered_token = "-".join(corrected_words)
    sorted_token = "-".join(sorted(corrected_words))
    return as_entered_token, sorted_token, any_corrected
