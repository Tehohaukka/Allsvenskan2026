"""
Match view: pick two teams, get Poisson probabilities.
Shows 1X2, over/under, Asian handicap, and score heatmap.
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.data_loader import load_strengths_and_averages, load_teams_2026, get_strength
from model.strengths import expected_goals
from model.poisson import DC_RHO
from model.poisson import (
    score_matrix, result_probabilities, over_under,
    asian_handicap,
)


def render():
    st.title("Matchanalys")

    with st.spinner("Laddar data..."):
        strengths, avg_home, avg_away = load_strengths_and_averages()
        teams = load_teams_2026()

    if not teams:
        st.error("Inga lag hittades. Kontrollera API-nyckel eller säsongstillgänglighet.")
        return

    team_names = sorted(t["name"] for t in teams)
    team_map = {t["name"]: t["id"] for t in teams}

    preset_home = st.session_state.pop("match_home", None)
    preset_away = st.session_state.pop("match_away", None)

    if preset_home in team_names:
        st.session_state["sel_home"] = preset_home

    col1, col2 = st.columns(2)
    with col1:
        home_name = st.selectbox("Hemmalag", team_names, key="sel_home")
    with col2:
        away_options = [n for n in team_names if n != home_name]
        if preset_away in away_options:
            st.session_state["sel_away"] = preset_away
        elif st.session_state.get("sel_away") not in away_options:
            st.session_state["sel_away"] = away_options[0]
        away_name = st.selectbox("Bortalag", away_options, key="sel_away")

    home_id = team_map[home_name]
    away_id = team_map[away_name]

    home_s = get_strength(strengths, home_id)
    away_s = get_strength(strengths, away_id)

    with st.expander("Modellparametrar", expanded=False):
        avg_home = st.slider("Hemma avg mål/match", 0.5, 3.0, float(round(avg_home, 4)), step=0.01)
        avg_away = st.slider("Borta avg mål/match", 0.5, 3.0, float(round(avg_away, 4)), step=0.01)
        rho = st.slider("Dixon-Coles ρ", -0.30, 0.0, float(DC_RHO), step=0.01,
                        help="Negativt värde ökar sannolikheten för oavgjort och 1-målsmatcher")

        st.divider()
        st.markdown(f"**{home_name} (hemma)**")
        c1, c2 = st.columns(2)
        home_att = c1.slider("Anfallskraft", 0.3, 2.5, float(round(home_s["attack"], 3)), step=0.01, key=f"home_att_{home_id}")
        home_def = c2.slider("Försvar", 0.3, 2.5, float(round(home_s["defense"], 3)), step=0.01, key=f"home_def_{home_id}",
                             help="Lägre = bättre")

        st.markdown(f"**{away_name} (borta)**")
        c3, c4 = st.columns(2)
        away_att = c3.slider("Anfallskraft", 0.3, 2.5, float(round(away_s["attack"], 3)), step=0.01, key=f"away_att_{away_id}")
        away_def = c4.slider("Försvar", 0.3, 2.5, float(round(away_s["defense"], 3)), step=0.01, key=f"away_def_{away_id}",
                             help="Lägre = bättre")

    xg_home, xg_away = expected_goals(
        home_att, away_def,
        away_att, home_def,
        avg_home=avg_home,
        avg_away=avg_away,
    )

    matrix = score_matrix(xg_home, xg_away, rho=rho)
    results = result_probabilities(matrix)

    st.divider()
    st.subheader("Förväntade mål")
    c1, c2 = st.columns(2)
    c1.metric(f"{home_name} xG", f"{xg_home:.2f}")
    c2.metric(f"{away_name} xG", f"{xg_away:.2f}")

    st.divider()
    st.subheader("1X2")
    c1, c2, c3 = st.columns(3)
    for col, key, label in [(c1, "1", f"1 ({home_name})"),
                             (c2, "X", "X (oavgjort)"),
                             (c3, "2", f"2 ({away_name})")]:
        p = results[key]
        col.metric(label, f"{p*100:.1f}%", f"Fair odds {1/p:.2f}")

    st.divider()
    st.subheader("Över mål")
    ou_lines = [1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5]
    import pandas as pd
    ou_data = []
    for line in ou_lines:
        ou = over_under(matrix, line)
        ou_data.append({
            "Rad": f"Över {line}",
            "Sannolikhet": f"{(1/ou['fair_odds'])*100:.1f}%",
            "Fair odds": f"{ou['fair_odds']:.2f}",
        })
    st.dataframe(pd.DataFrame(ou_data), hide_index=True)

    st.divider()
    st.subheader("Asiatiska handikapp")
    ah_lines = [-2.0, -1.75, -1.5, -1.25, -1.0, -0.75, -0.5, -0.25,
                0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
    ah_data = []
    for line in ah_lines:
        p = asian_handicap(matrix, line)
        ah_data.append({
            "Handikapp (hemma)": f"{line:+.2f}",
            f"{home_name}": f"{p['home']*100:.1f}%",
            f"{away_name}": f"{p['away']*100:.1f}%",
        })

    st.dataframe(pd.DataFrame(ah_data), use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Resultatmatris")
    _plot_heatmap(matrix, home_name, away_name)


def _plot_heatmap(matrix: np.ndarray, home_name: str, away_name: str, max_show: int = 7):
    m = matrix[:max_show, :max_show] * 100
    fig = go.Figure(data=go.Heatmap(
        z=m,
        x=[str(i) for i in range(max_show)],
        y=[str(i) for i in range(max_show)],
        colorscale=[[0, "#d73027"], [0.5, "#ffffbf"], [1, "#1a9850"]],
        text=[[f"{m[i][j]:.1f}%" for j in range(max_show)] for i in range(max_show)],
        texttemplate="%{text}",
        showscale=False,
    ))
    fig.update_layout(
        xaxis_title=f"{away_name} mål",
        yaxis_title=f"{home_name} mål",
        margin=dict(l=40, r=20, t=20, b=40),
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)
