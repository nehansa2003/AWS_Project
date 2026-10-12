import io
import json
import logging
import urllib.parse
import boto3
import pandas as pd

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3 = boto3.client("s3")

# Expected 18 columns for the Retail Customer Churn dataset
REQUIRED_COLUMNS = [
    "customer_id",
    "age_group",
    "gender",
    "region",
    "customer_segment",
    "preferred_channel",
    "purchase_frequency",
    "avg_order_value",
    "total_spent",
    "recency_days",
    "website_visits",
    "discount_usage_rate",
    "email_open_rate",
    "cart_abandonment_rate",
    "loyalty_score",
    "engagement_score",
    "churn_risk",
    "churn_flag",
]


def lambda_handler(event, context):
    """
    AWS Lambda handler triggered by S3 ObjectCreated events.
    Validates uploaded retail customer churn CSV datasets from the 'raw/' folder,
    checks schema and data quality, and saves validated data to 'processed/'.
    """
    logger.info("Lambda function triggered for retail churn data validation.")
    results = []

    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        
        # AWS S3 URL-encodes object keys (spaces become '+', special chars encoded)
        raw_key = record["s3"]["object"]["key"]
        key = urllib.parse.unquote_plus(raw_key)

        logger.info(f"New upload detected: s3://{bucket}/{key}")

        # 1. Skip non-CSV files
        if not key.lower().endswith(".csv"):
            logger.info(f"Skipping non-CSV file: {key}")
            continue

        # 2. Prevent infinite loops: only process files within 'raw/'
        if not key.startswith("raw/"):
            logger.info(f"Skipping file outside 'raw/' prefix: {key}")
            continue

        # 3. Guard against processing already validated outputs
        if "_validated.csv" in key:
            logger.info(f"Skipping already validated file: {key}")
            continue

        try:
            # 4. Fetch the file from S3
            obj = s3.get_object(Bucket=bucket, Key=key)
            csv_bytes = obj["Body"].read()
            df = pd.read_csv(io.BytesIO(csv_bytes))

            # 5. Schema validation: check required columns
            missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
            if missing_cols:
                logger.error(f"Validation FAILED for {key}. Missing required columns: {missing_cols}")
                results.append({
                    "file": key,
                    "status": "FAILED",
                    "missing_columns": missing_cols
                })
                continue

            # 6. Check for unexpected additional columns (optional warning)
            unexpected_cols = [c for c in df.columns if c not in REQUIRED_COLUMNS]
            if unexpected_cols:
                logger.warning(f"File {key} contains unexpected columns: {unexpected_cols}")

            # 7. Data Quality & Summary Statistics
            row_count = len(df)
            if row_count == 0:
                logger.error(f"Validation FAILED for {key}: Dataset contains 0 rows.")
                results.append({
                    "file": key,
                    "status": "FAILED",
                    "reason": "Empty dataset"
                })
                continue

            null_pct = df[REQUIRED_COLUMNS].isnull().mean().round(4).to_dict()
            duplicate_ids = int(df["customer_id"].duplicated().sum()) if "customer_id" in df.columns else 0

            logger.info(f"File {key} validated successfully: {row_count} rows, {duplicate_ids} duplicate customer IDs.")
            logger.info(f"Null proportions: {null_pct}")

            # 8. Define output destination: raw/path.csv -> processed/path_validated.csv
            out_key = key.replace("raw/", "processed/").replace(".csv", "_validated.csv")

            # Write validated DataFrame to S3 processed folder
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)

            s3.put_object(
                Bucket=bucket,
                Key=out_key,
                Body=csv_buffer.getvalue().encode("utf-8"),
                ContentType="text/csv"
            )
            logger.info(f"Validated data successfully written to: s3://{bucket}/{out_key}")

            results.append({
                "file": key,
                "output": out_key,
                "status": "OK",
                "rows": row_count,
                "duplicate_customer_ids": duplicate_ids
            })

        except Exception as error:
            logger.exception(f"Error validating {key}: {str(error)}")
            results.append({
                "file": key,
                "status": "ERROR",
                "message": str(error)
            })

    return {
        "statusCode": 200,
        "results": results
    }
