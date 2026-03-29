"""
Central data loading and caching for the Streamlit app.
Uses st.cache_data to avoid re-fetching on every rerender.
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.football_api import get_fixtures, get_teams, get_players
from model.strengths import fixtures_to_df, calculate_strengths, league_averages
from config import VEIKKAUSLIIGA_ID, SEASON_2025, SEASON_2026
from data.overrides import load_raw_overrides, normalise, NAME_OVERRIDES

# Manual league average overrides (goals/game).
# Based on 2025 home average (1.670) and home/away ratio 1.25,
# reflecting the upward trend in VL scoring while assuming moderate home advantage.
_AVG_HOME_OVERRIDE: float = 1.67
_AVG_AWAY_OVERRIDE: float = 1.336


@st.cache_data(ttl=3600, show_spinner=False)
def load_strengths_and_averages() -> tuple:
    """
    Load 2025 fixtures for team strengths.
    League avg_home/avg_away are set manually via _AVG_HOME_OVERRIDE / _AVG_AWAY_OVERRIDE.
    Returns (strengths_df, avg_home, avg_away).
    """
    fixtures_2025 = get_fixtures(VEIKKAUSLIIGA_ID, SEASON_2025)
    df_2025 = fixtures_to_df(fixtures_2025)
    strengths = calculate_strengths(df_2025)

    return strengths, _AVG_HOME_OVERRIDE, _AVG_AWAY_OVERRIDE


def get_session_overrides() -> dict[int, dict]:
    """Return normalised overrides from the user's session (per-user, not cached globally)."""
    raw = st.session_state.get("raw_overrides", load_raw_overrides())
    return normalise(raw)


@st.cache_data(ttl=3600, show_spinner=False)
def load_teams_2026():
    """Load 2026 season team list."""
    return get_teams(VEIKKAUSLIIGA_ID, SEASON_2026)


@st.cache_data(ttl=86400, show_spinner=False)
def load_squad(team_id: int):
    """Load squad for a team."""
    return get_players(team_id, SEASON_2026)


def get_strength(strengths_df, team_id: int) -> dict:
    """Return strength dict for a team, applying manual overrides where defined."""
    row = strengths_df[strengths_df["team_id"] == team_id]
    if row.empty:
        base = {"attack": 1.0, "defense": 1.0, "games": 0, "scored": 0, "conceded": 0}
    else:
        r = row.iloc[0]
        base = {
            "attack": r["attack"],
            "defense": r["defense"],
            "games": int(r["games"]),
            "scored": int(r["scored"]),
            "conceded": int(r["conceded"]),
        }
    overrides = get_session_overrides()
    if team_id in overrides:
        base.update(overrides[team_id])
        base["overridden"] = True
    return base
