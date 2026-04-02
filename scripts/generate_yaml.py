"""One-time script to export act data from Python schedule files to YAML.

Run with: do_cmd -p .,dev -- python scripts/generate_yaml.py
"""

from pathlib import Path

import yaml

from fqf.schedule import SCHEDULE

# Use literal block scalars (|) for multi-line strings so the YAML is readable.
class _LiteralStr(str):
    pass


def _literal_representer(dumper: yaml.Dumper, data: str) -> yaml.ScalarNode:
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


yaml.add_representer(_LiteralStr, _literal_representer)


def act_to_dict(act):  # type: ignore[no-untyped-def]
    about = _LiteralStr(act.about) if act.about else act.about
    return {
        "name": act.name,
        "stage": act.stage,
        "date": act.date.isoformat(),
        "start": act.start.strftime("%H:%M"),
        "end": act.end.strftime("%H:%M"),
        "genre": str(act.genre),
        "about": about,
        "about_source": str(act.about_source),
        "websites": list(act.websites),
    }


output = {
    "festival": {
        "name": "French Quarter Festival",
        "year": 2026,
        "dates": ["2026-04-16", "2026-04-17", "2026-04-18", "2026-04-19"],
    },
    "acts": [act_to_dict(a) for a in SCHEDULE],
}

out_path = Path(__file__).parent.parent / "src" / "fqf" / "data" / "fq2026_acts.yaml"
out_path.parent.mkdir(parents=True, exist_ok=True)

with out_path.open("w") as f:
    yaml.dump(output, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=100)

print(f"Wrote {len(SCHEDULE)} acts to {out_path}")
