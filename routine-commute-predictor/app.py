import streamlit as st

from src.prediction import get_demo_route_options, score_route_options, build_today_summary
from src.recommendation import attach_route_statuses
from src.ui import inject_global_css, render_top_nav


st.set_page_config(
    page_title="TripMate",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def initialise_state() -> None:
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {
            "name": "Nawfal",
            "origin": "Parramatta",
            "destination": "Central",
            "departure_time": "07:42",
            "arrival_goal": "08:30",
            "walking_tolerance": 8,
            "priority": "Lower stress",
            "weights": {
                "speed": 30,
                "stress": 50,
                "reliability": 20,
            },
        }

    refresh_predictions()


def refresh_predictions() -> None:
    profile = st.session_state.user_profile
    raw_routes = get_demo_route_options(profile)
    scored_routes = score_route_options(profile, raw_routes)
    enriched_routes = attach_route_statuses(scored_routes)
    today_summary = build_today_summary(profile, enriched_routes)

    st.session_state.route_options = enriched_routes
    st.session_state.today_summary = today_summary

    if "history_df" not in st.session_state:
        import pandas as pd

        st.session_state.history_df = pd.DataFrame(
            {
                "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "Duration": [39, 42, 47, 41, 44, 36, 34],
                "Stress": [52, 61, 78, 55, 69, 28, 20],
            }
        )


inject_global_css()
initialise_state()
render_top_nav("home")


profile = st.session_state.user_profile
today = st.session_state.today_summary

logo_col, text_col = st.columns([1, 4])

with logo_col:
    st.image("assets/logo.png", width=150)

with text_col:
    st.markdown(
        """
        <div class="hero-card">
            <div class="pill">Routine commute predictor</div>
            <div class="pill">Sydney Trains</div>
            <div class="pill">Transport resilience</div>
            <h1 style="margin-top: 0.8rem; margin-bottom: 0.4rem;">A cleaner, calmer way to commute every morning.</h1>
            <p class="small-note" style="font-size: 1.05rem;">
                TripMate gives routine rail commuters a fast daily briefing:
                what changed, how stressful the trip may feel, and whether a better option exists today.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Expected duration", f"{today['expected_duration']} min")
with col2:
    st.metric("Stress score", f"{today['stress_score']}/100")
with col3:
    st.metric("Reliability", today["reliability"])

st.write("")
left, right = st.columns([1.35, 1])

with left:
    st.markdown(
        f"""
        <div class="soft-card">
            <h3 class="section-title">Today at a glance</h3>
            <p class="small-note" style="margin-bottom: 0.7rem;">
                <strong>{profile['origin']}</strong> to <strong>{profile['destination']}</strong> · usual departure <strong>{profile['departure_time']}</strong>
            </p>
            <div class="info-banner">
                {today['alert']}
            </div>
            <p style="margin-top: 1rem; margin-bottom: 0.4rem;"><strong>Recommended action</strong></p>
            <p style="margin-top: 0;">{today['recommendation']}</p>
            <p class="small-note" style="margin-bottom: 0;">Usual route: {today['usual_route']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        f"""
        <div class="soft-card">
            <h3 class="section-title">Your profile</h3>
            <p style="font-size: 2rem; font-weight: 700; margin-bottom: 0.2rem;">{profile['priority']}</p>
            <p class="small-note">Current journey preference</p>
            <p style="margin-top: 1rem; margin-bottom: 0.4rem;"><strong>Travel weighting</strong></p>
            <p class="small-note" style="margin: 0;">
                Speed: {profile['weights']['speed']}%<br>
                Stress: {profile['weights']['stress']}%<br>
                Reliability: {profile['weights']['reliability']}%
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.markdown("### Explore the product")
a, b, c = st.columns(3)

with a:
    st.markdown(
        """
        <div class="soft-card">
            <h4 style="margin-top:0;">⚙️ Personal setup</h4>
            <p class="small-note">Set home station, destination, departure time, and your travel priorities.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with b:
    st.markdown(
        """
        <div class="soft-card">
            <h4 style="margin-top:0;">🌤️ Daily summary</h4>
            <p class="small-note">See delays, route stress, and a morning recommendation in seconds.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c:
    st.markdown(
        """
        <div class="soft-card">
            <h4 style="margin-top:0;">🧭 Route comparison</h4>
            <p class="small-note">Compare the fastest, least stressful, and most reliable ways to travel today.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )