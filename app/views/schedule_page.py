"""
Schedule page: shows all 2026 fixtures grouped by round.
Clicking a match navigates to match analysis with teams pre-filled.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from api.football_api import get_fixtures
from config import ALLSVENSKAN_ID, SEASON_2026
from data.overrides import NAME_OVERRIDES


@st.cache_data(ttl=3600, show_spinner=False)
def _load_fixtures():
    fixtures = get_fixtures(ALLSVENSKAN_ID, SEASON_2026)
    rounds = {}
    for f in fixtures:
        status = f["fixture"]["status"]["short"]
        round_name = f["league"]["round"]
        date = f["fixture"]["date"][:10]
        home_id = f["teams"]["home"]["id"]
        away_id = f["teams"]["away"]["id"]
        home = NAME_OVERRIDES.get(home_id, f["teams"]["home"]["name"])
        away = NAME_OVERRIDES.get(away_id, f["teams"]["away"]["name"])
        goals_home = f["goals"]["home"]
        goals_away = f["goals"]["away"]

        if round_name not in rounds:
            rounds[round_name] = []
        rounds[round_name].append({
            "fixture_id": f["fixture"]["id"],
            "date": date,
            "home": home,
            "away": away,
            "home_id": home_id,
            "away_id": away_id,
            "status": status,
            "goals_home": goals_home,
            "goals_away": goals_away,
        })
    return rounds


def _round_number(round_name: str) -> int:
    try:
        return int(round_name.split("-")[-1].strip())
    except ValueError:
        return 999


def render():
    st.title("Matchprogram 2026")

    col_title, col_refresh = st.columns([5, 1])
    with col_refresh:
        if st.button("🔄 Uppdatera"):
            _load_fixtures.clear()

    with st.spinner("Laddar matchprogram..."):
        rounds = _load_fixtures()

    sorted_rounds = sorted(rounds.keys(), key=_round_number)

    round_labels = {r: f"Omgång {_round_number(r)}" for r in sorted_rounds}

    col1, col2 = st.columns([2, 1])
    with col1:
        show_played = st.toggle("Visa spelade matcher", value=True)
    with col2:
        label_options = ["—"] + [round_labels[r] for r in sorted_rounds]
        selected_label = st.selectbox("Gå till omgång", label_options, label_visibility="collapsed")
        jump_to = next((r for r in sorted_rounds if round_labels[r] == selected_label), "—")

    _active_round = next(
        (r for r in sorted_rounds if any(m["status"] == "NS" or m["goals_home"] is None
                                         for m in rounds[r])),
        sorted_rounds[-1] if sorted_rounds else None,
    )

    if jump_to != "—":
        sorted_rounds = [r for r in sorted_rounds if r == jump_to] + \
                        [r for r in sorted_rounds if r != jump_to]

    for round_name in sorted_rounds:
        matches = rounds[round_name]
        has_unplayed = any(m["status"] == "NS" for m in matches)

        if not show_played and not has_unplayed:
            continue

        dates = sorted(set(m["date"] for m in matches))
        date_str = dates[0] if len(dates) == 1 else f"{dates[0]} – {dates[-1]}"
        round_num = _round_number(round_name)

        with st.expander(f"**Omgång {round_num}** — {date_str}", expanded=(round_name == _active_round)):
            for m in sorted(matches, key=lambda x: x["date"]):
                if not show_played and m["status"] != "NS":
                    continue

                col_date, col_match, col_analysera, col_rapport = st.columns([1.2, 3, 1, 1.2])

                with col_date:
                    st.caption(m["date"])

                with col_match:
                    if m["status"] == "NS":
                        st.write(f"**{m['home']}** vs **{m['away']}**")
                    else:
                        score = f"{m['goals_home']}–{m['goals_away']}"
                        st.write(f"{m['home']} **{score}** {m['away']}")

                with col_analysera:
                    if st.button("Analysera →", key=f"match_{m['home']}_{m['away']}_{m['date']}"):
                        st.session_state["match_home"] = m["home"]
                        st.session_state["match_away"] = m["away"]
                        st.session_state["page"] = "Matchanalys"
                        st.rerun()

                with col_rapport:
                    played = m["status"] != "NS" and m["goals_home"] is not None
                    if played:
                        if st.button("Rapport →", key=f"report_{m['home']}_{m['away']}_{m['date']}"):
                            st.session_state["report_fixture"] = m
                            st.session_state["page"] = "Matchrapport"
                            st.rerun()
                    else:
                        st.caption("Rapport", help="Tillgänglig efter matchen")
