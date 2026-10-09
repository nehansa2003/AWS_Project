"""
Configuration settings for the Retail Customer Churn Prediction project.
Extracted from: original notebook 'Data Preparation' and 'Final Model Selection' sections.
"""

import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

# File Paths
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw", "retail_customer_churn_100k (1).csv")
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed", "processed_customer_churn.csv")
MODEL_OUTPUT_PATH = os.path.join(MODELS_DIR, "best_customer_churn_model.pkl")

# ML Configuration
RANDOM_STATE = 42
TEST_SIZE = 0.20
N_SPLITS = 5

# Feature definitions
TARGET = "churn_flag"
EXCLUDED_FEATURES = ["customer_id", "churn_risk"]

CATEGORICAL_FEATURES = [
    "age_group",
    "gender",
    "region",
    "customer_segment",
    "preferred_channel"
]

NUMERICAL_FEATURES = [
    "purchase_frequency",
    "avg_order_value",
    "total_spent",
    "recency_days",
    "website_visits",
    "discount_usage_rate",
    "email_open_rate",
    "cart_abandonment_rate",
    "loyalty_score",
    "engagement_score"
]
