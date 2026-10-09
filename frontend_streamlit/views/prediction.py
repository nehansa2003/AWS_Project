
import plotly.graph_objects as go
import requests
import streamlit as st


# Replace these choices with the exact categories in your training dataset.
OPTIONS = {
    "age_group": ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
    "gender": ["Female", "Male", "Other", "Prefer not to say"],
    "region": [
        "Western", "Central", "Southern", "Northern", "Eastern",
        "North Western", "North Central", "Uva", "Sabaragamuwa",
    ],
    "customer_segment": [
        "New", "Regular", "Occasional", "Loyal", "Premium", "At Risk",
    ],
    "preferred_channel": [
        "Online", "In-store", "Mobile App", "Email", "Social Media",
    ],
}


def select_index(options, value):
    """Return a valid default index for a selectbox."""
    return options.index(value) if value in options else 0


def render(api_url):
    st.markdown("## 🎯 Customer churn prediction")
    st.write(
        "Enter the customer's information below, then submit it to your "
        "machine learning API."
    )

    st.markdown(
        '<div class="section-card"><h3>👤 Customer profile</h3>'
        '<p>Choose a category for each customer attribute.</p></div>',
        unsafe_allow_html=True,
    )

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
                index=select_index(OPTIONS["region"], "Western"),
            )
            customer_segment = st.selectbox(
                "Customer segment",
                OPTIONS["customer_segment"],
                index=select_index(OPTIONS["customer_segment"], "Regular"),
            )

        with c3:
            preferred_channel = st.selectbox(
                "Preferred channel",
                OPTIONS["preferred_channel"],
                index=select_index(OPTIONS["preferred_channel"], "Online"),
            )

        st.divider()
        st.markdown("### 🛒 Purchasing behaviour")

        c1, c2, c3 = st.columns(3)

        with c1:
            purchase_frequency = st.number_input(
                "Purchase frequency",
                min_value=0,
                value=2,
                step=1,
                help="Use the same time period as the training data.",
            )
            avg_order_value = st.number_input(
                "Average order value",
                min_value=0.0,
                value=3500.0,
                step=100.0,
                help="Use the currency and scale used by the training dataset.",
            )

        with c2:
            total_spent = st.number_input(
                "Total spent",
                min_value=0.0,
                value=7000.0,
                step=500.0,
            )
            recency_days = st.number_input(
                "Days since last purchase",
                min_value=0,
                value=90,
                step=1,
            )

        with c3:
            website_visits = st.number_input(
                "Website visits",
                min_value=0,
                value=2,
                step=1,
            )
            discount_usage_rate = st.slider(
                "Discount usage rate",
                min_value=0.0,
                max_value=1.0,
                value=0.1,
                step=0.05,
                help="This slider assumes the model uses rates between 0 and 1.",
            )

        st.divider()
        st.markdown("### 💌 Engagement and loyalty")
        st.caption(
            "Adjust the sliders and scores to describe the customer's "
            "engagement. Check the scale used in your training data."
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            email_open_rate = st.slider(
                "Email open rate",
                min_value=0.0,
                max_value=1.0,
                value=0.05,
                step=0.05,
            )

        with c2:
            cart_abandonment_rate = st.slider(
                "Cart abandonment rate",
                min_value=0.0,
                max_value=1.0,
                value=0.8,
                step=0.05,
            )

        with c3:
            loyalty_score = st.number_input(
                "Loyalty score",
                min_value=0.0,
                value=20.0,
                step=1.0,
            )
            engagement_score = st.number_input(
                "Engagement score",
                min_value=0.0,
                value=15.0,
                step=1.0,
            )

        st.divider()

        submitted = st.form_submit_button(
            "✨ Predict customer churn",
            type="primary",
            use_container_width=True,
        )

    if submitted:
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
                        "If this is a validation or category error, compare "
                        "the input categories and types with the model's "
                        "training data and API schema."
                    )
                    return

                result = response.json()
                predicted_churn = int(result["predicted_churn"])
                probability = float(result["churn_probability"])

                if predicted_churn not in (0, 1):
                    st.error("The API returned an unexpected predicted class.")
                    return

                if not 0 <= probability <= 1:
                    st.error("The API returned an invalid probability.")
                    return

                st.divider()
                st.markdown("## ✨ Prediction results")

                result_col, chart_col = st.columns([1, 1], gap="large")

                with result_col:
                    if predicted_churn == 1:
                        st.markdown(
                            """
                            <div class="risk-high">
                                <h3>⚠️ Likely to churn</h3>
                                <p>The model returned predicted class 1.</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            """
                            <div class="risk-low">
                                <h3>✅ Unlikely to churn</h3>
                                <p>The model returned predicted class 0.</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    st.metric("Churn probability", f"{probability:.2%}")
                    st.progress(probability)
                    st.caption(
                        "This is a model estimate, not a guarantee of future "
                        "customer behaviour."
                    )

                with chart_col:
                    fig = go.Figure(
                        go.Pie(
                            labels=["Churn probability", "Remaining probability"],
                            values=[probability, 1 - probability],
                            hole=0.68,
                            marker=dict(
                                colors=["#8B5CF6", "#DDE5FF"],
                                line=dict(color="#FFFFFF", width=3),
                            ),
                            textinfo="none",
                        )
                    )

                    fig.update_layout(
                        title="Predicted risk",
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
                        margin=dict(t=60, b=20, l=10, r=10),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#30205F"),
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with st.expander("View submitted customer information"):
                    st.json(customer)

                with st.expander("View raw API response"):
                    st.json(result)

            except requests.RequestException as exc:
                st.error(f"Could not reach the prediction API: {exc}")
                st.info(
                    "Make sure Docker is running and the backend URL is correct."
                )
            except (KeyError, TypeError, ValueError) as exc:
                st.error(f"The API returned an unexpected response: {exc}")