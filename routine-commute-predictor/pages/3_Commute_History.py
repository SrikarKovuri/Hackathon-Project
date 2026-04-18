import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Commute History | CommutePulse",
    page_icon="📈",
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

        .soft-card {
            background: rgba(255,255,255,0.92);
            border: 1px solid #e7eefc;
            padding: 1.2rem;
            border-radius: 22px;
            box-shadow: 0 12px 28px rgba(31, 59, 119, 0.07);
            height: 100%;
        }

        .subtle {
            color: #62728d;
        }

        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.94);
            border: 1px solid #e8eefc;
            padding: 1rem;
            border-radius: 22px;
            box-shadow: 0 10px 24px rgba(31, 59, 119, 0.07);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialise_state() -> None:
    if "history_df" not in st.session_state:
        st.session_state.history_df = pd.DataFrame(
            {
                "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "Duration": [39, 42, 47, 41, 44, 36, 34],
                "Stress": [52, 61, 78, 55, 69, 28, 20],
            }
        )


inject_css()
initialise_state()

df = st.session_state.history_df.copy()

st.markdown(
    """
    <div class="page-card">
        <h1 style="margin-top:0; margin-bottom:0.35rem;">Your recent commute history</h1>
        <p class="subtle" style="font-size:1rem; margin-bottom:0;">
            This dashboard helps the app feel personalised by showing patterns in time, stress, and disruption impact.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

avg_duration = round(df["Duration"].mean(), 1)
avg_stress = round(df["Stress"].mean(), 1)
worst_day = df.loc[df["Stress"].idxmax(), "Day"]
best_day = df.loc[df["Stress"].idxmin(), "Day"]

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Average duration", f"{avg_duration} min")
with c2:
    st.metric("Average stress", f"{avg_stress}/100")
with c3:
    st.metric("Most stressful day", worst_day)
with c4:
    st.metric("Least stressful day", best_day)

st.write("")
left, right = st.columns(2)

with left:
    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.subheader("Travel time trend")
    fig_duration = px.line(
        df,
        x="Day",
        y="Duration",
        markers=True,
        title="Duration across the week",
    )
    fig_duration.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=50, b=10),
        height=350,
    )
    st.plotly_chart(fig_duration, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.subheader("Stress trend")
    fig_stress = px.bar(
        df,
        x="Day",
        y="Stress",
        title="Stress score across the week",
    )
    fig_stress.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=50, b=10),
        height=350,
    )
    st.plotly_chart(fig_stress, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
bottom_left, bottom_right = st.columns([1.1, 0.9])

with bottom_left:
    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.subheader("Weekly log")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

with bottom_right:
    st.markdown(
        f"""
        <div class="soft-card">
            <h3 style="margin-top:0;">Quick insights</h3>
            <p class="subtle">
                Your commute appears most demanding mid-week, with a clear spike in both time and stress on <strong>{worst_day}</strong>.
                This is where your recommendation engine can add the most value by nudging you towards more reliable options.
            </p>
            <p class="subtle" style="margin-bottom:0;">
                In the final version, this page can also show:
                recommendation success rate, disruption frequency, and route-switch behaviour.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )