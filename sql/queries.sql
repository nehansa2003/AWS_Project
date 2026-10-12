-- ====================================================================
-- Retail Customer Churn (ChurnIQ) — AWS Athena SQL Analytics Queries
-- Table: retail_churn
-- Location: s3://retail-customer-churn-group-project/processed/
-- ====================================================================

-- --------------------------------------------------------------------
-- DDL: Create External Parquet Table
-- --------------------------------------------------------------------
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


-- --------------------------------------------------------------------
-- Query 1: Churn Rate and Revenue Exposure by Customer Segment
-- Identifies high-risk customer tiers (e.g. VIP, Returning, New)
-- --------------------------------------------------------------------
SELECT 
    customer_segment,
    COUNT(*) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100, 2) AS churn_rate_pct,
    ROUND(AVG(total_spent), 2) AS avg_total_spent,
    ROUND(AVG(avg_order_value), 2) AS avg_order_value
FROM retail_churn
GROUP BY customer_segment
ORDER BY churn_rate_pct DESC;


-- --------------------------------------------------------------------
-- Query 2: Financial & Behavioral Profiling by Churn Status
-- Quantifies revenue gap and purchase frequency between churned and retained customers
-- --------------------------------------------------------------------
SELECT 
    CASE WHEN churn_flag = 1 THEN 'Churned' ELSE 'Retained' END AS customer_status,
    COUNT(*) AS customer_count,
    ROUND(AVG(total_spent), 2) AS avg_total_spent,
    ROUND(AVG(avg_order_value), 2) AS avg_order_value,
    ROUND(AVG(purchase_frequency), 1) AS avg_purchase_frequency,
    ROUND(AVG(engagement_score), 1) AS avg_engagement_score,
    ROUND(AVG(loyalty_score), 1) AS avg_loyalty_score
FROM retail_churn
GROUP BY churn_flag;


-- --------------------------------------------------------------------
-- Query 3: Channel Friction: Churn Rate & Cart Abandonment by Preferred Channel
-- Explores digital shopping friction across Mobile App, Online, and In-Store
-- --------------------------------------------------------------------
SELECT 
    preferred_channel,
    COUNT(*) AS total_customers,
    ROUND(AVG(churn_flag) * 100, 2) AS churn_rate_pct,
    ROUND(AVG(cart_abandonment_rate) * 100, 2) AS avg_cart_abandonment_pct,
    ROUND(AVG(website_visits), 1) AS avg_website_visits,
    ROUND(AVG(email_open_rate) * 100, 2) AS avg_email_open_pct
FROM retail_churn
GROUP BY preferred_channel
ORDER BY churn_rate_pct DESC;


-- --------------------------------------------------------------------
-- Query 4: Promotion Sensitivity: Discount Usage Tiers vs Churn
-- Evaluates if high discount seekers churn once promotional pricing ends
-- --------------------------------------------------------------------
SELECT 
    CASE 
        WHEN discount_usage_rate < 0.20 THEN 'Low Discount (<20%)'
        WHEN discount_usage_rate < 0.50 THEN 'Moderate Discount (20-50%)'
        WHEN discount_usage_rate < 0.75 THEN 'High Discount (50-75%)'
        ELSE 'Extreme Discount (>75%)'
    END AS discount_tier,
    COUNT(*) AS total_customers,
    ROUND(AVG(churn_flag) * 100, 2) AS churn_rate_pct,
    ROUND(AVG(total_spent), 2) AS avg_total_spent
FROM retail_churn
GROUP BY 1
ORDER BY churn_rate_pct DESC;


-- --------------------------------------------------------------------
-- Query 5: Inactivity Risk Window: Recency Buckets vs Churn Probability
-- Establishes the critical recency thresholds for triggering retention interventions
-- --------------------------------------------------------------------
SELECT 
    CASE 
        WHEN recency_days < 30 THEN '1. Active (<30 days)'
        WHEN recency_days < 60 THEN '2. Moderate (30-60 days)'
        WHEN recency_days < 90 THEN '3. At-Risk (60-90 days)'
        WHEN recency_days < 180 THEN '4. Dormant (90-180 days)'
        ELSE '5. Lapsed (>180 days)'
    END AS recency_bucket,
    COUNT(*) AS customer_count,
    ROUND(AVG(churn_flag) * 100, 2) AS churn_rate_pct,
    ROUND(AVG(engagement_score), 2) AS avg_engagement_score,
    ROUND(AVG(loyalty_score), 2) AS avg_loyalty_score
FROM retail_churn
GROUP BY 1
ORDER BY 1;
