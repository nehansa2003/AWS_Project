
import os

import requests
import streamlit as st

from views.overview import render as render_overview
from views.prediction import render as render_prediction
from views.about import render as render_about


st.set_page_config(
    page_title="ChurnIQ | Customer Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_API_URL = os.getenv(
    "CHURN_API_URL",
    "http://localhost:8001",
)


def apply_styles():
    st.markdown(
        """
        <style>
        /* =========================================
           MAIN PAGE
        ========================================= */

        .stApp {
            background: linear-gradient(
                135deg,
                #F5F3FF 0%,
                #EFF6FF 55%,
                #F0FDFA 100%
            );
            color: #1F2937;
        }

        [data-testid="stHeader"] {
            background: rgba(245, 243, 255, 0.92);
        }

        [data-testid="stMain"] {
            color: #1F2937;
        }


        /* =========================================
           SIDEBAR BACKGROUND
        ========================================= */

        [data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #24104F 0%,
                #43218B 55%,
                #5B3CC4 100%
            );
        }
        /* Sidebar collapse/expand arrow */
        [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stSidebarCollapseButton"] button svg,
        [data-testid="stSidebarCollapsedControl"] button,
        [data-testid="stSidebarCollapsedControl"] svg {
            color: white !important;
            fill: white !important;
            stroke: white !important;
        }

        /* Sidebar main title: ChurnIQ */
        [data-testid="stSidebar"] h1 {
            color: #FFFFFF !important;
            font-size: 2rem !important;
            font-weight: 800 !important;
            line-height: 1.25 !important;
        }

        /* Sidebar section headings */
        [data-testid="stSidebar"] h2 {
            color: #FFFFFF !important;
            font-size: 1.4rem !important;
            font-weight: 700 !important;
        }

        [data-testid="stSidebar"] h3 {
            color: #FFFFFF !important;
            font-size: 1.25rem !important;
            font-weight: 700 !important;
        }

        /* General sidebar text */
        [data-testid="stSidebar"] p {
            color: #FFFFFF !important;
            font-size: 1rem !important;
        }

        /* Sidebar captions and helper text */
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
            color: #F3E8FF !important;
            font-size: 0.88rem !important;
        }

        /* Sidebar widget labels */
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"],
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
        [data-testid="stSidebar"] label {
            color: #FFFFFF !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
        }


        /* =========================================
           SIDEBAR NAVIGATION
        ========================================= */

        /* NAVIGATION heading */
        [data-testid="stSidebar"] [data-testid="stRadio"]
        [data-testid="stWidgetLabel"] p {
            color: #FFFFFF !important;
            font-size: 1.05rem !important;
            font-weight: 800 !important;
            letter-spacing: 0.5px !important;
        }

        /* Individual navigation options */
        [data-testid="stSidebar"] [data-testid="stRadio"] label {
            color: #FFFFFF !important;
            font-size: 1.08rem !important;
            font-weight: 600 !important;
            line-height: 1.5 !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] label p,
        [data-testid="stSidebar"] [data-testid="stRadio"] label span,
        [data-testid="stSidebar"] [data-testid="stRadio"] label div {
            color: #FFFFFF !important;
            font-size: 1.08rem !important;
        }

        /* Navigation spacing */
        [data-testid="stSidebar"] [data-testid="stRadio"] {
            margin-top: 5px;
            margin-bottom: 5px;
        }


        /* =========================================
           BACKEND URL INPUT
        ========================================= */

        /* Keep backend URL field white with dark,
           readable text */
        [data-testid="stSidebar"] input {
            background: #FFFFFF !important;
            color: #202344 !important;
            -webkit-text-fill-color: #202344 !important;
            caret-color: #6D28D9 !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
        }

        /* Input placeholder */
        [data-testid="stSidebar"] input::placeholder {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            opacity: 1 !important;
        }

        /* Backend URL label */
        [data-testid="stSidebar"] [data-testid="stTextInput"]
        [data-testid="stWidgetLabel"] {
            color: #FFFFFF !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
        }

        /* Backend URL help icon and related text */
        [data-testid="stSidebar"] [data-testid="stTextInput"] {
            margin-bottom: 8px;
        }


        /* =========================================
           SIDEBAR SELECTS
        ========================================= */

        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: #FFFFFF !important;
            color: #202344 !important;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] * {
            color: #202344 !important;
        }


        /* =========================================
           GENERAL MARKDOWN AND LABELS
        ========================================= */

        .stMarkdown,
        .stText,
        label,
        [data-testid="stWidgetLabel"],
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li {
            color: #25304A;
        }


        /* =========================================
           MAIN PAGE INPUTS
        ========================================= */

        input,
        textarea,
        [data-baseweb="input"] input {
            background: #FFFFFF !important;
            color: #202344 !important;
            -webkit-text-fill-color: #202344 !important;
            caret-color: #6D28D9 !important;
        }

        [data-baseweb="input"],
        [data-baseweb="select"] > div,
        [data-baseweb="textarea"] {
            background: #FFFFFF !important;
            border-color: #D8DDF0 !important;
            border-radius: 10px !important;
        }

        [data-baseweb="select"] > div {
            color: #202344 !important;
        }

        [data-baseweb="select"] [role="combobox"],
        [data-baseweb="select"] [role="combobox"] * {
            color: #202344 !important;
        }

        /* Dropdown popup and options */
        [data-baseweb="popover"],
        [data-baseweb="menu"],
        [role="listbox"],
        [role="option"] {
            background: #FFFFFF !important;
            color: #202344 !important;
        }

        [role="option"] * {
            color: #202344 !important;
        }

        [role="option"]:hover {
            background: #EDE9FE !important;
        }

        /* Main-page checkboxes and radio controls */
        [data-testid="stCheckbox"] label,
        [data-testid="stRadio"] label {
            color: #25304A !important;
        }


        /* =========================================
           HERO SECTION
        ========================================= */

        .hero {
            padding: 30px;
            border-radius: 23px;
            background: linear-gradient(
                115deg,
                #6D28D9,
                #2563EB 58%,
                #06B6D4
            );
            color: #FFFFFF;
            margin-bottom: 25px;
            box-shadow: 0 12px 32px rgba(79, 70, 229, .18);
        }

        .hero h1 {
            color: #FFFFFF !important;
            font-size: 2.25rem;
            margin: 0 0 8px 0;
        }

        .hero p {
            color: #F0F9FF !important;
            margin: 0;
            font-size: 1.03rem;
        }


        /* =========================================
           CARDS
        ========================================= */

        .metric-card,
        .section-card {
            padding: 22px;
            border-radius: 18px;
            background: #FFFFFF;
            border: 1px solid #E0E7FF;
            box-shadow: 0 6px 22px rgba(55, 48, 163, .07);
            margin-bottom: 15px;
        }

        .metric-label {
            color: #596780 !important;
            font-size: .9rem;
            margin-bottom: 9px;
        }

        .metric-value {
            color: #4C1D95 !important;
            font-size: 1.8rem;
            font-weight: 800;
        }

        .metric-caption {
            color: #65718A !important;
            font-size: .8rem;
            margin-top: 6px;
        }

        .section-card h3 {
            color: #4C1D95 !important;
        }

        .risk-high {
            padding: 20px;
            border-radius: 15px;
            background: #FFF1F2;
            border: 1px solid #FDA4AF;
            color: #9F1239 !important;
        }

        .risk-high h3,
        .risk-high p {
            color: #9F1239 !important;
        }

        .risk-low {
            padding: 20px;
            border-radius: 15px;
            background: #ECFDF5;
            border: 1px solid #6EE7B7;
            color: #065F46 !important;
        }

        .risk-low h3,
        .risk-low p {
            color: #065F46 !important;
        }

        .eyebrow {
            color: #6D28D9 !important;
            font-size: .72rem;
            font-weight: 800;
            letter-spacing: 1.3px;
        }


        /* =========================================
           BUTTONS
        ========================================= */

        /* Primary buttons */
        div.stButton > button[kind="primary"],
        button[kind="primaryFormSubmit"] {
            background: linear-gradient(
                100deg,
                #7C3AED,
                #2563EB
            ) !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            border: none !important;
            border-radius: 11px !important;
            min-height: 46px;
            font-size: 1rem !important;
            font-weight: 700 !important;
        }

        /* Force primary button child text to white */
        div.stButton > button[kind="primary"] *,
        button[kind="primaryFormSubmit"] * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        /* Secondary buttons */
        div.stButton > button[kind="secondary"] {
            background: #FFFFFF !important;
            color: #4C1D95 !important;
            -webkit-text-fill-color: #4C1D95 !important;
            border: 1px solid #C4B5FD !important;
            border-radius: 10px !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
        }

        /* Fix the Check API health button text.
           This also handles Streamlit versions where
           the button kind selector differs. */
        [data-testid="stSidebar"] div.stButton > button {
            background: linear-gradient(
                100deg,
                #7C3AED,
                #2563EB
            ) !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px !important;
            min-height: 46px !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
        }

        [data-testid="stSidebar"] div.stButton > button * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        [data-testid="stSidebar"] div.stButton > button:hover {
            background: linear-gradient(
                100deg,
                #6D28D9,
                #1D4ED8
            ) !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }


        /* =========================================
           FOCUS INDICATORS
        ========================================= */

        input:focus,
        textarea:focus {
            border-color: #7C3AED !important;
            box-shadow: 0 0 0 2px #DDD6FE !important;
        }


        /* =========================================
           ALERTS
        ========================================= */

        [data-testid="stAlert"] {
            border-radius: 12px;
        }


        /* =========================================
           FOOTER
        ========================================= */

        .app-footer {
            padding: 18px 0 5px;
            color: #64748B !important;
            text-align: center;
            font-size: .8rem;
        }

        footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


apply_styles()


# =========================================
# SIDEBAR
# =========================================

with st.sidebar:
    st.markdown("# 💎 ChurnIQ")
    st.caption("CUSTOMER INTELLIGENCE PLATFORM")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "📊 Overview",
            "🎯 Churn Prediction",
            "ℹ️ About",
        ],
        label_visibility="visible",
        key="navigation",
    )

    st.divider()

    st.markdown("### 🔌 API connection")

    if "api_url" not in st.session_state:
        st.session_state.api_url = DEFAULT_API_URL

    api_url = st.text_input(
        "Backend URL",
        key="api_url",
        help="Local Docker API: http://localhost:8001",
    ).rstrip("/")

    if st.button(
        "Check API health",
        use_container_width=True,
        type="primary",
    ):
        try:
            health = requests.get(
                f"{api_url}/health",
                timeout=5,
            )

            if health.ok:
                st.success("API is responding")
                st.json(health.json())
            else:
                st.error(
                    f"API returned HTTP {health.status_code}"
                )

        except requests.RequestException as exc:
            st.error(f"Could not connect: {exc}")

    st.divider()

    st.caption("Streamlit · FastAPI · Machine Learning")


# =========================================
# SHARED HERO
# =========================================

st.markdown(
    """
    <div class="hero">
        <h1>Customer Churn Intelligence ✨</h1>
        <p>
            Understand customer risk.
            Make smarter retention decisions.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================
# PAGE ROUTING
# =========================================

if page == "📊 Overview":
    render_overview()

elif page == "🎯 Churn Prediction":
    render_prediction(api_url)

else:
    render_about()


# =========================================
# FOOTER
# =========================================

st.markdown(
    """
    <div class="app-footer">
        ChurnIQ · Customer Intelligence · ML Demo
    </div>
    """,
    unsafe_allow_html=True,
)