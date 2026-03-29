"""
Calculate team attack and defense strengths from historical fixture data.

Methodology:
  attack_i  = (goals_scored_i / games_i) / league_avg_goals_per_game
  defense_i = (goals_conceded_i / games_i) / league_avg_goals_per_game

  xG_home = attack_home * defense_away * avg_home_goals
  xG_away = attack_away * defense_home * avg_away_goals

Both strengths are normalised so league average = 1.0.
Defense: lower is better (hard to score against).
Home advantage is captured implicitly by avg_home_goals > avg_away_goals.
"""

import pandas as pd


def fixtures_to_df(fixtures: list[dict]) -> pd.DataFrame:
    """Parse API fixtures list into a flat DataFrame of results."""
    rows = []
    for f in fixtures:
        status = f["fixture"]["status"]["short"]
        if status not in ("FT", "AET", "PEN"):
            continue
        rows.append({
            "fixture_id": f["fixture"]["id"],
            "date": f["fixture"]["date"],
            "home_id": f["teams"]["home"]["id"],
            "home_name": f["teams"]["home"]["name"],
            "away_id": f["teams"]["away"]["id"],
            "away_name": f["teams"]["away"]["name"],
            "home_goals": f["goals"]["home"],
            "away_goals": f["goals"]["away"],
        })
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


def calculate_strengths(df: pd.DataFrame) -> pd.DataFrame:
    """
    Given a DataFrame of results, return a DataFrame with columns:
      team_id, team_name, games, scored, conceded, attack, defense
    """
    if df.empty:
        return pd.DataFrame()

    home = df[["home_id", "home_name", "home_goals", "away_goals"]].copy()
    home.columns = ["team_id", "team_name", "scored", "conceded"]

    away = df[["away_id", "away_name", "away_goals", "home_goals"]].copy()
    away.columns = ["team_id", "team_name", "scored", "conceded"]

    combined = pd.concat([home, away], ignore_index=True)
    stats = (
        combined.groupby(["team_id", "team_name"])
        .agg(games=("scored", "count"), scored=("scored", "sum"), conceded=("conceded", "sum"))
        .reset_index()
    )

    league_avg = stats["scored"].sum() / stats["games"].sum()

    stats["attack"] = (stats["scored"] / stats["games"]) / league_avg
    stats["defense"] = (stats["conceded"] / stats["games"]) / league_avg

    return stats.sort_values("team_name").reset_index(drop=True)


def league_averages(df: pd.DataFrame) -> dict[str, float]:
    """
    Compute average home and away goals per game from a fixtures DataFrame.
    Returns {"avg_home": float, "avg_away": float}.
    """
    if df.empty:
        return {"avg_home": 1.5, "avg_away": 1.2}
    return {
        "avg_home": float(df["home_goals"].mean()),
        "avg_away": float(df["away_goals"].mean()),
    }


def expected_goals(home_attack: float, away_defense: float,
                   away_attack: float, home_defense: float,
                   avg_home: float, avg_away: float) -> tuple[float, float]:
    """
    Return (xG_home, xG_away).

    xG_home = attack_home * defense_away * avg_home_goals
    xG_away = attack_away * defense_home * avg_away_goals
    """
    xg_home = home_attack * away_defense * avg_home
    xg_away = away_attack * home_defense * avg_away
    return xg_home, xg_away
