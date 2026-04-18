"""
Match report view: xG (manual entry) + structured lineup display + betting notes.
Navigated to from schedule page via session state 'report_fixture'.
"""

import re
import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from data.match_reports import get_report, save_report, make_key


def render():
    st.title("Matchrapport")

    fixture = st.session_state.get("report_fixture")
    if not fixture:
        st.info("Välj en match från matchprogrammet.")
        return

    home = fixture["home"]
    away = fixture["away"]
    date = fixture["date"]
    goals_home = fixture["goals_home"]
    goals_away = fixture["goals_away"]
    home_id = fixture["home_id"]
    away_id = fixture["away_id"]

    key = make_key(home_id, away_id, date)
    report = get_report(key)

    st.subheader(f"{home} {goals_home}–{goals_away} {away}")
    st.caption(date)
    st.divider()

    xg_home = report.get("xg_home")
    xg_away = report.get("xg_away")

    col_xg1, col_xg2, col_xg3 = st.columns([2, 1, 2])
    if xg_home is not None and xg_away is not None:
        col_xg1.metric(f"{home} xG", f"{xg_home:.2f}")
        col_xg3.metric(f"{away} xG", f"{xg_away:.2f}")
    else:
        col_xg2.write("")

    with st.expander("Redigera xG-värden"):
        with st.form("xg_form"):
            c1, c2 = st.columns(2)
            xg_h = c1.number_input(f"{home} xG", value=float(xg_home or 0.0),
                                   min_value=0.0, max_value=10.0, step=0.01, format="%.2f")
            xg_a = c2.number_input(f"{away} xG", value=float(xg_away or 0.0),
                                   min_value=0.0, max_value=10.0, step=0.01, format="%.2f")
            if st.form_submit_button("Spara xG", type="primary"):
                save_report(key, {"xg_home": xg_h, "xg_away": xg_a})
                st.rerun()

    st.divider()

    lineup_home = report.get("lineup_home")
    lineup_away = report.get("lineup_away")
    subs_home = report.get("subs_home", [])
    subs_away = report.get("subs_away", [])

    if lineup_home and lineup_away:
        st.subheader("Laguppställningar")
        col_h, col_a = st.columns(2)
        with col_h:
            _render_lineup(home, lineup_home, subs_home)
        with col_a:
            _render_lineup(away, lineup_away, subs_away)
        st.divider()

    notes = report.get("notes", "")
    if notes:
        st.subheader("Rapport")
        st.markdown(_safe_md(notes), unsafe_allow_html=True)
    else:
        st.subheader("Rapport")
        _notes_form(key, notes)


def _render_lineup(team_name: str, lineup: dict, subs: list) -> None:
    formation = lineup.get("formation", "")
    st.markdown(f"**{team_name}** _{formation}_")

    rows = [
        ("MV", lineup.get("gk", [])),
        ("DEF", lineup.get("def", [])),
        ("MF", lineup.get("mid", [])),
        ("FWD", lineup.get("fwd", [])),
    ]
    for label, players in rows:
        if players:
            st.markdown(
                f"<span style='color:gray;font-size:0.78em'>{label}</span> "
                + " · ".join(players),
                unsafe_allow_html=True,
            )

    if subs:
        st.markdown(
            "<span style='color:gray;font-size:0.78em'>BYTEN</span>",
            unsafe_allow_html=True,
        )
        for s in subs:
            st.markdown(
                f"<span style='font-size:0.85em'>{s['min']}' ↑ {s['in']} / ↓ {s['out']}</span>",
                unsafe_allow_html=True,
            )


def _safe_md(text: str) -> str:
    """Escape characters that confuse Streamlit's markdown parser."""
    text = re.sub(r':([^\s:])', lambda m: '&#58;' + m.group(1), text)
    text = re.sub(r'^(\d+)\.', r'\1\\.', text, flags=re.MULTILINE)
    return text


def _notes_form(key: str, current: str) -> None:
    new_notes = st.text_area(
        "Rapport",
        value=current,
        height=300,
        label_visibility="collapsed",
    )
    if st.button("Spara rapport", type="primary"):
        save_report(key, {"notes": new_notes})
        st.rerun()
