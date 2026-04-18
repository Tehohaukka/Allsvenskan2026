"""
Styrkeförhållanden: lagstabell med stjärnklassificering och redigeringsknapp.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from data.overrides import load_raw_overrides, save_raw_overrides, normalise
from data.team_notes import TEAM_NOTES
from app.data_loader import load_strengths_and_averages


def render():
    st.title("Styrkeförhållanden")

    if "editing_team" not in st.session_state:
        st.session_state["editing_team"] = None

    raw = load_raw_overrides()
    normalised = normalise(raw)
    sorted_ids = sorted(raw, key=lambda k: raw[k]["attack"], reverse=True)

    cols = st.columns([0.4, 2.5, 1.8, 1.2, 1.2, 1.2, 1.2])
    for col, label in zip(cols, ["**#**", "**Lag**", "**Stjärnor**",
                                  "**Anfall**", "**Försvar**", "**Kvot**", ""]):
        col.markdown(label)
    st.divider()

    for i, tid in enumerate(sorted_ids, 1):
        entry = raw[tid]
        s = normalised[tid]
        ratio = s["attack"] / s["defense"]
        notes = TEAM_NOTES.get(tid)

        stars = ""
        if notes:
            t = notes["stjarnor"]
            stars = "★" * int(t) + ("½" if t % 1 else "") + "☆" * (5 - int(t) - (1 if t % 1 else 0))

        c_rank, c_name, c_stars, c_att, c_def, c_ratio, c_btn = st.columns([0.4, 2.5, 1.8, 1.2, 1.2, 1.2, 1.2])
        c_rank.write(str(i))
        c_name.write(f"**{entry['name']}**")
        c_stars.write(stars)
        c_att.write(f"{s['attack']:.3f}")
        c_def.write(f"{s['defense']:.3f}")
        c_ratio.write(f"{ratio:.3f}")

        if st.session_state["editing_team"] == tid:
            if c_btn.button("Stäng", key=f"close_{tid}"):
                st.session_state["editing_team"] = None
                st.rerun()

            with st.form(key=f"form_{tid}"):
                st.markdown(f"**Redigera: {entry['name']}** *(råvärden, normaliseras vid sparande)*")
                fc1, fc2 = st.columns(2)
                new_att = fc1.number_input("Anfall", value=float(entry["attack"]),
                                           min_value=0.3, max_value=2.5, step=0.01, format="%.3f")
                new_def = fc2.number_input("Försvar *(lägre = bättre)*",
                                           value=float(entry["defense"]),
                                           min_value=0.3, max_value=2.5, step=0.01, format="%.3f")
                if st.form_submit_button("💾 Spara", type="primary"):
                    raw[tid]["attack"] = new_att
                    raw[tid]["defense"] = new_def
                    save_raw_overrides(raw)
                    load_strengths_and_averages.clear()
                    st.session_state["editing_team"] = None
                    st.rerun()
        else:
            if c_btn.button("Redigera", key=f"edit_{tid}"):
                st.session_state["editing_team"] = tid
                st.rerun()

        st.divider()
