"""YAML-based schedule loader.

Reads fq2026_acts.yaml and returns a list of Act instances identical to the
ones previously constructed inline in the per-day Python files.

Stage names in the YAML are the string values (e.g. "Abita Beer Stage"),
not the Python constant names — validated against models.ALL_STAGES on load.
"""

from datetime import date, time
from importlib import resources
from pathlib import Path
from typing import Any

import yaml

from fqf.models import ALL_STAGES, Act, Genre

_YAML_PATH = Path(__file__).parent.parent / "data" / "fq2026_acts.yaml"

_VALID_STAGES: frozenset[str] = frozenset(ALL_STAGES)


def _parse_act(raw: dict[str, Any]) -> Act:
    act_date = date.fromisoformat(raw["date"])
    h_start, m_start = map(int, raw["start"].split(":"))
    h_end, m_end = map(int, raw["end"].split(":"))
    stage = raw["stage"]
    if stage not in _VALID_STAGES:
        raise ValueError(f"Unknown stage {stage!r} in YAML — not in models.ALL_STAGES")
    return Act(
        name=raw["name"],
        stage=stage,
        date=act_date,
        start=time(h_start, m_start),
        end=time(h_end, m_end),
        genre=raw.get("genre", Genre.UNKNOWN),
        about=raw.get("about", ""),
        about_source=raw.get("about_source", ""),
        websites=list(raw.get("websites") or []),
    )


def load_schedule() -> list[Act]:
    """Load and return the full schedule from fq2026_acts.yaml."""
    with _YAML_PATH.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return [_parse_act(raw) for raw in data["acts"]]
