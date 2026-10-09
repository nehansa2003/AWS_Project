
import streamlit as st
import pandas as pd


def metric_card(title, value, description):
    st.markdown(
        f"""
        <div style="
            background: white;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #E5E7EB;
            min-height: 120px;
        ">
            <div style="color: #666; font-size: 14px;">{title}</div>
            <div style="color: #202344; font-size: 26px; font-weight: bold;">
                {value}
            </div>
            <div style="color: #666; font-size: 12px;">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render():
    st.title("📊 Customer Churn Overview")
    st.write(
        "Explore the customer churn prediction system and its main components."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Model inputs", "15", "Customer attributes")

    with col2:
        metric_card("Backend", "FastAPI", "Prediction API")

    with col3:
        metric_card("Model serving", "Docker", "Containerized API")

    with col4:
        metric_card("Frontend", "Streamlit", "Interactive dashboard")

    st.subheader("How the system works")

    st.markdown(
        """
        1. **Enter customer information** on the Churn Prediction page.
        2. **Send the information** to the FastAPI backend.
        3. **Generate a prediction** using the trained machine-learning model.
        4. **Display the result** and estimated churn probability.
        """
    )

    st.subheader("Customer feature groups")

    # Define the DataFrame before using it.
    feature_groups = pd.DataFrame(
        {
            "Feature group": [
                "Customer profile",
                "Purchasing behaviour",
                "Engagement and loyalty",
            ],
            "Number of inputs": [5, 6, 4],
        }
    )

    st.dataframe(
        feature_groups,
        use_container_width=True,
        hide_index=True,
    )

    st.info(
        "This overview describes the application structure. "
        "Live customer metrics will appear only if connected data is available."
    )