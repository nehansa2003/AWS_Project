# --- Markdown 0 ---
#Business Understanding


# --- Markdown 1 ---
project tilte


# --- Cell 2 ---
# ============================================================
# CUSTOMER CHURN PREDICTION AND ANALYTICS
# Data Science Project
# ============================================================

PROJECT_NAME = "Retail Customer Churn Prediction and Analytics"

print(PROJECT_NAME)
print("=" * 60)


# --- Markdown 3 ---
##Business problem


# --- Cell 4 ---
business_problem = """
A retail company wants to understand why customers leave and
identify customers who are at higher risk of churn.

The objective is to analyze customer behavior, identify factors
associated with churn, develop predictive classification models,
compare multiple models, and select the best reliable model
for future churn prediction.
"""

print(business_problem)


# --- Markdown 5 ---
##Project objectives


# --- Cell 6 ---
objectives = [
    "Understand customer characteristics and churn behavior",
    "Identify data quality issues",
    "Perform exploratory data analysis",
    "Identify factors associated with customer churn",
    "Prepare data for machine learning",
    "Train and compare five classification models",
    "Select the best model using suitable evaluation metrics",
    "Explain the important drivers of churn",
    "Save the final model for deployment"
]

for i, objective in enumerate(objectives, 1):
    print(f"{i}. {objective}")


# --- Markdown 7 ---
#Data collection


# --- Markdown 8 ---
import libraries


# --- Cell 9 ---
# Data manipulation
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Machine learning
from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_validate,
    RandomizedSearchCV
)

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

from sklearn.impute import SimpleImputer

# Models
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay,
    RocCurveDisplay
)

# Model saving
import joblib

# Utilities
import warnings
warnings.filterwarnings("ignore")

print("Libraries imported successfully.")


# --- Markdown 10 ---
Upload dataset to colab


# --- Cell 11 ---
from google.colab import files

uploaded = files.upload()

print("Uploaded files:")
for filename in uploaded.keys():
    print(filename)


# --- Markdown 12 ---
Load dataset


# --- Cell 13 ---
import io

filename = list(uploaded.keys())[0]

df = pd.read_csv(io.BytesIO(uploaded[filename]))

print("Dataset loaded successfully.")
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")


# --- Markdown 14 ---
#Data Understanding


# --- Markdown 15 ---
##First records


# --- Cell 16 ---
df.head()


# --- Markdown 17 ---
##Last records


# --- Cell 18 ---
df.tail()


# --- Markdown 19 ---
##Dataset dimentions


# --- Cell 20 ---
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])


# --- Markdown 21 ---
##Column names


# --- Cell 22 ---
for i, column in enumerate(df.columns, 1):
    print(f"{i:02d}. {column}")


# --- Markdown 23 ---
##Data types


# --- Cell 24 ---
df.dtypes


# --- Markdown 25 ---
##Dataset information


# --- Cell 26 ---
df.info()


# --- Markdown 27 ---
# Data Quality


# --- Markdown 28 ---
##Mising values


# --- Cell 29 ---
missing = pd.DataFrame({
    "Missing_Count": df.isnull().sum(),
    "Missing_Percentage": df.isnull().mean() * 100
})

missing = missing.sort_values(
    "Missing_Count",
    ascending=False
)

missing


# --- Markdown 30 ---
##Duplicate rows


# --- Cell 31 ---
duplicate_count = df.duplicated().sum()

print("Duplicate rows:", duplicate_count)


# --- Markdown 32 ---
##Duplicate customer IDs


# --- Cell 33 ---
duplicate_customer_ids = df["customer_id"].duplicated().sum()

print("Duplicate customer IDs:", duplicate_customer_ids)


# --- Markdown 34 ---
##Uniqe values


# --- Cell 35 ---
unique_summary = pd.DataFrame({
    "Column": df.columns,
    "Unique Values": [df[col].nunique() for col in df.columns]
})

unique_summary


# --- Markdown 36 ---
##Categorical values


# --- Cell 37 ---
categorical_columns = df.select_dtypes(
    include=["object"]
).columns

for column in categorical_columns:
    print("\n" + "=" * 50)
    print(column)
    print(df[column].value_counts())


# --- Markdown 38 ---
#Target Analysis


# --- Markdown 39 ---
##Churn distribution


# --- Cell 40 ---
print(df["churn_flag"].value_counts())

print("\nPercentage:")
print(
    df["churn_flag"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)


# --- Markdown 41 ---
##Churn visualization


# --- Cell 42 ---
plt.figure(figsize=(7, 5))

sns.countplot(
    data=df,
    x="churn_flag"
)

plt.title("Customer Churn Distribution")
plt.xlabel("Churn Flag")
plt.ylabel("Number of Customers")

plt.show()


# --- Markdown 43 ---
#Data Leakage Check


# --- Markdown 44 ---
##Investigate Churn risk


# --- Cell 45 ---
risk_churn = pd.crosstab(
    df["churn_risk"],
    df["churn_flag"],
    normalize="index"
) * 100

risk_churn.round(2)


# --- Markdown 46 ---
##Visualize leakage


# --- Cell 47 ---
plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="churn_risk",
    hue="churn_flag"
)

plt.title("Churn Risk vs Actual Churn")
plt.xlabel("Churn Risk")
plt.ylabel("Number of Customers")

plt.show()


# --- Markdown 48 ---
Explain leakage


# --- Cell 49 ---
print("""
DATA LEAKAGE DECISION
---------------------

The feature 'churn_risk' will NOT be used for machine learning.

Reason:
It has an almost direct relationship with the target 'churn_flag'.
Using it would allow the model to indirectly see the answer.

Therefore:
    churn_risk → excluded from predictive features

This produces a more realistic and defensible machine learning model.
""")


# --- Markdown 50 ---
#EDA


# --- Markdown 51 ---
#Numarical columns


# --- Cell 52 ---
numerical_columns = df.select_dtypes(
    include=np.number
).columns.tolist()

print(numerical_columns)


# --- Markdown 53 ---
##Numerical distribution


# --- Cell 54 ---
df[numerical_columns].hist(
    figsize=(18, 14),
    bins=30
)

plt.tight_layout()
plt.show()


# --- Markdown 55 ---
##Chuurn vs recency


# --- Cell 56 ---
plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="churn_flag",
    y="recency_days"
)

plt.title("Recency Days vs Churn")
plt.xlabel("Churn")
plt.ylabel("Recency Days")

plt.show()


# --- Markdown 57 ---
#Churn vs purchase frequency


# --- Cell 58 ---
plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="churn_flag",
    y="purchase_frequency"
)

plt.title("Purchase Frequency vs Churn")
plt.show()


# --- Markdown 59 ---
#Churn vs loyalty


# --- Cell 60 ---
plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="churn_flag",
    y="loyalty_score"
)

plt.title("Loyalty Score vs Churn")
plt.show()


# --- Markdown 61 ---
#Churn vs Engagement



# --- Cell 62 ---
plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="churn_flag",
    y="engagement_score"
)

plt.title("Engagement Score vs Churn")
plt.show()


# --- Markdown 63 ---
#Churn by customer segment


# --- Cell 64 ---
segment_churn = pd.crosstab(
    df["customer_segment"],
    df["churn_flag"],
    normalize="index"
) * 100

segment_churn.round(2)


# --- Markdown 65 ---
##Coustomer segment visualization


# --- Cell 66 ---
plt.figure(figsize=(9, 5))

sns.barplot(
    data=df,
    x="customer_segment",
    y="churn_flag"
)

plt.title("Average Churn Rate by Customer Segment")
plt.ylabel("Churn Rate")

plt.show()


# --- Markdown 67 ---
##Churn by preferred channel


# --- Cell 68 ---
channel_churn = pd.crosstab(
    df["preferred_channel"],
    df["churn_flag"],
    normalize="index"
) * 100

channel_churn.round(2)


# --- Markdown 69 ---
##Channel visualization


# --- Cell 70 ---
plt.figure(figsize=(9, 5))

sns.barplot(
    data=df,
    x="preferred_channel",
    y="churn_flag"
)

plt.title("Churn Rate by Preferred Channel")
plt.ylabel("Churn Rate")

plt.show()


# --- Markdown 71 ---
#Region visualiation


# --- Cell 72 ---
plt.figure(figsize=(9, 5))

sns.barplot(
    data=df,
    x="region",
    y="churn_flag"
)

plt.title("Churn Rate by Region")
plt.ylabel("Churn Rate")

plt.show()


# --- Markdown 73 ---
##Correlation matrix


# --- Cell 74 ---
correlation = df[numerical_columns].corr()

plt.figure(figsize=(12, 8))

sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)

plt.title("Numerical Feature Correlation Matrix")

plt.show()


# --- Markdown 75 ---
#Churn Characteristics


# --- Markdown 76 ---
##Numerical comparison by churn


# --- Cell 77 ---
churn_comparison = df.groupby(
    "churn_flag"
)[numerical_columns].mean().T

churn_comparison


# --- Markdown 78 ---
#Data Preparation


# --- Markdown 79 ---
#Creating modeling dataset


# --- Cell 80 ---
model_df = df.copy()

# Remove customer identifier
# Remove churn_risk because it causes target leakage
model_df = model_df.drop(
    columns=[
        "customer_id",
        "churn_risk"
    ]
)

print("Original shape:", df.shape)
print("Modeling shape:", model_df.shape)


# --- Markdown 81 ---
#Seperate X and y


# --- Cell 82 ---
X = model_df.drop(
    columns=["churn_flag"]
)

y = model_df["churn_flag"]

print("X shape:", X.shape)
print("y shape:", y.shape)


# --- Markdown 83 ---
##Identify feature types


# --- Cell 84 ---
categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()

numerical_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

print("Categorical features:")
print(categorical_features)

print("\nNumerical features:")
print(numerical_features)


# --- Markdown 85 ---
#Train  & Split


# --- Markdown 86 ---
##split dataset


# --- Cell 87 ---
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", X_train.shape[0])
print("Testing samples :", X_test.shape[0])


# --- Markdown 88 ---
#Preprocessing Pipeline


# --- Markdown 89 ---
##Create preporcessing pipeline


# --- Cell 90 ---
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
        (
            "num",
            numeric_pipeline,
            numerical_features
        ),
        (
            "cat",
            categorical_pipeline,
            categorical_features
        )
    ]
)

print("Preprocessing pipeline created.")


# --- Markdown 91 ---
#Five ML Models
1. Logistic Regression
2. Random Forest
3. Extra Trees
4. Gradient Boosting
5. XGBoost



# --- Cell 92 ---
!pip -q install xgboost


# --- Cell 93 ---
from xgboost import XGBClassifier

print("XGBoost imported successfully.")


# --- Markdown 94 ---
##Define Models


# --- Markdown 95 ---
##Five models


# --- Cell 96 ---
models = {

    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),

    "Extra Trees": ExtraTreesClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=5,
        random_state=42
    ),

    "XGBoost": XGBClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1
    )
}

print("Number of models:", len(models))


# --- Markdown 97 ---
#Create ML Pipelines


# --- Cell 98 ---
pipelines = {}

for name, model in models.items():

    pipelines[name] = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

print("All model pipelines created.")


# --- Markdown 99 ---
#Train five Models


# --- Cell 100 ---
trained_models = {}

for name, pipeline in pipelines.items():

    print(f"\nTraining: {name}")

    pipeline.fit(
        X_train,
        y_train
    )

    trained_models[name] = pipeline

    print(f"{name} completed.")


# --- Markdown 101 ---
#Model Evaluation


# --- Markdown 102 ---
##Evaluation function


# --- Cell 103 ---
def evaluate_model(model, X_test, y_test):

    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]

    return {
        "Accuracy": accuracy_score(
            y_test,
            predictions
        ),

        "Precision": precision_score(
            y_test,
            predictions
        ),

        "Recall": recall_score(
            y_test,
            predictions
        ),

        "F1 Score": f1_score(
            y_test,
            predictions
        ),

        "ROC-AUC": roc_auc_score(
            y_test,
            probabilities
        )
    }


# --- Markdown 104 ---
##Evaluate all five


# --- Cell 105 ---
results = []

for name, model in trained_models.items():

    metrics = evaluate_model(
        model,
        X_test,
        y_test
    )

    metrics["Model"] = name

    results.append(metrics)

results_df = pd.DataFrame(results)

results_df = results_df[
    [
        "Model",
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC"
    ]
]

results_df.sort_values(
    "ROC-AUC",
    ascending=False
)


# --- Markdown 106 ---
#Visual Model Comparison


# --- Markdown 107 ---
##Compare models


# --- Cell 108 ---
comparison = results_df.set_index("Model")

comparison.plot(
    kind="bar",
    figsize=(14, 7)
)

plt.title("Performance Comparison of Five Classification Models")
plt.ylabel("Score")
plt.ylim(0, 1)

plt.xticks(rotation=30)

plt.legend(
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

plt.tight_layout()
plt.show()


# --- Markdown 109 ---
#F1 Score comparison


# --- Cell 110 ---
plt.figure(figsize=(10, 6))

sns.barplot(
    data=results_df.sort_values(
        "F1 Score",
        ascending=False
    ),
    x="F1 Score",
    y="Model"
)

plt.title("F1 Score Comparison")
plt.xlim(0, 1)

plt.show()


# --- Markdown 111 ---
#ROC AUC Comparison


# --- Cell 112 ---
plt.figure(figsize=(10, 6))

sns.barplot(
    data=results_df.sort_values(
        "ROC-AUC",
        ascending=False
    ),
    x="ROC-AUC",
    y="Model"
)

plt.title("ROC-AUC Comparison")
plt.xlim(0, 1)

plt.show()


# --- Markdown 113 ---
#Cross Validation


# --- Markdown 114 ---
5 flod cross validation


# --- Cell 115 ---
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

cv_results = []

for name, pipeline in pipelines.items():

    print(f"Cross-validating: {name}")

    scores = cross_validate(
        pipeline,
        X,
        y,
        cv=cv,
        scoring=[
            "accuracy",
            "precision",
            "recall",
            "f1",
            "roc_auc"
        ],
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

cv_df = pd.DataFrame(cv_results)

cv_df.sort_values(
    "CV ROC-AUC",
    ascending=False
)


# --- Markdown 116 ---
#Final Model Selection


# --- Cell 117 ---
final_comparison = results_df.merge(
    cv_df,
    on="Model"
)

final_comparison.sort_values(
    "CV ROC-AUC",
    ascending=False
)


# --- Markdown 118 ---
##Select best model


# --- Cell 119 ---
best_model_name = (
    final_comparison
    .sort_values(
        "CV ROC-AUC",
        ascending=False
    )
    .iloc[0]["Model"]
)

best_model = trained_models[
    best_model_name
]

print("Best Model:")
print(best_model_name)


# --- Markdown 120 ---
#Confution Metrix


# --- Cell 121 ---
y_pred = best_model.predict(X_test)

cm = confusion_matrix(
    y_test,
    y_pred
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm
)

disp.plot()

plt.title(
    f"Confusion Matrix - {best_model_name}"
)

plt.show()


# --- Markdown 122 ---
#Classification Report


# --- Cell 123 ---
print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "No Churn",
            "Churn"
        ]
    )
)


# --- Markdown 124 ---
#ROC curves for all 5 models


# --- Cell 125 ---
plt.figure(figsize=(10, 7))

for name, model in trained_models.items():

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    from sklearn.metrics import roc_curve

    fpr, tpr, _ = roc_curve(
        y_test,
        probabilities
    )

    auc = roc_auc_score(
        y_test,
        probabilities
    )

    plt.plot(
        fpr,
        tpr,
        label=f"{name} (AUC={auc:.3f})"
    )

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title("ROC Curves - Five Classification Models")

plt.legend()

plt.show()


# --- Markdown 126 ---
#Feature Importance


# --- Cell 127 ---
model_step = best_model.named_steps["model"]

if hasattr(model_step, "feature_importances_"):

    importances = model_step.feature_importances_

    print("Feature importance available.")

else:

    print(
        "The selected model does not provide "
        "feature_importances_ directly."
    )


# --- Markdown 128 ---
##Get feature names


# --- Cell 129 ---
preprocessor_fitted = (
    best_model
    .named_steps["preprocessor"]
)

feature_names = (
    preprocessor_fitted
    .get_feature_names_out()
)

print("Number of processed features:")
print(len(feature_names))


# --- Markdown 130 ---
##Feature importance table


# --- Cell 131 ---
if hasattr(model_step, "feature_importances_"):

    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    })

    importance_df = importance_df.sort_values(
        "Importance",
        ascending=False
    )

    importance_df.head(20)


# --- Markdown 132 ---
#Business Insights


# --- Markdown 133 ---
##Automatically identify high churn groups


# --- Cell 134 ---
def churn_rate_table(data, column):

    result = (
        data.groupby(column)["churn_flag"]
        .agg(
            Customers="count",
            Churn_Rate="mean"
        )
        .sort_values(
            "Churn_Rate",
            ascending=False
        )
    )

    result["Churn_Rate"] *= 100

    return result.round(2)


# --- Markdown 135 ---
##Segment insights


# --- Cell 136 ---
churn_rate_table(
    df,
    "customer_segment"
)


# --- Markdown 137 ---
##Channel insights



# --- Cell 138 ---
churn_rate_table(
    df,
    "preferred_channel"
)


# --- Markdown 139 ---
##Region insights


# --- Cell 140 ---
churn_rate_table(
    df,
    "region"
)


# --- Markdown 141 ---
##Age insights


# --- Cell 142 ---
churn_rate_table(
    df,
    "age_group"
)


# --- Markdown 143 ---
#High Risk Customer Analysis



# --- Cell 144 ---
test_results = X_test.copy()

test_results["actual_churn"] = y_test.values
test_results["predicted_churn"] = y_pred

test_results.head()


# --- Markdown 145 ---
#Save Processed Data


# --- Cell 146 ---
processed_data = model_df.copy()

processed_data.to_csv(
    "processed_customer_churn.csv",
    index=False
)

print(
    "Processed dataset saved successfully."
)


# --- Markdown 147 ---
#Save Best Model


# --- Cell 148 ---
joblib.dump(
    best_model,
    "best_customer_churn_model.pkl"
)

print(
    f"Saved model: {best_model_name}"
)


# --- Markdown 149 ---
#Save model information


# --- Cell 150 ---
model_information = {
    "model_name": best_model_name,
    "target": "churn_flag",
    "excluded_features": [
        "customer_id",
        "churn_risk"
    ],
    "training_rows": len(X_train),
    "testing_rows": len(X_test),
    "selection_metric": "CV ROC-AUC"
}

model_information


# --- Markdown 151 ---
#Deployment -Ready Prediction Function


# --- Cell 152 ---
def predict_customer_churn(
    customer_data,
    model=best_model
):

    prediction = model.predict(
        customer_data
    )

    probability = model.predict_proba(
        customer_data
    )[:, 1]

    result = customer_data.copy()

    result["predicted_churn"] = prediction
    result["churn_probability"] = probability

    return result


# --- Markdown 153 ---
#Test One customer


# --- Cell 154 ---
sample_customer = X_test.iloc[[0]]

prediction_result = predict_customer_churn(
    sample_customer
)

prediction_result


# --- Markdown 155 ---
#Test Multiple customers


# --- Cell 156 ---
sample_customers = X_test.head(10)

predictions = predict_customer_churn(
    sample_customers
)

predictions[
    [
        "predicted_churn",
        "churn_probability"
    ]
]


# --- Markdown 157 ---
#Download Model


# --- Cell 158 ---
from google.colab import files

files.download(
    "best_customer_churn_model.pkl"
)


# --- Markdown 159 ---
#Download preprocessed data


# --- Cell 160 ---
files.download(
    "processed_customer_churn.csv"
)


# --- Cell 161 ---



