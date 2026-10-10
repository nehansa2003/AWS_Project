
import math

import plotly.graph_objects as go
import requests
import streamlit as st


# =========================================================
# CUSTOMER CATEGORIES
# These values match the categories in the training dataset.
# =========================================================

OPTIONS = {
    "age_group": ["18-24", "25-34", "35-44", "45-54", "55+"],
    "gender": ["Female", "Male", "Other"],
    "region": ["West", "Central", "South", "North", "East"],
    "customer_segment": ["Loyal", "New", "Returning", "VIP"],
    "preferred_channel": ["Online", "In-store", "Mobile App"],
}


# =========================================================
# EXPECTED MODEL FEATURES
# Exclude customer_id, churn_risk, and churn_flag.
# =========================================================

EXPECTED_FEATURES = [
    "age_group",
    "gender",
    "region",
    "customer_segment",
    "preferred_channel",
    "purchase_frequency",
    "avg_order_value",
    "total_spent",
    "recency_days",
    "website_visits",
    "discount_usage_rate",
    "email_open_rate",
    "cart_abandonment_rate",
    "loyalty_score",
    "engagement_score",
]


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def select_index(options, value):
    """Return a valid default index for a selectbox."""
    return options.index(value) if value in options else 0


def validate_customer(customer):
    """Validate customer inputs against observed dataset ranges."""

    if set(customer.keys()) != set(EXPECTED_FEATURES):
        raise ValueError(
            "Customer features do not match the expected model schema."
        )

    numeric_fields = [
        "purchase_frequency",
        "avg_order_value",
        "total_spent",
        "recency_days",
        "website_visits",
        "discount_usage_rate",
        "email_open_rate",
        "cart_abandonment_rate",
        "loyalty_score",
        "engagement_score",
    ]

    # Ensure numerical values are valid and finite.
    for field in numeric_fields:
        value = customer[field]

        if isinstance(value, bool):
            raise ValueError(f"{field} must be numeric.")

        try:
            value = float(value)
        except (TypeError, ValueError, OverflowError):
            raise ValueError(f"{field} must be numeric.") from None

        if not math.isfinite(value):
            raise ValueError(f"{field} must be a finite number.")

        customer[field] = value

    # Validate categories.
    for field, options in OPTIONS.items():
        if customer[field] not in options:
            raise ValueError(f"Invalid category for {field}.")

    # Integer-valued features and observed ranges.
    integer_ranges = {
        "purchase_frequency": (1, 60),
        "recency_days": (1, 364),
        "website_visits": (2, 479),
        "loyalty_score": (10, 99),
        "engagement_score": (10, 92),
    }

    for field, (minimum, maximum) in integer_ranges.items():
        value = customer[field]

        if not value.is_integer():
            raise ValueError(f"{field} must be a whole number.")

        if not minimum <= value <= maximum:
            raise ValueError(
                f"{field} must be between {minimum} and {maximum}."
            )

    # Observed continuous feature ranges.
    continuous_ranges = {
        "avg_order_value": (20.03, 400.0),
        "total_spent": (17.87, 28444.24),
        "discount_usage_rate": (0.05, 0.80),
        "email_open_rate": (0.05, 0.90),
        "cart_abandonment_rate": (0.05, 0.85),
    }

    for field, (minimum, maximum) in continuous_ranges.items():
        value = customer[field]

        if not minimum <= value <= maximum:
            raise ValueError(
                f"{field} must be between {minimum} and {maximum}."
            )


# =========================================================
# MAIN STREAMLIT VIEW
# =========================================================

def render(api_url):

    st.markdown("## 🎯 Customer churn prediction")

    st.write(
        "Enter the customer's information below, then submit it "
        "to your machine learning API."
    )

    st.markdown(
        '<div class="section-card">'
        '<h3>👤 Customer profile</h3>'
        '<p>Choose a category for each customer attribute.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # =====================================================
    # CUSTOMER INPUT FORM
    # =====================================================

    with st.form("customer_prediction_form"):

        st.markdown("### 🪪 Basic information")

        c1, c2, c3 = st.columns(3)

        with c1:
            age_group = st.selectbox(
                "Age group",
                OPTIONS["age_group"],
                index=select_index(OPTIONS["age_group"], "25-34"),
            )

            gender = st.selectbox(
                "Gender",
                OPTIONS["gender"],
                index=select_index(OPTIONS["gender"], "Female"),
            )

        with c2:
            region = st.selectbox(
                "Region",
                OPTIONS["region"],
                index=select_index(OPTIONS["region"], "West"),
            )

            customer_segment = st.selectbox(
                "Customer segment",
                OPTIONS["customer_segment"],
                index=select_index(OPTIONS["customer_segment"], "Loyal"),
            )

        with c3:
            preferred_channel = st.selectbox(
                "Preferred channel",
                OPTIONS["preferred_channel"],
                index=select_index(OPTIONS["preferred_channel"], "Online"),
            )

        # -------------------------------------------------
        # Purchasing behaviour
        # -------------------------------------------------

        st.divider()
        st.markdown("### 🛒 Purchasing behaviour")

        c1, c2, c3 = st.columns(3)

        with c1:
            purchase_frequency = st.number_input(
                "Purchase frequency",
                min_value=1,
                max_value=60,
                value=8,
                step=1,
                help="Observed training range: 1–60.",
            )

            avg_order_value = st.number_input(
                "Average order value",
                min_value=20.03,
                max_value=400.0,
                value=209.49,
                step=1.0,
                help="Use the currency and scale used in the training data.",
            )

        with c2:
            total_spent = st.number_input(
                "Total spent",
                min_value=17.87,
                max_value=28444.24,
                value=1089.18,
                step=50.0,
                help="Observed training range: 17.87–28444.24.",
            )

            recency_days = st.number_input(
                "Days since last purchase",
                min_value=1,
                max_value=364,
                value=182,
                step=1,
            )

        with c3:
            website_visits = st.number_input(
                "Website visits",
                min_value=2,
                max_value=479,
                value=29,
                step=1,
            )

            discount_usage_rate = st.slider(
                "Discount usage rate",
                min_value=0.05,
                max_value=0.80,
                value=0.43,
                step=0.01,
                help="Enter a rate between 0 and 1, not a percentage.",
            )

        # -------------------------------------------------
        # Engagement and loyalty
        # -------------------------------------------------

        st.divider()
        st.markdown("### 💌 Engagement and loyalty")

        st.caption(
            "Adjust these values to describe the customer's "
            "engagement and loyalty."
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            email_open_rate = st.slider(
                "Email open rate",
                min_value=0.05,
                max_value=0.90,
                value=0.47,
                step=0.01,
            )

        with c2:
            cart_abandonment_rate = st.slider(
                "Cart abandonment rate",
                min_value=0.05,
                max_value=0.85,
                value=0.45,
                step=0.01,
            )

        with c3:
            loyalty_score = st.number_input(
                "Loyalty score",
                min_value=10,
                max_value=99,
                value=55,
                step=1,
            )

            engagement_score = st.number_input(
                "Engagement score",
                min_value=10,
                max_value=92,
                value=51,
                step=1,
            )

        st.divider()

        submitted = st.form_submit_button(
            "✨ Predict customer churn",
            type="primary",
            use_container_width=True,
        )

    # =====================================================
    # PROCESS FORM ONLY AFTER SUBMISSION
    # Keep this section OUTSIDE the with st.form block.
    # =====================================================

    if not submitted:
        return

    # Create the customer payload with exactly 15 features.
    customer = {
        "age_group": age_group,
        "gender": gender,
        "region": region,
        "customer_segment": customer_segment,
        "preferred_channel": preferred_channel,
        "purchase_frequency": purchase_frequency,
        "avg_order_value": avg_order_value,
        "total_spent": total_spent,
        "recency_days": recency_days,
        "website_visits": website_visits,
        "discount_usage_rate": discount_usage_rate,
        "email_open_rate": email_open_rate,
        "cart_abandonment_rate": cart_abandonment_rate,
        "loyalty_score": loyalty_score,
        "engagement_score": engagement_score,
    }

    # =====================================================
    # VALIDATE INPUT
    # =====================================================

    try:
        validate_customer(customer)

    except (ValueError, TypeError, OverflowError) as exc:
        st.error(f"Please check the customer information: {exc}")
        return

    # =====================================================
    # CALL BACKEND API
    # =====================================================

    with st.spinner("✨ Analysing customer information..."):

        try:
            response = requests.post(
                f"{api_url.rstrip('/')}/predict",
                json=customer,
                timeout=30,
            )

            if not response.ok:
                st.error(
                    f"API error ({response.status_code}): "
                    f"{response.text[:1200]}"
                )

                st.info(
                    "Check that the backend is running and its input "
                    "schema matches the model's expected features."
                )
                return

            try:
                result = response.json()

            except ValueError:
                st.error("The prediction API did not return valid JSON.")
                return

            if not isinstance(result, dict):
                st.error("The API response must be a JSON object.")
                return

            if (
                "predicted_churn" not in result
                or "churn_probability" not in result
            ):
                st.error(
                    "The API response must contain predicted_churn "
                    "and churn_probability."
                )
                return

            raw_prediction = result["predicted_churn"]
            raw_probability = result["churn_probability"]

            if isinstance(raw_prediction, bool):
                st.error("The API returned an invalid predicted class.")
                return

            if isinstance(raw_prediction, str):
                if raw_prediction.strip() not in ("0", "1"):
                    st.error("The API returned an invalid predicted class.")
                    return

            elif isinstance(raw_prediction, (int, float)):
                if not math.isfinite(float(raw_prediction)):
                    st.error("The API returned an invalid predicted class.")
                    return

                if float(raw_prediction) not in (0.0, 1.0):
                    st.error("The API returned an invalid predicted class.")
                    return

            else:
                st.error("The API returned an invalid predicted class.")
                return

            predicted_churn = int(raw_prediction)

            if isinstance(raw_probability, bool):
                st.error("The API returned an invalid churn probability.")
                return

            try:
                probability = float(raw_probability)

            except (TypeError, ValueError, OverflowError):
                st.error("The API returned an invalid churn probability.")
                return

            if not math.isfinite(probability) or not 0 <= probability <= 1:
                st.error("The API returned an invalid churn probability.")
                return

        except requests.Timeout:
            st.error(
                "The prediction API took too long to respond. "
                "Please try again."
            )
            return

        except requests.ConnectionError:
            st.error("Could not connect to the prediction API.")

            st.info(
                "Make sure the backend or Docker container is running "
                "and the API URL is correct."
            )
            return

        except requests.RequestException as exc:
            st.error(f"Prediction request failed: {exc}")
            return

    # =====================================================
    # DISPLAY PREDICTION RESULTS
    # =====================================================

    st.divider()
    st.markdown("## ✨ Prediction Results")

    result_col, chart_col = st.columns([1, 1], gap="large")

    with result_col:

        if predicted_churn == 1:
            st.markdown(
                """
                <div class="risk-high">
                    <h3>⚠️ Likely to churn</h3>
                    <p>The model predicted customer churn.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:
            st.markdown(
                """
                <div class="risk-low">
                    <h3>✅ Unlikely to churn</h3>
                    <p>The model predicted customer retention.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.metric(
            "Churn probability",
            f"{probability:.2%}",
        )

        st.progress(probability)

        st.caption(
            "This probability is a model estimate, not a guarantee "
            "of future customer behaviour."
        )

    # -----------------------------------------------------
    # Donut chart
    # -----------------------------------------------------

    with chart_col:

        fig = go.Figure(
            go.Pie(
                labels=[
                    "Churn probability",
                    "Remaining probability",
                ],
                values=[
                    probability,
                    1 - probability,
                ],
                hole=0.68,
                marker=dict(
                    colors=["#8B5CF6", "#DDE5FF"],
                    line=dict(
                        color="#FFFFFF",
                        width=3,
                    ),
                ),
                textinfo="none",
            )
        )

        fig.update_layout(
            title="Predicted Churn Risk",
            annotations=[
                dict(
                    text=f"{probability:.1%}",
                    x=0.5,
                    y=0.5,
                    font_size=27,
                    font_color="#30205F",
                    showarrow=False,
                )
            ],
            showlegend=True,
            height=320,
            margin=dict(
                t=60,
                b=20,
                l=10,
                r=10,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#30205F"),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # =====================================================
    # DEBUGGING INFORMATION
    # =====================================================

    with st.expander("View submitted customer information"):
        st.json(customer)

    with st.expander("View raw API response"):
        st.json(result)

