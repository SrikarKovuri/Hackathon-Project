import streamlit as st


st.set_page_config(
    page_title="CommutePulse",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded",
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
            max-width: 1200px;
        }

        h1, h2, h3 {
            color: #102542;
            letter-spacing: -0.02em;
        }

        .hero-card {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(255, 255, 255, 0.7);
            padding: 2rem;
            border-radius: 28px;
            box-shadow: 0 18px 45px rgba(31, 59, 119, 0.10);
            backdrop-filter: blur(8px);
        }

        .soft-card {
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid #e7eefc;
            padding: 1.2rem 1.25rem;
            border-radius: 24px;
            box-shadow: 0 12px 30px rgba(31, 59, 119, 0.08);
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
            margin-right: 0.45rem;
            margin-bottom: 0.45rem;
        }

        .big-stat {
            font-size: 2rem;
            font-weight: 700;
            color: #102542;
            margin-bottom: 0.2rem;
        }

        .subtle {
            color: #5f6f89;
            font-size: 0.95rem;
        }

        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #e8eefc;
            padding: 1rem;
            border-radius: 22px;
            box-shadow: 0 10px 24px rgba(31, 59, 119, 0.07);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #f6f9ff 100%);
            border-right: 1px solid #e9eef8;
        }

        .info-banner {
            padding: 1rem 1.2rem;
            border-radius: 18px;
            background: linear-gradient(135deg, #e8f5ff 0%, #f4ebff 100%);
            border: 1px solid #dde8ff;
            color: #21405f;
            font-weight: 500;
        }
        </style>
        """,
        unsafe_allow_html=True,
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

    if "today_summary" not in st.session_state:
        st.session_state.today_summary = {
            "expected_duration": 41,
            "stress_score": 74,
            "reliability": "Medium",
            "alert": "T1 Western Line delays are increasing transfer risk near Redfern.",
            "recommendation": "Take the 7:32 service instead of your usual 7:42 train.",
            "usual_route": "Parramatta → Redfern → Central",
        }

    if "route_options" not in st.session_state:
        st.session_state.route_options = [
            {
                "name": "Usual route",
                "duration": 41,
                "transfers": 2,
                "stress": 74,
                "reliability": 61,
                "status": "At risk",
                "notes": "Fastest on paper, but sensitive to delays.",
            },
            {
                "name": "Lower-stress option",
                "duration": 46,
                "transfers": 0,
                "stress": 29,
                "reliability": 86,
                "status": "Recommended",
                "notes": "Direct service with better reliability this morning.",
            },
            {
                "name": "Balanced option",
                "duration": 43,
                "transfers": 1,
                "stress": 48,
                "reliability": 73,
                "status": "Stable",
                "notes": "Slightly longer but safer than your usual route.",
            },
        ]

    if "history_df" not in st.session_state:
        import pandas as pd

        st.session_state.history_df = pd.DataFrame(
            {
                "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "Duration": [39, 42, 47, 41, 44, 36, 34],
                "Stress": [52, 61, 78, 55, 69, 28, 20],
            }
        )


inject_css()
initialise_state()

profile = st.session_state.user_profile
today = st.session_state.today_summary

st.sidebar.title("🚆 CommutePulse")
st.sidebar.markdown("Your daily Sydney commute check-in.")
st.sidebar.page_link("app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/1_Setup.py", label="Setup", icon="⚙️")
st.sidebar.page_link("pages/2_Today_Summary.py", label="Today Summary", icon="🌤️")
st.sidebar.page_link("pages/3_Commute_History.py", label="Commute History", icon="📈")
st.sidebar.page_link("pages/4_Route_Comparison.py", label="Route Comparison", icon="🧭")

st.markdown(
    """
    <div class="hero-card">
        <div class="pill">Routine commute predictor</div>
        <div class="pill">Sydney Trains</div>
        <div class="pill">Hackathon demo</div>
        <h1 style="margin-top: 0.8rem; margin-bottom: 0.4rem;">Make your morning commute easier in under a minute.</h1>
        <p class="subtle" style="font-size: 1.05rem;">
            CommutePulse gives routine rail commuters a quick daily briefing:
            what changed, how stressful the trip is likely to feel, and whether a better route exists today.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Expected duration today", f"{today['expected_duration']} min", "+3 min")

with col2:
    st.metric("Stress score", f"{today['stress_score']}/100", "High")

with col3:
    st.metric("Reliability", today["reliability"], "-1 level")

st.write("")
left, right = st.columns([1.35, 1])

with left:
    st.markdown(
        f"""
        <div class="soft-card">
            <h3 style="margin-top: 0;">Today at a glance</h3>
            <p class="subtle" style="margin-bottom: 0.7rem;">
                <strong>{profile['origin']}</strong> to <strong>{profile['destination']}</strong> · usual departure <strong>{profile['departure_time']}</strong>
            </p>
            <div class="info-banner">
                {today['alert']}
            </div>
            <p style="margin-top: 1rem; margin-bottom: 0.4rem;"><strong>Recommended action</strong></p>
            <p style="margin-top: 0; color: #29435f;">{today['recommendation']}</p>
            <p class="subtle" style="margin-bottom: 0;">Usual route: {today['usual_route']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        f"""
        <div class="soft-card">
            <h3 style="margin-top: 0;">Your profile</h3>
            <div class="big-stat">{profile['priority']}</div>
            <p class="subtle">Current journey preference</p>
            <p style="margin-top: 1rem; margin-bottom: 0.4rem;"><strong>Travel weighting</strong></p>
            <p class="subtle" style="margin: 0;">
                Speed: {profile['weights']['speed']}%<br>
                Stress: {profile['weights']['stress']}%<br>
                Reliability: {profile['weights']['reliability']}%
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.markdown("### Explore the demo")
a, b, c = st.columns(3)

with a:
    st.markdown(
        """
        <div class="soft-card">
            <h4 style="margin-top:0;">⚙️ Setup</h4>
            <p class="subtle">Set home station, destination, departure time, and personal travel preferences.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with b:
    st.markdown(
        """
        <div class="soft-card">
            <h4 style="margin-top:0;">🌤️ Daily summary</h4>
            <p class="subtle">See delays, route stress, and a recommendation in a quick morning snapshot.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c:
    st.markdown(
        """
        <div class="soft-card">
            <h4 style="margin-top:0;">🧭 Route comparison</h4>
            <p class="subtle">Compare the fastest, least stressful, and most reliable ways to travel today.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.info("Start with the Setup page, then open Today Summary for the main demo screen.")