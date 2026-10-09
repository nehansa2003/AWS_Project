import sys
import os
import json
import pandas as pd
from unittest.mock import MagicMock

# Mock xgboost before importing our modules to avoid libomp crash on Mac
sys.modules['xgboost'] = MagicMock()

try:
    from src.config import *
    from src.data_processor import load_data, validate_data, prepare_model_data, split_features_target
    from src.model_trainer import build_preprocessing_pipeline, perform_cross_validation, train_and_select_best_model
    from src.evaluate import evaluate_model
    from src.predict import predict_customer_churn
    import src.model_trainer as mt
except Exception as e:
    print(f"Error importing src modules: {e}")

def run_validation():
    results = {}
    
    # Task 1: Verify Data
    df = load_data(RAW_DATA_PATH)
    results['data'] = {
        'rows': df.shape[0],
        'cols': df.shape[1],
        'target_col': TARGET,
        'missing': int(df.isnull().sum().sum()),
        'duplicate_rows': int(df.duplicated().sum()),
        'duplicate_customer_ids': int(df['customer_id'].duplicated().sum()),
        'target_dist': df[TARGET].value_counts().to_dict()
    }
    
    # Task 5 & 6: Run Training Pipeline
    try:
        model_df = prepare_model_data(df)
        X, y = split_features_target(model_df)
        
        # Remove XGBoost from the get_models dict dynamically for this run
        original_get_models = mt.get_models
        def new_get_models():
            models = original_get_models()
            if "XGBoost" in models:
                del models["XGBoost"]
            return models
        mt.get_models = new_get_models
            
        best_pipeline, cv_df, X_test, y_test, best_model_name = train_and_select_best_model(X, y)
        
        # Record CV results
        cv_results = cv_df.set_index("Model").to_dict(orient="index")
        
        # Re-evaluate all trained pipelines to get test metrics
        test_results = {}
        models = mt.get_models()
        preprocessor = build_preprocessing_pipeline()
        
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
        )
        
        for name, model in models.items():
            pipe = mt.Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
            pipe.fit(X_train, y_train)
            test_results[name] = evaluate_model(pipe, X_test, y_test)
            
        results['cv_results'] = cv_results
        results['test_results'] = test_results
        results['best_model'] = best_model_name
            
    except Exception as e:
        import traceback
        results['training_error'] = traceback.format_exc()
        
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    run_validation()
