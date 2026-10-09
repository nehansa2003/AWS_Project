"""
Data Processing module.
Extracted from: original notebook 'Data Preparation' section (cells 78-84).
"""

import pandas as pd
import sys
from src.config import TARGET, EXCLUDED_FEATURES

def load_data(file_path: str) -> pd.DataFrame:
    """Load the raw dataset from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

def validate_data(df: pd.DataFrame) -> bool:
    """Basic validation to ensure required columns are present."""
    required_columns = EXCLUDED_FEATURES + [TARGET]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        print(f"Missing essential columns: {missing_cols}")
        return False
    return True

def prepare_model_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare dataset for modeling by removing identifier and leaky features.
    Extracted from: 'Creating modeling dataset' cell in notebook.
    """
    model_df = df.copy()
    
    # Drop features like customer_id and churn_risk to prevent leakage
    cols_to_drop = [col for col in EXCLUDED_FEATURES if col in model_df.columns]
    model_df = model_df.drop(columns=cols_to_drop)
    
    return model_df

def split_features_target(model_df: pd.DataFrame):
    """Separate features (X) and target (y)."""
    X = model_df.drop(columns=[TARGET])
    y = model_df[TARGET]
    return X, y
