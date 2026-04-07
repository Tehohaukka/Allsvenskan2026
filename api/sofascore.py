"""
Sofascore unofficial API — fetch xG for a played match.
Searches events by date, matches by team name, extracts Expected Goals.
"""

from __future__ import annotations

import requests

_BASE = "https://api.sofascore.com/api/v1"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://www.sofascore.com/",
}


def _normalize(name: str) -> str:
    return name.lower().replace("-", " ").replace(".", "").strip()


def find_event_id(date: str, home_name: str, away_name: str) -> int | None:
    """
    Find Sofascore event ID for a match on a given date.
    date: 'YYYY-MM-DD'
    Returns event_id or None if not found.
    """
    url = f"{_BASE}/sport/football/scheduled-events/{date}"
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        events = resp.json().get("events", [])
    except Exception:
        return None

    h = _normalize(home_name)
    a = _normalize(away_name)

    for event in events:
        ht = _normalize(event.get("homeTeam", {}).get("name", ""))
        at = _normalize(event.get("awayTeam", {}).get("name", ""))
        if h in ht or ht in h:
            if a in at or at in a:
                return event["id"]
    return None


def fetch_xg(date: str, home_name: str, away_name: str) -> dict | None:
    """
    Fetch xG for a match.
    Returns {"xg_home": float, "xg_away": float, "event_id": int}
    or None if not found / xG unavailable.
    """
    event_id = find_event_id(date, home_name, away_name)
    if event_id is None:
        return None

    url = f"{_BASE}/event/{event_id}/statistics"
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        stats = resp.json().get("statistics", [])
    except Exception:
        return None

    for period in stats:
        if period.get("period") != "ALL":
            continue
        for group in period.get("groups", []):
            for item in group.get("statisticsItems", []):
                if "expected" in item.get("name", "").lower():
                    try:
                        return {
                            "xg_home": float(item["home"]),
                            "xg_away": float(item["away"]),
                            "event_id": event_id,
                        }
                    except (KeyError, ValueError, TypeError):
                        pass
    return None
