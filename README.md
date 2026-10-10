# ChurnIQ — Customer Churn Prediction and Intelligence Application

## Project Overview
ChurnIQ is a machine learning application designed to explore customer churn risk and predict whether customers are likely to leave based on their purchasing behavior, engagement, and other relevant attributes. The project combines a robust predictive machine learning model, a FastAPI backend for real-time predictions, and an interactive Streamlit web dashboard for customer intelligence.

## Key Features
- **Machine Learning Classification**: Evaluates multiple models (Logistic Regression, Random Forest, Extra Trees, Gradient Boosting) to accurately classify churn risk.
- **FastAPI Backend**: A RESTful API that serves the trained machine learning model and processes prediction requests in real-time.
- **Interactive Streamlit Dashboard**: 
  - **Overview**: A high-level dashboard displaying customer insights.
  - **Churn Prediction**: A dynamic interface to input customer details and instantly evaluate churn probability and risk.
  - **About**: Detailed context about the platform and its methodologies.

## Technologies and Libraries Used
- **Frontend**: Streamlit, Plotly
- **Backend API**: FastAPI, Uvicorn, Pydantic, HTTPX
- **Machine Learning & Data Processing**: Scikit-Learn, Pandas, NumPy, XGBoost, Joblib
- **Data Visualization**: Matplotlib, Seaborn

## Machine Learning Model and Prediction Workflow
1. **Preprocessing**: 
   - Numerical Features: Median Imputation followed by Standard Scaling.
   - Categorical Features: Most Frequent Imputation followed by One-Hot Encoding.
   - Irrelevant or leaky features (like `customer_id` and `churn_risk`) are explicitly excluded.
2. **Model Training and Selection**: 
   - Evaluated using Accuracy, Precision, Recall, F1 Score, and ROC-AUC with 5-fold Stratified K-Fold cross-validation.
   - The final model selected is **Logistic Regression** based on the highest CV ROC-AUC score.
3. **Prediction Workflow**: 
   - The best model is serialized as a `.pkl` file and loaded by the FastAPI application.
   - The Streamlit frontend sends customer data to the FastAPI `/predict` endpoint, which returns the predicted churn class and churn probability.

## Dataset Description
The dataset contains approximately 100,000 retail customer records. It includes 18 features detailing customer purchasing behavior and engagement. The target variable is `churn_flag` (1 for Churn, 0 for No Churn), with a distribution of 53,776 retained customers and 46,224 churned customers.

## Project Directory Structure
```text
project_root/
├── api/                  # FastAPI backend for real-time predictions
├── data/                 # Raw and processed customer datasets
├── frontend_streamlit/   # Streamlit UI web application
├── models/               # Serialized ML model artifacts (.pkl)
├── notebooks/            # Jupyter notebooks for EDA and model exploration
├── outputs/              # Validation outputs, generated plots, and reports
├── src/                  # Modular Python source code (data processing, training, etc.)
├── tests/                # Unit tests suite
├── requirements.txt      # Main project dependencies
├── README.md             # Project documentation
└── validation_output.json # JSON report of model evaluation metrics
```

## Prerequisites
- Python 3.8+
- Git

## Installation Instructions

1. **Clone the repository:**
   *(Note: Replace with your actual git clone command if your project is hosted on a remote repository)*
   ```bash
   git clone <repository-url>
   cd AWS_Project
   ```

2. **Set up a Python Virtual Environment:**
   Create and activate a virtual environment to manage dependencies cleanly.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   First, install the main backend and data processing dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Then, navigate to the frontend directory and install the UI dependencies:
   ```bash
   cd frontend_streamlit
   pip install -r requirements.txt
   cd ..
   ```

## Configuration and Environment Variables
By default, the Streamlit frontend communicates with the FastAPI backend at `http://localhost:8001`. You can configure this by setting the `CHURN_API_URL` environment variable before running the Streamlit app.
```bash
export CHURN_API_URL="http://localhost:8001"
```

## Running the Application

You need to run both the FastAPI backend and the Streamlit frontend concurrently.

1. **Start the FastAPI Backend:**
   From the root of the project, run:
   ```bash
   python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
   ```
   The API will be available at `http://localhost:8001`.

2. **Start the Streamlit Frontend:**
   Open a new terminal window, activate your virtual environment, navigate to the frontend directory, and run the app:
   ```bash
   source .venv/bin/activate
   cd frontend_streamlit
   streamlit run app.py
   ```
   The dashboard will open automatically in your browser (typically at `http://localhost:8501`).

## Usage Guide
1. Open the Streamlit dashboard in your web browser.
2. In the sidebar, ensure the **Backend URL** is pointing to your active FastAPI instance (e.g., `http://localhost:8001`) and click **Check API health** to verify the connection.
3. Use the **Navigation** menu to switch between pages:
   - **Overview**: Explore top-level metrics and general insights on the dataset.
   - **Churn Prediction**: Fill out the customer attribute form and click "Predict" to receive real-time churn probability and risk analysis.
   - **About**: Read the context, objective, and underlying technology of the ChurnIQ project.

## Model Evaluation Metrics
Based on the latest evaluation on the test set, the final **Logistic Regression** model achieved the following metrics:
- **Accuracy**: 94.59%
- **Precision**: 94.19%
- **Recall**: 94.10%
- **F1 Score**: 94.15%
- **ROC-AUC**: 99.04%

## Limitations and Future Improvements
- **Containerization**: Use Docker to containerize both the FastAPI backend and Streamlit frontend for seamless, uniform deployment.
- **Cloud Deployment**: Deploy the containerized solution using AWS services (e.g., ECS, SageMaker) or other cloud providers.
- **Feature Engineering**: Incorporate more granular behavioral data to further enhance prediction accuracy.
