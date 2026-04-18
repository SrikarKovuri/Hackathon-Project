import streamlit as st


def inject_global_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #0f1115;
            --bg-soft: #171a20;
            --card: rgba(255, 255, 255, 0.06);
            --card-strong: rgba(255, 255, 255, 0.10);
            --border: rgba(255, 255, 255, 0.12);
            --text: #f5f7fa;
            --muted: #b6bfcb;
            --blue: #00a8e8;
            --orange: #ff8c42;
            --shadow: 0 20px 50px rgba(0, 0, 0, 0.28);
            --radius-xl: 28px;
            --radius-lg: 22px;
            --radius-md: 16px;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(0,168,232,0.12), transparent 28%),
                radial-gradient(circle at top right, rgba(255,140,66,0.10), transparent 24%),
                linear-gradient(180deg, #0d0f13 0%, #11141a 55%, #0c0f14 100%);
            color: var(--text);
        }

        .block-container {
            max-width: 1280px;
            padding-top: 1.4rem;
            padding-bottom: 2rem;
        }

        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="collapsedControl"] {
            display: none;
        }

        h1, h2, h3, h4, h5, h6,
        p, span, label, div {
            color: var(--text);
        }

        .muted {
            color: var(--muted) !important;
        }

        .glass {
            background: linear-gradient(180deg, rgba(255,255,255,0.09) 0%, rgba(255,255,255,0.05) 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
        }

        .hero-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0.05) 100%);
            border: 1px solid var(--border);
            padding: 2rem;
            border-radius: 30px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(20px);
        }

        .soft-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.04) 100%);
            border: 1px solid var(--border);
            padding: 1.2rem 1.25rem;
            border-radius: 24px;
            box-shadow: 0 16px 34px rgba(0,0,0,0.20);
            height: 100%;
            backdrop-filter: blur(16px);
        }

        .pill {
            display: inline-block;
            padding: 0.38rem 0.82rem;
            border-radius: 999px;
            background: linear-gradient(135deg, rgba(0,168,232,0.16) 0%, rgba(255,140,66,0.16) 100%);
            border: 1px solid rgba(255,255,255,0.10);
            color: #ffffff;
            font-size: 0.88rem;
            font-weight: 600;
            margin-right: 0.45rem;
            margin-bottom: 0.45rem;
        }

        .top-nav-wrap {
            position: sticky;
            top: 0.5rem;
            z-index: 999;
            margin-bottom: 1.2rem;
        }

        .top-nav {
            background: linear-gradient(180deg, rgba(16,18,23,0.88) 0%, rgba(20,23,29,0.78) 100%);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 26px;
            padding: 0.85rem 1rem;
            box-shadow: 0 16px 36px rgba(0,0,0,0.24);
            backdrop-filter: blur(20px);
        }

        .brand-title {
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.12rem;
            letter-spacing: -0.02em;
        }

        .brand-sub {
            color: var(--muted);
            font-size: 0.85rem;
        }

        .nav-button-row {
            margin-top: 0.25rem;
        }

        div[data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(255,255,255,0.09) 0%, rgba(255,255,255,0.04) 100%);
            border: 1px solid var(--border);
            padding: 1rem;
            border-radius: 22px;
            box-shadow: 0 14px 28px rgba(0,0,0,0.18);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--muted);
        }

        div[data-testid="stMetricValue"] {
            color: #ffffff;
        }

        .info-banner {
            padding: 1rem 1.1rem;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(0,168,232,0.14) 0%, rgba(255,140,66,0.14) 100%);
            border: 1px solid rgba(255,255,255,0.10);
            color: #ffffff;
            font-weight: 500;
        }

        .alert-box {
            background: linear-gradient(135deg, rgba(255,140,66,0.18) 0%, rgba(255,255,255,0.06) 100%);
            border: 1px solid rgba(255,140,66,0.25);
            color: #ffffff;
            padding: 1rem 1.1rem;
            border-radius: 18px;
        }

        .recommend-box {
            background: linear-gradient(135deg, rgba(0,168,232,0.18) 0%, rgba(255,255,255,0.06) 100%);
            border: 1px solid rgba(0,168,232,0.24);
            color: #ffffff;
            padding: 1rem 1.1rem;
            border-radius: 18px;
        }

        .stButton > button,
        div[data-testid="stFormSubmitButton"] button,
        a[data-testid="stPageLink-NavLink"] {
            border-radius: 999px !important;
            border: 1px solid rgba(255,255,255,0.10) !important;
            background: linear-gradient(135deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0.05) 100%) !important;
            color: #ffffff !important;
            min-height: 44px !important;
            font-weight: 600 !important;
            transition: 0.2s ease all !important;
        }

        .stButton > button:hover,
        div[data-testid="stFormSubmitButton"] button:hover,
        a[data-testid="stPageLink-NavLink"]:hover {
            border-color: rgba(0,168,232,0.35) !important;
            box-shadow: 0 8px 22px rgba(0,168,232,0.18) !important;
            transform: translateY(-1px);
        }

        .nav-active a[data-testid="stPageLink-NavLink"] {
            background: linear-gradient(135deg, rgba(0,168,232,0.22) 0%, rgba(255,140,66,0.18) 100%) !important;
            border-color: rgba(255,255,255,0.16) !important;
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        textarea,
        input {
            background: rgba(255,255,255,0.06) !important;
            border-radius: 16px !important;
            color: #ffffff !important;
        }

        .stSlider [data-baseweb="slider"] {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }

        .stDataFrame, .stTable {
            border-radius: 20px;
            overflow: hidden;
        }

        .small-note {
            color: var(--muted);
            font-size: 0.95rem;
        }

        hr {
            border-color: rgba(255,255,255,0.08);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_top_nav(active_page: str) -> None:
    st.markdown('<div class="top-nav-wrap"><div class="top-nav">', unsafe_allow_html=True)

    brand_col, nav_col = st.columns([1.2, 4])

    with brand_col:
        st.image("assets/logo.png", width=72)
        st.markdown('<div class="brand-title">TripMate</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Smart daily Sydney commuting</div>', unsafe_allow_html=True)

    with nav_col:
        c1, c2, c3, c4, c5, c6 = st.columns(6)

        with c1:
            if active_page == "home":
                st.markdown('<div class="nav-active">', unsafe_allow_html=True)
            st.page_link("app.py", label="Home", icon="🏠")
            if active_page == "home":
                st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            if active_page == "setup":
                st.markdown('<div class="nav-active">', unsafe_allow_html=True)
            st.page_link("pages/1_Setup.py", label="Setup", icon="⚙️")
            if active_page == "setup":
                st.markdown("</div>", unsafe_allow_html=True)

        with c3:
            if active_page == "today":
                st.markdown('<div class="nav-active">', unsafe_allow_html=True)
            st.page_link("pages/2_Today_Summary.py", label="Today", icon="🌤️")
            if active_page == "today":
                st.markdown("</div>", unsafe_allow_html=True)

        with c4:
            if active_page == "history":
                st.markdown('<div class="nav-active">', unsafe_allow_html=True)
            st.page_link("pages/3_Commute_History.py", label="History", icon="📈")
            if active_page == "history":
                st.markdown("</div>", unsafe_allow_html=True)

        with c5:
            if active_page == "routes":
                st.markdown('<div class="nav-active">', unsafe_allow_html=True)
            st.page_link("pages/4_Route_Comparison.py", label="Routes", icon="🧭")
            if active_page == "routes":
                st.markdown("</div>", unsafe_allow_html=True)

        with c6:
            if active_page == "weather":
                st.markdown('<div class="nav-active">', unsafe_allow_html=True)
            st.page_link("pages/5_Weather_Shelter_Access.py", label="Shelter", icon="🌧️")
            if active_page == "weather":
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)