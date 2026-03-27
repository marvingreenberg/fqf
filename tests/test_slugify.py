"""Tests for deterministic slug generation."""

from fqf.slugify import slugify


class TestSlugify:
    def test_simple_name(self) -> None:
        assert slugify("Rebirth Brass Band") == "rebirth-brass-band"

    def test_ampersand(self) -> None:
        assert slugify("Kermit Ruffins & the Barbecue Swingers") == (
            "kermit-ruffins-the-barbecue-swingers"
        )

    def test_apostrophe(self) -> None:
        assert slugify("George Porter Jr & Runnin' Pardners") == (
            "george-porter-jr-runnin-pardners"
        )

    def test_unicode_accent(self) -> None:
        assert slugify("Arsène Delay & Charlie Wooton") == ("arsene-delay-charlie-wooton")

    def test_unicode_special(self) -> None:
        assert slugify("Fermín Ceballos + Merengue4FOUR") == ("fermin-ceballos-merengue4four")

    def test_parentheses(self) -> None:
        assert slugify("Sir Chantz Powell & The Sound Of Funk (S.O.F.)") == (
            "sir-chantz-powell-the-sound-of-funk-s-o-f"
        )

    def test_quotes(self) -> None:
        assert slugify("John 'Papa' Gros") == "john-papa-gros"

    def test_featuring(self) -> None:
        assert slugify("Stanton Moore featuring Joe Ashlar and Danny Abel") == (
            "stanton-moore-featuring-joe-ashlar-and-danny-abel"
        )

    def test_numeric_prefix(self) -> None:
        assert slugify("504 Millz") == "504-millz"

    def test_deterministic(self) -> None:
        name = "The Dirty Dozen Brass Band"
        assert slugify(name) == slugify(name)

    def test_ecirb_muller(self) -> None:
        assert slugify("Ecirb Müller's Twisted Dixie") == ("ecirb-mullers-twisted-dixie")

    def test_presents_in_name(self) -> None:
        assert slugify("Ovi-G presents 'Xtra Cash!'") == ("ovi-g-presents-xtra-cash")
