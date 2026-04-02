"""Festival-level configuration for French Quarter Festival 2026.

Centralises all festival-specific metadata so that switching to a different
festival (Jazz Fest, Voodoo Fest, etc.) only requires updating this file.
"""

from datetime import date

FESTIVAL_NAME = "French Quarter Festival"
FESTIVAL_SHORT_NAME = "FQF"
FESTIVAL_YEAR = 2026
FESTIVAL_DATES = [date(2026, 4, 16), date(2026, 4, 17), date(2026, 4, 18), date(2026, 4, 19)]
FESTIVAL_URL = "https://frenchquarterfest.org"

# Prefix used when generating share/route URLs (no trailing slash)
ROUTE_PREFIX = "/fq2026"

THEME_COLORS: dict[str, str] = {
    "primary": "#4a1a6b",  # purple
    "accent": "#d4a843",  # gold
    "green": "#1a7a4a",
}

# Human-readable labels for each festival date, keyed by ISO date string.
DAY_LABELS: dict[str, str] = {
    "2026-04-16": "Thu 16",
    "2026-04-17": "Fri 17",
    "2026-04-18": "Sat 18",
    "2026-04-19": "Sun 19",
}
