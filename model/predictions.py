"""
Prediction snapshot generator.

Before each round, run save_predictions.py to capture the model's
current probability outputs for all upcoming fixtures.

Stores per-match:
  - 1X2 probabilities
  - Asian handicap: line closest to 50/50
  - Totals: line closest to 50/50

Lines are searched in 0.25 steps.
Pinnacle closing odds and results are filled in manually afterwards.
"""

import json
import os
from datetime import datetime, timezone

import numpy as np

from model.poisson import score_matrix, result_probabilities, over_under, asian_handicap

# AH candidate lines: -3.0 to +3.0 in 0.25 steps
_AH_LINES = [round(x * 0.25, 2) for x in range(-12, 13)]

# Totals candidate lines: 1.5 to 6.5 in 0.25 steps
_TOTAL_LINES = [round(x * 0.25, 2) for x in range(6, 27)]


def _closest_ah(matrix: np.ndarray) -> dict:
    """Return the AH line where |p_home - p_away| is minimised."""
    best_line = 0.0
    best_diff = float("inf")
    for line in _AH_LINES:
        probs = asian_handicap(matrix, line)
        diff = abs(probs["home"] - probs["away"])
        if diff < best_diff:
            best_diff = diff
            best_line = line
    probs = asian_handicap(matrix, best_line)
    return {
        "line": best_line,
        "home": round(probs["home"], 4),
        "away": round(probs["away"], 4),
    }


def _closest_total(matrix: np.ndarray) -> dict:
    """Return the totals line where |p_over - p_under| is minimised."""
    best_line = 2.5
    best_diff = float("inf")
    for line in _TOTAL_LINES:
        result = over_under(matrix, line)
        p_over = 1.0 / result["fair_odds"] if result["fair_odds"] > 0 else 0.0
        p_under = 1.0 - p_over
        diff = abs(p_over - p_under)
        if diff < best_diff:
            best_diff = diff
            best_line = line
    result = over_under(matrix, best_line)
    p_over = round(1.0 / result["fair_odds"], 4) if result["fair_odds"] > 0 else 0.0
    return {
        "line": best_line,
        "over": p_over,
        "under": round(1.0 - p_over, 4),
    }


def build_prediction(fixture_id: int, home_name: str, away_name: str,
                     xg_home: float, xg_away: float) -> dict:
    """Build a single match prediction snapshot."""
    matrix = score_matrix(xg_home, xg_away)
    res = result_probabilities(matrix)
    return {
        "fixture_id": fixture_id,
        "home": home_name,
        "away": away_name,
        "model": {
            "xg_home": round(xg_home, 3),
            "xg_away": round(xg_away, 3),
            "p1": round(res["1"], 4),
            "pX": round(res["X"], 4),
            "p2": round(res["2"], 4),
            "ah": _closest_ah(matrix),
            "totals": _closest_total(matrix),
        },
        "pinnacle_closing": {
            "1x2": {"1": None, "X": None, "2": None},
            "ah": {"line": None, "home": None, "away": None},
            "totals": {"line": None, "over": None, "under": None},
        },
        "result": {
            "home_goals": None,
            "away_goals": None,
        },
    }


def save_round(round_number: int, predictions: list[dict],
               path: str = "data/predictions.json") -> None:
    """
    Append a round snapshot to predictions.json.
    If the file exists, loads it and replaces any existing entry for this round.
    """
    snapshot = {
        "round": round_number,
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "matches": predictions,
    }

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    # Replace existing snapshot for this round if present
    data = [s for s in data if s["round"] != round_number]
    data.append(snapshot)
    data.sort(key=lambda s: s["round"])

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved round {round_number} ({len(predictions)} matches) -> {path}")
