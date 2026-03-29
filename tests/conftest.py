"""Shared test fixtures."""

import os

import pytest

from fqf.models import ABITA, FRI, NEWORLEANS, THU, TROPICAL, Act, Genre, t

# Disable rate limiting globally for the test suite so that test suites making many
# rapid requests don't trip the per-IP limits. Individual rate-limit tests override
# this via monkeypatch when they need to exercise the limiting behavior.
os.environ["DISABLE_RATE_LIMIT"] = "1"


@pytest.fixture
def sample_acts() -> list[Act]:
    """A small set of acts for unit testing."""
    return [
        Act("Alpha Band", ABITA, THU, t(11, 0), t(12, 0)),
        Act("Beta Brass", NEWORLEANS, THU, t(11, 30), t(12, 30)),
        Act("Gamma Jazz", TROPICAL, THU, t(14, 0), t(15, 0), genre=Genre.JAZZ_TRADITIONAL),
        Act("Delta Blues", ABITA, FRI, t(11, 0), t(12, 0), genre=Genre.BLUES),
    ]
