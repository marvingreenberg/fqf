"""Tests for data models, enums, and constants."""

from datetime import date, time

from fqf.models import (
    ABITA,
    ALL_STAGES,
    FESTIVAL_DATES,
    FRI,
    NEWORLEANS,
    SAT,
    STAGE_LOCATIONS,
    STAGE_ORDER,
    SUN,
    THU,
    AboutSource,
    Act,
    Genre,
    StageLocation,
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
    EXPECTED_STAGE_COUNT = 19

    def test_stage_count(self) -> None:
        assert len(ALL_STAGES) == self.EXPECTED_STAGE_COUNT

    def test_no_duplicates(self) -> None:
        assert len(ALL_STAGES) == len(set(ALL_STAGES))

    def test_geographic_order_matches_latitude(self) -> None:
        latitudes = [STAGE_LOCATIONS[s].lat for s in ALL_STAGES]
        assert latitudes == sorted(latitudes)


class TestStageLocations:
    def test_all_stages_have_locations(self) -> None:
        for stage in ALL_STAGES:
            assert stage in STAGE_LOCATIONS, f"Missing location for {stage}"

    def test_location_is_named_tuple(self) -> None:
        loc = STAGE_LOCATIONS[ABITA]
        assert isinstance(loc, StageLocation)
        assert isinstance(loc.lat, float)
        assert isinstance(loc.lng, float)

    def test_coordinates_in_new_orleans_area(self) -> None:
        min_lat, max_lat = 29.94, 29.97
        min_lng, max_lng = -90.08, -90.05
        for stage, loc in STAGE_LOCATIONS.items():
            assert min_lat <= loc.lat <= max_lat, f"{stage} lat {loc.lat} out of range"
            assert min_lng <= loc.lng <= max_lng, f"{stage} lng {loc.lng} out of range"


class TestStageOrder:
    def test_all_stages_have_order(self) -> None:
        for stage in ALL_STAGES:
            assert stage in STAGE_ORDER

    def test_order_values_contiguous(self) -> None:
        expected = set(range(len(ALL_STAGES)))
        assert set(STAGE_ORDER.values()) == expected


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

    def test_default_websites(self) -> None:
        act = Act("Test", ABITA, THU, t(11, 0), t(12, 0))
        assert act.websites == []

    def test_websites_with_values(self) -> None:
        test_url = "https://example.com"
        act = Act("Test", ABITA, THU, t(11, 0), t(12, 0), websites=[test_url])
        assert act.websites == [test_url]

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
