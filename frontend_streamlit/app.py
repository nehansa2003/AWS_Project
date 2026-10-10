import os
import requests
import streamlit as st

from views.overview import render as render_overview
from views.prediction import render as render_prediction
from views.about import render as render_about

st.set_page_config(
    page_title="ChurnIQ | Customer Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_API_URL = os.getenv("CHURN_API_URL", "http://localhost:8001")

def apply_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* =========================================
           MAIN PAGE
        ========================================= */
        .stApp {
            background: linear-gradient(135deg, #F5F3FF 0%, #EFF6FF 55%, #F0FDFA 100%);
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
            background: linear-gradient(180deg, #24104F 0%, #43218B 55%, #5B3CC4 100%);
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

        /* Sidebar text visibility fixes */
        [data-testid="stSidebar"] * {
            color: #FFFFFF;
        }

        [data-testid="stSidebar"] h1 {
            color: #FFFFFF !important;
            font-size: 2rem !important;
            font-weight: 800 !important;
        }

        /* Navigation Radio Buttons */
        [data-testid="stSidebar"] [role="radiogroup"] label {
            background: transparent !important;
            color: #FFFFFF !important;
            border-radius: 8px;
            transition: all 0.2s ease;
            padding: 0.5rem 1rem;
            cursor: pointer;
            margin-bottom: 0.2rem;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(255, 255, 255, 0.15) !important;
        }
        [data-testid="stSidebar"] [role="radiogroup"] div[data-testid="stMarkdownContainer"] p {
            color: #FFFFFF !important;
            font-weight: 600;
            font-size: 1.05rem;
            margin: 0;
        }

        /* =========================================
           MAIN DASHBOARD & TYPOGRAPHY
        ========================================= */
        [data-testid="stMain"] h1, 
        [data-testid="stMain"] h2, 
        [data-testid="stMain"] h3,
        [data-testid="stMain"] h4 {
            color: #25304A;
            font-weight: 700;
        }

        /* Hero Section */
        .hero-container {
            background: linear-gradient(115deg, #6D28D9, #2563EB 58%, #06B6D4);
            padding: 2.5rem 3rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            margin-top: 1rem;
            color: white;
            box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.18);
        }
        .hero-container h1 {
            color: #FFFFFF !important;
            margin-top: 0;
            margin-bottom: 0.5rem;
            font-size: 2.25rem;
            font-weight: 800;
        }
        .hero-container p {
            color: #F0F9FF;
            font-size: 1.1rem;
            margin-bottom: 0;
            font-weight: 400;
        }

        /* Dashboard Cards */
        .dashboard-card {
            background: #FFFFFF;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 6px 22px rgba(55, 48, 163, 0.07);
            border: 1px solid #E0E7FF;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            height: 100%;
        }
        .dashboard-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(55, 48, 163, 0.12);
        }
        .card-title {
            color: #596780;
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        .card-value {
            color: #4C1D95;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.25rem;
        }
        .card-description {
            color: #65718A;
            font-size: 0.875rem;
        }

        /* Form Inputs */
        [data-testid="stForm"] {
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 2rem;
            border: 1px solid #E0E7FF;
            box-shadow: 0 6px 22px rgba(55, 48, 163, 0.05);
        }
        [data-testid="stMain"] input, 
        [data-testid="stMain"] [data-baseweb="select"] {
            border-radius: 8px;
        }
        [data-testid="stMain"] [data-baseweb="input"],
        [data-testid="stMain"] [data-baseweb="select"] > div {
            border-color: #D8DDF0 !important;
            background-color: #FFFFFF !important;
            transition: all 0.2s;
        }
        [data-testid="stMain"] [data-baseweb="input"] input,
        [data-testid="stMain"] [data-baseweb="select"] * {
            color: #202344 !important;
            -webkit-text-fill-color: #202344 !important;
        }
        [data-testid="stMain"] [data-baseweb="input"]:focus-within,
        [data-testid="stMain"] [data-baseweb="select"] > div:focus-within {
            border-color: #7C3AED !important;
            box-shadow: 0 0 0 2px #DDD6FE !important;
        }

        /* Dropdown popups */
        [data-baseweb="menu"], [role="listbox"], [role="option"] {
            background: #FFFFFF !important;
            color: #202344 !important;
        }
        [role="option"] * {
            color: #202344 !important;
        }
        [role="option"]:hover {
            background: #EDE9FE !important;
        }

        /* Prediction Button */
        [data-testid="stMain"] div.stButton > button[kind="primary"],
        button[kind="primaryFormSubmit"] {
            background: linear-gradient(100deg, #7C3AED, #2563EB) !important;
            color: #FFFFFF !important;
            border-radius: 11px !important;
            padding: 0.75rem 1.5rem;
            font-weight: 700 !important;
            font-size: 1.05rem !important;
            border: none !important;
            transition: all 0.2s;
            box-shadow: 0 4px 6px -1px rgba(124, 58, 237, 0.2);
            min-height: 46px;
        }
        [data-testid="stMain"] div.stButton > button[kind="primary"]:hover,
        button[kind="primaryFormSubmit"]:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 15px -3px rgba(124, 58, 237, 0.3);
            background: linear-gradient(100deg, #6D28D9, #1D4ED8) !important;
        }
        [data-testid="stMain"] div.stButton > button[kind="primary"] *,
        button[kind="primaryFormSubmit"] * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        /* Result Panels */
        .result-high {
            background-color: #FFF1F2;
            border: 1px solid #FDA4AF;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .result-high h3 {
            color: #9F1239 !important;
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.5rem;
        }
        .result-high p {
            color: #9F1239 !important;
            margin-bottom: 0;
            font-size: 1.1rem;
        }
        
        .result-low {
            background-color: #ECFDF5;
            border: 1px solid #6EE7B7;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .result-low h3 {
            color: #065F46 !important;
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.5rem;
        }
        .result-low p {
            color: #065F46 !important;
            margin-bottom: 0;
            font-size: 1.1rem;
        }
        
        /* Metric Styling override */
        [data-testid="stMetricValue"] {
            color: #4C1D95 !important;
            font-weight: 800;
        }
        [data-testid="stMetricLabel"] {
            color: #596780 !important;
            font-weight: 600;
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
    st.markdown("""
        <div style="padding-bottom: 1.5rem; border-bottom: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 1.5rem;">
            <h1 style="color: white; margin-bottom: 0; font-size: 2.2rem; font-weight: 800;">💎 ChurnIQ</h1>
            <p style="color: #F3E8FF; font-size: 0.85rem; margin-top: 0; font-weight: 600; letter-spacing: 0.05em;">CUSTOMER INTELLIGENCE</p>
        </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "NAVIGATION",
        [
            "📊 Overview",
            "🎯 Churn Prediction",
            "ℹ️ About",
        ],
        label_visibility="collapsed",
    )

# =========================================
# PAGE ROUTING
# =========================================
if page == "📊 Overview":
    render_overview()
elif page == "🎯 Churn Prediction":
    render_prediction(DEFAULT_API_URL.rstrip("/"))
else:
    render_about()