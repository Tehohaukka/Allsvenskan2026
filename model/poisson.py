"""
Poisson match probability calculations.

Given xG_home and xG_away, compute:
  - Full score probability matrix (up to max_goals per side)
  - 1X2 probabilities
  - Over/under goal totals
  - Asian handicap
"""

import numpy as np
from scipy.stats import poisson


MAX_GOALS = 10  # truncation limit for score matrix
DC_RHO = -0.20  # Dixon-Coles correlation. Backtested on Allsvenskan 2026 k1-5 vs 2025 training.


def _tau(i: int, j: int, lam: float, mu: float, rho: float) -> float:
    """
    Dixon-Coles (1997) correction factor for low-scoring outcomes.
    Adjusts the four cells (0-0, 1-0, 0-1, 1-1) to correct for
    the underestimation of draws and 1-goal results in pure Poisson.
    """
    if i == 0 and j == 0:
        return 1 - lam * mu * rho
    elif i == 1 and j == 0:
        return 1 + mu * rho
    elif i == 0 and j == 1:
        return 1 + lam * rho
    elif i == 1 and j == 1:
        return 1 - rho
    return 1.0


def score_matrix(xg_home: float, xg_away: float,
                 max_goals: int = MAX_GOALS, rho: float = DC_RHO) -> np.ndarray:
    """
    Returns an (max_goals+1) x (max_goals+1) matrix where
    matrix[i][j] = P(home scores i, away scores j).

    Applies Dixon-Coles correction to low-scoring outcomes (i+j <= 2)
    to account for the empirical over-representation of draws and
    1-goal results relative to pure independent Poisson.
    Matrix is renormalised to sum to 1 after correction.
    """
    home_probs = poisson.pmf(np.arange(max_goals + 1), xg_home)
    away_probs = poisson.pmf(np.arange(max_goals + 1), xg_away)
    matrix = np.outer(home_probs, away_probs)

    for i in range(2):
        for j in range(2):
            matrix[i, j] *= _tau(i, j, xg_home, xg_away, rho)

    matrix /= matrix.sum()  # renormalise after correction
    return matrix


def result_probabilities(matrix: np.ndarray) -> dict[str, float]:
    """Return P(home win), P(draw), P(away win) from score matrix."""
    n = matrix.shape[0]
    home_win = float(np.sum(np.tril(matrix, k=-1)))
    draw = float(np.sum(np.diag(matrix)))
    away_win = float(np.sum(np.triu(matrix, k=1)))
    return {"1": home_win, "X": draw, "2": away_win}


def over_under(matrix: np.ndarray, line: float = 2.5) -> dict[str, float]:
    """
    Return fair_odds for an Asian total (over) bet, handling all line types:

      .5  lines: simple win/lose, no push.
      .0  lines: push (stake returned) when total == line.
      .25 lines: split of (line-0.25) whole + (line+0.25) half.
                 Exactly (line-0.25) goals → half-loss.
      .75 lines: split of (line-0.25) half + (line+0.25) whole.
                 Exactly (line+0.25) goals → half-win.

    In all cases: fair_odds = (1 - B) / A
      where A = weighted P(win), B = weighted P(push returns).
    EV probability = 1 / fair_odds.
    """
    n = matrix.shape[0]
    dist = np.zeros((2 * n - 1,))
    for i in range(n):
        for j in range(n):
            dist[i + j] += matrix[i, j]

    def _p_over(l):
        return float(sum(p for g, p in enumerate(dist) if g > l))

    def _p_exact(l):
        idx = int(round(l))
        return float(dist[idx]) if 0 <= idx < len(dist) else 0.0

    frac = round((line % 1) * 4)  # 0=whole, 1=.25, 2=half, 3=.75

    if frac == 2:        # .5 line — no push
        A, B = _p_over(line), 0.0
    elif frac == 0:      # .0 line — push on exact total
        A, B = _p_over(line), _p_exact(line)
    elif frac == 1:      # .25 line — split: lower is whole (.0), upper is half (.5)
        L1, L2 = line - 0.25, line + 0.25
        A = 0.5 * _p_over(L1) + 0.5 * _p_over(L2)
        B = 0.5 * _p_exact(L1)          # only the whole sub-line can push
    else:                # .75 line — split: lower is half (.5), upper is whole (.0)
        L1, L2 = line - 0.25, line + 0.25
        A = 0.5 * _p_over(L1) + 0.5 * _p_over(L2)
        B = 0.5 * _p_exact(L2)          # only the whole sub-line can push

    fair_odds = (1 - B) / A if A > 0 else float("inf")
    return {"fair_odds": fair_odds, "line": line}


def asian_handicap(matrix: np.ndarray, handicap: float) -> dict[str, float]:
    """
    Calculate Asian Handicap probabilities.

    handicap: applied to home team (negative = home gives handicap).
    e.g. handicap=-1.5 means home must win by 2+ for home bet to win.

    Handles quarter-ball lines (e.g. -1.25) by splitting into adjacent half-lines.
    Returns {"home": p_home, "away": p_away} (push is split, not shown separately).
    """
    # Handle quarter lines by splitting
    lower = np.floor(handicap * 2) / 2
    upper = lower + 0.5
    if handicap == lower:
        return _ah_half_line(matrix, handicap)
    # Quarter line: 50/50 split between floor and ceiling half-lines
    p_lower = _ah_half_line(matrix, lower)
    p_upper = _ah_half_line(matrix, upper)
    return {
        "home": 0.5 * p_lower["home"] + 0.5 * p_upper["home"],
        "away": 0.5 * p_lower["away"] + 0.5 * p_upper["away"],
    }


def _ah_half_line(matrix: np.ndarray, handicap: float) -> dict[str, float]:
    """Asian handicap for exact half-ball lines (push possible on whole numbers)."""
    n = matrix.shape[0]
    home_win = 0.0
    away_win = 0.0
    push = 0.0
    for i in range(n):
        for j in range(n):
            margin = (i - j) + handicap  # adjusted margin from home perspective
            p = matrix[i, j]
            if margin > 0:
                home_win += p
            elif margin < 0:
                away_win += p
            else:
                push += p
    # On push, stake returned — normalise to exclude push
    total = home_win + away_win + push
    if total == 0:
        return {"home": 0.5, "away": 0.5}
    # Return raw probabilities; stake refund on push handled by caller if needed
    return {"home": home_win + push * 0.5, "away": away_win + push * 0.5}


def most_likely_scores(matrix: np.ndarray, top_n: int = 5) -> list[tuple[int, int, float]]:
    """Return top_n most likely scores as list of (home_goals, away_goals, probability)."""
    n = matrix.shape[0]
    scores = [
        (i, j, matrix[i, j])
        for i in range(n)
        for j in range(n)
    ]
    scores.sort(key=lambda x: x[2], reverse=True)
    return scores[:top_n]
