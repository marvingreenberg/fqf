"""Tests for NOLA-themed token generation, fuzzy resolution, and pool validation."""

import re

import pytest

from fqf.tokens.fuzzy import MAX_CORRECTION_DISTANCE, fuzzy_resolve, normalize_triple
from fqf.tokens.generator import (
    FINGERPRINT_HASH_SEPARATOR,
    generate_token,
    generate_token_deterministic,
    validate_token_format,
)
from fqf.tokens.words import (
    POOL_MUSIC,
    POOL_NOLA,
    POOL_PLACES,
    levenshtein_distance,
    validate_pools,
    validate_word_pools,
)

EXPECTED_MIN_POOL_SIZE = 90
TOKEN_PATTERN = re.compile(r"^[a-z]+-[a-z]+-[a-z]+$")
KNOWN_FINGERPRINT = "abc123"

# A word guaranteed to be in the pool (first entry of each pool)
KNOWN_PLACE = POOL_PLACES[0]
KNOWN_MUSIC = POOL_MUSIC[0]
KNOWN_NOLA = POOL_NOLA[0]

DETERMINISTIC_GENERATION_COUNT = 10_000


class TestWordPools:
    def test_places_pool_size(self) -> None:
        assert len(POOL_PLACES) >= EXPECTED_MIN_POOL_SIZE

    def test_music_pool_size(self) -> None:
        assert len(POOL_MUSIC) >= EXPECTED_MIN_POOL_SIZE

    def test_nola_pool_size(self) -> None:
        assert len(POOL_NOLA) >= EXPECTED_MIN_POOL_SIZE

    def test_no_duplicates_within_pools(self) -> None:
        for pool in [POOL_PLACES, POOL_MUSIC, POOL_NOLA]:
            assert len(pool) == len(set(pool))

    def test_all_lowercase_alpha(self) -> None:
        for pool in [POOL_PLACES, POOL_MUSIC, POOL_NOLA]:
            for word in pool:
                assert word == word.lower(), f"Word not lowercase: {word}"
                assert word.isalpha(), f"Word has non-alpha chars: {word}"


class TestGenerateToken:
    def test_format_three_words(self) -> None:
        token = generate_token()
        parts = token.split("-")
        assert len(parts) == 3

    def test_matches_pattern(self) -> None:
        token = generate_token()
        assert TOKEN_PATTERN.match(token), f"Token doesn't match pattern: {token}"

    def test_words_sorted(self) -> None:
        for _ in range(20):
            token = generate_token()
            parts = token.split("-")
            assert parts == sorted(parts), f"Random token words not sorted: {token}"

    def test_uniqueness_over_many_generations(self) -> None:
        # Pool has ~100^3 = 1,000,000 combinations; 100 draws have negligible collision probability.
        GENERATION_COUNT = 100
        tokens = {generate_token() for _ in range(GENERATION_COUNT)}
        assert len(tokens) == GENERATION_COUNT  # no collisions expected at this scale

    def test_words_from_pools(self) -> None:
        token = generate_token()
        parts = token.split("-")
        all_words = set(POOL_PLACES) | set(POOL_MUSIC) | set(POOL_NOLA)
        assert all(p in all_words for p in parts)


class TestValidateTokenFormat:
    def test_valid(self) -> None:
        assert validate_token_format("treme-funky-crawfish") is True

    def test_too_few_words(self) -> None:
        assert validate_token_format("treme-funky") is False

    def test_too_many_words(self) -> None:
        assert validate_token_format("treme-funky-crawfish-extra") is False

    def test_empty(self) -> None:
        assert validate_token_format("") is False

    def test_uppercase_rejected(self) -> None:
        assert validate_token_format("Treme-Funky-Crawfish") is False

    def test_numbers_rejected(self) -> None:
        assert validate_token_format("treme-funky-504") is False


class TestDeterministicGeneration:
    def test_same_inputs_produce_same_token(self) -> None:
        t1 = generate_token_deterministic(KNOWN_FINGERPRINT, 0)
        t2 = generate_token_deterministic(KNOWN_FINGERPRINT, 0)
        assert t1 == t2

    def test_different_fingerprints_produce_different_tokens(self) -> None:
        t1 = generate_token_deterministic("fingerprint-A", 0)
        t2 = generate_token_deterministic("fingerprint-B", 0)
        assert t1 != t2

    def test_different_counters_produce_different_tokens(self) -> None:
        t1 = generate_token_deterministic(KNOWN_FINGERPRINT, 0)
        t2 = generate_token_deterministic(KNOWN_FINGERPRINT, 1)
        assert t1 != t2

    def test_token_matches_format(self) -> None:
        token = generate_token_deterministic(KNOWN_FINGERPRINT, 0)
        assert TOKEN_PATTERN.match(token), f"Token doesn't match pattern: {token}"

    def test_words_sorted(self) -> None:
        for counter in range(20):
            token = generate_token_deterministic(KNOWN_FINGERPRINT, counter)
            parts = token.split("-")
            assert parts == sorted(parts), f"Token words not sorted: {token}"

    def test_words_come_from_pools(self) -> None:
        all_words = set(POOL_PLACES) | set(POOL_MUSIC) | set(POOL_NOLA)
        for counter in range(20):
            token = generate_token_deterministic(KNOWN_FINGERPRINT, counter)
            assert all(p in all_words for p in token.split("-"))

    def test_10k_different_inputs_produce_different_tokens(self) -> None:
        """Sanity-check distribution: 10K distinct inputs should yield mostly distinct tokens."""
        tokens = {
            generate_token_deterministic(f"fp-{i}", 0)
            for i in range(DETERMINISTIC_GENERATION_COUNT)
        }
        # With ~1M possible combinations, collision chance is negligible at 10K draws.
        assert len(tokens) > DETERMINISTIC_GENERATION_COUNT * 0.99


class TestNormalizeTriple:
    def test_hyphen_separated(self) -> None:
        assert normalize_triple("funky-treme-crawfish") == ["funky", "treme", "crawfish"]

    def test_space_separated(self) -> None:
        assert normalize_triple("funky treme crawfish") == ["funky", "treme", "crawfish"]

    def test_mixed_separators(self) -> None:
        assert normalize_triple("funky treme-crawfish") == ["funky", "treme", "crawfish"]

    def test_uppercase_lowercased(self) -> None:
        assert normalize_triple("Funky-Treme-Crawfish") == ["funky", "treme", "crawfish"]

    def test_extra_separators_ignored(self) -> None:
        assert normalize_triple("  funky -- treme  crawfish  ") == ["funky", "treme", "crawfish"]


class TestFuzzyResolve:
    def _make_exact_triple(self) -> str:
        """Build a raw string using real pool words."""
        return f"{KNOWN_PLACE}-{KNOWN_MUSIC}-{KNOWN_NOLA}"

    def test_exact_match_returns_no_suggestion(self) -> None:
        raw = f"{KNOWN_PLACE}-{KNOWN_MUSIC}-{KNOWN_NOLA}"
        token, suggestion = fuzzy_resolve(raw)
        assert suggestion is None
        parts = token.split("-")
        all_words = set(POOL_PLACES) | set(POOL_MUSIC) | set(POOL_NOLA)
        assert all(p in all_words for p in parts)

    def test_exact_match_token_is_sorted(self) -> None:
        raw = f"{KNOWN_PLACE}-{KNOWN_MUSIC}-{KNOWN_NOLA}"
        token, _ = fuzzy_resolve(raw)
        parts = token.split("-")
        assert parts == sorted(parts)

    def test_input_order_insensitive(self) -> None:
        """Same three pool words in different orders produce the same token."""
        words = [KNOWN_PLACE, KNOWN_MUSIC, KNOWN_NOLA]
        tokens = set()
        for perm in [
            f"{words[0]}-{words[1]}-{words[2]}",
            f"{words[2]}-{words[0]}-{words[1]}",
            f"{words[1]}-{words[2]}-{words[0]}",
        ]:
            token, _ = fuzzy_resolve(perm)
            tokens.add(token)
        assert len(tokens) == 1

    def test_one_char_typo_corrected_with_suggestion(self) -> None:
        # "treme" is in POOL_PLACES; "tremo" differs by 1 char
        raw = f"tremo-{KNOWN_MUSIC}-{KNOWN_NOLA}"
        token, suggestion = fuzzy_resolve(raw)
        assert suggestion is not None
        assert "Did you mean:" in suggestion
        assert "treme" in token or any(p == "treme" for p in token.split("-"))

    def test_two_char_typo_raises_value_error(self) -> None:
        # "xxyy" is not close to any pool word
        raw = f"xxyyzz-{KNOWN_MUSIC}-{KNOWN_NOLA}"
        with pytest.raises(ValueError):
            fuzzy_resolve(raw)

    def test_wrong_word_count_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Expected 3 words"):
            fuzzy_resolve("only-two")

    def test_too_many_words_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Expected 3 words"):
            fuzzy_resolve("one-two-three-four")

    def test_max_correction_distance_is_1(self) -> None:
        assert MAX_CORRECTION_DISTANCE == 1


class TestFingerprintHashSeparator:
    def test_separator_is_defined(self) -> None:
        assert isinstance(FINGERPRINT_HASH_SEPARATOR, str)
        assert len(FINGERPRINT_HASH_SEPARATOR) > 0

    def test_separator_prevents_collisions(self) -> None:
        """fp='a', counter=12 must differ from fp='a1', counter=2."""
        t1 = generate_token_deterministic("a", 12)
        t2 = generate_token_deterministic("a1", 2)
        assert t1 != t2


class TestLevenshteinDistance:
    def test_identical_strings_distance_zero(self) -> None:
        assert levenshtein_distance("crawfish", "crawfish") == 0

    def test_empty_vs_word(self) -> None:
        assert levenshtein_distance("", "abc") == 3

    def test_word_vs_empty(self) -> None:
        assert levenshtein_distance("abc", "") == 3

    def test_one_char_diff(self) -> None:
        assert levenshtein_distance("treme", "tremo") == 1

    def test_one_char_insertion(self) -> None:
        assert levenshtein_distance("funky", "funky1") == 1

    def test_two_char_diff(self) -> None:
        assert levenshtein_distance("jazz", "fizz") == 2

    def test_completely_different_words(self) -> None:
        assert levenshtein_distance("jazz", "zydecc") > 1


class TestValidateWordPools:
    def test_returns_list(self) -> None:
        result = validate_word_pools()
        assert isinstance(result, list)

    def test_each_entry_is_three_tuple(self) -> None:
        result = validate_word_pools()
        for entry in result:
            w1, w2, dist = entry
            assert isinstance(w1, str)
            assert isinstance(w2, str)
            assert isinstance(dist, int)
            assert dist <= 1

    def test_no_close_matches_across_pools(self) -> None:
        """No word pairs within edit distance 1 — fuzzy correction must be unambiguous."""
        conflicts = validate_word_pools()
        assert conflicts == [], (
            f"Found {len(conflicts)} ambiguous word pair(s) — rename the offending words. "
            f"Pairs: {conflicts[:5]}"
        )

    def test_validate_pools_is_alias(self) -> None:
        """validate_pools and validate_word_pools return the same result."""
        assert validate_pools() == validate_word_pools()


class TestValidatePools:
    def test_validate_pools_returns_list(self) -> None:
        result = validate_pools()
        assert isinstance(result, list)

    def test_each_entry_is_three_tuple(self) -> None:
        result = validate_pools()
        for entry in result:
            w1, w2, dist = entry
            assert isinstance(w1, str)
            assert isinstance(w2, str)
            assert isinstance(dist, int)
            assert dist <= 1

    def test_current_pools_have_no_ambiguous_pairs(self) -> None:
        """Warn if there are ambiguous word pairs — this is a design concern, not a hard failure.

        If this test fails it means two pool words are within edit distance 1 of each other,
        which can cause fuzzy_resolve to be ambiguous. Pools should be redesigned.
        """
        conflicts = validate_pools()
        assert conflicts == [], (
            f"Found {len(conflicts)} ambiguous word pair(s) in pools — fuzzy correction "
            f"may be unreliable. Pairs: {conflicts[:5]}"
        )
