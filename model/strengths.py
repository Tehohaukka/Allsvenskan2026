"""
Calculate team attack and defense strengths from historical fixture data.

Methodology:
  attack_i  = (weighted_goals_scored_i / weighted_games_i) / league_avg_goals_per_game
  defense_i = (weighted_goals_conceded_i / weighted_games_i) / league_avg_goals_per_game

  xG_home = attack_home * defense_away * avg_home_goals
  xG_away = attack_away * defense_home * avg_away_goals

Both strengths are normalised so league average = 1.0.
Defense: lower is better (hard to score against).
Home advantage is captured implicitly by avg_home_goals > avg_away_goals.

Weighting: fixtures can carry a 'weight' column so recent/relevant seasons
are emphasised over older data. 2026 fixtures are weighted 2x over 2025.

Bayesian shrinkage: teams with few weighted games are pulled towards the
league average (1.0) to avoid extreme ratings from small samples.
"""

import pandas as pd


def fixtures_to_df(fixtures: list[dict], weight: float = 1.0) -> pd.DataFrame:
    """Parse API fixtures list into a flat DataFrame of results.

    weight: row-level weight applied to every fixture in this list.
            Use weight=2.0 for current-season data to emphasise recency.
    """
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
            "weight": weight,
        })
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


def calculate_strengths(df: pd.DataFrame, shrinkage_games: float = 0.0) -> pd.DataFrame:
    """
    Given a DataFrame of results, return a DataFrame with columns:
      team_id, team_name, games, scored, conceded, attack, defense

    Parameters
    ----------
    df : DataFrame from fixtures_to_df (may contain a 'weight' column).
    shrinkage_games : Bayesian prior weight equivalent to this many average-team
                      games. Pulls attack/defense towards 1.0 for teams with
                      little data. Good default: 10.
    """
    if df.empty:
        return pd.DataFrame()

    weight_vals = df["weight"].values if "weight" in df.columns else [1.0] * len(df)

    home = df[["home_id", "home_name", "home_goals", "away_goals"]].copy()
    home.columns = ["team_id", "team_name", "scored", "conceded"]
    home["weight"] = weight_vals

    away = df[["away_id", "away_name", "away_goals", "home_goals"]].copy()
    away.columns = ["team_id", "team_name", "scored", "conceded"]
    away["weight"] = weight_vals

    combined = pd.concat([home, away], ignore_index=True)
    combined["w_scored"] = combined["scored"] * combined["weight"]
    combined["w_conceded"] = combined["conceded"] * combined["weight"]

    stats = (
        combined.groupby(["team_id", "team_name"])
        .agg(
            games=("weight", "sum"),
            scored=("w_scored", "sum"),
            conceded=("w_conceded", "sum"),
        )
        .reset_index()
    )

    league_avg = stats["scored"].sum() / stats["games"].sum()

    stats["attack"] = (stats["scored"] / stats["games"]) / league_avg
    stats["defense"] = (stats["conceded"] / stats["games"]) / league_avg

    if shrinkage_games > 0:
        w = stats["games"] / (stats["games"] + shrinkage_games)
        stats["attack"] = w * stats["attack"] + (1.0 - w)
        stats["defense"] = w * stats["defense"] + (1.0 - w)

    return stats.sort_values("team_name").reset_index(drop=True)


def league_averages(df: pd.DataFrame) -> dict[str, float]:
    """
    Compute weighted average home and away goals per game.
    Returns {"avg_home": float, "avg_away": float}.
    """
    if df.empty:
        return {"avg_home": 1.5, "avg_away": 1.2}
    if "weight" in df.columns:
        w = df["weight"]
        return {
            "avg_home": float((df["home_goals"] * w).sum() / w.sum()),
            "avg_away": float((df["away_goals"] * w).sum() / w.sum()),
        }
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
