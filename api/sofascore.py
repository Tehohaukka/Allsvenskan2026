"""
Sofascore unofficial API — fetch xG and fixtures for Allsvenskan.
Uses undetected_chromedriver to bypass bot protection.
Caches raw data to data/raw/sofascore_allsvenskan_2026.json.
"""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

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

_SOFASCORE_ALLSVENSKAN_ID = 40
_SOFASCORE_ALLSVENSKAN_2026_SEASON = 87925
_SOFASCORE_ALLSVENSKAN_2025_SEASON = 69956
_CACHE_DIR = Path(__file__).parent.parent / "data" / "raw"
_FIXTURES_CACHE = _CACHE_DIR / "sofascore_allsvenskan_2026.json"
_FIXTURES_CACHE_2025 = _CACHE_DIR / "sofascore_allsvenskan_2025.json"

_STATUS_MAP = {
    "finished": "FT",
    "notstarted": "NS",
    "inprogress": "LIVE",
    "postponed": "PST",
    "canceled": "CANC",
    "cancelled": "CANC",
    "interrupted": "INT",
    "suspended": "SUSP",
}


def _normalize(name: str) -> str:
    return name.lower().replace("-", " ").replace(".", "").strip()


def _sofascore_event_to_apifootball(event: dict) -> dict:
    """Convert a Sofascore event dict to API-Football fixture format."""
    round_num = event.get("_round", 0)
    ts = event.get("startTimestamp", 0)
    date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S+00:00") if ts else ""
    status_type = event.get("status", {}).get("type", "notstarted")
    status_short = _STATUS_MAP.get(status_type, "NS")

    home = event.get("homeTeam", {})
    away = event.get("awayTeam", {})
    home_score = event.get("homeScore", {})
    away_score = event.get("awayScore", {})

    goals_home = home_score.get("current") if status_short == "FT" else None
    goals_away = away_score.get("current") if status_short == "FT" else None

    return {
        "fixture": {
            "id": event.get("id", 0),
            "date": date_str,
            "status": {"short": status_short, "long": status_type},
        },
        "league": {
            "id": 113,
            "name": "Allsvenskan",
            "round": f"Regular Season - {round_num}",
        },
        "teams": {
            "home": {"id": home.get("id", 0), "name": home.get("name", "")},
            "away": {"id": away.get("id", 0), "name": away.get("name", "")},
        },
        "goals": {"home": goals_home, "away": goals_away},
        "score": {
            "halftime": {
                "home": home_score.get("period1"),
                "away": away_score.get("period1"),
            },
            "fulltime": {"home": goals_home, "away": goals_away},
        },
    }


def load_fixtures_from_cache(season: int = 2026) -> list[dict]:
    """Load and convert cached Sofascore fixtures to API-Football format."""
    cache = _FIXTURES_CACHE if season == 2026 else _FIXTURES_CACHE_2025
    if not cache.exists():
        return []
    with open(cache, encoding="utf-8") as f:
        raw = json.load(f)
    return [_sofascore_event_to_apifootball(e) for e in raw]


def fetch_all_fixtures(force_refresh: bool = False) -> list[dict]:
    """
    Fetch all Allsvenskan 2026 fixtures from Sofascore via browser.
    Saves raw events to cache. Returns API-Football-format list.
    """
    if _FIXTURES_CACHE.exists() and not force_refresh:
        return load_fixtures_from_cache()

    try:
        import undetected_chromedriver as uc
    except ImportError:
        print("VIRHE: undetected_chromedriver ei ole asennettu.")
        return load_fixtures_from_cache()

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)

    all_events: list[dict] = []
    try:
        driver.get("https://www.sofascore.com")
        time.sleep(3)

        for round_num in range(1, 31):
            url = (
                f"{_BASE}/unique-tournament/{_SOFASCORE_ALLSVENSKAN_ID}"
                f"/season/{_SOFASCORE_ALLSVENSKAN_2026_SEASON}/events/round/{round_num}"
            )
            driver.get(url)
            time.sleep(1.2)
            body = driver.find_element("tag name", "body").text
            data = json.loads(body)
            events = data.get("events", [])
            if not events:
                break
            for e in events:
                e["_round"] = round_num
            all_events.extend(events)
            print(f"  Kierros {round_num}: {len(events)} ottelua")

        driver.quit()
    except Exception as exc:
        print(f"Sofascore-haku epäonnistui: {exc}")
        try:
            driver.quit()
        except Exception:
            pass

    if all_events:
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        with open(_FIXTURES_CACHE, "w", encoding="utf-8") as f:
            json.dump(all_events, f, ensure_ascii=False, indent=2)

    return [_sofascore_event_to_apifootball(e) for e in all_events]


# ── xG ────────────────────────────────────────────────────────────────────────

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
