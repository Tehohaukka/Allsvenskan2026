"""
Bets view: table of placed bets with rationale and closing line tracking.
Read-only — edits via Claude or source.
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
from data.bets import load_bets


def render():
    st.title("Vad")

    bets = load_bets()

    open_bets = [b for b in bets if b["result"] is None]
    settled = [b for b in bets if b["profit_units"] is not None]
    total_pl = sum(b["profit_units"] for b in settled)
    total_staked = sum(b["stake_units"] for b in settled)
    roi = (total_pl / total_staked * 100) if total_staked else 0.0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Öppna vad", len(open_bets))
    c2.metric("Avgjorda", len(settled))
    c3.metric("P/L (u)", f"{total_pl:+.2f}" if settled else "—")
    c4.metric("ROI", f"{roi:.1f} %" if settled else "—")

    st.divider()

    if not bets:
        st.info("Inga registrerade vad.")
        return

    rows = []
    for b in bets:
        rows.append({
            "Datum": b["date_placed"],
            "Match": b["match"],
            "Marknad": b["market"],
            "Sajt": b["bookmaker"],
            "Odds": b["odds"],
            "Modell %": round(b["model_prob"] * 100, 1),
            "EV %": round((b["model_prob"] * b["odds"] - 1) * 100, 1),
            "Insats (u)": b["stake_units"],
            "P.stäng": b.get("closing_odds"),
            "No-vig %": round(b["closing_no_vig_prob"] * 100, 1) if b.get("closing_no_vig_prob") else None,
            "CLV %": b.get("clv_percent"),
            "Resultat": b["result"] or "—",
            "P/L (u)": b["profit_units"],
        })

    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Odds": st.column_config.NumberColumn(format="%.3f"),
            "Modell %": st.column_config.NumberColumn(format="%.1f"),
            "EV %": st.column_config.NumberColumn(format="%+.1f"),
            "P.stäng": st.column_config.NumberColumn(format="%.3f"),
            "No-vig %": st.column_config.NumberColumn(format="%.1f"),
            "CLV %": st.column_config.NumberColumn(format="%+.1f"),
            "P/L (u)": st.column_config.NumberColumn(format="%+.2f"),
        },
    )

    st.divider()

    st.subheader("Vaddetaljer")
    for b in bets:
        label = f"{b['date_placed']} · {b['match']} · {b['market']} @ {b['odds']}"
        with st.expander(label):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Odds", f"{b['odds']:.3f}")
            c2.metric("Modell", f"{b['model_prob']*100:.1f} %")
            edge = b["model_prob"] - (1 / b["odds"])
            c3.metric("Edge", f"{edge*100:+.1f} pp")
            c4.metric("Insats", f"{b['stake_units']} u")

            if b.get("closing_odds") or b.get("closing_no_vig_prob"):
                st.markdown("**Stängningskurser**")
                cc1, cc2, cc3 = st.columns(3)
                if b.get("closing_odds"):
                    cc1.metric("Pinnacle stäng", f"{b['closing_odds']:.3f}")
                if b.get("closing_no_vig_prob"):
                    cc2.metric("No-vig stäng", f"{b['closing_no_vig_prob']*100:.1f} %")
                if b.get("clv_percent") is not None:
                    cc3.metric("CLV", f"{b['clv_percent']:+.1f} %")

            if b.get("rationale"):
                st.markdown("**Motivering**")
                st.markdown(b["rationale"])

            if b.get("notes"):
                st.caption(b["notes"])
