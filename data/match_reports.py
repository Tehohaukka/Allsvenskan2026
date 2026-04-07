"""
Persistent storage for match reports: xG values and notes.
Keyed by '{home_id}_{away_id}_{date}'.
"""

import json
from pathlib import Path

_PATH = Path(__file__).parent / "match_reports.json"


def _load() -> dict:
    if _PATH.exists():
        with open(_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save(data: dict) -> None:
    with open(_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def make_key(home_id: int, away_id: int, date: str) -> str:
    return f"{home_id}_{away_id}_{date}"


def get_report(key: str) -> dict:
    """Return report dict or empty dict."""
    return _load().get(key, {})


def save_report(key: str, updates: dict) -> None:
    """Merge updates into existing report and persist."""
    data = _load()
    existing = data.get(key, {})
    existing.update(updates)
    data[key] = existing
    _save(data)
