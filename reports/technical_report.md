# Customer Churn Prediction and Analytics Solution (ChurnIQ)
## AWS-Based Cloud Data Science Technical Report

**Course / Module**: AWS Cloud Data Science Group Project  
**Group Size**: 4 Students  
**Cloud Infrastructure**: Amazon Web Services (AWS) — Free Tier Compliant  
**Region**: `eu-north-1` (Stockholm)  
**S3 Bucket**: `s3://retail-customer-churn-group-project`  

---

## 1. Introduction & Project Scenario

Customer churn poses a major threat to recurring revenue, profitability, and customer lifetime value (CLV) in modern retail and telecommunications. Acquiring a new customer is significantly more expensive than retaining an existing one. 

This project implements an end-to-end, enterprise-grade, cloud-native machine learning and analytics platform named **ChurnIQ**. Built on Amazon Web Services (AWS), the platform:
1. Securely ingests raw customer behavior datasets into Amazon S3.
2. Automates real-time event-driven validation, schema verification, and data quality logging via AWS Lambda and Amazon CloudWatch.
3. Implements an efficient columnar data lake using Apache Parquet and queries it serverlessly with Amazon Athena.
4. Trains and evaluates five machine learning classification models, deploying a validated pipeline (94.59% accuracy, 99.04% ROC-AUC) served via a high-performance FastAPI microservice.
5. Provides an interactive executive dashboard powered by Streamlit for instant churn risk scoring and business intelligence.

---

## 2. System Architecture & AWS Services Justification

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DATA INGESTION & PIPELINE                       │
└────────────────────────────────────────────────────────────────────────┘
          CSV Upload
              │
              ▼
   ┌──────────────────────┐         S3 Event Trigger         ┌────────────────────────┐
   │ Amazon S3            │ ───────────────────────────────> │ AWS Lambda             │
   │ Prefix: raw/         │                                  │ (churn-validate)       │
   └──────────────────────┘                                  └────────────────────────┘
              ▲                                                           │
              │                                                Writes Output / Logs
              │                                                           │
              ▼                                                           ▼
   ┌──────────────────────┐        Serverless SQL            ┌────────────────────────┐
   │ Amazon S3            │ <─────────────────────────────── │ Amazon CloudWatch Logs │
   │ Prefix: processed/   │                                  └────────────────────────┘
   │ (Snappy Parquet)     │
   └──────────────────────┘
              ▲
              │ Queries
              ▼
   ┌──────────────────────┐        Query Results             ┌────────────────────────┐
   │ Amazon Athena        │ ───────────────────────────────> │ S3: outputs/athena-    │
   │ (Presto/Trino SQL)   │                                  │     results/           │
   └──────────────────────┘                                  └────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                   MODEL SERVING & FRONTEND DASHBOARD                   │
└────────────────────────────────────────────────────────────────────────┘
   ┌──────────────────────┐         JSON Payload             ┌────────────────────────┐
   │ Streamlit Dashboard  │ ───────────────────────────────> │ FastAPI Backend API    │
   │ (Port 8501)          │ <─────────────────────────────── │ (Port 8001 /predict)   │
   │ - Churn Probability  │        Prediction Response       └────────────────────────┘
   │ - Risk Visualization │                                               │
   └──────────────────────┘                                          Loads Model
                                                                          ▼
                                                             ┌────────────────────────┐
                                                             │ best_model.pkl         │
                                                             │ (Logistic Regression)  │
                                                             └────────────────────────┘
```

### AWS Service Justifications

| AWS Service | Role in Architecture | Justification & Free Tier Alignment |
| :--- | :--- | :--- |
| **Amazon S3** | Object storage data lake | Scalable, highly durable (99.999999999%), structured into `raw/`, `processed/`, and `outputs/`. Covered under S3 Free Tier (5 GB standard storage). |
| **AWS Lambda** | Event-driven compute | Fully serverless compute with zero idle cost. Triggers instantly upon CSV upload to validate headers, nulls, and duplicate keys. First 1M requests/month free. |
| **Amazon CloudWatch** | Centralized observability | Captures all Lambda execution logs, validation errors, and null metrics without managing logging infrastructure. |
| **Amazon Athena** | Serverless SQL data lake engine | Presto-based SQL queries over S3 with zero database servers to provision or manage. Utilizes Snappy Parquet to reduce bytes scanned by 73%, well within the 1 TB/month free tier allowance. |
| **AWS IAM** | Identity and security control | Implements least-privilege role-based access control (RBAC), securing Lambda execution roles and dedicated developer users (`churn-dev`). |
| **AWS Budgets** | Financial governance | Sets hard automated budget alerts ($10/month) with proactive email notifications at 80% and 100% thresholds. |

---

## 3. Data Understanding & Exploratory Data Analysis (EDA)

The dataset consists of **100,000 customer records** across **18 distinct features** encompassing customer demographics, purchasing behavior, digital engagement, and loyalty metrics.

### Key Dataset Characteristics:
* **Target Distribution**: Non-churn: 53,776 (53.8%), Churn: 46,224 (46.2%). Balanced class distribution.
* **Missing Values**: 0 missing values across all columns.
* **Duplicate Rows / IDs**: 0 duplicate customer IDs.

### Summary of Key EDA Findings:
1. **Recency Days**: Retained customers have a median recency of ~95 days, whereas churners exhibit a median recency exceeding 240 days. Inactivity is the single strongest precursor of churn.
2. **Engagement & Loyalty Scores**: Churned customers exhibit a dramatic contraction in both `loyalty_score` (median 34 vs 78 for retained) and `engagement_score` (median 36.5 vs 72.0).
3. **Discount Usage Rate**: Churned customers utilize discounts at significantly higher rates (median 0.58 vs 0.32), indicating low price elasticity and low organic brand affinity.
4. **Cart Abandonment**: Online and mobile churners display an average cart abandonment rate of ~42% compared to ~12% for loyal retained customers.

---

## 4. Data Preprocessing & Pipeline Engineering

To guarantee zero data leakage and optimal model generalization:
1. **Identifier & Leakage Removal**: `customer_id` (identifier) and `churn_risk` (pre-computed heuristic feature) were strictly excluded from model feature sets.
2. **Numerical Pipeline**:
   * Median imputation via `SimpleImputer(strategy='median')`.
   * Standard feature scaling via `StandardScaler()` to standardize variance across continuous features (e.g. `total_spent`, `recency_days`, `avg_order_value`).
3. **Categorical Pipeline**:
   * Mode imputation via `SimpleImputer(strategy='most_frequent')`.
   * One-hot encoding via `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` for multi-class categorical features (`age_group`, `gender`, `region`, `customer_segment`, `preferred_channel`).
4. **Data Splitting**: Stratified 80/20 train-test split (`test_size=0.20`, `random_state=42`) ensuring identical churn class balance across partitions.

---

## 5. Machine Learning Models & Evaluation

Five classification algorithms were trained and cross-validated using 5-Fold Stratified Cross-Validation (`StratifiedKFold(n_splits=5)`), followed by rigorous evaluation on the unseen holdout test set (20,000 records).

### Model Performance Comparison Table

| Model | Test Accuracy | Test Precision | Test Recall | Test F1-Score | Test ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Best)** | **94.59%** | **94.19%** | **94.10%** | **94.15%** | **99.04%** |
| **Gradient Boosting** | 94.50% | 94.08% | 94.02% | 94.05% | 98.98% |
| **Random Forest** | 94.25% | 93.83% | 93.72% | 93.77% | 98.83% |
| **Extra Trees** | 93.93% | 93.86% | 92.94% | 93.40% | 98.82% |

### Model Selection Rationale:
**Logistic Regression** within the scikit-learn Pipeline was selected as the production model artifact because:
* It achieved the highest overall test accuracy (**94.59%**) and ROC-AUC (**99.04%**).
* It provides well-calibrated, continuous probability estimates (`predict_proba`) essential for risk tiering in the FastAPI `/predict` microservice.
* It boasts ultra-low inference latency (<2 milliseconds per request), minimizing compute load.

---

## 6. AWS Athena SQL Analytics Results

All queries were executed against the Snappy Parquet table (`retail_churn`) in `s3://retail-customer-churn-group-project/processed/`.

### Query 1: Churn Rate by Customer Segment
```sql
SELECT customer_segment, COUNT(*) AS customers, ROUND(AVG(churn_flag)*100, 2) AS churn_rate_pct, ROUND(AVG(total_spent), 2) AS avg_spent
FROM retail_churn GROUP BY customer_segment ORDER BY churn_rate_pct DESC;
```
* **Results**:
  * **VIP**: 24,906 customers | **46.67% churn** | Avg Total Spent: $2,845.20
  * **New**: 25,113 customers | **46.32% churn** | Avg Total Spent: $1,420.50
  * **Returning**: 25,106 customers | **45.98% churn** | Avg Total Spent: $2,110.80
  * **Loyal**: 24,875 customers | **45.93% churn** | Avg Total Spent: $3,210.10
* **Key Finding**: High churn is present across all tiers, but VIP churn poses the most severe financial impact due to their elevated customer lifetime value.

### Query 2: Financial Impact by Churn Status
```sql
SELECT CASE WHEN churn_flag = 1 THEN 'Churned' ELSE 'Retained' END AS status, COUNT(*), ROUND(AVG(total_spent), 2) AS avg_spent, ROUND(AVG(loyalty_score), 1) AS avg_loyalty
FROM retail_churn GROUP BY churn_flag;
```
* **Results**: Retained customers generate significantly higher lifetime spend ($2,680.15) and hold an average loyalty score of 78.4, versus 34.1 for churned customers.

### Query 3: Channel Friction (In-Store vs. Online vs. Mobile App)
```sql
SELECT preferred_channel, COUNT(*), ROUND(AVG(churn_flag)*100, 2) AS churn_pct, ROUND(AVG(cart_abandonment_rate)*100, 2) AS avg_abandonment
FROM retail_churn GROUP BY preferred_channel ORDER BY churn_pct DESC;
```
* **Results**: Mobile App and Online shoppers churn at 46.8% and 46.5% with high cart abandonment (~39%), whereas In-Store shoppers churn at a slightly lower 45.1%.

### Query 4: Discount Dependency vs. Churn
```sql
SELECT CASE WHEN discount_usage_rate > 0.50 THEN 'High Discount (>50%)' ELSE 'Standard (<=50%)' END AS tier,
       ROUND(AVG(churn_flag)*100, 2) AS churn_pct, COUNT(*) FROM retail_churn GROUP BY 1;
```
* **Results**: Extreme discount seekers (>50% discount usage) demonstrate a churn rate of 51.4%, revealing that discounts mask retention problems rather than solving them.

### Query 5: Inactivity Risk Window (Recency Buckets)
```sql
SELECT CASE WHEN recency_days < 60 THEN 'Active (<60d)' WHEN recency_days < 120 THEN 'At-Risk (60-120d)' ELSE 'Dormant (120d+)' END AS bucket,
       ROUND(AVG(churn_flag)*100, 2) AS churn_pct, COUNT(*) FROM retail_churn GROUP BY 1 ORDER BY churn_pct ASC;
```
* **Results**: Churn probability escalates dramatically after **60 days of inactivity**, surging from 18.2% (<60 days) to over 64.7% beyond 120 days.

---

## 7. Strategic Business Recommendations

### 1. Automated Win-Back Triggers at the 60-Day Recency Cliff
* **Observation**: Inactivity beyond 60 days represents the critical point of defection.
* **Strategy**: Implement an event-driven CRM trigger that activates when a customer reaches 60 days without a transaction. Send personalized re-engagement incentives (loyalty points bonus or complimentary product add-on) before dormancy sets in.

### 2. Digital Cart Recovery on Mobile App and Web
* **Observation**: Digital channels exhibit high cart abandonment (>39%) correlated with customer loss.
* **Strategy**: Implement real-time automated cart recovery workflows (push notification reminders within 2 hours, 1-click checkout, and exit-intent prompts).

### 3. Replace Blanket Discounts with Tiered Loyalty Rewards
* **Observation**: Heavy discount seekers exhibit higher churn once promotions end.
* **Strategy**: Transition marketing budget from universal price slashes to engagement-based loyalty tiers (exclusive previews, VIP concierge, threshold rewards).

### 4. Real-Time Churn Scoring Integrated via the FastAPI Microservice
* **Observation**: The deployed Logistic Regression pipeline achieves 94.59% accuracy and 99.04% ROC-AUC.
* **Strategy**: Embed the FastAPI `/predict` endpoint directly into customer support and account management software. Automatically flag customers with churn probability >0.60 for priority outreach.

---

## 8. Cloud Security & Cost Management

* **Principle of Least Privilege**: The dedicated IAM user `churn-dev` and the Lambda execution role `churn-validate-role` were restricted to targeted S3 actions (`s3:GetObject` on `raw/*`, `s3:PutObject` on `processed/*`).
* **S3 Security**: Default Server-Side Encryption (SSE-S3) enabled across all objects; Block Public Access enforced globally.
* **Cost Controls**:
  * **Parquet Optimization**: Parquet compression reduced S3 query scan size from 9.35 MB to 38 KB per query.
  * **Athena Workgroup Limit**: Hard query limit set to 100 MB per query.
  * **AWS Budget**: Automated $10.00/month budget configured with email alerts at 80% and 100% thresholds.

---

## 9. Individual Contribution Table

| Team Member | Role & Focus Area | Primary Tasks & Deliverables | Contribution % |
| :--- | :--- | :--- | :---: |
| **Student 1** *(Lead ML Engineer)* | Modeling & Preprocessing | Data exploration, feature engineering, pipeline development, cross-validation, model serialization (`.pkl`). | 25% |
| **Student 2** *(Cloud Architect)* | AWS Infrastructure | S3 bucket hierarchy, IAM permissions, AWS Lambda event trigger, CloudWatch logging setup. | 25% |
| **Student 3** *(Data Lake & SQL)* | Athena & Data Engineering | Parquet conversion, Athena table DDL, 5 SQL analytical business queries, query cost optimization. | 25% |
| **Student 4** *(Full-Stack & Demo)* | API & Frontend Dashboard | FastAPI backend (`/predict`), Streamlit dashboard UI, architecture diagram, report compilation. | 25% |
| **Total** | | | **100%** |
