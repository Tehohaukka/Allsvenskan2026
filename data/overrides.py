"""
Manual strength overrides for 2026 season.
Raw values are stored in data/overrides.json and editable via the UI.
Normalised so that league average attack = defense = 1.0.
"""

import json
from pathlib import Path

NAME_OVERRIDES: dict[int, str] = {
    1168: "TPS",
}

_JSON_PATH = Path(__file__).parent / "overrides.json"

# Hardcoded fallback if JSON is missing
_FALLBACK_RAW: dict[int, dict] = {
    649:  {"name": "HJK Helsinki",  "attack": 1.450, "defense": 0.835},
    1164: {"name": "Inter Turku",   "attack": 1.300, "defense": 0.780},
    1163: {"name": "Ilves",         "attack": 1.230, "defense": 0.795},
    1165: {"name": "KuPS",          "attack": 1.215, "defense": 0.790},
    2077: {"name": "AC Oulu",       "attack": 1.180, "defense": 1.020},
    689:  {"name": "SJK",           "attack": 1.120, "defense": 1.015},
    2082: {"name": "Gnistan",       "attack": 0.985, "defense": 1.040},
    650:  {"name": "VPS",           "attack": 0.820, "defense": 1.000},
    587:  {"name": "IFK Mariehamn", "attack": 0.790, "defense": 1.085},
    1166: {"name": "Lahti",         "attack": 0.782, "defense": 1.242},
    2075: {"name": "FF Jaro",       "attack": 0.737, "defense": 1.150},
    1168: {"name": "TPS",           "attack": 0.690, "defense": 1.290},
}


def load_raw_overrides() -> dict[int, dict]:
    """Load raw (un-normalised) overrides from JSON, falling back to hardcoded defaults."""
    if _JSON_PATH.exists():
        with open(_JSON_PATH) as f:
            data = json.load(f)
        return {int(k): v for k, v in data.items()}
    return _FALLBACK_RAW


def save_raw_overrides(raw: dict[int, dict]) -> None:
    """Persist raw overrides to JSON."""
    with open(_JSON_PATH, "w") as f:
        json.dump({str(k): v for k, v in raw.items()}, f, indent=2)


def normalise(raw: dict[int, dict]) -> dict[int, dict]:
    """Return normalised strengths (league avg attack = defense = 1.0)."""
    n = len(raw)
    att_avg = sum(v["attack"] for v in raw.values()) / n
    def_avg = sum(v["defense"] for v in raw.values()) / n
    return {
        k: {"attack": v["attack"] / att_avg, "defense": v["defense"] / def_avg}
        for k, v in raw.items()
    }
