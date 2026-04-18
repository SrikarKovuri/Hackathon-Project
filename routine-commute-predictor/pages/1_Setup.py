import streamlit as st

from src.prediction import get_demo_route_options, score_route_options, build_today_summary
from src.recommendation import attach_route_statuses


st.set_page_config(
    page_title="Setup | CommutePulse",
    page_icon="⚙️",
    layout="wide",
)


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #f8fbff 0%, #eef6ff 45%, #f7f4ff 100%);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1100px;
        }

        .page-card {
            background: rgba(255,255,255,0.88);
            border: 1px solid #e7eefc;
            padding: 1.5rem;
            border-radius: 26px;
            box-shadow: 0 14px 36px rgba(31, 59, 119, 0.08);
        }

        .section-card {
            background: rgba(255,255,255,0.92);
            border: 1px solid #e6edfb;
            padding: 1.2rem;
            border-radius: 22px;
            box-shadow: 0 10px 28px rgba(31, 59, 119, 0.06);
            height: 100%;
        }

        .pill {
            display: inline-block;
            padding: 0.35rem 0.8rem;
            border-radius: 999px;
            background: linear-gradient(135deg, #dff1ff 0%, #efe3ff 100%);
            color: #244064;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
        }

        h1, h2, h3 {
            color: #102542;
            letter-spacing: -0.02em;
        }

        .subtle {
            color: #61728d;
        }

        div[data-testid="stForm"] {
            background: rgba(255,255,255,0.75);
            border: 1px solid #e5ecfb;
            border-radius: 22px;
            padding: 1rem 1rem 0.2rem 1rem;
        }

        div.stButton > button, div[data-testid="stFormSubmitButton"] button {
            border-radius: 999px !important;
            border: none !important;
            padding: 0.6rem 1.2rem !important;
            font-weight: 600 !important;
            background: linear-gradient(135deg, #8fd3ff 0%, #c6a6ff 100%) !important;
            color: #102542 !important;
            box-shadow: 0 8px 18px rgba(137, 188, 255, 0.35) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
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


inject_css()
initialise_state()

profile = st.session_state.user_profile

st.markdown(
    """
    <div class="page-card">
        <div class="pill">Personalise your commute</div>
        <h1 style="margin-top: 0.3rem; margin-bottom: 0.4rem;">Set your routine once, then check in each morning.</h1>
        <p class="subtle" style="font-size: 1rem;">
            This demo stores everything locally in session state, which is perfect for a hackathon prototype.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

stations = [
    "Parramatta",
    "Central",
    "Redfern",
    "Town Hall",
    "Wynyard",
    "Strathfield",
    "Chatswood",
    "Burwood",
    "Blacktown",
    "Lidcombe",
    "Ashfield",
    "North Sydney",
    "Hornsby",
    "Penrith",
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
        origin = st.selectbox(
            "Home station",
            options=stations,
            index=stations.index(profile["origin"]) if profile["origin"] in stations else 0,
        )
        destination = st.selectbox(
            "Destination station",
            options=stations,
            index=stations.index(profile["destination"]) if profile["destination"] in stations else 1,
        )
        departure_time = st.text_input("Usual departure time", value=profile["departure_time"])

    with right:
        arrival_goal = st.text_input("Target arrival time", value=profile["arrival_goal"])
        walking_tolerance = st.slider(
            "Walking tolerance between interchanges (minutes)",
            min_value=0,
            max_value=20,
            value=int(profile["walking_tolerance"]),
        )
        priority = st.selectbox(
            "Main priority",
            options=priority_options,
            index=priority_options.index(profile["priority"]) if profile["priority"] in priority_options else 1,
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
    st.success("Your commute profile has been updated for this demo session.")

st.write("")
st.markdown("### Current saved settings")
a, b, c = st.columns(3)

with a:
    st.markdown(
        f"""
        <div class="section-card">
            <h4 style="margin-top:0;">Routine</h4>
            <p class="subtle" style="margin-bottom:0;">
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
        <div class="section-card">
            <h4 style="margin-top:0;">Preference</h4>
            <p class="subtle" style="margin-bottom:0;">
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
        <div class="section-card">
            <h4 style="margin-top:0;">Weighting</h4>
            <p class="subtle" style="margin-bottom:0;">
                Speed: {st.session_state.user_profile['weights']['speed']}%<br>
                Stress: {st.session_state.user_profile['weights']['stress']}%<br>
                Reliability: {st.session_state.user_profile['weights']['reliability']}%
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.info("Next, open Today Summary to see how these preferences affect your morning recommendation.")