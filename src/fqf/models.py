"""Data models, enums, and constants for FQF 2026."""

from dataclasses import dataclass, field
from datetime import date, time
from enum import StrEnum

from fqf.slugify import slugify


class Genre(StrEnum):
    """Controlled vocabulary for act genres."""

    BRASS_BAND = "Brass Band"
    JAZZ_TRADITIONAL = "Jazz (Traditional)"
    JAZZ_CONTEMPORARY = "Jazz (Contemporary)"
    ZYDECO = "Zydeco"
    CAJUN = "Cajun"
    RNB_SOUL = "R&B / Soul"
    BLUES = "Blues"
    FUNK = "Funk"
    ROCK = "Rock"
    WORLD = "World"
    LATIN = "Latin"
    REGGAE = "Reggae"
    GOSPEL = "Gospel"
    SINGER_SONGWRITER = "Singer-Songwriter"
    ELECTRONIC_DJ = "Electronic / DJ"
    INDIAN_MARDI_GRAS = "Indian Mardi Gras"
    MIXED_ECLECTIC = "Mixed / Eclectic"
    UNKNOWN = "Unknown"


class AboutSource(StrEnum):
    """How the act bio was obtained."""

    RESEARCHED = "researched"
    GENERATED = "generated"
    NONE = ""


# ── Date constants ─────────────────────────────────────────────────────
THU = date(2026, 4, 16)
FRI = date(2026, 4, 17)
SAT = date(2026, 4, 18)
SUN = date(2026, 4, 19)

FESTIVAL_DATES = [THU, FRI, SAT, SUN]

# ── Stage constants ────────────────────────────────────────────────────
ABITA = "Abita Beer Stage"
NEWORLEANS = "NewOrleans.com Stage"
TROPICAL = "Tropical Isle Hand Grenade Stage"
JACKDANIELS = "Jack Daniel's Stage"
WILLOW = "Willow Dispensary Stage"
LOYOLA = "Loyola Esplanade in the Shade Stage"
FISHFRY = "Louisiana Fish Fry Stage"
ENTERGY = "Entergy Songwriter Stage"
PANAMLIFE = "Pan-American Life Insurance Group Stage"
JAZZPLAYHOUSE = "Jazz Playhouse at the Royal Sonesta"
FRENCHMARKET = "French Market Traditional Jazz Stage"
DUTCHALLEY = "French Market Dutch Alley Stage"
HOUSEOFBLUES = "House of Blues Voodoo Garden Stage"
JAZZPARK = "New Orleans Jazz National Historical Park Stage"
SCHOOLHOUSE = "Ernie's Schoolhouse Stage"
HANCOCK = "Hancock Whitney Stage"
OMNI = "Omni Royal Orleans Stage"
KREWE = "KREWE Eyewear Stage"
CAFEBEIGNET = "Cafe Beignet Stage"

ALL_STAGES = [
    ABITA,
    NEWORLEANS,
    TROPICAL,
    JACKDANIELS,
    WILLOW,
    LOYOLA,
    FISHFRY,
    ENTERGY,
    PANAMLIFE,
    JAZZPLAYHOUSE,
    FRENCHMARKET,
    DUTCHALLEY,
    HOUSEOFBLUES,
    JAZZPARK,
    SCHOOLHOUSE,
    HANCOCK,
    OMNI,
    KREWE,
    CAFEBEIGNET,
]


def t(h: int, m: int) -> time:
    """Shorthand for time(h, m)."""
    return time(h, m)


@dataclass(frozen=True)
class Act:
    """A single performance at the festival."""

    name: str
    stage: str
    date: date
    start: time
    end: time
    genre: str = Genre.UNKNOWN
    about: str = ""
    about_source: str = AboutSource.NONE
    slug: str = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "slug", slugify(self.name))

    def __str__(self) -> str:
        return (
            f"{self.name:<60} | {self.stage:<45} | "
            f"{self.date.strftime('%a %b %d')} | "
            f"{self.start.strftime('%-I:%M %p')} - {self.end.strftime('%-I:%M %p')}"
        )
