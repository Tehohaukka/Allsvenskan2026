"""
Central data loading and caching for the Streamlit app.
Uses st.cache_data to avoid re-fetching on every rerender.

Model training strategy:
  - 2025 Allsvenskan (weight=1.0): historical baseline, 240 matches
  - 2026 Allsvenskan FT matches (weight=2.0): recency emphasis
  - Bayesian shrinkage (k=10): stabilises ratings for teams with few games
  - DC_RHO=-0.20: Dixon-Coles correction tuned on 2026 k1-5 backtest
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.football_api import get_fixtures, get_teams, get_players
from model.strengths import fixtures_to_df, calculate_strengths, league_averages
from config import ALLSVENSKAN_ID, SEASON_2025, SEASON_2026
from data.overrides import load_raw_overrides, normalise, NAME_OVERRIDES

import pandas as pd

_SHRINKAGE_GAMES: float = 10.0   # Bayesian prior weight
_WEIGHT_2026: float = 2.0        # 2026 data weighted 2x over 2025


@st.cache_data(ttl=3600, show_spinner=False)
def load_strengths_and_averages() -> tuple:
    """
    Load 2025 + 2026 (FT) fixtures for team strengths.
    2026 fixtures are weighted 2x. Bayesian shrinkage applied.
    Returns (strengths_df, avg_home, avg_away).
    """
    fixtures_2025 = get_fixtures(ALLSVENSKAN_ID, SEASON_2025)
    df_2025 = fixtures_to_df(fixtures_2025, weight=1.0)

    fixtures_2026 = get_fixtures(ALLSVENSKAN_ID, SEASON_2026)
    df_2026 = fixtures_to_df(fixtures_2026, weight=_WEIGHT_2026)

    df_combined = pd.concat([df_2025, df_2026], ignore_index=True)
    strengths = calculate_strengths(df_combined, shrinkage_games=_SHRINKAGE_GAMES)
    avgs = league_averages(df_combined)

    return strengths, avgs["avg_home"], avgs["avg_away"]


def get_session_overrides() -> dict[int, dict]:
    """Return normalised overrides from the user's session (per-user, not cached globally)."""
    raw = st.session_state.get("raw_overrides", load_raw_overrides())
    return normalise(raw)


@st.cache_data(ttl=3600, show_spinner=False)
def load_teams_2026():
    """Load 2026 season team list."""
    return get_teams(ALLSVENSKAN_ID, SEASON_2026)


@st.cache_data(ttl=86400, show_spinner=False)
def load_squad(team_id: int):
    """Load squad for a team."""
    return get_players(team_id, SEASON_2026)


def get_strength(strengths_df, team_id: int) -> dict:
    """Return strength dict for a team, applying manual overrides where defined."""
    base = {"attack": 1.0, "defense": 1.0, "games": 0, "scored": 0, "conceded": 0}
    if not strengths_df.empty and "team_id" in strengths_df.columns:
        row = strengths_df[strengths_df["team_id"] == team_id]
        if not row.empty:
            r = row.iloc[0]
            base = {
                "attack": r["attack"],
                "defense": r["defense"],
                "games": float(r["games"]),
                "scored": float(r["scored"]),
                "conceded": float(r["conceded"]),
            }
    overrides = get_session_overrides()
    if team_id in overrides:
        base.update(overrides[team_id])
        base["overridden"] = True
    return base
