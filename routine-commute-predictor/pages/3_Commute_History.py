import pandas as pd
import plotly.express as px
import streamlit as st

from src.ui import inject_global_css, render_top_nav


st.set_page_config(
    page_title="Commute History | TripMate",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
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


inject_global_css()
initialise_state()
render_top_nav("history")

df = st.session_state.history_df.copy()

st.markdown(
    """
    <div class="hero-card">
        <h1 style="margin-top:0; margin-bottom:0.35rem;">Your recent commute history</h1>
        <p class="small-note" style="font-size:1rem; margin-bottom:0;">
            This dashboard shows patterns in time, stress, and daily commute variability.
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
    fig_duration = px.line(df, x="Day", y="Duration", markers=True, title="Duration across the week")
    fig_duration.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=10, r=10, t=50, b=10),
        height=350,
    )
    st.plotly_chart(fig_duration, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.subheader("Stress trend")
    fig_stress = px.bar(df, x="Day", y="Stress", title="Stress score across the week")
    fig_stress.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
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
            <h3 class="section-title">Quick insights</h3>
            <p class="small-note">
                Your commute appears most demanding mid-week, with a clear spike in both time and stress on <strong>{worst_day}</strong>.
            </p>
            <p class="small-note" style="margin-bottom:0;">
                This is where recommendation logic adds the most value by nudging you towards more reliable options.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )