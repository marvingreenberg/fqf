"""Tests for the fuzzy triple token resolution module."""

import pytest

from fqf.tokens.fuzzy import correct_word, fuzzy_resolve_triple, normalize_triple

# ── normalize_triple ──────────────────────────────────────────────────────────

HYPHEN_TRIPLE = "foo-bar-baz"
SPACE_TRIPLE = "Foo Bar Baz"
MESSY_TRIPLE = "foo  bar--baz"
EXPECTED_NORMALIZED = ["foo", "bar", "baz"]

TOO_FEW_WORDS = "only-two"
TOO_MANY_WORDS = "one-two-three-four"


class TestNormalizeTriple:
    def test_hyphen_separated(self) -> None:
        assert normalize_triple(HYPHEN_TRIPLE) == EXPECTED_NORMALIZED

    def test_space_separated_and_lowercased(self) -> None:
        assert normalize_triple(SPACE_TRIPLE) == EXPECTED_NORMALIZED

    def test_mixed_separators(self) -> None:
        assert normalize_triple(MESSY_TRIPLE) == EXPECTED_NORMALIZED

    def test_too_few_words_raises(self) -> None:
        with pytest.raises(ValueError):
            normalize_triple(TOO_FEW_WORDS)

    def test_too_many_words_raises(self) -> None:
        with pytest.raises(ValueError):
            normalize_triple(TOO_MANY_WORDS)


# ── correct_word ──────────────────────────────────────────────────────────────

# Exact words from the pools
EXACT_PLACE = "treme"
EXACT_MUSIC = "funky"
EXACT_NOLA = "crawfish"

# 1-char typo: "funky" → "funku"
TYPO_ONE_CHAR = "funku"
CORRECTED_ONE_CHAR = "funky"

# 2-char diff: "funky" → "zznky"
TYPO_TWO_CHAR = "zznky"


class TestCorrectWord:
    def test_exact_match_returns_no_correction(self) -> None:
        word, corrected = correct_word(EXACT_PLACE)
        assert word == EXACT_PLACE
        assert corrected is False

    def test_exact_match_music_pool(self) -> None:
        word, corrected = correct_word(EXACT_MUSIC)
        assert word == EXACT_MUSIC
        assert corrected is False

    def test_exact_match_nola_pool(self) -> None:
        word, corrected = correct_word(EXACT_NOLA)
        assert word == EXACT_NOLA
        assert corrected is False

    def test_one_char_typo_is_corrected(self) -> None:
        word, corrected = correct_word(TYPO_ONE_CHAR)
        assert word == CORRECTED_ONE_CHAR
        assert corrected is True

    def test_two_char_diff_raises(self) -> None:
        with pytest.raises(ValueError):
            correct_word(TYPO_TWO_CHAR)


# ── fuzzy_resolve_triple ──────────────────────────────────────────────────────

# All three are exact pool words: treme (POOL_PLACES), funky (POOL_MUSIC), crawfish (POOL_NOLA)
EXACT_TRIPLE = "treme-funky-crawfish"
SORTED_EXACT = "crawfish-funky-treme"

# One typo: "funku" instead of "funky"
TYPO_TRIPLE = "treme-funku-crawfish"

# Order-invariant: same words in different order
REVERSED_TRIPLE = "crawfish-funky-treme"


class TestFuzzyResolveTriple:
    def test_exact_match_no_correction(self) -> None:
        as_entered, sorted_tok, corrected = fuzzy_resolve_triple(EXACT_TRIPLE)
        assert as_entered == EXACT_TRIPLE
        assert sorted_tok == SORTED_EXACT
        assert corrected is False

    def test_typo_is_corrected(self) -> None:
        as_entered, sorted_tok, corrected = fuzzy_resolve_triple(TYPO_TRIPLE)
        assert as_entered == EXACT_TRIPLE
        assert sorted_tok == SORTED_EXACT
        assert corrected is True

    def test_sorted_output_is_consistent_regardless_of_order(self) -> None:
        _, sorted_forward, _ = fuzzy_resolve_triple(EXACT_TRIPLE)
        _, sorted_reversed, _ = fuzzy_resolve_triple(REVERSED_TRIPLE)
        assert sorted_forward == sorted_reversed

    def test_wrong_word_count_raises(self) -> None:
        with pytest.raises(ValueError):
            fuzzy_resolve_triple("treme-funky")

    def test_unresolvable_word_raises(self) -> None:
        # "zzzzz" is far from any pool word
        with pytest.raises(ValueError):
            fuzzy_resolve_triple("treme-zzzzz-crawfish")
