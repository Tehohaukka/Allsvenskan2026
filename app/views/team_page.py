"""
Team page: overview table of all teams, click to see individual team detail.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.data_loader import load_strengths_and_averages, load_teams_2026, load_squad, get_strength, get_session_overrides
from data.overrides import NAME_OVERRIDES, normalise
from data.team_notes import TEAM_NOTES


def render():
    if "editing_team" not in st.session_state:
        st.session_state["editing_team"] = None
    if "team_detail" in st.session_state and st.session_state["team_detail"]:
        _render_team_detail()
    else:
        _render_overview()


def _render_overview():
    st.title("Lag 2026")

    with st.spinner("Laddar data..."):
        strengths, avg_home, avg_away = load_strengths_and_averages()
        teams = load_teams_2026()

    if not teams:
        st.error("Inga lag hittades.")
        return

    team_map = {t["id"]: NAME_OVERRIDES.get(t["id"], t["name"]) for t in teams}

    rows = []
    for tid, s in get_session_overrides().items():
        name = team_map.get(tid, f"id={tid}")
        ratio = s["attack"] / s["defense"]
        rows.append((ratio, name, tid, s["attack"], s["defense"]))
    rows.sort(reverse=True)

    st.caption(
        f"Hemmalagets målförväntning **{avg_home:.2f}** baseras på föregående säsong (2025). "
        f"Bortalaget **{avg_away:.2f}** är en utjämnad uppskattning baserad på Allsvenskans "
        f"historiska data och hemmafördelens storlek i liknande ligor. "
        f"Anfall- och försvarskoefficienterna är normaliserade så att ligasnittet = 1,00."
    )

    raw = st.session_state["raw_overrides"]

    st.subheader("Styrketabell")
    header = st.columns([0.4, 2.5, 1.8, 1.2, 1.2, 1.2, 1.5])
    for col, label in zip(header, ["**#**", "**Lag**", "**Stjärnor**",
                                    "**Anfall**", "**Försvar**", "**Kvot**", ""]):
        col.markdown(label)
    st.divider()

    for i, (ratio, name, tid, attack, defense) in enumerate(rows, 1):
        col_rank, col_name, col_stars, col_att, col_def, col_ratio, col_btns = st.columns([0.4, 2.5, 1.8, 1.2, 1.2, 1.2, 1.5])
        col_rank.write(f"{i}")
        col_name.write(f"**{name}**")
        notes = TEAM_NOTES.get(tid)
        if notes:
            t = notes["stjarnor"]
            stars = "★" * int(t) + ("½" if t % 1 else "") + "☆" * (5 - int(t) - (1 if t % 1 else 0))
            col_stars.write(stars)
        col_att.write(f"{attack:.3f}")
        col_def.write(f"{defense:.3f}")
        col_ratio.write(f"{ratio:.3f}")
        b1, b2 = col_btns.columns(2)
        if b1.button("Öppna →", key=f"team_{tid}"):
            st.session_state["team_detail"] = {"id": tid, "name": name}
            st.rerun()
        if st.session_state["editing_team"] == tid:
            if b2.button("Stäng", key=f"close_{tid}"):
                st.session_state["editing_team"] = None
                st.rerun()
            with st.form(key=f"form_{tid}"):
                st.markdown(f"**Redigera: {name}** *(råvärden, normaliseras vid sparande)*")
                fc1, fc2 = st.columns(2)
                new_att = fc1.number_input("Anfall", value=float(raw[tid]["attack"]),
                                           min_value=0.3, max_value=2.5, step=0.01, format="%.3f")
                new_def = fc2.number_input("Försvar *(lägre = bättre)*",
                                           value=float(raw[tid]["defense"]),
                                           min_value=0.3, max_value=2.5, step=0.01, format="%.3f")
                if st.form_submit_button("💾 Spara", type="primary"):
                    raw[tid]["attack"] = new_att
                    raw[tid]["defense"] = new_def
                    st.session_state["raw_overrides"] = raw
                    st.session_state["editing_team"] = None
                    st.rerun()
        else:
            if b2.button("Redigera", key=f"edit_{tid}"):
                st.session_state["editing_team"] = tid
                st.rerun()

    st.divider()
    n = len(rows)
    avg_att = sum(r[3] for r in rows) / n
    avg_def = sum(r[4] for r in rows) / n
    avg_ratio = avg_att / avg_def
    stjarnor_vals = [TEAM_NOTES[r[2]]["stjarnor"] for r in rows if r[2] in TEAM_NOTES]
    avg_stars = sum(stjarnor_vals) / len(stjarnor_vals) if stjarnor_vals else None

    avg_cols = st.columns([0.4, 2.5, 1.8, 1.2, 1.2, 1.2, 1.2])
    avg_cols[0].markdown("**—**")
    avg_cols[1].markdown("**Genomsnitt**")
    avg_cols[2].markdown(f"**{avg_stars:.1f} / 5**" if avg_stars is not None else "")
    avg_cols[3].markdown(f"**{avg_att:.3f}**")
    avg_cols[4].markdown(f"**{avg_def:.3f}**")
    avg_cols[5].markdown(f"**{avg_ratio:.3f}**")


def _render_team_detail():
    team = st.session_state["team_detail"]
    team_id = team["id"]
    team_name = team["name"]

    if st.button("← Tillbaka"):
        st.session_state["team_detail"] = None
        st.rerun()

    st.title(team_name)

    with st.spinner("Laddar data..."):
        strengths, _, _ = load_strengths_and_averages()

    s = get_strength(strengths, team_id)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Matcher (2025)", s["games"])
    col2.metric("Gjorda mål", s["scored"])
    col3.metric("Insläppta mål", s["conceded"])
    col4.metric("Mål / match", f"{s['scored']/s['games']:.2f}" if s["games"] else "–")

    col_a, col_d = st.columns(2)
    with col_a:
        st.subheader("Anfallskraft")
        st.metric(label="(ligasnitt = 1,00)", value=f"{s['attack']:.3f}",
                  delta=f"{s['attack'] - 1.0:+.3f}")
        st.progress(min(int(s["attack"] / 2.0 * 100), 100))

    with col_d:
        st.subheader("Försvarskraft")
        st.metric(label="(lägre = bättre, snitt = 1,00)", value=f"{s['defense']:.3f}",
                  delta=f"{1.0 - s['defense']:+.3f} vs snitt")
        st.progress(min(int((2.0 - s["defense"]) / 2.0 * 100), 100))

    notes = TEAM_NOTES.get(team_id)
    if notes:
        st.divider()

        t = notes["stjarnor"]
        stars_filled = "★" * int(t)
        stars_half   = "½" if t % 1 else ""
        stars_empty  = "☆" * (5 - int(t) - (1 if stars_half else 0))
        st.markdown(
            f"**{stars_filled}{stars_half}{stars_empty}** &nbsp; *{notes['kategori']}* &ensp; | &ensp; "
            f"Placering 2025: {notes['placering_2025']}"
        )

        col_notes, col_lineup = st.columns([1.3, 1])

        with col_notes:
            st.subheader("Anteckningar")

            transfers = notes.get("transfers", {})
            if transfers.get("in"):
                st.markdown("**Anlänt:** " + ", ".join(transfers["in"]))
            if transfers.get("out"):
                st.markdown("**Lämnat:** " + ", ".join(transfers["out"]))

            st.markdown("")
            for bullet in notes.get("anteckningar", []):
                st.markdown(f"- {bullet}")

        with col_lineup:
            ko = notes.get("startuppstallning")
            if ko:
                st.subheader(f"Startuppställning ({ko['formation']})")
                for rivi in ko["rader"]:
                    cols = st.columns(len(rivi))
                    for col, namn in zip(cols, rivi):
                        col.markdown(
                            f"<div style='text-align:center; background:#1565c0; "
                            f"color:#ffffff; font-weight:600; "
                            f"border-radius:8px; padding:10px 6px; "
                            f"font-size:1em;'>{namn}</div>",
                            unsafe_allow_html=True,
                        )
                    st.markdown("")

    st.divider()
    st.subheader("Spelartrupp (API)")

    with st.spinner("Laddar spelare..."):
        squad = load_squad(team_id)

    if not squad:
        st.info("Spelaruppgifter inte tillgängliga.")
        return

    pos_order = {"Goalkeeper": 0, "Defender": 1, "Midfielder": 2, "Attacker": 3}
    pos_labels = {"Goalkeeper": "Målvakter", "Defender": "Försvarare",
                  "Midfielder": "Mittfältare", "Attacker": "Anfallare"}
    squad_sorted = sorted(squad, key=lambda p: pos_order.get(p.get("position", ""), 9))

    current_pos = None
    for player in squad_sorted:
        pos = player.get("position", "Unknown")
        if pos != current_pos:
            st.markdown(f"**{pos_labels.get(pos, pos)}**")
            current_pos = pos
        number = player.get("number") or "–"
        st.write(f"  #{number} {player['name']}")
