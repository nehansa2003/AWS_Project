import math
import plotly.graph_objects as go
import requests
import streamlit as st

# =========================================================
# CUSTOMER CATEGORIES
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
# =========================================================
EXPECTED_FEATURES = [
    "age_group", "gender", "region", "customer_segment", "preferred_channel",
    "purchase_frequency", "avg_order_value", "total_spent", "recency_days",
    "website_visits", "discount_usage_rate", "email_open_rate",
    "cart_abandonment_rate", "loyalty_score", "engagement_score",
]

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def select_index(options, value):
    return options.index(value) if value in options else 0

def validate_customer(customer):
    if set(customer.keys()) != set(EXPECTED_FEATURES):
        raise ValueError("Customer features do not match the expected model schema.")

    numeric_fields = [
        "purchase_frequency", "avg_order_value", "total_spent", "recency_days",
        "website_visits", "discount_usage_rate", "email_open_rate",
        "cart_abandonment_rate", "loyalty_score", "engagement_score",
    ]

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

    for field, options in OPTIONS.items():
        if customer[field] not in options:
            raise ValueError(f"Invalid category for {field}.")

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
            raise ValueError(f"{field} must be between {minimum} and {maximum}.")

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
            raise ValueError(f"{field} must be between {minimum} and {maximum}.")

# =========================================================
# MAIN STREAMLIT VIEW
# =========================================================
def render(api_url):
    st.markdown(
        """
        <div class="hero-container">
            <h1>Churn Prediction</h1>
            <p>Enter customer attributes below to instantly evaluate churn risk and probability.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =====================================================
    # CUSTOMER INPUT FORM
    # =====================================================
    with st.form("customer_prediction_form", clear_on_submit=False):
        
        st.markdown("#### 👤 Basic Information")
        st.caption("Select the demographic and segment details of the customer.")
        c1, c2, c3 = st.columns(3)
        with c1:
            age_group = st.selectbox("Age group", OPTIONS["age_group"], index=select_index(OPTIONS["age_group"], "25-34"))
            gender = st.selectbox("Gender", OPTIONS["gender"], index=select_index(OPTIONS["gender"], "Female"))
        with c2:
            region = st.selectbox("Region", OPTIONS["region"], index=select_index(OPTIONS["region"], "West"))
            customer_segment = st.selectbox("Customer segment", OPTIONS["customer_segment"], index=select_index(OPTIONS["customer_segment"], "Loyal"))
        with c3:
            preferred_channel = st.selectbox("Preferred channel", OPTIONS["preferred_channel"], index=select_index(OPTIONS["preferred_channel"], "Online"))

        st.markdown("<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #E0E7FF;'>", unsafe_allow_html=True)
        
        st.markdown("#### 🛒 Purchasing Behaviour")
        st.caption("Enter the historical purchase metrics.")
        c1, c2, c3 = st.columns(3)
        with c1:
            purchase_frequency = st.number_input("Purchase frequency", min_value=1, max_value=60, value=8, step=1, help="Observed training range: 1–60.")
            avg_order_value = st.number_input("Average order value", min_value=20.03, max_value=400.0, value=209.49, step=1.0)
        with c2:
            total_spent = st.number_input("Total spent", min_value=17.87, max_value=28444.24, value=1089.18, step=50.0)
            recency_days = st.number_input("Days since last purchase", min_value=1, max_value=364, value=182, step=1)
        with c3:
            website_visits = st.number_input("Website visits", min_value=2, max_value=479, value=29, step=1)
            discount_usage_rate = st.slider("Discount usage rate", min_value=0.05, max_value=0.80, value=0.43, step=0.01)

        st.markdown("<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #E0E7FF;'>", unsafe_allow_html=True)
        
        st.markdown("#### 💌 Engagement and Loyalty")
        st.caption("Adjust the sliders to represent the customer's digital engagement.")
        c1, c2, c3 = st.columns(3)
        with c1:
            email_open_rate = st.slider("Email open rate", min_value=0.05, max_value=0.90, value=0.47, step=0.01)
        with c2:
            cart_abandonment_rate = st.slider("Cart abandonment rate", min_value=0.05, max_value=0.85, value=0.45, step=0.01)
        with c3:
            loyalty_score = st.number_input("Loyalty score", min_value=10, max_value=99, value=55, step=1)
            engagement_score = st.number_input("Engagement score", min_value=10, max_value=92, value=51, step=1)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✨ Predict Customer Churn Risk", type="primary")

    if not submitted:
        return

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

    try:
        validate_customer(customer)
    except (ValueError, TypeError, OverflowError) as exc:
        st.error(f"Please check the customer information: {exc}")
        return

    # =====================================================
    # CALL BACKEND API
    # =====================================================
    with st.spinner("Analyzing customer profile..."):
        try:
            response = requests.post(
                f"{api_url.rstrip('/')}/predict",
                json=customer,
                timeout=30,
            )

            if not response.ok:
                st.error(f"API error ({response.status_code}): {response.text[:1200]}")
                st.info("Check that the backend is running and its input schema matches the model's expected features.")
                return

            try:
                result = response.json()
            except ValueError:
                st.error("The prediction API did not return valid JSON.")
                return

            if not isinstance(result, dict) or "predicted_churn" not in result or "churn_probability" not in result:
                st.error("The API response is missing required fields: predicted_churn and churn_probability.")
                return

            raw_prediction = result["predicted_churn"]
            raw_probability = result["churn_probability"]

            if isinstance(raw_prediction, str):
                if raw_prediction.strip() not in ("0", "1"):
                    st.error("The API returned an invalid predicted class.")
                    return
            elif isinstance(raw_prediction, (int, float)):
                if not math.isfinite(float(raw_prediction)) or float(raw_prediction) not in (0.0, 1.0):
                    st.error("The API returned an invalid predicted class.")
                    return
            else:
                st.error("The API returned an invalid predicted class.")
                return

            predicted_churn = int(raw_prediction)

            try:
                probability = float(raw_probability)
            except (TypeError, ValueError, OverflowError):
                st.error("The API returned an invalid churn probability.")
                return

            if not math.isfinite(probability) or not 0 <= probability <= 1:
                st.error("The API returned an invalid churn probability.")
                return

        except requests.Timeout:
            st.error("The prediction API took too long to respond. Please try again.")
            return
        except requests.ConnectionError:
            st.error("Could not connect to the prediction API.")
            st.info("Make sure the backend or Docker container is running and the API URL is correct.")
            return
        except requests.RequestException as exc:
            st.error(f"Prediction request failed: {exc}")
            return

    # =====================================================
    # DISPLAY PREDICTION RESULTS
    # =====================================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## ✨ Prediction Results")

    result_col, chart_col = st.columns([1, 1], gap="large")

    with result_col:
        if predicted_churn == 1:
            st.markdown(
                """
                <div class="result-high">
                    <h3>⚠️ Likely to Churn</h3>
                    <p>The model predicts a high risk of customer churn.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="result-low">
                    <h3>✅ Unlikely to Churn</h3>
                    <p>The model predicts the customer will be retained.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.metric("Estimated Churn Probability", f"{probability:.2%}")
        st.progress(probability)
        st.caption("Note: This probability is an estimate generated by the ML model, not a guarantee of future behaviour.")

    with chart_col:
        fig = go.Figure(
            go.Pie(
                labels=["Churn Probability", "Retention Probability"],
                values=[probability, 1 - probability],
                hole=0.68,
                marker=dict(
                    colors=["#8B5CF6", "#DDE5FF"],
                    line=dict(color="#FFFFFF", width=3),
                ),
                textinfo="none",
                hoverinfo="label+percent"
            )
        )

        fig.update_layout(
            annotations=[
                dict(
                    text=f"{probability:.1%}",
                    x=0.5,
                    y=0.5,
                    font_size=27,
                    font_color="#30205F",
                    showarrow=False,
                    font_weight="bold"
                )
            ],
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            height=320,
            margin=dict(t=20, b=20, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#30205F"),
        )

        st.plotly_chart(fig)
