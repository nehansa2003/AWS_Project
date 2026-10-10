# ChurnIQ — Customer Churn Prediction and Intelligence Application

## Project Overview
ChurnIQ is a machine learning application designed to explore customer churn risk and predict whether customers are likely to leave based on their purchasing behavior, engagement, and other relevant attributes. The project combines a robust predictive machine learning model, a FastAPI backend for real-time predictions, and an interactive, professionally-designed Streamlit web dashboard for customer intelligence.

## Key Features
- **Machine Learning Classification**: Accurately classifies churn risk using a validated machine learning pipeline.
- **FastAPI Backend**: A highly performant RESTful API that serves the trained machine learning model and securely processes prediction requests in real-time.
- **Interactive Streamlit Dashboard**: 
  - **Overview**: A dashboard displaying system architecture, application workflows, and feature groups.
  - **Churn Prediction**: A dynamic, column-based interface to input 15 customer details (demographics, purchasing behavior, and engagement) to instantly evaluate churn probability.
  - **About**: Detailed context about the platform's objectives, dataset, technologies, and responsible use limitations.

## Technologies and Tools Used
- **Frontend**: Streamlit, Plotly, Custom CSS styling
- **Backend API**: FastAPI, Uvicorn, Pydantic
- **Machine Learning & Data Processing**: Scikit-Learn, Pandas, NumPy, XGBoost, Joblib
- **Data Visualization**: Matplotlib, Seaborn

## System Architecture and Frontend/Backend Interaction
1. **Model Deployment**: 
   - The best trained model (Logistic Regression) is serialized as a `.pkl` artifact.
   - The FastAPI backend loads this model automatically upon startup.
2. **Prediction Workflow**: 
   - The Streamlit frontend captures user input through a polished, intuitive form.
   - When the user clicks **Predict Customer Churn Risk**, the frontend makes a POST request sending a JSON payload to the FastAPI `/predict` endpoint.
   - The backend validates the input using Pydantic, converts it into a Pandas DataFrame, and executes the machine learning pipeline.
   - The API returns a JSON response containing the `predicted_churn` (0 or 1) and `churn_probability`.
   - The frontend renders these results dynamically with interactive Plotly donut charts and colored risk alert panels.

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
├── requirements.txt      # Main backend project dependencies
├── README.md             # Project documentation
└── validation_output.json # JSON report of model evaluation metrics
```

## Prerequisites
- Python 3.8+
- Git

## Installation and Setup Instructions

1. **Clone the repository:**
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
   The API will be available at `http://localhost:8001`. The health check endpoint is at `http://localhost:8001/health`.

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
2. Ensure both the FastAPI backend and Streamlit frontend are running. Streamlit automatically connects to the backend API defined by the `CHURN_API_URL` environment variable.
3. Use the **Navigation** menu in the sidebar to switch between pages:
   - **Overview**: Explore the system architecture, workflow instructions, and feature category breakdown.
   - **Churn Prediction**: Fill out the customer attribute form (demographics, purchasing behavior, and engagement) and click "Predict Customer Churn Risk" to receive real-time churn probability and visual risk analysis.
   - **About**: Read the context, dataset overview, limitations, and underlying technology stack of the ChurnIQ project.

## Model Evaluation Metrics
Based on the latest evaluation on the test set, the final **Logistic Regression** model achieved the following metrics:
- **Accuracy**: 94.59%
- **Precision**: 94.19%
- **Recall**: 94.10%
- **F1 Score**: 94.15%
- **ROC-AUC**: 99.04%

## Troubleshooting
- **API Error / Connection Refused in Streamlit**: Ensure the FastAPI server is running on the correct port (`8001`). If you are running the backend on a different port or host, set the `CHURN_API_URL` environment variable before starting Streamlit.
- **Missing Module Errors**: Ensure you have activated your virtual environment and installed dependencies in *both* the root directory and the `frontend_streamlit/` directory.

## Limitations and Future Improvements
- **Containerization**: Use Docker to containerize both the FastAPI backend and Streamlit frontend for seamless, uniform deployment.
- **Cloud Deployment**: Deploy the containerized solution using cloud services.
- **Feature Engineering**: Incorporate more granular behavioral data to further enhance prediction accuracy.
