"""Tests for schedule query functions."""

from fqf.models import (
    ABITA,
    FISHFRY,
    FRI,
    JACKDANIELS,
    NEWORLEANS,
    SAT,
    STAGE_ORDER,
    SUN,
    THU,
    TROPICAL,
    t,
)
from fqf.schedule import SCHEDULE, at, get_by_slug, on, search

THURSDAY_ACTS = [a for a in SCHEDULE if a.date == THU]
FRIDAY_ACTS = [a for a in SCHEDULE if a.date == FRI]
SATURDAY_ACTS = [a for a in SCHEDULE if a.date == SAT]
SUNDAY_ACTS = [a for a in SCHEDULE if a.date == SUN]

EXPECTED_ACT_COUNT = 302
EXPECTED_THURSDAY_COUNT = 47
EXPECTED_FRIDAY_COUNT = 70
EXPECTED_SATURDAY_COUNT = 94
EXPECTED_SUNDAY_COUNT = 91


class TestScheduleData:
    def test_total_act_count(self) -> None:
        assert len(SCHEDULE) == EXPECTED_ACT_COUNT

    def test_thursday_act_count(self) -> None:
        assert len(THURSDAY_ACTS) == EXPECTED_THURSDAY_COUNT

    def test_friday_act_count(self) -> None:
        assert len(FRIDAY_ACTS) == EXPECTED_FRIDAY_COUNT

    def test_saturday_act_count(self) -> None:
        assert len(SATURDAY_ACTS) == EXPECTED_SATURDAY_COUNT

    def test_sunday_act_count(self) -> None:
        assert len(SUNDAY_ACTS) == EXPECTED_SUNDAY_COUNT

    def test_all_dates_are_festival_dates(self) -> None:
        valid_dates = {THU, FRI, SAT, SUN}
        for act in SCHEDULE:
            assert act.date in valid_dates, f"{act.name} has invalid date {act.date}"

    def test_start_before_end(self) -> None:
        for act in SCHEDULE:
            assert act.start < act.end, f"{act.name} starts at {act.start} but ends at {act.end}"

    def test_all_slugs_unique(self) -> None:
        slugs = [act.slug for act in SCHEDULE]
        duplicates = [s for s in slugs if slugs.count(s) > 1]
        assert len(slugs) == len(set(slugs)), f"Duplicate slugs: {set(duplicates)}"

    def test_known_act_exists(self) -> None:
        names = [act.name for act in SCHEDULE]
        assert "Rebirth Brass Band" in names
        assert "The Soul Rebels" in names
        assert "Tuba Skinny" in names

    def test_thursday_acts_all_on_thu(self) -> None:
        assert all(a.date == THU for a in THURSDAY_ACTS)

    def test_friday_acts_all_on_fri(self) -> None:
        assert all(a.date == FRI for a in FRIDAY_ACTS)

    def test_saturday_acts_all_on_sat(self) -> None:
        assert all(a.date == SAT for a in SATURDAY_ACTS)

    def test_sunday_acts_all_on_sun(self) -> None:
        assert all(a.date == SUN for a in SUNDAY_ACTS)


class TestAt:
    def test_returns_acts_at_time(self) -> None:
        results = at(FRI, t(14, 0))
        assert len(results) > 0
        for act in results:
            assert act.date == FRI
            assert act.start <= t(14, 0) < act.end

    def test_no_results_outside_hours(self) -> None:
        results = at(THU, t(6, 0))
        assert results == []

    def test_sorted_by_geographic_stage_order(self) -> None:
        results = at(SAT, t(14, 0))
        stage_indices = [STAGE_ORDER[act.stage] for act in results]
        assert stage_indices == sorted(stage_indices)

    def test_boundary_start_included(self) -> None:
        # Acts starting exactly at the query time should be included
        results = at(THU, t(11, 30))
        names = [a.name for a in results]
        assert "Seguenon Kone featuring Ivorie Spectacle" in names

    def test_boundary_end_excluded(self) -> None:
        # Acts ending exactly at the query time should NOT be included
        results = at(THU, t(12, 30))
        names = [a.name for a in results]
        assert "Seguenon Kone featuring Ivorie Spectacle" not in names


class TestSearch:
    def test_search_by_name(self) -> None:
        results = search("Rebirth")
        assert any(a.name == "Rebirth Brass Band" for a in results)

    def test_search_by_stage(self) -> None:
        results = search("Fish Fry")
        assert all(FISHFRY.lower() in a.stage.lower() for a in results)

    def test_search_case_insensitive(self) -> None:
        assert search("rebirth") == search("REBIRTH")

    def test_search_no_results(self) -> None:
        assert search("zzzznonexistent") == []

    def test_sorted_by_date_time(self) -> None:
        results = search("brass")
        for i in range(len(results) - 1):
            assert (results[i].date, results[i].start) <= (
                results[i + 1].date,
                results[i + 1].start,
            )

    def test_search_by_partial_name(self) -> None:
        results = search("Zydeco")
        assert len(results) > 0

    def test_search_returns_all_matching_days(self) -> None:
        # "brass" should span multiple days
        results = search("brass band")
        days = {a.date for a in results}
        assert len(days) > 1


class TestOn:
    def test_all_acts_on_day(self) -> None:
        results = on(SAT)
        assert len(results) > 0
        assert all(a.date == SAT for a in results)

    def test_filter_by_stage(self) -> None:
        results = on(THU, stage="Jack Daniel")
        assert all(JACKDANIELS.lower() in a.stage.lower() for a in results)
        assert len(results) > 0

    def test_sorted_by_geographic_stage_then_time(self) -> None:
        results = on(FRI)
        for i in range(len(results) - 1):
            assert (STAGE_ORDER[results[i].stage], results[i].start) <= (
                STAGE_ORDER[results[i + 1].stage],
                results[i + 1].start,
            )

    def test_no_stage_filter_returns_all_day_acts(self) -> None:
        thu_results = on(THU)
        assert len(thu_results) == EXPECTED_THURSDAY_COUNT

    def test_stage_filter_case_insensitive(self) -> None:
        lower = on(SAT, stage="abita beer")
        upper = on(SAT, stage="Abita Beer")
        assert lower == upper

    def test_stage_filter_no_match(self) -> None:
        results = on(THU, stage="nonexistent stage xyz")
        assert results == []


class TestGetBySlug:
    def test_found(self) -> None:
        act = get_by_slug("rebirth-brass-band")
        assert act is not None
        assert act.name == "Rebirth Brass Band"

    def test_not_found(self) -> None:
        assert get_by_slug("nonexistent-band") is None

    def test_all_acts_retrievable_by_slug(self) -> None:
        for act in SCHEDULE:
            retrieved = get_by_slug(act.slug)
            assert retrieved is not None
            assert retrieved.name == act.name

    def test_tuba_skinny_slug(self) -> None:
        act = get_by_slug("tuba-skinny")
        assert act is not None
        assert act.stage == NEWORLEANS
        assert act.date == SUN

    def test_soul_rebels_slug(self) -> None:
        act = get_by_slug("the-soul-rebels")
        assert act is not None
        assert act.stage == ABITA
        assert act.date == THU
