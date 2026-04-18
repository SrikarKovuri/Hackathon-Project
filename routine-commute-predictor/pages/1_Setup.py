import streamlit as st

from src.prediction import get_demo_route_options, score_route_options, build_today_summary
from src.recommendation import attach_route_statuses
from src.ui import inject_global_css, render_top_nav


st.set_page_config(
    page_title="Setup | TripMate",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def refresh_predictions() -> None:
    profile = st.session_state.user_profile
    raw_routes = get_demo_route_options(profile)
    scored_routes = score_route_options(profile, raw_routes)
    enriched_routes = attach_route_statuses(scored_routes)
    today_summary = build_today_summary(profile, enriched_routes)

    st.session_state.route_options = enriched_routes
    st.session_state.today_summary = today_summary


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
            "weights": {"speed": 30, "stress": 50, "reliability": 20},
        }
    refresh_predictions()


inject_global_css()
initialise_state()
render_top_nav("setup")

profile = st.session_state.user_profile

st.markdown(
    """
    <div class="hero-card">
        <div class="pill">Personalise your commute</div>
        <h1 style="margin-top: 0.3rem; margin-bottom: 0.4rem;">Set your routine once, then check in each morning.</h1>
        <p class="small-note" style="font-size: 1rem;">
            Configure your usual journey, travel priorities, and tolerance for walking or transfers.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

stations = [
    "Parramatta", "Central", "Redfern", "Town Hall", "Wynyard", "Strathfield",
    "Chatswood", "Burwood", "Blacktown", "Lidcombe", "Ashfield", "North Sydney",
    "Hornsby", "Penrith",
]

priority_options = [
    "Fastest route",
    "Lower stress",
    "Highest reliability",
    "Fewest transfers",
]

with st.form("setup_form"):
    left, right = st.columns(2)

    with left:
        name = st.text_input("Name", value=profile["name"])
        origin = st.selectbox("Home station", options=stations, index=stations.index(profile["origin"]))
        destination = st.selectbox("Destination station", options=stations, index=stations.index(profile["destination"]))
        departure_time = st.text_input("Usual departure time", value=profile["departure_time"])

    with right:
        arrival_goal = st.text_input("Target arrival time", value=profile["arrival_goal"])
        walking_tolerance = st.slider(
            "Walking tolerance between interchanges (minutes)",
            0, 20, int(profile["walking_tolerance"])
        )
        priority = st.selectbox(
            "Main priority",
            options=priority_options,
            index=priority_options.index(profile["priority"])
        )

    st.markdown("### Personal weighting")
    c1, c2, c3 = st.columns(3)

    with c1:
        speed = st.slider("Speed", 0, 100, int(profile["weights"]["speed"]), step=5)
    with c2:
        stress = st.slider("Stress", 0, 100, int(profile["weights"]["stress"]), step=5)
    with c3:
        reliability = st.slider("Reliability", 0, 100, int(profile["weights"]["reliability"]), step=5)

    submitted = st.form_submit_button("Save commute profile")

if submitted:
    st.session_state.user_profile = {
        "name": name.strip() or "Commuter",
        "origin": origin,
        "destination": destination,
        "departure_time": departure_time.strip() or "07:42",
        "arrival_goal": arrival_goal.strip() or "08:30",
        "walking_tolerance": walking_tolerance,
        "priority": priority,
        "weights": {
            "speed": speed,
            "stress": stress,
            "reliability": reliability,
        },
    }
    refresh_predictions()
    st.success("Your commute profile has been updated.")

st.write("")
a, b, c = st.columns(3)

with a:
    st.markdown(
        f"""
        <div class="soft-card">
            <h4 style="margin-top:0;">Routine</h4>
            <p class="small-note">
                {st.session_state.user_profile['origin']} → {st.session_state.user_profile['destination']}<br>
                Leave at {st.session_state.user_profile['departure_time']}<br>
                Arrive by {st.session_state.user_profile['arrival_goal']}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with b:
    st.markdown(
        f"""
        <div class="soft-card">
            <h4 style="margin-top:0;">Preference</h4>
            <p class="small-note">
                Main priority: {st.session_state.user_profile['priority']}<br>
                Walking tolerance: {st.session_state.user_profile['walking_tolerance']} min
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c:
    st.markdown(
        f"""
        <div class="soft-card">
            <h4 style="margin-top:0;">Weighting</h4>
            <p class="small-note">
                Speed: {st.session_state.user_profile['weights']['speed']}%<br>
                Stress: {st.session_state.user_profile['weights']['stress']}%<br>
                Reliability: {st.session_state.user_profile['weights']['reliability']}%
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )