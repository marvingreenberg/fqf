"""Data models, enums, and constants for FQF 2026."""

from dataclasses import dataclass, field
from datetime import date, time
from enum import StrEnum
from typing import NamedTuple

from fqf.festival_config import FESTIVAL_DATES as _FESTIVAL_DATES
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
# These are convenience aliases for the schedule files; authoritative source is festival_config.py.
THU, FRI, SAT, SUN = _FESTIVAL_DATES

FESTIVAL_DATES = _FESTIVAL_DATES

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
    FISHFRY,
    ABITA,
    HOUSEOFBLUES,
    TROPICAL,
    JAZZPARK,
    WILLOW,
    CAFEBEIGNET,
    JAZZPLAYHOUSE,
    HANCOCK,
    OMNI,
    NEWORLEANS,
    KREWE,
    JACKDANIELS,
    FRENCHMARKET,
    SCHOOLHOUSE,
    PANAMLIFE,
    DUTCHALLEY,
    LOYOLA,
    ENTERGY,
]

STAGE_ORDER: dict[str, int] = {stage: idx for idx, stage in enumerate(ALL_STAGES)}


# ── Stage locations (lat/lng from fqf2026_stages.csv) ─────────────────


class StageLocation(NamedTuple):
    """GPS coordinates for a festival stage."""

    lat: float
    lng: float


STAGE_LOCATIONS: dict[str, StageLocation] = {
    FISHFRY: StageLocation(29.95107, -90.06280),
    ABITA: StageLocation(29.95278, -90.06307),
    HOUSEOFBLUES: StageLocation(29.95338, -90.06627),
    TROPICAL: StageLocation(29.95373, -90.06301),
    JAZZPARK: StageLocation(29.95504, -90.06471),
    WILLOW: StageLocation(29.95544, -90.06368),
    CAFEBEIGNET: StageLocation(29.95582, -90.06843),
    JAZZPLAYHOUSE: StageLocation(29.95582, -90.06850),
    HANCOCK: StageLocation(29.95600, -90.06651),
    OMNI: StageLocation(29.95631, -90.06562),
    NEWORLEANS: StageLocation(29.95721, -90.06293),
    KREWE: StageLocation(29.95763, -90.06521),
    JACKDANIELS: StageLocation(29.95884, -90.05917),
    FRENCHMARKET: StageLocation(29.96044, -90.05856),
    SCHOOLHOUSE: StageLocation(29.96070, -90.06265),
    PANAMLIFE: StageLocation(29.96073, -90.05650),
    DUTCHALLEY: StageLocation(29.96083, -90.05823),
    LOYOLA: StageLocation(29.96116, -90.05774),
    ENTERGY: StageLocation(29.96145, -90.05825),
}


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
    websites: list[str] = field(default_factory=list)
    slug: str = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "slug", slugify(self.name))

    def __str__(self) -> str:
        return (
            f"{self.name:<60} | {self.stage:<45} | "
            f"{self.date.strftime('%a %b %d')} | "
            f"{self.start.strftime('%-I:%M %p')} - {self.end.strftime('%-I:%M %p')}"
        )
