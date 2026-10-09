"""
Model Evaluation module.
Extracted from: original notebook 'Model Evaluation', 'Confution Metrix', 'Classification Report' and 'ROC curves for all 5 models' sections.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report, ConfusionMatrixDisplay, roc_curve
)

def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """
    Evaluates a single model returning standard metrics.
    Extracted from: 'Evaluation function' section.
    """
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    return {
        "Accuracy": accuracy_score(y_test, predictions),
        "Precision": precision_score(y_test, predictions),
        "Recall": recall_score(y_test, predictions),
        "F1 Score": f1_score(y_test, predictions),
        "ROC-AUC": roc_auc_score(y_test, probabilities)
    }

def generate_classification_report(model, X_test: pd.DataFrame, y_test: pd.Series):
    """
    Prints the classification report.
    Extracted from: 'Classification Report' section.
    """
    predictions = model.predict(X_test)
    report = classification_report(y_test, predictions, target_names=["No Churn", "Churn"])
    print(report)
    return report

def plot_confusion_matrix(model, X_test: pd.DataFrame, y_test: pd.Series, model_name: str, save_path: str = None):
    """
    Plots the confusion matrix.
    Extracted from: 'Confution Metrix' section.
    """
    predictions = model.predict(X_test)
    cm = confusion_matrix(y_test, predictions)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.title(f"Confusion Matrix - {model_name}")
    if save_path:
        plt.savefig(save_path)
    plt.close()

def plot_roc_curves(trained_models: dict, X_test: pd.DataFrame, y_test: pd.Series, save_path: str = None):
    """
    Plots ROC curves for all models.
    Extracted from: 'ROC curves for all 5 models' section.
    """
    plt.figure(figsize=(10, 7))
    for name, model in trained_models.items():
        probabilities = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, probabilities)
        auc = roc_auc_score(y_test, probabilities)
        plt.plot(fpr, tpr, label=f"{name} (AUC={auc:.3f})")
        
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curves - Five Classification Models")
    plt.legend()
    if save_path:
        plt.savefig(save_path)
    plt.close()
