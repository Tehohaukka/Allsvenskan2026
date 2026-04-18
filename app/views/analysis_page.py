"""
Analysis view: model predictions vs Pinnacle closing odds.

For each saved round, shows per-match comparison of:
  - 1X2 probabilities
  - Asian handicap (closest-to-even line)
  - Totals (closest-to-even line)

Pinnacle closing odds are converted to no-vig probabilities using
the standard normalization: p_i = (1/odds_i) / sum(1/odds_j).
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from data.predictions import load_predictions


# ── Helpers ──────────────────────────────────────────────────────────────────

def _no_vig_2way(o1: float, o2: float) -> tuple[float, float]:
    """Remove vig from a 2-way market."""
    p1, p2 = 1 / o1, 1 / o2
    total = p1 + p2
    return p1 / total, p2 / total


def _no_vig_3way(o1: float, oX: float, o2: float) -> tuple[float, float, float]:
    """Remove vig from a 3-way market."""
    p1, pX, p2 = 1 / o1, 1 / oX, 1 / o2
    total = p1 + pX + p2
    return p1 / total, pX / total, p2 / total


def _delta(model: float, closing: float) -> str:
    """Format probability delta as signed percentage points."""
    if model is None or closing is None:
        return "—"
    d = (model - closing) * 100
    return f"{d:+.1f} pp"


def _pct(v: float) -> str:
    if v is None:
        return "—"
    return f"{v * 100:.1f} %"


# ── Match card ────────────────────────────────────────────────────────────────

def _render_match(match: dict) -> None:
    m = match["model"]
    pc = match["pinnacle_closing"]
    res = match["result"]

    result_str = ""
    if res["home_goals"] is not None and res["away_goals"] is not None:
        result_str = f"  —  {res['home_goals']}–{res['away_goals']}"

    with st.expander(f"**{match['home']} vs {match['away']}**{result_str}", expanded=True):
        st.markdown("**1X2**")
        o1x2 = pc["1x2"]
        has_1x2 = all(o1x2.get(k) for k in ("1", "X", "2"))

        if has_1x2:
            c_p1, c_pX, c_p2 = _no_vig_3way(o1x2["1"], o1x2["X"], o1x2["2"])
        else:
            c_p1 = c_pX = c_p2 = None

        cols = st.columns(6)
        cols[0].metric("Modell 1", _pct(m["p1"]))
        cols[1].metric("Stäng 1", _pct(c_p1), delta=_delta(m["p1"], c_p1))
        cols[2].metric("Modell X", _pct(m["pX"]))
        cols[3].metric("Stäng X", _pct(c_pX), delta=_delta(m["pX"], c_pX))
        cols[4].metric("Modell 2", _pct(m["p2"]))
        cols[5].metric("Stäng 2", _pct(c_p2), delta=_delta(m["p2"], c_p2))

        st.divider()

        ah_m = m["ah"]
        ah_c = pc["ah"]
        has_ah = ah_c.get("home") is not None and ah_c.get("away") is not None

        if has_ah:
            c_ah_home, c_ah_away = _no_vig_2way(ah_c["home"], ah_c["away"])
        else:
            c_ah_home = c_ah_away = None

        line_label = f"AH {ah_m['line']:+.2f} (modell)"
        close_line = ah_c.get("line")
        close_label = f"AH {close_line:+.2f} (Pinnacle)" if close_line is not None else "AH (Pinnacle)"
        st.markdown(f"**{line_label}  ·  {close_label}**")

        cols = st.columns(4)
        cols[0].metric("Modell hemma", _pct(ah_m["home"]))
        cols[1].metric("Stäng hemma", _pct(c_ah_home), delta=_delta(ah_m["home"], c_ah_home))
        cols[2].metric("Modell borta", _pct(ah_m["away"]))
        cols[3].metric("Stäng borta", _pct(c_ah_away), delta=_delta(ah_m["away"], c_ah_away))

        st.divider()

        tot_m = m["totals"]
        tot_c = pc["totals"]
        has_tot = tot_c.get("over") is not None and tot_c.get("under") is not None

        if has_tot:
            c_over, c_under = _no_vig_2way(tot_c["over"], tot_c["under"])
        else:
            c_over = c_under = None

        tot_line_label = f"O/U {tot_m['line']} (modell)"
        c_tot_line = tot_c.get("line")
        c_tot_label = f"O/U {c_tot_line} (Pinnacle)" if c_tot_line is not None else "O/U (Pinnacle)"
        st.markdown(f"**{tot_line_label}  ·  {c_tot_label}**")

        cols = st.columns(4)
        cols[0].metric("Modell över", _pct(tot_m["over"]))
        cols[1].metric("Stäng över", _pct(c_over), delta=_delta(tot_m["over"], c_over))
        cols[2].metric("Modell under", _pct(tot_m["under"]))
        cols[3].metric("Stäng under", _pct(c_under), delta=_delta(tot_m["under"], c_under))


# ── Main render ───────────────────────────────────────────────────────────────

def render():
    st.title("Analys")

    data = load_predictions()
    if not data:
        st.info("Inga sparade förutsägelser. Kör save_predictions.py före omgången.")
        return

    rounds = sorted(s["round"] for s in data)
    selected = st.selectbox("Omgång", rounds, index=len(rounds) - 1,
                            format_func=lambda r: f"Omgång {r}")

    snap = next(s for s in data if s["round"] == selected)
    st.caption(f"Sparad: {snap['saved_at'][:16].replace('T', ' ')} UTC")
    st.divider()

    for match in snap["matches"]:
        _render_match(match)
