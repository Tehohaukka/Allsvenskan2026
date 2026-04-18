"""
API-Football wrapper with simple file-based caching.
Caches responses to data/raw/ to avoid burning free-tier quota.
"""

import json
import os
import requests
from pathlib import Path
from config import API_FOOTBALL_KEY, API_FOOTBALL_BASE

CACHE_DIR = Path("data/raw")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_path(endpoint: str, params: dict) -> Path:
    key = endpoint.replace("/", "_") + "_" + "_".join(f"{k}{v}" for k, v in sorted(params.items()))
    return CACHE_DIR / f"{key}.json"


def _get(endpoint: str, params: dict, force_refresh: bool = False) -> dict:
    cache_file = _cache_path(endpoint, params)
    if cache_file.exists() and not force_refresh:
        with open(cache_file) as f:
            return json.load(f)

    if not API_FOOTBALL_KEY:
        # Returnera tom respons i stället för att krascha — appen degraderar elegant
        print(f"VARNING: '{cache_file}' saknas och API_FOOTBALL_KEY är inte inställd.")
        return {"get": endpoint, "parameters": params, "errors": [], "results": 0, "response": []}

    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    url = f"{API_FOOTBALL_BASE}/{endpoint}"
    resp = requests.get(url, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    with open(cache_file, "w") as f:
        json.dump(data, f, indent=2)

    return data


def get_standings(league_id: int, season: int) -> list[dict]:
    """Return standings list for a league/season."""
    data = _get("standings", {"league": league_id, "season": season})
    return data["response"][0]["league"]["standings"][0]


def get_teams(league_id: int, season: int) -> list[dict]:
    """Return list of teams in the league/season."""
    data = _get("teams", {"league": league_id, "season": season})
    return [item["team"] for item in data["response"]]


def get_fixtures(league_id: int, season: int, force_refresh: bool = False) -> list[dict]:
    """Return all fixtures for a league/season."""
    data = _get("fixtures", {"league": league_id, "season": season}, force_refresh=force_refresh)
    return data["response"]


def get_team_statistics(team_id: int, league_id: int, season: int) -> dict:
    """Return team statistics for a league/season."""
    data = _get("teams/statistics", {"team": team_id, "league": league_id, "season": season})
    return data["response"]


def get_players(team_id: int, season: int) -> list[dict]:
    """Return squad list for a team."""
    data = _get("players/squads", {"team": team_id})
    if data["response"]:
        return data["response"][0]["players"]
    return []
