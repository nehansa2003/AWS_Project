"""
Model Training module.
Extracted from: original notebook 'Preprocessing Pipeline', 'Five ML Models', 'Train five Models', and 'Cross Validation' sections.
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier

from src.config import (
    NUMERICAL_FEATURES, CATEGORICAL_FEATURES, RANDOM_STATE, 
    TEST_SIZE, N_SPLITS, MODEL_OUTPUT_PATH
)

def build_preprocessing_pipeline() -> ColumnTransformer:
    """
    Builds the preprocessing pipeline exactly as in the notebook.
    Extracted from: 'Create preporcessing pipeline' section.
    """
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                )
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERICAL_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES)
        ]
    )
    return preprocessor

def get_models() -> dict:
    """
    Returns the five classification models with their original hyperparameters.
    Extracted from: 'Five models' section.
    """
    return {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            random_state=RANDOM_STATE
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            random_state=RANDOM_STATE,
            n_jobs=-1
        ),
        "Extra Trees": ExtraTreesClassifier(
            n_estimators=300,
            random_state=RANDOM_STATE,
            n_jobs=-1
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=5,
            random_state=RANDOM_STATE
        ),
        "XGBoost": XGBClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=RANDOM_STATE,
            n_jobs=-1
        )
    }

def perform_cross_validation(pipelines: dict, X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
    """
    Performs 5-fold Stratified K-Fold cross validation on all models.
    Extracted from: 'Cross Validation' section.
    """
    cv = StratifiedKFold(
        n_splits=N_SPLITS,
        shuffle=True,
        random_state=RANDOM_STATE
    )

    cv_results = []
    
    for name, pipeline in pipelines.items():
        print(f"Cross-validating: {name}")
        scores = cross_validate(
            pipeline,
            X,
            y,
            cv=cv,
            scoring=["accuracy", "precision", "recall", "f1", "roc_auc"],
            n_jobs=-1
        )

        cv_results.append({
            "Model": name,
            "CV Accuracy": scores["test_accuracy"].mean(),
            "CV Precision": scores["test_precision"].mean(),
            "CV Recall": scores["test_recall"].mean(),
            "CV F1": scores["test_f1"].mean(),
            "CV ROC-AUC": scores["test_roc_auc"].mean()
        })

    return pd.DataFrame(cv_results)

def train_and_select_best_model(X: pd.DataFrame, y: pd.Series):
    """
    Splits data, creates pipelines, cross-validates, and selects the best model.
    Extracted from: 'Train five Models' and 'Final Model Selection' sections.
    """
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    preprocessor = build_preprocessing_pipeline()
    models = get_models()
    
    pipelines = {}
    for name, model in models.items():
        pipelines[name] = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])

    trained_pipelines = {}
    for name, pipeline in pipelines.items():
        print(f"Training: {name}")
        pipeline.fit(X_train, y_train)
        trained_pipelines[name] = pipeline

    cv_df = perform_cross_validation(pipelines, X, y)
    
    # Select best model by highest CV ROC-AUC
    best_model_name = cv_df.sort_values("CV ROC-AUC", ascending=False).iloc[0]["Model"]
    print(f"Best Model Selected: {best_model_name}")
    
    best_pipeline = trained_pipelines[best_model_name]
    
    return best_pipeline, cv_df, X_test, y_test, best_model_name

def save_model(pipeline, output_path=MODEL_OUTPUT_PATH):
    """Saves the pipeline to disk."""
    joblib.dump(pipeline, output_path)
    print(f"Saved model to {output_path}")
