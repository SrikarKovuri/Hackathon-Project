import streamlit as st

from src.prediction import get_demo_route_options, score_route_options, build_today_summary
from src.recommendation import attach_route_statuses
from src.ui import inject_global_css, render_top_nav


st.set_page_config(
    page_title="Today Summary | TripMate",
    page_icon="🌤️",
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
    today_summary = build_today_summary(profile, enriched_routes)

    st.session_state.route_options = enriched_routes
    st.session_state.today_summary = today_summary


inject_global_css()
refresh_predictions()
render_top_nav("today")

profile = st.session_state.user_profile
today = st.session_state.today_summary

st.markdown(
    f"""
    <div class="hero-card">
        <div class="pill">30-second daily check-in</div>
        <h1 style="margin-top: 0.2rem; margin-bottom: 0.35rem;">Good morning, {profile['name']}.</h1>
        <p class="small-note" style="font-size: 1rem; margin-bottom: 0;">
            Here's your personalised commute summary for <strong>{profile['origin']} → {profile['destination']}</strong>.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Expected duration", f"{today['expected_duration']} min")
with m2:
    st.metric("Stress score", f"{today['stress_score']}/100")
with m3:
    st.metric("Reliability", today["reliability"])
with m4:
    st.metric("Usual departure", profile["departure_time"])

st.write("")
left, right = st.columns([1.3, 1])

with left:
    st.markdown(
        f"""
        <div class="soft-card">
            <h3 class="section-title">Network alert</h3>
            <div class="alert-box">{today['alert']}</div>
            <p class="small-note" style="margin-top: 1rem; margin-bottom: 0;">
                Usual route: {today['usual_route']}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown(
        f"""
        <div class="soft-card">
            <h3 class="section-title">Recommended action</h3>
            <div class="recommend-box">
                <strong>{today['recommendation']}</strong>
            </div>
            <p style="margin-top: 1rem; margin-bottom: 0.35rem;"><strong>Why this is being recommended</strong></p>
            <ul class="small-note" style="margin-top: 0.3rem;">
                <li>{today['reason_1']}</li>
                <li>{today['reason_2']}</li>
                <li>{today['reason_3']}</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="soft-card">
            <h3 class="section-title">How today feels</h3>
            <p class="small-note">
                This trip is predicted using reliability, transfer burden, walking effort,
                crowding, and delay exposure. The goal is to summarise commuter friction quickly.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    score = int(today["stress_score"])
    if score >= 70:
        stress_label = "High"
    elif score >= 40:
        stress_label = "Moderate"
    else:
        stress_label = "Low"

    st.markdown(
        f"""
        <div class="soft-card">
            <h3 class="section-title">Stress interpretation</h3>
            <p style="font-size: 2rem; font-weight: 700; margin-bottom: 0.2rem;">{stress_label}</p>
            <p class="small-note">
                Your current preference profile places extra weight on low-stress travel,
                so direct and reliable routes are favoured more heavily than small time savings.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown(
        f"""
        <div class="soft-card">
            <h3 class="section-title">Preference snapshot</h3>
            <p class="small-note" style="margin-bottom:0;">
                Priority: {profile['priority']}<br>
                Speed weighting: {profile['weights']['speed']}%<br>
                Stress weighting: {profile['weights']['stress']}%<br>
                Reliability weighting: {profile['weights']['reliability']}%
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )