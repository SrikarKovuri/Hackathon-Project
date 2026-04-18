import streamlit as st


def inject_global_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg-1: #0a0c10;
            --bg-2: #10141b;
            --bg-3: #0d1117;
            --card: rgba(255, 255, 255, 0.08);
            --card-strong: rgba(255, 255, 255, 0.12);
            --border: rgba(255, 255, 255, 0.14);
            --text: #f5f7fb;
            --text-strong: #ffffff;
            --muted: #c7d0db;
            --blue: #0aa7e8;
            --orange: #ff8c42;
            --shadow: 0 20px 50px rgba(0, 0, 0, 0.32);
            --radius-xl: 30px;
            --radius-lg: 24px;
            --radius-md: 18px;
        }

        html, body, [class*="css"] {
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "SF Pro Display",
                "SF Pro Text",
                "Helvetica Neue",
                Helvetica,
                Arial,
                sans-serif !important;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(10,167,232,0.13), transparent 28%),
                radial-gradient(circle at top right, rgba(255,140,66,0.10), transparent 24%),
                linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 50%, var(--bg-3) 100%);
            color: var(--text);
        }

        .block-container {
            max-width: 1320px;
            padding-top: 1.1rem;
            padding-bottom: 2.2rem;
        }

        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="collapsedControl"] {
            display: none;
        }

        p, span, label, div, li {
            color: var(--text);
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--text-strong) !important;
            letter-spacing: -0.03em;
            font-weight: 700 !important;
        }

        .small-note, .muted {
            color: var(--muted) !important;
        }

        .hero-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.11) 0%, rgba(255,255,255,0.06) 100%);
            border: 1px solid var(--border);
            padding: 2.15rem;
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
        }

        .soft-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.09) 0%, rgba(255,255,255,0.05) 100%);
            border: 1px solid var(--border);
            padding: 1.25rem 1.3rem;
            border-radius: var(--radius-lg);
            box-shadow: 0 16px 34px rgba(0,0,0,0.22);
            height: 100%;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }

        .route-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.09) 0%, rgba(255,255,255,0.05) 100%);
            border: 1px solid var(--border);
            padding: 1.3rem;
            border-radius: var(--radius-lg);
            box-shadow: 0 14px 28px rgba(0,0,0,0.20);
            height: 100%;
        }

        .recommended-card {
            background: linear-gradient(180deg, rgba(10,167,232,0.18) 0%, rgba(255,140,66,0.12) 100%);
            border: 1px solid rgba(255,255,255,0.18);
            padding: 1.3rem;
            border-radius: var(--radius-lg);
            box-shadow: 0 16px 36px rgba(0,0,0,0.28);
            height: 100%;
        }

        .pill {
            display: inline-block;
            padding: 0.42rem 0.9rem;
            border-radius: 999px;
            background: linear-gradient(135deg, rgba(10,167,232,0.18) 0%, rgba(255,140,66,0.18) 100%);
            border: 1px solid rgba(255,255,255,0.12);
            color: #ffffff !important;
            font-size: 0.9rem;
            font-weight: 600;
            margin-right: 0.45rem;
            margin-bottom: 0.5rem;
        }

        .tag {
            display: inline-block;
            padding: 0.32rem 0.76rem;
            border-radius: 999px;
            background: linear-gradient(135deg, rgba(10,167,232,0.20) 0%, rgba(255,140,66,0.20) 100%);
            color: #ffffff !important;
            font-size: 0.84rem;
            font-weight: 700;
            margin-bottom: 0.9rem;
        }

        .top-nav-wrap {
            position: sticky;
            top: 0.45rem;
            z-index: 999;
            margin-bottom: 1.2rem;
        }

        .top-nav {
            background: linear-gradient(180deg, rgba(18,21,27,0.88) 0%, rgba(21,25,32,0.78) 100%);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 26px;
            padding: 0.9rem 1rem;
            box-shadow: 0 16px 36px rgba(0,0,0,0.25);
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
        }

        .brand-title {
            font-size: 1.08rem;
            font-weight: 700;
            margin-bottom: 0.1rem;
            letter-spacing: -0.03em;
            color: #ffffff !important;
        }

        .brand-sub {
            color: var(--muted) !important;
            font-size: 0.86rem;
        }

        div[data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0.05) 100%);
            border: 1px solid var(--border);
            padding: 1rem 1rem 1.1rem 1rem;
            border-radius: 24px;
            box-shadow: 0 14px 28px rgba(0,0,0,0.18);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--muted) !important;
            font-weight: 500 !important;
        }

        div[data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }

        div[data-testid="stMetricDelta"] {
            color: #ffffff !important;
        }

        .info-banner {
            padding: 1rem 1.1rem;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(10,167,232,0.16) 0%, rgba(255,140,66,0.14) 100%);
            border: 1px solid rgba(255,255,255,0.12);
            color: #ffffff !important;
            font-weight: 500;
        }

        .alert-box {
            background: linear-gradient(135deg, rgba(255,140,66,0.20) 0%, rgba(255,255,255,0.06) 100%);
            border: 1px solid rgba(255,140,66,0.28);
            color: #ffffff !important;
            padding: 1rem 1.1rem;
            border-radius: 18px;
        }

        .recommend-box {
            background: linear-gradient(135deg, rgba(10,167,232,0.20) 0%, rgba(255,255,255,0.06) 100%);
            border: 1px solid rgba(10,167,232,0.26);
            color: #ffffff !important;
            padding: 1rem 1.1rem;
            border-radius: 18px;
        }

        .section-title {
            margin-top: 0;
            margin-bottom: 0.45rem;
            color: #ffffff !important;
        }

        .stButton > button,
        div[data-testid="stFormSubmitButton"] button,
        a[data-testid="stPageLink-NavLink"] {
            border-radius: 999px !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            background: linear-gradient(135deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0.05) 100%) !important;
            color: #ffffff !important;
            min-height: 44px !important;
            font-weight: 600 !important;
            box-shadow: none !important;
            transition: 0.2s ease all !important;
        }

        .stButton > button:hover,
        div[data-testid="stFormSubmitButton"] button:hover,
        a[data-testid="stPageLink-NavLink"]:hover {
            border-color: rgba(10,167,232,0.35) !important;
            box-shadow: 0 8px 22px rgba(10,167,232,0.18) !important;
            transform: translateY(-1px);
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        textarea,
        input {
            background: rgba(255,255,255,0.07) !important;
            border-radius: 16px !important;
            color: #ffffff !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
        }

        input::placeholder,
        textarea::placeholder {
            color: #c7d0db !important;
            opacity: 1 !important;
        }

        .stSlider [data-baseweb="slider"] {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }

        .stMarkdown, .stText, .stCaption {
            color: #ffffff !important;
        }

        .stDataFrame, .stTable {
            border-radius: 20px;
            overflow: hidden;
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
            st.page_link("app.py", label="Home", icon="🏠")
        with c2:
            st.page_link("pages/1_Setup.py", label="Setup", icon="⚙️")
        with c3:
            st.page_link("pages/2_Today_Summary.py", label="Today", icon="🌤️")
        with c4:
            st.page_link("pages/3_Commute_History.py", label="History", icon="📈")
        with c5:
            st.page_link("pages/4_Route_Comparison.py", label="Routes", icon="🧭")
        with c6:
            st.page_link("pages/5_Weather_Shelter_Access.py", label="Shelter", icon="🌧️")

    st.markdown("</div></div>", unsafe_allow_html=True)