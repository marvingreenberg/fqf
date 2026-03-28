"""Tests for NOLA-themed token generation."""

import re

from fqf.tokens.generator import generate_token, validate_token_format
from fqf.tokens.words import POOL_MUSIC, POOL_NOLA, POOL_PLACES

EXPECTED_MIN_POOL_SIZE = 40
TOKEN_PATTERN = re.compile(r"^[a-z]+-[a-z]+-[a-z]+$")


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

    def test_uniqueness_over_many_generations(self) -> None:
        # Pool has 50^3 = 125,000 combinations; 50 draws have negligible collision probability.
        # Using 200 draws risks ~15% collision chance per run, making the test flaky.
        GENERATION_COUNT = 50
        tokens = {generate_token() for _ in range(GENERATION_COUNT)}
        assert len(tokens) == GENERATION_COUNT

    def test_words_from_pools(self) -> None:
        token = generate_token()
        parts = token.split("-")
        assert parts[0] in POOL_PLACES
        assert parts[1] in POOL_MUSIC
        assert parts[2] in POOL_NOLA


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
