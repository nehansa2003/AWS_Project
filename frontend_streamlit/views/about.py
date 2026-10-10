
import streamlit as st


def render():
    st.markdown("## ℹ️ About ChurnIQ")
    st.caption(
        "A machine learning application for exploring customer churn risk."
    )

    # About ChurnIQ
    st.markdown(
        """
        <div class="section-card">
            <h3>💎 Customer Churn Intelligence</h3>
            <p>
                ChurnIQ is a machine learning application designed to
                predict customer churn risk using customer purchasing
                behavior, engagement, loyalty, and retention indicators.
                Users can enter customer information and explore the
                predicted churn class and probability.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Machine learning model
    st.markdown("### 🤖 About the Machine Learning Model")

    st.markdown(
        """
        ChurnIQ uses a trained machine learning classification model
        developed using the <b>Retail Intelligence: Customer Churn Dataset</b>.
        The dataset contains approximately 100,000 retail customer records
        representing customer demographics, purchasing activity, spending,
        website engagement, loyalty, and churn indicators.

        The model analyzes the available customer features to estimate
        churn risk and support customer retention analysis.
        """,
        unsafe_allow_html=True,
    )

    # Dataset overview
    st.markdown(
        """
        <div class="section-card">
            <h3>📊 Dataset Overview</h3>
            <ul>
                <li><b>Dataset:</b> Retail Intelligence: Customer Churn Dataset</li>
                <li><b>Dataset size:</b> Approximately 100,000 customer records</li>
                <li><b>Prediction target:</b> Customer churn status</li>
                <li><b>Machine learning task:</b> Binary classification</li>
                <li><b>Primary objective:</b> Customer churn risk assessment</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Prediction details
    st.markdown("### 🎯 What Does This Model Predict?")

    st.markdown(
        """
        The model estimates whether a customer is likely to churn
        based on the customer information submitted through the
        ChurnIQ application.

        - **Purchasing behavior:** Purchase frequency, recency, and spending.
        - **Customer engagement:** Website visits and available engagement metrics.
        - **Loyalty indicators:** Loyalty scores and discount usage.
        - **Churn indicators:** Inactivity and cart abandonment, where available.

        The prediction interface displays the predicted churn class and
        probability when supported by the deployed model.
        """
    )

    # Scope and limitations
    st.markdown("### 🌍 Model Scope and Limitations")

    st.markdown(
        """
        <div class="section-card">
            <h3>📍 Dataset-Specific Predictions</h3>
            <p>
                The model learns customer behavior patterns from the
                population represented in its training dataset. Its
                predictions are most appropriately interpreted within
                the scope of the customer profiles and characteristics
                represented by that data.
            </p>
            <p>
                The model may not perform equally well for customers
                from different geographical regions, retail markets,
                or business environments. Differences in customer
                behavior and purchasing patterns can affect prediction
                reliability.
            </p>
            <p>
                The model has not necessarily been validated for every
                geographical region or customer population. Its
                effectiveness in a particular market should be assessed
                using relevant customer data and appropriate performance
                evaluation.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Important: ChurnIQ provides estimates rather than guaranteed "
        "outcomes. Prediction reliability depends on input data quality "
        "and how closely the customer profiles match the data used to "
        "train and evaluate the model."
    )

    # Use cases
    st.markdown("### 🚀 Intended Use Cases")

    st.markdown(
        """
        - Customer churn risk assessment
        - Retail customer behavior analysis
        - Customer segmentation
        - Customer retention planning
        - Machine learning experimentation
        - Exploring customer engagement patterns
        """
    )

    # Technology stack
    st.markdown("### 🧱 Technology Stack")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="section-card">
                <h3>🎨 Frontend</h3>
                <p>Python and Streamlit</p>
                <p>Interactive user interface and visualizations</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-card">
                <h3>⚡ Backend</h3>
                <p>FastAPI REST API</p>
                <p>JSON-based request and response handling</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="section-card">
                <h3>🤖 Machine Learning</h3>
                <p>Trained classification model</p>
                <p>Customer churn class and probability prediction</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-card">
                <h3>🐳 Deployment</h3>
                <p>Dockerized API environment</p>
                <p>AWS deployment and hosting</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Responsible use
    st.markdown("### 🔍 Responsible Use")

    st.warning(
        "A churn prediction does not explain why a customer may leave. "
        "Evaluate model performance using appropriate test data, consider "
        "potential bias, and use predictions alongside other relevant "
        "information before making business decisions."
    )

    # Footer
    st.caption(
        "ChurnIQ · Customer Intelligence · Machine Learning"
    )
