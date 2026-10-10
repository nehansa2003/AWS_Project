import streamlit as st

def render():
    st.markdown(
        """
        <div class="hero-container">
            <h1>About ChurnIQ</h1>
            <p>Context, objectives, and technology behind the customer intelligence platform.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎯 Project Objectives")
    st.markdown(
        """
        <div class="dashboard-card" style="margin-bottom: 2rem;">
            <p style="margin-bottom: 0; font-size: 1.05rem; line-height: 1.6; color: #65718A;">
                <strong>ChurnIQ</strong> is a machine learning application designed to
                predict customer churn risk using customer purchasing
                behavior, engagement, loyalty, and retention indicators.
                Users can input customer information and instantly explore the
                predicted churn class and probability to make informed retention decisions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("### 📊 Dataset Overview")
        st.markdown(
            """
            <div class="dashboard-card">
                <ul style="margin: 0; padding-left: 1.2rem; color: #65718A; font-size: 1rem; line-height: 1.8;">
                    <li><b>Dataset:</b> Retail Intelligence: Customer Churn Dataset</li>
                    <li><b>Size:</b> ~100,000 customer records</li>
                    <li><b>Prediction Target:</b> Customer churn status</li>
                    <li><b>Task:</b> Binary Classification</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🚀 Use Cases")
        st.markdown(
            """
            <div class="dashboard-card">
                <ul style="margin: 0; padding-left: 1.2rem; color: #65718A; font-size: 1rem; line-height: 1.8;">
                    <li>Customer churn risk assessment</li>
                    <li>Retail customer behavior analysis</li>
                    <li>Customer segmentation & retention planning</li>
                    <li>Exploring engagement patterns</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("### ⚙️ Technology Stack")
        st.markdown(
            """
            <div class="dashboard-card">
                <div style="margin-bottom: 1rem;">
                    <b style="color: #25304A;">🎨 Frontend</b>
                    <p style="margin: 0.25rem 0 0; color: #65718A;">Python, Streamlit, and Plotly for an interactive user interface.</p>
                </div>
                <div style="margin-bottom: 1rem;">
                    <b style="color: #25304A;">⚡ Backend</b>
                    <p style="margin: 0.25rem 0 0; color: #65718A;">FastAPI REST API with robust validation via Pydantic.</p>
                </div>
                <div>
                    <b style="color: #25304A;">🤖 Machine Learning</b>
                    <p style="margin: 0.25rem 0 0; color: #65718A;">Scikit-Learn and XGBoost for data processing and model evaluation.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ⚠️ Scope and Limitations")
    
    st.info(
        "**Dataset-Specific Predictions:** The model learns customer behavior patterns from the population "
        "represented in its training dataset. Predictions are most reliable for similar customer profiles and "
        "may require validation if applied to different geographical regions or retail markets.",
        icon="💡"
    )
    
    st.warning(
        "**Responsible Use:** A churn prediction does not explain *why* a customer may leave. Evaluate model "
        "performance using appropriate test data, consider potential bias, and use predictions alongside other "
        "business insights before making retention decisions.",
        icon="⚠️"
    )
