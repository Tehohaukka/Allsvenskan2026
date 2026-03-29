"""
Voimasuhteet-sivu: joukkuetaulukko tähtiluokituksineen, MUOKKAA-napilla avattava editointi.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from data.overrides import load_raw_overrides, save_raw_overrides, normalise
from data.team_notes import TEAM_NOTES
from app.data_loader import load_strength_overrides


def render():
    st.title("Voimasuhteet")

    if "editing_team" not in st.session_state:
        st.session_state["editing_team"] = None

    raw = load_raw_overrides()
    normalised = normalise(raw)
    sorted_ids = sorted(raw, key=lambda k: raw[k]["attack"], reverse=True)

    # Header
    cols = st.columns([0.4, 2.5, 1.8, 1.2, 1.2, 1.2, 1.2])
    for col, label in zip(cols, ["**#**", "**Joukkue**", "**Positiossa-tähdet**",
                                  "**Hyökkäys**", "**Puolustus**", "**Ratio**", ""]):
        col.markdown(label)
    st.divider()

    for i, tid in enumerate(sorted_ids, 1):
        entry = raw[tid]
        s = normalised[tid]
        ratio = s["attack"] / s["defense"]
        notes = TEAM_NOTES.get(tid)

        # Stars
        stars = ""
        if notes:
            t = notes["tahdet"]
            stars = "★" * int(t) + ("½" if t % 1 else "") + "☆" * (5 - int(t) - (1 if t % 1 else 0))

        c_rank, c_name, c_stars, c_att, c_def, c_ratio, c_btn = st.columns([0.4, 2.5, 1.8, 1.2, 1.2, 1.2, 1.2])
        c_rank.write(str(i))
        c_name.write(f"**{entry['name']}**")
        c_stars.write(stars)
        c_att.write(f"{s['attack']:.3f}")
        c_def.write(f"{s['defense']:.3f}")
        c_ratio.write(f"{ratio:.3f}")

        if st.session_state["editing_team"] == tid:
            if c_btn.button("Sulje", key=f"close_{tid}"):
                st.session_state["editing_team"] = None
                st.rerun()

            with st.form(key=f"form_{tid}"):
                st.markdown(f"**Muokkaa: {entry['name']}** *(raakaarvot, normalisoidaan tallennettaessa)*")
                fc1, fc2 = st.columns(2)
                new_att = fc1.number_input("Hyökkäys", value=float(entry["attack"]),
                                           min_value=0.3, max_value=2.5, step=0.01, format="%.3f")
                new_def = fc2.number_input("Puolustus *(pienempi = parempi)*",
                                           value=float(entry["defense"]),
                                           min_value=0.3, max_value=2.5, step=0.01, format="%.3f")
                if st.form_submit_button("💾 Tallenna", type="primary"):
                    raw[tid]["attack"] = new_att
                    raw[tid]["defense"] = new_def
                    save_raw_overrides(raw)
                    load_strength_overrides.clear()
                    st.session_state["editing_team"] = None
                    st.rerun()
        else:
            if c_btn.button("Muokkaa", key=f"edit_{tid}"):
                st.session_state["editing_team"] = tid
                st.rerun()

        st.divider()
