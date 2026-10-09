"""
Prediction logic for serving the trained pipeline.
Extracted from: original notebook 'Deployment -Ready Prediction Function' section.
"""

import pandas as pd
import joblib
import os
from src.config import MODEL_OUTPUT_PATH

def load_saved_model(model_path: str = MODEL_OUTPUT_PATH):
    """Loads the serialized pipeline from disk."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Train the model first.")
    return joblib.load(model_path)

def predict_customer_churn(customer_data: pd.DataFrame, model=None) -> pd.DataFrame:
    """
    Predict churn for a batch of customers.
    Extracted from: 'Deployment -Ready Prediction Function' section.
    """
    if model is None:
        model = load_saved_model()
        
    prediction = model.predict(customer_data)
    probability = model.predict_proba(customer_data)[:, 1]
    
    result = customer_data.copy()
    result["predicted_churn"] = prediction
    result["churn_probability"] = probability
    
    return result
