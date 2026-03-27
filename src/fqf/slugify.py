"""Deterministic slug generation for act names."""

import re
import unicodedata


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug.

    Normalizes unicode, lowercases, replaces non-alphanumeric
    characters with hyphens, and strips leading/trailing hyphens.
    """
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    # Remove apostrophes without inserting a separator (e.g. "Müller's" -> "mullers")
    text = re.sub(r"['\"]", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text
