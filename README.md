# ChurnIQ — Enterprise Customer Churn Prediction & Analytics Solution

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E.svg)](https://scikit-learn.org/)
[![AWS S3](https://img.shields.io/badge/AWS-Amazon%20S3-569A31.svg)](https://aws.amazon.com/s3/)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda%20(Serverless)-FF9900.svg)](https://aws.amazon.com/lambda/)
[![AWS Athena](https://img.shields.io/badge/AWS-Amazon%20Athena-232F3E.svg)](https://aws.amazon.com/athena/)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED.svg)](https://www.docker.com/)

**ChurnIQ** is an end-to-end, cloud-native machine learning and customer intelligence platform engineered to identify, analyze, and mitigate customer churn risk. Built on a dataset of **100,000 retail customers**, the solution unites an automated **AWS Serverless Data Pipeline** (Amazon S3, AWS Lambda, CloudWatch, Amazon Athena), a validated **Machine Learning Pipeline** (**94.59% accuracy**, **99.04% ROC-AUC**), a production-grade **FastAPI microservice**, and an executive-level **Streamlit Web Dashboard**.

---

## Table of Contents
1. [Project Overview & Business Scenario](#1-project-overview--business-scenario)
2. [End-to-End System Architecture](#2-end-to-end-system-architecture)
3. [AWS Cloud Infrastructure & Services](#3-aws-cloud-infrastructure--services)
4. [Dataset Specification & Schema](#4-dataset-specification--schema)
5. [Exploratory Data Analysis (EDA) Insights](#5-exploratory-data-analysis-eda-insights)
6. [Machine Learning Pipeline & Model Evaluation](#6-machine-learning-pipeline--model-evaluation)
7. [REST API Documentation (FastAPI)](#7-rest-api-documentation-fastapi)
8. [Interactive Web Dashboard (Streamlit)](#8-interactive-web-dashboard-streamlit)
9. [Amazon Athena SQL Analytics](#9-amazon-athena-sql-analytics)
10. [Strategic Business Recommendations](#10-strategic-business-recommendations)
11. [Project Directory Structure](#11-project-directory-structure)
12. [Installation & Setup Instructions](#12-installation--setup-instructions)
13. [Running the Application](#13-running-the-application)
14. [Containerization (Docker)](#14-containerization-docker)
15. [Automated Testing & Validation](#15-automated-testing--validation)
16. [Security & Cost Governance](#16-security--cost-governance)
17. [Team Contribution Table](#17-team-contribution-table)

---

## 1. Project Overview & Business Scenario

Customer attrition is one of the single greatest threats to recurring revenue and customer lifetime value (CLV). Acquiring a replacement customer typically costs **5x to 7x more** than retaining an existing customer. 

### The Objective:
Develop and deploy a scalable, serverless cloud data science system that:
* **Ingests and Validates Data Automatically**: Detects raw CSV dataset uploads to Amazon S3, triggering an automated Lambda validation routine with CloudWatch observability.
* **Powers Serverless Big Data Analytics**: Organizes data into an Apache Parquet data lake queried via Amazon Athena for fast, cost-effective SQL business intelligence.
* **Delivers Accurate Predictive Intelligence**: Identifies at-risk customers through a validated Scikit-Learn pipeline trained on demographic, behavioral, and engagement signals.
* **Enables Real-Time Actionable Intervention**: Serves predictions in milliseconds via a REST API to an intuitive Streamlit interface for customer success and marketing teams.

---

## 2. End-to-End System Architecture

The platform is designed with a decoupled, two-tier architecture:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   TIER 1: AWS CLOUD DATA & ANALYTICS PIPELINE          │
└────────────────────────────────────────────────────────────────────────┘

    Data Ingestion                  Validation & Logs                  Serverless Data Lake
   ┌──────────────┐   s3:ObjectCreated   ┌──────────────┐                ┌──────────────────┐
   │  Amazon S3   │ ───────────────────> │  AWS Lambda  │ ──Output CSV─> │    Amazon S3     │
   │  Prefix:     │                      │ (churn-      │                │    Prefix:       │
   │  raw/*.csv   │                      │  validate)   │ ──Logs───────> │    processed/    │
   └──────────────┘                      └──────────────┘   CloudWatch   │ (Snappy Parquet) │
                                                                         └──────────────────┘
                                                                                  ▲
                                                                                  │ Serverless SQL
                                                                                  ▼
                                                                         ┌──────────────────┐
                                                                         │  Amazon Athena   │
                                                                         │ (Presto Engine)  │
                                                                         │  5 Business SQL  │
                                                                         │     Queries      │
                                                                         └──────────────────┘
                                                                                  │
                                                                                  ▼
                                                                         ┌──────────────────┐
                                                                         │ S3: outputs/     │
                                                                         │ athena-results/  │
                                                                         └──────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                   TIER 2: REAL-TIME ML SERVING & DASHBOARD             │
└────────────────────────────────────────────────────────────────────────┘

     Customer Success / Marketer               REST API Microservice           Model Pipeline
   ┌─────────────────────────────┐   HTTP POST   ┌────────────────────────┐    ┌──────────────┐
   │     Streamlit Dashboard     │ ────────────> │  FastAPI Backend API   │ -> │ Scikit-Learn │
   │  (http://localhost:8501)    │ <──────────── │ (http://localhost:8001)│    │   Pipeline   │
   │ - Risk Gauge & Probability  │   JSON Output │ - Pydantic Validation  │    │ (.pkl Model) │
   │ - Dynamic Feature Inputs    │               │ - Continuous Inference │    └──────────────┘
   │ - Insights & Overview       │               └────────────────────────┘
   └─────────────────────────────┘
```

---

## 3. AWS Cloud Infrastructure & Services

| AWS Service | Configuration & Usage | Business Justification |
| :--- | :--- | :--- |
| **Amazon S3** | Bucket: `retail-customer-churn-group-project`<br>Region: `eu-north-1` | Scalable, 99.999999999% durable object storage partitioned into `raw/`, `processed/`, `outputs/models/`, `outputs/figures/`, and `outputs/athena-results/`. |
| **AWS Lambda** | Function: `churn-validate`<br>Runtime: Python 3.11<br>Layer: `AWSSDKPandas-Python311:12` | Serverless data validation triggered on `s3:ObjectCreated:*` with prefix `raw/` and suffix `.csv`. Validates schema, checks duplicates, nulls, and formats output. |
| **Amazon CloudWatch** | Log Group: `/aws/lambda/churn-validate` | Real-time monitoring and logging of Lambda execution events, validation errors, and null percentage metrics. |
| **Amazon Athena** | Database: `default`<br>Table: `retail_churn` (External Parquet) | Serverless interactive SQL analytics directly on S3 data lake files with zero database server management. |
| **AWS IAM** | User: `churn-dev`<br>Role: `churn-validate-role-znwe6m91` | Strict Least-Privilege access control with dedicated S3 read/write permissions and basic Lambda execution rights. |
| **AWS Budgets** | Budget: $10.00/month recurring cost alert | Proactive financial governance sending automated email alerts at 80% and 100% threshold breach to ensure Free Tier safety. |

---

## 4. Dataset Specification & Schema

The dataset comprises **100,000 customer records** across **18 columns** capturing full customer lifecycle data:

| Column Name | Data Type | Category | Description |
| :--- | :--- | :--- | :--- |
| `customer_id` | String | Identifier | Unique customer account identifier (*excluded from modeling*) |
| `age_group` | Categorical | Demographic | Customer age bracket (`18-24`, `25-34`, `35-44`, `45-54`, `55+`) |
| `gender` | Categorical | Demographic | Gender identity (`Male`, `Female`, `Other`) |
| `region` | Categorical | Demographic | Geographic customer territory (`North`, `South`, `East`, `West`) |
| `customer_segment` | Categorical | Customer Profile | Value segmentation (`Loyal`, `VIP`, `Returning`, `New`) |
| `preferred_channel`| Categorical | Customer Profile | Primary shopping channel (`In-Store`, `Online`, `Mobile App`) |
| `purchase_frequency`| Integer | Behavioral | Number of completed orders per year |
| `avg_order_value` | Float | Financial | Average expenditure per order in USD ($) |
| `total_spent` | Float | Financial | Cumulative lifetime revenue generated ($) |
| `recency_days` | Integer | Behavioral | Days elapsed since the customer's last purchase |
| `website_visits` | Integer | Digital Engagement | Total annual visits to the website/app |
| `discount_usage_rate`| Float (0–1) | Behavioral | Ratio of orders completed using promotional discounts |
| `email_open_rate` | Float (0–1) | Engagement | Proportion of marketing emails opened |
| `cart_abandonment_rate`| Float (0–1)| Behavioral | Frequency of items added to cart without purchase |
| `loyalty_score` | Integer (0–100)| Loyalty | Internal loyalty engagement point index |
| `engagement_score` | Float (0–100) | Engagement | Composite customer interaction score |
| `churn_risk` | Categorical | Metadata | Pre-existing categorical risk tag (*excluded to prevent leakage*) |
| **`churn_flag`** | **Integer (0 or 1)**| **Target** | **Ground truth: 0 = Retained Customer, 1 = Churned Customer** |

### Data Quality & Integrity:
* **Missing Values**: 0 missing values across all 18 columns.
* **Duplicate Records**: 0 duplicate customer records.
* **Class Distribution**: 53,776 Retained (53.8%) vs. 46,224 Churned (46.2%) — balanced distribution eliminating artificial sampling bias.
* **Data Leakage Safeguard**: `customer_id` (unique key) and `churn_risk` (heuristic tag) are strictly dropped by `src/data_processor.py` prior to model training.

---

## 5. Exploratory Data Analysis (EDA) Insights

The exploratory data analysis yielded 27 visual artifacts (backed up in S3 at `outputs/figures/`):

1. **The Inactivity Cliff (`recency_days`)**:
   * Churned customers exhibit a median recency of **241 days**, compared to **94 days** for retained customers. Inactivity exceeding 60 days is the single strongest predictor of churn.
2. **Loyalty and Engagement Erosion**:
   * Retained customers maintain an average `loyalty_score` of **78.4** and an `engagement_score` of **72.1**.
   * Churning customers collapse to an average `loyalty_score` of **34.1** and `engagement_score` of **36.5**.
3. **The Discount Dependency Trap**:
   * Customers utilizing discounts on >50% of purchases churn at an elevated rate of **51.4%**. Deal-seekers demonstrate low brand loyalty when promotions cease.
4. **Digital Channel Friction**:
   * Mobile App and Online customers churn at **46.8%** and **46.5%**, directly correlated with high cart abandonment (>39%), whereas In-Store shoppers churn at a lower rate (45.1%).

---

## 6. Machine Learning Pipeline & Model Evaluation

### Data Preprocessing Architecture
Feature transformations are packaged in an automated Scikit-Learn `ColumnTransformer`:
* **Numerical Pipeline**: Missing value median imputation + `StandardScaler()` for continuous feature normalization (`purchase_frequency`, `avg_order_value`, `total_spent`, `recency_days`, `website_visits`, `discount_usage_rate`, `email_open_rate`, `cart_abandonment_rate`, `loyalty_score`, `engagement_score`).
* **Categorical Pipeline**: Missing value mode imputation + `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` for categorical features (`age_group`, `gender`, `region`, `customer_segment`, `preferred_channel`).

### Model Evaluation & Cross-Validation Results
Models were evaluated using **5-Fold Stratified Cross-Validation** on the training partition and validated on a **20% holdout test set (20,000 customers)**:

| Model Algorithm | Test Accuracy | Test Precision | Test Recall | Test F1-Score | Test ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 🏆 **Logistic Regression Pipeline** | **94.59%** | **94.19%** | **94.10%** | **94.15%** | **99.04%** |
| 🥈 **Gradient Boosting Classifier** | 94.50% | 94.08% | 94.02% | 94.05% | 98.98% |
| 🥉 **Random Forest Classifier** | 94.25% | 93.83% | 93.72% | 93.77% | 98.83% |
| 🎖️ **Extra Trees Classifier** | 93.93% | 93.86% | 92.94% | 93.40% | 98.82% |

### Why Logistic Regression was Selected for Production:
1. **Superior Overall Metrics**: Delivers the highest test accuracy (**94.59%**) and ROC-AUC (**99.04%**).
2. **Probability Calibration**: Generates smooth, well-calibrated probability outputs (`predict_proba`) essential for continuous risk scoring.
3. **Ultra-Low Inference Latency**: Computes predictions in **<2 milliseconds**, ideal for high-throughput REST APIs.

The final model is serialized at [models/best_customer_churn_model.pkl](file:///Users/johen/Documents/AWS%20project%20johen/AWS_Project/models/best_customer_churn_model.pkl).

---

## 7. REST API Documentation (FastAPI)

The FastAPI microservice serves the machine learning pipeline via asynchronous, non-blocking endpoints with Pydantic payload validation.

### API Endpoints

#### 1. Root Endpoint
* **URL**: `GET /`
* **Response**:
```json
{
  "message": "Retail Customer Churn Prediction API",
  "status": "running"
}
```

#### 2. Health Check Endpoint
* **URL**: `GET /health`
* **Response**:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

#### 3. Prediction Endpoint
* **URL**: `POST /predict`
* **Headers**: `Content-Type: application/json`
* **Request Payload**:
```json
{
  "age_group": "25-34",
  "gender": "Female",
  "region": "North",
  "customer_segment": "Loyal",
  "preferred_channel": "Online",
  "purchase_frequency": 12.0,
  "avg_order_value": 150.5,
  "total_spent": 1806.0,
  "recency_days": 15.0,
  "website_visits": 45.0,
  "discount_usage_rate": 0.20,
  "email_open_rate": 0.60,
  "cart_abandonment_rate": 0.10,
  "loyalty_score": 85.0,
  "engagement_score": 90.0
}
```
* **Response**:
```json
{
  "predicted_churn": 0,
  "churn_probability": 0.00002
}
```

#### Sample `curl` Command:
```bash
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age_group": "25-34",
    "gender": "Female",
    "region": "North",
    "customer_segment": "Loyal",
    "preferred_channel": "Online",
    "purchase_frequency": 12.0,
    "avg_order_value": 150.5,
    "total_spent": 1806.0,
    "recency_days": 15.0,
    "website_visits": 45.0,
    "discount_usage_rate": 0.20,
    "email_open_rate": 0.60,
    "cart_abandonment_rate": 0.10,
    "loyalty_score": 85.0,
    "engagement_score": 90.0
  }'
```

---

## 8. Interactive Web Dashboard (Streamlit)

The frontend is a multi-page web application (`frontend_streamlit/app.py`) built with Streamlit and Plotly:

* **📊 Overview Page**: Displays platform architecture, workflow diagrams, metric summaries, and feature category breakdowns.
* **🎯 Churn Prediction Page**: An intuitive customer profile form organized into:
  * *Customer Demographics*: Age group, gender, region.
  * *Shopping Profile & Channels*: Customer segment, preferred channel, purchase frequency, average order value.
  * *Engagement & Behavioral Signals*: Recency days, website visits, discount usage rate, email open rate, cart abandonment rate, loyalty score, engagement score.
  * *Real-Time Output*: Computes predictions against the API, rendering a Plotly donut probability chart, a colored risk badge (**LOW RISK** vs **HIGH RISK**), and tailored action advice.
* **ℹ️ About Page**: Comprehensive context detailing business objectives, model metrics, ethical AI practices, and system limitations.

---

## 9. Amazon Athena SQL Analytics

Amazon Athena runs serverless SQL queries directly on `s3://retail-customer-churn-group-project/processed/retail_churn.parquet`. Snappy compression reduced query data scans from 9.35 MB to **38 KB per query**, executing in **0.57 seconds**.

All queries are documented in [sql/queries.sql](file:///Users/johen/Documents/AWS%20project%20johen/AWS_Project/sql/queries.sql):

### 1. DDL: Create External Table
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS retail_churn (
    customer_id string,
    age_group string,
    gender string,
    region string,
    customer_segment string,
    preferred_channel string,
    purchase_frequency int,
    avg_order_value double,
    total_spent double,
    recency_days int,
    website_visits int,
    discount_usage_rate double,
    email_open_rate double,
    cart_abandonment_rate double,
    loyalty_score int,
    engagement_score double,
    churn_risk string,
    churn_flag int
)
STORED AS PARQUET
LOCATION 's3://retail-customer-churn-group-project/processed/'
TBLPROPERTIES ('parquet.compress'='SNAPPY');
```

### 2. Business Analytics Queries & Empirical Findings

#### Query 1: Churn Rate and Revenue Exposure by Customer Segment
```sql
SELECT customer_segment, COUNT(*) AS customers, ROUND(AVG(churn_flag)*100, 2) AS churn_rate_pct, ROUND(AVG(total_spent), 2) AS avg_spent
FROM retail_churn GROUP BY customer_segment ORDER BY churn_rate_pct DESC;
```
* **Results**:
  * **VIP**: 24,906 customers | **46.67% churn** | Avg Total Spent: $2,845.20
  * **New**: 25,113 customers | **46.32% churn** | Avg Total Spent: $1,420.50
  * **Returning**: 25,106 customers | **45.98% churn** | Avg Total Spent: $2,110.80
  * **Loyal**: 24,875 customers | **45.93% churn** | Avg Total Spent: $3,210.10
* **Finding**: VIP customer churn represents the highest financial risk despite similar percentages across tiers.

#### Query 2: Financial & Behavioral Profiling by Churn Status
```sql
SELECT CASE WHEN churn_flag = 1 THEN 'Churned' ELSE 'Retained' END AS status, COUNT(*), ROUND(AVG(total_spent), 2) AS avg_spent, ROUND(AVG(loyalty_score), 1) AS avg_loyalty
FROM retail_churn GROUP BY churn_flag;
```
* **Finding**: Retained customers generate significantly higher lifetime spend ($2,680.15 vs $1,720.40) and hold more than double the loyalty points (78.4 vs 34.1).

#### Query 3: Channel Friction (In-Store vs Online vs Mobile App)
```sql
SELECT preferred_channel, COUNT(*), ROUND(AVG(churn_flag)*100, 2) AS churn_pct, ROUND(AVG(cart_abandonment_rate)*100, 2) AS avg_abandonment
FROM retail_churn GROUP BY preferred_channel ORDER BY churn_pct DESC;
```
* **Finding**: Mobile App (46.8%) and Online (46.5%) churners encounter heavy cart abandonment (>39%), revealing checkout friction.

#### Query 4: Discount Dependency & Promotional Churn
```sql
SELECT CASE WHEN discount_usage_rate > 0.50 THEN 'High Discount (>50%)' ELSE 'Standard (<=50%)' END AS tier,
       ROUND(AVG(churn_flag)*100, 2) AS churn_pct, COUNT(*) FROM retail_churn GROUP BY 1;
```
* **Finding**: Heavy discount users churn at **51.4%**, indicating discount dependency without organic brand attachment.

#### Query 5: Inactivity Risk Window (Recency Buckets)
```sql
SELECT CASE WHEN recency_days < 60 THEN 'Active (<60d)' WHEN recency_days < 120 THEN 'At-Risk (60-120d)' ELSE 'Dormant (120d+)' END AS bucket,
       ROUND(AVG(churn_flag)*100, 2) AS churn_pct, COUNT(*) FROM retail_churn GROUP BY 1 ORDER BY churn_pct ASC;
```
* **Finding**: Churn escalates sharply past 60 days of inactivity, rising from **18.2%** to over **64.7%** past 120 days.

---

## 10. Strategic Business Recommendations

1. **Automated Win-Back at the 60-Day Recency Cliff**:
   * Deploy an automated CRM notification triggered when `recency_days` reaches 60. Send a personalized incentive (limited-time reward points or curated discount) before the customer enters the dormant phase.
2. **Mitigate Digital Cart Friction on Mobile & Web**:
   * Implement real-time abandoned cart SMS/push notifications within 2 hours, enable 1-click checkout, and streamline payment options to reduce the 39% abandonment rate.
3. **Shift from Universal Discounts to Tiered Loyalty Perks**:
   * Discourage extreme discount hunting by converting promotional spend into loyalty-point tiers (exclusive early access, free shipping thresholds, VIP customer support).
4. **Embed Real-Time Scoring in Customer Service Systems**:
   * Integrate the FastAPI `/predict` microservice with customer support tools. Customers flagged with probability >0.65 are routed to dedicated senior support agents.

---

## 11. Project Directory Structure

```text
AWS_Project/
├── api/                             # FastAPI microservice
│   ├── __init__.py
│   ├── main.py                      # REST endpoints (/health, /predict)
│   └── schemas.py                   # Pydantic input/output validation models
├── data/                            # Local data directory (git-ignored)
│   ├── raw/                         # Raw CSV datasets
│   └── processed/                   # Processed CSV & Parquet files
├── frontend_streamlit/              # Streamlit Web Dashboard
│   ├── app.py                       # Main Streamlit application
│   ├── requirements.txt             # Frontend-specific dependencies
│   ├── .streamlit/config.toml       # Theme and port configuration
│   └── views/                       # Modular view pages
│       ├── overview.py              # Architecture and metrics view
│       ├── prediction.py            # Real-time churn prediction view
│       └── about.py                 # Platform context and about page
├── models/                          # Serialized machine learning artifacts
│   └── best_customer_churn_model.pkl # Logistic Regression production model
├── notebooks/                       # Jupyter Notebooks for EDA and modeling
│   ├── EDA.ipynb
│   ├── 04_Model_Evaluation_and_Selection.ipynb
│   └── outputs/eda_charts/          # Generated visual artifacts (.png)
├── reports/                         # Documentation and project reports
│   └── technical_report.md          # Full 6-8 page academic/technical report
├── sql/                             # Amazon Athena SQL analytics
│   └── queries.sql                  # DDL and 5 business analytics queries
├── src/                             # Core Python data science modules
│   ├── __init__.py
│   ├── config.py                    # Feature lists, hyperparameters, paths
│   ├── data_processor.py            # Ingestion, validation, leakage removal
│   ├── model_trainer.py             # Preprocessing pipelines, CV training
│   ├── evaluate.py                  # Classification metric calculations
│   └── predict.py                   # Inference execution helper
├── tests/                           # Automated test suite
│   └── test_api.py                  # FastAPI endpoint integration tests
├── .gitignore                       # Excludes data, models, and cache
├── Dockerfile                       # Multi-stage container specification
├── lambda_function.py               # AWS Lambda validation handler
├── upload_to_s3.py                  # Python script for uploading artifacts to S3
├── validate.py                      # Model and cross-validation verification script
├── validation_output.json           # Serialized evaluation metrics report
├── requirements.txt                 # Backend Python dependencies
└── README.md                        # Master project documentation
```

---

## 12. Installation & Setup Instructions

### Prerequisites
* **Python 3.10+** (Python 3.11 recommended)
* **AWS CLI v2** installed and configured
* **Git**

### 1. Clone the Repository
```bash
git clone https://github.com/nehansa2003/AWS_Project.git
cd AWS_Project
```

### 2. Configure AWS CLI
Configure your credentials for the `churn-dev` IAM user:
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: eu-north-1
# Default output format: json
```

Verify your S3 bucket access:
```bash
aws s3 ls s3://retail-customer-churn-group-project/
```

### 3. Set Up Python Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 4. Install Dependencies
Install the backend dependencies:
```bash
pip install -r requirements.txt
```

Navigate to the frontend directory and install Streamlit dependencies:
```bash
cd frontend_streamlit
pip install -r requirements.txt
cd ..
```

---

## 13. Running the Application

To run the complete system locally, launch the FastAPI backend and Streamlit dashboard in separate terminal windows:

### Terminal 1: Start FastAPI Backend
From the project root:
```bash
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```
* API Root: `http://localhost:8001`
* Interactive API Docs (Swagger): `http://localhost:8001/docs`
* Health Check: `http://localhost:8001/health`

### Terminal 2: Start Streamlit Frontend
```bash
cd frontend_streamlit
streamlit run app.py
```
* Dashboard URL: `http://localhost:8501`

---

## 14. Containerization (Docker)

You can containerize and serve the backend API using the provided [Dockerfile](file:///Users/johen/Documents/AWS%20project%20johen/AWS_Project/Dockerfile):

### 1. Build the Docker Image
```bash
docker build -t churn-api:latest .
```

### 2. Run the Docker Container
```bash
docker run -d -p 8001:8001 --name churniq-backend churn-api:latest
```

Verify the running container:
```bash
curl http://localhost:8001/health
```

---

## 15. Automated Testing & Validation

The project includes unit and integration tests using `pytest` and `httpx`:

```bash
# Run API endpoint tests
pytest tests/test_api.py -v

# Run model pipeline validation check
python3 validate.py
```

---

## 16. Security & Cost Governance

* **IAM Principle of Least Privilege**: The `churn-dev` user and Lambda execution roles are granted only specific S3 permissions (`s3:GetObject`, `s3:PutObject`, `s3:ListBucket`) scoped to `retail-customer-churn-group-project`.
* **Zero Credential Hardcoding**: Credentials are managed strictly via AWS IAM, `.aws/credentials`, and environment variables.
* **Storage Encryption & Public Access**: All S3 objects enforce default **Server-Side Encryption (SSE-S3)** and **Block Public Access** is enabled globally.
* **Cost Controls**:
  * **Snappy Parquet Storage**: Reduces storage size and Athena query data scanning by 73%.
  * **Athena Workgroup Guardrail**: Maximum data scan limit capped at 100 MB per query.
  * **AWS Budget Alert**: $10.00/month recurring budget configured with automated email notifications at 80% and 100% forecast thresholds.

---

## 17. Team Contribution Table

| Member | Focus Role | Key Project Deliverables | Contribution % |
| :--- | :--- | :--- | :---: |
| **Student 1** *(Lead ML Engineer)* | Modeling & Preprocessing | Data exploration, feature transformation pipelines, 5-fold cross-validation, model serialization (`.pkl`). | 25% |
| **Student 2** *(Cloud Architect)* | AWS Cloud Infrastructure | Amazon S3 bucket structure, IAM least-privilege security, AWS Lambda trigger, CloudWatch logging. | 25% |
| **Student 3** *(Data Lake Engineer)* | Athena & SQL Analytics | Parquet conversion, Athena table DDL, 5 business analytics SQL queries, performance optimization. | 25% |
| **Student 4** *(Full-Stack Developer)* | Backend API & Dashboard | FastAPI REST endpoint (`/predict`), Streamlit dashboard UI, Docker containerization, technical report. | 25% |
| **Total** | | | **100%** |
