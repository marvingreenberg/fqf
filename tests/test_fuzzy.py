"""Tests for the fuzzy triple token resolution module."""

import pytest

from fqf.tokens.fuzzy import find_closest_word, fuzzy_resolve, normalize_triple
from fqf.tokens.words import POOL_MUSIC, POOL_NOLA, POOL_PLACES

_ALL_POOLS: list[list[str]] = [POOL_PLACES, POOL_MUSIC, POOL_NOLA]

# ── normalize_triple ──────────────────────────────────────────────────────────

HYPHEN_TRIPLE = "foo-bar-baz"
SPACE_TRIPLE = "Foo Bar Baz"
MESSY_TRIPLE = "foo  bar--baz"
EXPECTED_NORMALIZED = ["foo", "bar", "baz"]


class TestNormalizeTriple:
    def test_hyphen_separated(self) -> None:
        assert normalize_triple(HYPHEN_TRIPLE) == EXPECTED_NORMALIZED

    def test_space_separated_and_lowercased(self) -> None:
        assert normalize_triple(SPACE_TRIPLE) == EXPECTED_NORMALIZED

    def test_mixed_separators(self) -> None:
        assert normalize_triple(MESSY_TRIPLE) == EXPECTED_NORMALIZED


# ── find_closest_word ────────────────────────────────────────────────────────

EXACT_PLACE = "treme"
EXACT_MUSIC = "funky"
EXACT_NOLA = "crawfish"

TYPO_ONE_CHAR = "funku"
CORRECTED_ONE_CHAR = "funky"

TYPO_TWO_CHAR = "zznky"


class TestFindClosestWord:
    def test_exact_match_distance_zero(self) -> None:
        word, dist = find_closest_word(EXACT_PLACE, _ALL_POOLS)
        assert word == EXACT_PLACE
        assert dist == 0

    def test_exact_match_music_pool(self) -> None:
        word, dist = find_closest_word(EXACT_MUSIC, _ALL_POOLS)
        assert word == EXACT_MUSIC
        assert dist == 0

    def test_exact_match_nola_pool(self) -> None:
        word, dist = find_closest_word(EXACT_NOLA, _ALL_POOLS)
        assert word == EXACT_NOLA
        assert dist == 0

    def test_one_char_typo_returns_distance_one(self) -> None:
        word, dist = find_closest_word(TYPO_ONE_CHAR, _ALL_POOLS)
        assert word == CORRECTED_ONE_CHAR
        assert dist == 1

    def test_two_char_diff_returns_distance_two_plus(self) -> None:
        _word, dist = find_closest_word(TYPO_TWO_CHAR, _ALL_POOLS)
        assert dist >= 2


# ── fuzzy_resolve ─────────────────────────────────────────────────────────────

EXACT_TRIPLE = "treme-funky-crawfish"
TYPO_TRIPLE = "treme-funku-crawfish"
REVERSED_TRIPLE = "crawfish-funky-treme"
UNRESOLVABLE_TRIPLE = "treme-zzzzz-crawfish"


class TestFuzzyResolve:
    def test_exact_match_no_suggestion(self) -> None:
        token, suggestion = fuzzy_resolve(EXACT_TRIPLE)
        assert suggestion is None
        # Token is sorted
        words = token.split("-")
        assert words == sorted(words)

    def test_typo_returns_suggestion(self) -> None:
        token, suggestion = fuzzy_resolve(TYPO_TRIPLE)
        assert suggestion is not None
        assert "funku" in suggestion
        assert "funky" in suggestion

    def test_sorted_output_consistent_regardless_of_order(self) -> None:
        token_forward, _ = fuzzy_resolve(EXACT_TRIPLE)
        token_reversed, _ = fuzzy_resolve(REVERSED_TRIPLE)
        assert token_forward == token_reversed

    def test_wrong_word_count_raises(self) -> None:
        with pytest.raises(ValueError):
            fuzzy_resolve("treme-funky")

    def test_unresolvable_word_raises(self) -> None:
        with pytest.raises(ValueError):
            fuzzy_resolve(UNRESOLVABLE_TRIPLE)
