import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Route Comparison | CommutePulse",
    page_icon="🧭",
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
            max-width: 1200px;
        }

        .page-card {
            background: rgba(255,255,255,0.88);
            border: 1px solid #e7eefc;
            padding: 1.5rem;
            border-radius: 28px;
            box-shadow: 0 18px 40px rgba(31, 59, 119, 0.09);
        }

        .route-card {
            background: rgba(255,255,255,0.94);
            border: 1px solid #e7eefc;
            padding: 1.3rem;
            border-radius: 24px;
            box-shadow: 0 12px 28px rgba(31, 59, 119, 0.07);
            height: 100%;
        }

        .recommended-card {
            background: linear-gradient(180deg, #ffffff 0%, #f2fbff 100%);
            border: 2px solid #b6deff;
            padding: 1.3rem;
            border-radius: 24px;
            box-shadow: 0 14px 32px rgba(31, 59, 119, 0.09);
            height: 100%;
        }

        .tag {
            display: inline-block;
            padding: 0.3rem 0.75rem;
            border-radius: 999px;
            background: linear-gradient(135deg, #dff1ff 0%, #efe3ff 100%);
            color: #244064;
            font-size: 0.84rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
        }

        .subtle {
            color: #62728d;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialise_state() -> None:
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


inject_css()
initialise_state()

routes = st.session_state.route_options
df = pd.DataFrame(routes)

st.markdown(
    """
    <div class="page-card">
        <h1 style="margin-top:0; margin-bottom:0.35rem;">Compare today’s route options</h1>
        <p class="subtle" style="font-size:1rem; margin-bottom:0;">
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
        is_recommended = route["status"] == "Recommended"
        card_class = "recommended-card" if is_recommended else "route-card"

        st.markdown(
            f"""
            <div class="{card_class}">
                <div class="tag">{route['status']}</div>
                <h3 style="margin-top: 0; margin-bottom: 0.4rem;">{route['name']}</h3>
                <p class="subtle" style="margin-bottom: 1rem;">{route['notes']}</p>
                <p style="margin: 0.35rem 0;"><strong>Duration:</strong> {route['duration']} min</p>
                <p style="margin: 0.35rem 0;"><strong>Transfers:</strong> {route['transfers']}</p>
                <p style="margin: 0.35rem 0;"><strong>Stress:</strong> {route['stress']}/100</p>
                <p style="margin: 0.35rem 0;"><strong>Reliability:</strong> {route['reliability']}/100</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
st.subheader("Detailed comparison")
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("")
left, right = st.columns([1.05, 0.95])

with left:
    fastest = df.loc[df["duration"].idxmin(), "name"]
    lowest_stress = df.loc[df["stress"].idxmin(), "name"]
    most_reliable = df.loc[df["reliability"].idxmax(), "name"]

    st.markdown(
        f"""
        <div class="route-card">
            <h3 style="margin-top:0;">Best by category</h3>
            <p class="subtle" style="margin-bottom:0.4rem;"><strong>Fastest:</strong> {fastest}</p>
            <p class="subtle" style="margin-bottom:0.4rem;"><strong>Least stressful:</strong> {lowest_stress}</p>
            <p class="subtle" style="margin-bottom:0;"><strong>Most reliable:</strong> {most_reliable}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="route-card">
            <h3 style="margin-top:0;">Why this page matters</h3>
            <p class="subtle" style="margin-bottom:0;">
                Standard trip planners often default to the shortest journey.
                This comparison screen makes the trade-offs visible:
                a route can be slightly slower but dramatically less stressful and more dependable.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )