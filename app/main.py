"""
VL2026 — Veikkausliiga 2026 ennustemalli
Streamlit entry point
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

st.set_page_config(
    page_title="VL2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

from app.views import team_page, match_page, schedule_page
from data.overrides import load_raw_overrides

PAGES = {
    "Otteluohjelma": schedule_page,
    "Matsianalyysi": match_page,
    "Joukkueet": team_page,
}

# Allow schedule page to navigate directly to match analysis
if "raw_overrides" not in st.session_state:
    st.session_state["raw_overrides"] = load_raw_overrides()
if "page" not in st.session_state:
    st.session_state["page"] = "Otteluohjelma"
if "team_detail" not in st.session_state:
    st.session_state["team_detail"] = None

with st.sidebar:
    st.title("⚽ VL2026")
    st.caption("Veikkausliiga 2026 ennustemalli")
    selected = st.radio("Navigaatio", list(PAGES.keys()),
                        index=list(PAGES.keys()).index(st.session_state["page"]))
    if selected != st.session_state["page"]:
        st.session_state["page"] = selected
        st.rerun()

PAGES[st.session_state["page"]].render()
