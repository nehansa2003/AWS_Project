
import streamlit as st


def render():
    st.markdown("## ℹ️ About ChurnIQ")
    st.caption("A machine learning application for exploring customer churn risk.")

    st.markdown(
        """
        <div class="section-card">
            <h3>💎 Customer Churn Intelligence</h3>
            <p>
                ChurnIQ provides an interactive interface for submitting
                customer information to a machine learning model and viewing
                its predicted churn class and probability.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🧱 Technology stack")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="section-card">
                <h3>🎨 Frontend</h3>
                <p>Python and Streamlit</p>
                <p>Interactive controls and charts</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-card">
                <h3>⚡ Backend</h3>
                <p>FastAPI REST endpoint</p>
                <p>JSON request and response</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="section-card">
                <h3>🤖 Machine learning</h3>
                <p>Existing saved prediction model</p>
                <p>Customer features and churn probability</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-card">
                <h3>🐳 Deployment</h3>
                <p>Dockerized API</p>
                <p>AWS deployment planned</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 🔍 Responsible use")

    st.warning(
        "A churn prediction does not explain why a customer may leave. "
        "Validate model performance on held-out data, check for bias, and "
        "use predictions alongside other relevant information before "
        "making business decisions."
    )