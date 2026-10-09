from pydantic import BaseModel, Field

class CustomerData(BaseModel):
    # Categorical features
    age_group: str = Field(..., description="Age group of the customer")
    gender: str = Field(..., description="Gender of the customer")
    region: str = Field(..., description="Region of the customer")
    customer_segment: str = Field(..., description="Customer segment (e.g., Loyal, VIP)")
    preferred_channel: str = Field(..., description="Preferred communication/shopping channel")
    
    # Numerical features
    purchase_frequency: float = Field(..., description="Frequency of purchases")
    avg_order_value: float = Field(..., description="Average value of orders")
    total_spent: float = Field(..., description="Total amount spent")
    recency_days: float = Field(..., description="Days since last purchase")
    website_visits: float = Field(..., description="Number of website visits")
    discount_usage_rate: float = Field(..., description="Rate of discount usage")
    email_open_rate: float = Field(..., description="Rate of email opens")
    cart_abandonment_rate: float = Field(..., description="Rate of cart abandonment")
    loyalty_score: float = Field(..., description="Customer loyalty score")
    engagement_score: float = Field(..., description="Customer engagement score")

class PredictionResponse(BaseModel):
    predicted_churn: int
    churn_probability: float
