"""
Ensemble model: Dixon-Coles (50%) + Elo (30%) + Form (20%).

Elo handling:
  - 2025 (historical) data fitted with standard K=30.
  - Cross-season regression applied before 2026 predictions begin:
      new_rating = 1500 + (1 - regression_factor) * (old_rating - 1500)
  - 2026 matches fitted with decaying K (K_EARLY → K_FACTOR over K_TRANSITION rounds)
    so the model adapts quickly at the start of the new season.

DC handling:
  - Weighted training data (2026 = 2x weight) + Bayesian shrinkage on strengths.

Form handling:
  - Bradley-Terry model on last N match points-per-game from training data.
  - Fixed draw rate; form mainly signals relative home/away strength.
"""

from __future__ import annotations

import pandas as pd

from model.elo import EloRatings, K_EARLY, K_FACTOR, K_TRANSITION, REGRESSION_FACTOR
from model.strengths import calculate_strengths, league_averages, expected_goals
from model.poisson import score_matrix, result_probabilities, DC_RHO

WEIGHTS = {"dc": 0.50, "elo": 0.30, "form": 0.20}
FORM_N = 5
FORM_DRAW_RATE = 0.27
FORM_EPS = 0.15


# ── Form ──────────────────────────────────────────────────────────────────────

def _team_form(team_id: int, df: pd.DataFrame, n: int = FORM_N) -> dict:
    """Points-per-game from last n matches for team_id in df (training data only)."""
    home = df[df["home_id"] == team_id][["date", "home_goals", "away_goals"]].copy()
    home["pts"] = (home["home_goals"] > home["away_goals"]).astype(int) * 3 \
                + (home["home_goals"] == home["away_goals"]).astype(int)

    away = df[df["away_id"] == team_id][["date", "away_goals", "home_goals"]].copy()
    away["pts"] = (away["away_goals"] > away["home_goals"]).astype(int) * 3 \
                + (away["away_goals"] == away["home_goals"]).astype(int)

    recent = pd.concat([home[["date", "pts"]], away[["date", "pts"]]]) \
               .sort_values("date").tail(n)

    if recent.empty:
        return {"pts_per_game": 1.0, "n_games": 0}
    return {"pts_per_game": float(recent["pts"].mean()), "n_games": len(recent)}


def form_probs(form_h: dict, form_a: dict,
               draw_rate: float = FORM_DRAW_RATE,
               eps: float = FORM_EPS) -> dict[str, float]:
    """Convert form to 1X2 via Bradley-Terry with Bayesian smoothing."""
    ph = form_h["pts_per_game"] / 3.0
    pa = form_a["pts_per_game"] / 3.0
    strength = (ph + eps) / (ph + pa + 2.0 * eps)
    return {"p1": strength * (1.0 - draw_rate),
            "pX": draw_rate,
            "p2": (1.0 - strength) * (1.0 - draw_rate)}


# ── DC ────────────────────────────────────────────────────────────────────────

def dc_probs(home_name: str, away_name: str,
             strengths: dict, avg_home: float, avg_away: float,
             rho: float = DC_RHO) -> dict[str, float]:
    default = {"attack": 1.0, "defense": 1.0}
    hs = strengths.get(home_name, default)
    as_ = strengths.get(away_name, default)
    xgh, xga = expected_goals(hs["attack"], as_["defense"],
                               as_["attack"], hs["defense"],
                               avg_home, avg_away)
    p = result_probabilities(score_matrix(xgh, xga, rho=rho))
    return {"p1": p["1"], "pX": p["X"], "p2": p["2"],
            "xg_home": xgh, "xg_away": xga}


# ── Combine ───────────────────────────────────────────────────────────────────

def combine(dc: dict, elo: dict, form: dict,
            weights: dict = WEIGHTS) -> dict[str, float]:
    p1 = weights["dc"]*dc["p1"] + weights["elo"]*elo["p1"] + weights["form"]*form["p1"]
    pX = weights["dc"]*dc["pX"] + weights["elo"]*elo["pX"] + weights["form"]*form["pX"]
    p2 = weights["dc"]*dc["p2"] + weights["elo"]*elo["p2"] + weights["form"]*form["p2"]
    t = p1 + pX + p2
    return {"p1": p1/t, "pX": pX/t, "p2": p2/t}


# ── EnsembleModel ─────────────────────────────────────────────────────────────

class EnsembleModel:
    """
    Rolling ensemble. Call fit(df_train) before predicting each round.

    Parameters
    ----------
    rho              : Dixon-Coles correlation (default -0.20).
    shrinkage        : Bayesian shrinkage games for DC strengths.
    weights          : Component weights {'dc', 'elo', 'form'}.
    regression_factor: Fraction of Elo deviation removed at season start (0–1).
    k_early          : K-factor for round 1 of new season.
    k_base           : K-factor for rounds >= k_transition.
    k_transition     : Number of rounds for K to decay from k_early to k_base.
    """

    def __init__(
        self,
        rho: float = DC_RHO,
        shrinkage: float = 10.0,
        weights: dict = WEIGHTS,
        regression_factor: float = REGRESSION_FACTOR,
        k_early: float = K_EARLY,
        k_base: float = K_FACTOR,
        k_transition: int = K_TRANSITION,
    ) -> None:
        self.rho = rho
        self.shrinkage = shrinkage
        self.weights = weights
        self.regression_factor = regression_factor
        self.k_early = k_early
        self.k_base = k_base
        self.k_transition = k_transition
        self._strengths: dict = {}
        self._avg_home: float = 1.55
        self._avg_away: float = 1.40
        self._elo = EloRatings()
        self._df_train: pd.DataFrame = pd.DataFrame()

    def fit(self, df_train: pd.DataFrame) -> EnsembleModel:
        """
        Build all sub-models from combined training data.
        df_train must have 'weight' and optionally 'round' columns.
        Rows with date.year < 2026 are treated as historical; others as current season.
        """
        # ── DC strengths ──────────────────────────────────────────────────────
        sdf = calculate_strengths(df_train, shrinkage_games=self.shrinkage)
        avgs = league_averages(df_train)
        self._strengths = {r["team_name"]: {"attack": r["attack"], "defense": r["defense"]}
                           for _, r in sdf.iterrows()}
        self._avg_home = avgs["avg_home"]
        self._avg_away = avgs["avg_away"]

        # ── Elo: split historical (2025) vs current season (2026) ─────────────
        df_sorted = df_train.sort_values("date").reset_index(drop=True)
        is_hist = df_sorted["date"].dt.year < 2026

        df_hist = df_sorted[is_hist]
        df_curr = df_sorted[~is_hist]

        elo = EloRatings(k=self.k_base, home_adv=60.0)

        # 1. Fit on historical with standard K
        elo.fit(df_hist, k=self.k_base)

        # 2. Cross-season regression
        elo.regress_to_mean(self.regression_factor)

        # 3. Fit on current-season matches with decaying K
        if not df_curr.empty and "round" in df_curr.columns:
            elo.fit_with_rounds(df_curr,
                                k_early=self.k_early,
                                k_base=self.k_base,
                                n_transition=self.k_transition)
        else:
            elo.fit(df_curr, k=self.k_early)

        self._elo = elo
        self._df_train = df_sorted
        return self

    def predict_match(self, home_id: int, away_id: int,
                      home_name: str, away_name: str) -> dict:
        dc  = dc_probs(home_name, away_name, self._strengths,
                       self._avg_home, self._avg_away, self.rho)
        elo = self._elo.predict(home_id, away_id)
        fh  = _team_form(home_id, self._df_train)
        fa  = _team_form(away_id, self._df_train)
        frm = form_probs(fh, fa)
        ens = combine(dc, elo, frm, self.weights)
        return {
            "p1": ens["p1"], "pX": ens["pX"], "p2": ens["p2"],
            "xg_home": dc["xg_home"], "xg_away": dc["xg_away"],
            "dc":   {"p1": dc["p1"],  "pX": dc["pX"],  "p2": dc["p2"]},
            "elo":  {"p1": elo["p1"], "pX": elo["pX"], "p2": elo["p2"]},
            "form": {"p1": frm["p1"], "pX": frm["pX"], "p2": frm["p2"]},
            "form_h": fh, "form_a": fa,
        }
