"""
Elo rating system for Allsvenskan.

Key features:
  - Cross-season regression: pull ratings toward DEFAULT_RATING between seasons
    so previous-season outliers don't dominate early in the new season.
  - Decaying K-factor: higher K early in a season to let ratings settle faster;
    decays linearly toward the standard K over the first N rounds.
  - Home advantage modelled as an Elo point bonus for the home team.
  - Draw probability model: highest for balanced matches, decays with mismatch.
"""

from __future__ import annotations

import pandas as pd

DEFAULT_RATING: float = 1500.0
K_FACTOR: float = 30.0          # Standard K (used for historical seasons)
K_EARLY: float = 45.0           # K for round 1 of a new season
K_TRANSITION: int = 10          # Rounds over which K decays from K_EARLY to K_FACTOR
HOME_ADVANTAGE: float = 60.0    # Elo bonus for home team (~E_h=0.58 for equal teams)
DRAW_BASE: float = 0.27         # Peak draw probability for balanced matches
DRAW_DECAY: float = 2.0         # How fast draw prob falls as mismatch grows
REGRESSION_FACTOR: float = 0.35 # Fraction of (rating - mean) removed at season start


class EloRatings:
    """
    Maintains a dict of team_id -> Elo rating.
    Unknown / newly promoted teams default to DEFAULT_RATING.
    """

    def __init__(
        self,
        k: float = K_FACTOR,
        home_adv: float = HOME_ADVANTAGE,
        draw_base: float = DRAW_BASE,
        draw_decay: float = DRAW_DECAY,
    ) -> None:
        self.k = k
        self.home_adv = home_adv
        self.draw_base = draw_base
        self.draw_decay = draw_decay
        self._ratings: dict[int, float] = {}

    # ── Core ──────────────────────────────────────────────────────────────────

    def rating(self, team_id: int) -> float:
        return self._ratings.get(team_id, DEFAULT_RATING)

    def _expected(self, r_home: float, r_away: float) -> float:
        """Home expected score (win=1, draw=0.5, loss=0) including home advantage."""
        return 1.0 / (1.0 + 10.0 ** ((r_away - r_home - self.home_adv) / 400.0))

    def predict(self, home_id: int, away_id: int) -> dict[str, float]:
        """Return {'p1', 'pX', 'p2'} from current ratings."""
        e_h = self._expected(self.rating(home_id), self.rating(away_id))
        p_draw = self.draw_base * (1.0 - abs(2.0 * e_h - 1.0) ** self.draw_decay)
        p_draw = max(0.05, p_draw)
        p1 = max(0.01, e_h - p_draw / 2.0)
        p2 = max(0.01, 1.0 - e_h - p_draw / 2.0)
        total = p1 + p_draw + p2
        return {"p1": p1 / total, "pX": p_draw / total, "p2": p2 / total}

    def update(self, home_id: int, away_id: int,
               home_goals: int, away_goals: int,
               k: float | None = None) -> None:
        """Update ratings after a result. Optionally override K for this match."""
        k_eff = k if k is not None else self.k
        r_h = self.rating(home_id)
        r_a = self.rating(away_id)
        e_h = self._expected(r_h, r_a)
        s_h = 1.0 if home_goals > away_goals else (0.5 if home_goals == away_goals else 0.0)
        self._ratings[home_id] = r_h + k_eff * (s_h - e_h)
        self._ratings[away_id] = r_a + k_eff * ((1.0 - s_h) - (1.0 - e_h))

    # ── Season management ─────────────────────────────────────────────────────

    def regress_to_mean(self, factor: float = REGRESSION_FACTOR) -> EloRatings:
        """
        Pull all ratings toward DEFAULT_RATING at the start of a new season.
        factor: fraction of deviation removed.
          0.0 = no change, 1.0 = full reset to DEFAULT_RATING.
          0.35 means ratings move 35% of the way toward 1500.
        """
        for tid in self._ratings:
            deviation = self._ratings[tid] - DEFAULT_RATING
            self._ratings[tid] = DEFAULT_RATING + (1.0 - factor) * deviation
        return self

    @staticmethod
    def k_for_round(round_num: int,
                    k_early: float = K_EARLY,
                    k_base: float = K_FACTOR,
                    n_transition: int = K_TRANSITION) -> float:
        """
        Linear K-factor decay from k_early (round 1) to k_base (round n_transition+).
        round_num is 1-indexed (first round of new season = 1).
        """
        if round_num >= n_transition:
            return k_base
        t = (round_num - 1) / (n_transition - 1)
        return k_early + t * (k_base - k_early)

    # ── Batch fitting ──────────────────────────────────────────────────────────

    def fit(self, df: pd.DataFrame, k: float | None = None) -> EloRatings:
        """Process all matches in df chronologically. Optionally fix K for all."""
        for _, row in df.sort_values("date").iterrows():
            self.update(int(row["home_id"]), int(row["away_id"]),
                        int(row["home_goals"]), int(row["away_goals"]), k=k)
        return self

    def fit_with_rounds(self, df: pd.DataFrame,
                        k_early: float = K_EARLY,
                        k_base: float = K_FACTOR,
                        n_transition: int = K_TRANSITION) -> EloRatings:
        """
        Fit with round-dependent K. df must have a 'round' column (1-indexed).
        Matches without a round number use k_base.
        """
        for _, row in df.sort_values("date").iterrows():
            rnd = row.get("round", None)
            k = self.k_for_round(int(rnd), k_early, k_base, n_transition) \
                if rnd is not None and not pd.isna(rnd) else k_base
            self.update(int(row["home_id"]), int(row["away_id"]),
                        int(row["home_goals"]), int(row["away_goals"]), k=k)
        return self

    # ── Inspection ────────────────────────────────────────────────────────────

    def ratings_df(self) -> pd.DataFrame:
        rows = [{"team_id": tid, "elo": round(r, 1)}
                for tid, r in sorted(self._ratings.items(), key=lambda x: -x[1])]
        return pd.DataFrame(rows)
