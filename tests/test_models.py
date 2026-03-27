"""Tests for data models, enums, and constants."""

from datetime import date, time

from fqf.models import (
    ABITA,
    ALL_STAGES,
    FESTIVAL_DATES,
    FRI,
    NEWORLEANS,
    SAT,
    SUN,
    THU,
    AboutSource,
    Act,
    Genre,
    t,
)


class TestGenreEnum:
    def test_all_genres_have_string_values(self) -> None:
        for genre in Genre:
            assert isinstance(genre.value, str)
            assert len(genre.value) > 0

    def test_specific_values(self) -> None:
        assert Genre.BRASS_BAND == "Brass Band"
        assert Genre.JAZZ_TRADITIONAL == "Jazz (Traditional)"
        assert Genre.RNB_SOUL == "R&B / Soul"
        assert Genre.UNKNOWN == "Unknown"

    def test_genre_count(self) -> None:
        EXPECTED_GENRE_COUNT = 18  # 17 defined + Unknown
        assert len(Genre) == EXPECTED_GENRE_COUNT


class TestAboutSource:
    def test_values(self) -> None:
        assert AboutSource.RESEARCHED == "researched"
        assert AboutSource.GENERATED == "generated"
        assert AboutSource.NONE == ""


class TestDateConstants:
    def test_festival_dates(self) -> None:
        assert THU == date(2026, 4, 16)
        assert FRI == date(2026, 4, 17)
        assert SAT == date(2026, 4, 18)
        assert SUN == date(2026, 4, 19)

    def test_festival_dates_list(self) -> None:
        assert FESTIVAL_DATES == [THU, FRI, SAT, SUN]


class TestTimeHelper:
    def test_basic(self) -> None:
        assert t(14, 30) == time(14, 30)

    def test_zero_minutes(self) -> None:
        assert t(11, 0) == time(11, 0)


class TestStageConstants:
    def test_stage_count(self) -> None:
        EXPECTED_STAGE_COUNT = 19
        assert len(ALL_STAGES) == EXPECTED_STAGE_COUNT

    def test_no_duplicates(self) -> None:
        assert len(ALL_STAGES) == len(set(ALL_STAGES))


class TestAct:
    def test_basic_creation(self) -> None:
        act = Act("Rebirth Brass Band", ABITA, THU, t(17, 0), t(18, 20))
        assert act.name == "Rebirth Brass Band"
        assert act.stage == ABITA
        assert act.date == THU
        assert act.start == t(17, 0)
        assert act.end == t(18, 20)

    def test_slug_computed(self) -> None:
        act = Act("Rebirth Brass Band", ABITA, THU, t(17, 0), t(18, 20))
        assert act.slug == "rebirth-brass-band"

    def test_default_genre(self) -> None:
        act = Act("Test", ABITA, THU, t(11, 0), t(12, 0))
        assert act.genre == Genre.UNKNOWN

    def test_default_about(self) -> None:
        act = Act("Test", ABITA, THU, t(11, 0), t(12, 0))
        assert act.about == ""
        assert act.about_source == AboutSource.NONE

    def test_enriched_act(self) -> None:
        act = Act(
            "Rebirth Brass Band",
            ABITA,
            THU,
            t(17, 0),
            t(18, 20),
            genre=Genre.BRASS_BAND,
            about="One of the greatest brass bands in New Orleans history.",
            about_source=AboutSource.RESEARCHED,
        )
        assert act.genre == Genre.BRASS_BAND
        assert act.about_source == AboutSource.RESEARCHED

    def test_frozen(self) -> None:
        act = Act("Test", ABITA, THU, t(11, 0), t(12, 0))
        try:
            act.name = "Changed"  # type: ignore[misc]
            assert False, "Should have raised FrozenInstanceError"
        except AttributeError:
            pass

    def test_str(self) -> None:
        act = Act("Rebirth Brass Band", ABITA, THU, t(17, 0), t(18, 20))
        result = str(act)
        assert "Rebirth Brass Band" in result
        assert ABITA in result
