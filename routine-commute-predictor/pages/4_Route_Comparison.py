import pandas as pd
import streamlit as st

from src.prediction import get_demo_route_options, score_route_options
from src.recommendation import attach_route_statuses
from src.ui import inject_global_css, render_top_nav


st.set_page_config(
    page_title="Route Comparison | TripMate",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def refresh_predictions() -> None:
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {
            "name": "Nawfal",
            "origin": "Parramatta",
            "destination": "Central",
            "departure_time": "07:42",
            "arrival_goal": "08:30",
            "walking_tolerance": 8,
            "priority": "Lower stress",
            "weights": {"speed": 30, "stress": 50, "reliability": 20},
        }

    profile = st.session_state.user_profile
    raw_routes = get_demo_route_options(profile)
    scored_routes = score_route_options(profile, raw_routes)
    enriched_routes = attach_route_statuses(scored_routes)

    st.session_state.route_options = enriched_routes


inject_global_css()
refresh_predictions()
render_top_nav("routes")

routes = st.session_state.route_options
df = pd.DataFrame(routes)

st.markdown(
    """
    <div class="hero-card">
        <h1 style="margin-top:0; margin-bottom:0.35rem;">Compare today’s route options</h1>
        <p class="small-note" style="font-size:1rem; margin-bottom:0;">
            This page turns raw train conditions into a clear recommendation that matches the commuter’s preferences.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

cols = st.columns(len(routes))

for idx, route in enumerate(routes):
    with cols[idx]:
        card_class = "recommended-card" if route["status"] == "Recommended" else "route-card"

        st.markdown(
            f"""
            <div class="{card_class}">
                <div class="tag">{route['status']}</div>
                <h3 style="margin-top: 0; margin-bottom: 0.4rem;">{route['name']}</h3>
                <p class="small-note" style="margin-bottom: 1rem;">{route['notes']}</p>
                <p style="margin: 0.35rem 0;"><strong>Duration:</strong> {route['duration']} min</p>
                <p style="margin: 0.35rem 0;"><strong>Transfers:</strong> {route['transfers']}</p>
                <p style="margin: 0.35rem 0;"><strong>Stress:</strong> {route['stress']}/100</p>
                <p style="margin: 0.35rem 0;"><strong>Reliability:</strong> {route['reliability']}/100</p>
                <p style="margin: 0.35rem 0;"><strong>Stress level:</strong> {route['stress_label']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
st.subheader("Detailed comparison")

comparison_df = df[
    ["name", "duration", "transfers", "stress", "stress_label", "reliability", "status", "notes"]
].copy()
comparison_df.columns = [
    "Route",
    "Duration (min)",
    "Transfers",
    "Stress Score",
    "Stress Level",
    "Reliability",
    "Status",
    "Notes",
]

st.dataframe(comparison_df, use_container_width=True, hide_index=True)

st.write("")
left, right = st.columns([1.05, 0.95])

with left:
    fastest = df.loc[df["duration"].idxmin(), "name"]
    lowest_stress = df.loc[df["stress"].idxmin(), "name"]
    most_reliable = df.loc[df["reliability"].idxmax(), "name"]

    st.markdown(
        f"""
        <div class="soft-card">
            <h3 class="section-title">Best by category</h3>
            <p class="small-note" style="margin-bottom:0.4rem;"><strong>Fastest:</strong> {fastest}</p>
            <p class="small-note" style="margin-bottom:0.4rem;"><strong>Least stressful:</strong> {lowest_stress}</p>
            <p class="small-note" style="margin-bottom:0;"><strong>Most reliable:</strong> {most_reliable}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="soft-card">
            <h3 class="section-title">Why this page matters</h3>
            <p class="small-note" style="margin-bottom:0;">
                Standard trip planners often default to the shortest journey. This comparison screen makes the trade-offs visible.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )