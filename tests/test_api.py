from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"

def test_health_check():
    response = client.get("/health")
    # If the model is loaded properly, it returns 200. Otherwise 503.
    assert response.status_code in (200, 503)
    data = response.json()
    assert "model_loaded" in data

def test_predict_valid():
    valid_payload = {
        "age_group": "25-34",
        "gender": "Female",
        "region": "West",
        "customer_segment": "Loyal",
        "preferred_channel": "Online",
        "purchase_frequency": 12.0,
        "avg_order_value": 150.5,
        "total_spent": 1806.0,
        "recency_days": 15.0,
        "website_visits": 45.0,
        "discount_usage_rate": 0.2,
        "email_open_rate": 0.6,
        "cart_abandonment_rate": 0.1,
        "loyalty_score": 85.0,
        "engagement_score": 90.0
    }
    response = client.post("/predict", json=valid_payload)
    if response.status_code == 200:
        data = response.json()
        assert "predicted_churn" in data
        assert "churn_probability" in data
    else:
        # if model not loaded, it'll return 503.
        assert response.status_code == 503

def test_predict_missing_fields():
    invalid_payload = {
        "age_group": "25-34",
        # Missing many fields
    }
    response = client.post("/predict", json=invalid_payload)
    # FastAPI validation error
    assert response.status_code == 422

def test_predict_invalid_data_types():
    invalid_payload = {
        "age_group": "25-34",
        "gender": "Female",
        "region": "West",
        "customer_segment": "Loyal",
        "preferred_channel": "Online",
        "purchase_frequency": "not_a_number",  # Invalid type
        "avg_order_value": 150.5,
        "total_spent": 1806.0,
        "recency_days": 15.0,
        "website_visits": 45.0,
        "discount_usage_rate": 0.2,
        "email_open_rate": 0.6,
        "cart_abandonment_rate": 0.1,
        "loyalty_score": 85.0,
        "engagement_score": 90.0
    }
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422
