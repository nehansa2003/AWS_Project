import streamlit as st
import pandas as pd


def metric_card(title, value, description, icon=""):
    st.markdown(
        f"""
        <div class="dashboard-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div class="card-title">{title}</div>
                <div style="font-size: 1.5rem; opacity: 0.8;">{icon}</div>
            </div>
            <div class="card-value">{value}</div>
            <div class="card-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render():
    st.markdown(
        """
        <div class="hero-container">
            <h1>Customer Churn Overview</h1>
            <p>Explore the customer churn prediction system, architecture, and feature distribution.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 📈 System Architecture")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Model Inputs", "15", "Customer attributes", "📊")
    with col2:
        metric_card("Backend", "FastAPI", "Prediction API", "⚡")
    with col3:
        metric_card("Serving", "Docker", "Containerized API", "🐳")
    with col4:
        metric_card("Frontend", "Streamlit", "Dashboard UI", "🎨")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_workflow, col_features = st.columns([1, 1], gap="large")
    
    with col_workflow:
        st.markdown("### 🔍 Workflow")
        st.info(
            "**1. Enter Information** on the Churn Prediction page.\n\n"
            "**2. Send Data** securely to the FastAPI backend.\n\n"
            "**3. Predict Risk** using the machine-learning model.\n\n"
            "**4. View Results** and churn probabilities interactively.",
            icon="🚀"
        )
        
        st.markdown(
            """
            <div class="dashboard-card" style="margin-top: 1rem;">
                <div class="card-title" style="color: #25304A;">Data Connectivity</div>
                <p style="color: #65718A; font-size: 0.9rem; margin-top: 0.5rem; margin-bottom: 0;">
                    This overview describes the application structure. Live customer metrics and aggregate predictions will appear here when connected to a live database or data warehouse.
                </p>
            </div>
            """, unsafe_allow_html=True
        )

    with col_features:
        st.markdown("### 📋 Feature Groups")
        
        feature_groups = pd.DataFrame(
            {
                "Feature Category": [
                    "👤 Customer Profile",
                    "🛒 Purchasing Behaviour",
                    "💌 Engagement & Loyalty",
                ],
                "Inputs": [5, 6, 4],
                "Examples": [
                    "Age, Gender, Region...",
                    "Frequency, Total Spent...",
                    "Email Open Rate...",
                ]
            }
        )
        
        st.dataframe(
            feature_groups,
            hide_index=True,
        )