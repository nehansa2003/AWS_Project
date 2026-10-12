
import boto3
import csv
import io
import json
import logging
import urllib.parse

s3 = boto3.client("s3")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

EXPECTED_COLUMNS = [
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
    "churn_flag"
]


def lambda_handler(event, context):
    results = []

    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(
            record["s3"]["object"]["key"]
        )

        if not key.lower().endswith(".csv"):
            logger.info("Skipped non-CSV file: %s", key)
            continue

        logger.info("Validating s3://%s/%s", bucket, key)

        try:
            response = s3.get_object(
                Bucket=bucket,
                Key=key
            )

            content = response["Body"].read().decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(content))

            actual_columns = reader.fieldnames or []

            if not actual_columns:
                raise ValueError("CSV has no header row.")

            missing_columns = [
                col for col in EXPECTED_COLUMNS
                if col not in actual_columns
            ]

            unexpected_columns = [
                col for col in actual_columns
                if col not in EXPECTED_COLUMNS
            ]

            if missing_columns:
                raise ValueError(
                    f"Missing columns: {missing_columns}"
                )

            if unexpected_columns:
                raise ValueError(
                    f"Unexpected columns: {unexpected_columns}"
                )

            row_count = 0
            invalid_rows = 0
            seen_customer_ids = set()

            for row in reader:
                row_count += 1

                # Check that required fields are not empty.
                if any(
                    not row.get(col) or not row[col].strip()
                    for col in EXPECTED_COLUMNS
                ):
                    invalid_rows += 1

                customer_id = row.get("customer_id", "").strip()

                if customer_id in seen_customer_ids:
                    invalid_rows += 1
                else:
                    seen_customer_ids.add(customer_id)

            if row_count == 0:
                raise ValueError("CSV contains no data rows.")

            if invalid_rows > 0:
                status = "invalid"
            else:
                status = "valid"

            result = {
                "file": key,
                "rows": row_count,
                "columns": len(actual_columns),
                "invalid_rows": invalid_rows,
                "status": status
            }

            logger.info(
                "Validation result: %s",
                json.dumps(result)
            )

            results.append(result)

        except Exception as error:
            logger.exception("Validation failed for %s", key)

            results.append({
                "file": key,
                "status": "error",
                "message": str(error)
            })

    return {
        "statusCode": 200,
        "body": json.dumps(results)
    }
