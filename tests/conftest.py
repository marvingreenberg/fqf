"""Shared test fixtures."""

import pytest

from fqf.models import ABITA, FRI, NEWORLEANS, THU, TROPICAL, Act, Genre, t


@pytest.fixture
def sample_acts() -> list[Act]:
    """A small set of acts for unit testing."""
    return [
        Act("Alpha Band", ABITA, THU, t(11, 0), t(12, 0)),
        Act("Beta Brass", NEWORLEANS, THU, t(11, 30), t(12, 30)),
        Act("Gamma Jazz", TROPICAL, THU, t(14, 0), t(15, 0), genre=Genre.JAZZ_TRADITIONAL),
        Act("Delta Blues", ABITA, FRI, t(11, 0), t(12, 0), genre=Genre.BLUES),
    ]
