"""
Manuella styrkeöverskridningar för säsongen 2026.
Råvärden lagras i data/overrides.json och kan redigeras via UI.
Normaliserade så att ligasnittet anfall = försvar = 1,0.
"""

import json
from pathlib import Path

NAME_OVERRIDES: dict[int, str] = {
    # Lägg till eventuella namnmappningar här om API-namnet skiljer sig
}

_JSON_PATH = Path(__file__).parent / "overrides.json"

# Standardvärden om JSON saknas (API-Football team-ID:n för Allsvenskan — verifiera vid första API-hämtning)
_FALLBACK_RAW: dict[int, dict] = {
    362:  {"name": "Malmö FF",          "attack": 1.450, "defense": 0.800},
    363:  {"name": "IF Elfsborg",        "attack": 1.350, "defense": 0.850},
    359:  {"name": "IFK Göteborg",       "attack": 1.250, "defense": 0.900},
    357:  {"name": "AIK",                "attack": 1.200, "defense": 0.900},
    361:  {"name": "Djurgårdens IF",     "attack": 1.200, "defense": 0.880},
    365:  {"name": "Hammarby IF",        "attack": 1.180, "defense": 0.920},
    568:  {"name": "Mjällby AIF",        "attack": 1.150, "defense": 0.930},
    366:  {"name": "BK Häcken",          "attack": 1.120, "defense": 0.950},
    569:  {"name": "IK Sirius",          "attack": 1.050, "defense": 1.000},
    371:  {"name": "Halmstads BK",       "attack": 0.950, "defense": 1.050},
    570:  {"name": "Degerfors IF",       "attack": 0.900, "defense": 1.100},
    372:  {"name": "GAIS",               "attack": 0.880, "defense": 1.120},
    370:  {"name": "IF Brommapojkarna",  "attack": 0.850, "defense": 1.150},
    369:  {"name": "Kalmar FF",          "attack": 0.820, "defense": 1.180},
    573:  {"name": "Västerås SK",        "attack": 0.780, "defense": 1.220},
    574:  {"name": "Örgryte IS",         "attack": 0.750, "defense": 1.250},
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
