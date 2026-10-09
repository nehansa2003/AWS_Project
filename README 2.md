# Retail Customer Churn Prediction and Analytics

## Project Purpose
This project aims to understand why customers leave and identify those at higher risk of churn. It analyzes customer behavior, identifies churn factors, and develops predictive classification models to accurately forecast future churn.

## Dataset
The dataset contains approximately 100,000 retail customer records.

## Target Variable
The target variable is `churn_flag` (1 for Churn, 0 for No Churn).

## ML Models Evaluated
1. Logistic Regression
2. Random Forest
3. Extra Trees
4. Gradient Boosting
5. XGBoost

## Preprocessing
- **Numerical Features:** Median Imputation → Standard Scaling
- **Categorical Features:** Most Frequent Imputation → One-Hot Encoding
- Features like `customer_id` and `churn_risk` are explicitly excluded from modeling to prevent data leakage.

## Evaluation and Selection
Models are evaluated using Accuracy, Precision, Recall, F1 Score, and ROC-AUC. 
A 5-fold Stratified K-Fold cross-validation is performed. The final model is selected based on the highest **CV ROC-AUC** score.

## Project Structure
```
project_root/
├── notebooks/      # Original analysis notebook
├── data/           # Raw and processed datasets
├── src/            # Modularized Python source code (config, data processing, training, evaluation, inference)
├── models/         # Serialized model artifacts (.pkl)
├── outputs/        # Generated plots, reports, etc.
├── tests/          # Unit tests (to be implemented)
├── requirements.txt
├── .gitignore
└── README.md
```

## Future Extensions
This project is currently structured as a modular Python package. In the future, it will be extended with:
- **FastAPI:** To wrap the prediction logic into a production-ready REST API.
- **Docker:** To containerize the training and API environments for seamless deployment.
- **AWS:** To deploy the solution using AWS services.
