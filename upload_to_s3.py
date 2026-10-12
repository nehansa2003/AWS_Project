"""
Day 11: Upload Model Artifacts, Evaluation Reports, and Figures to S3.
Target Bucket: retail-customer-churn-group-project (eu-north-1)
"""

import os
import glob
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "retail-customer-churn-group-project"
REGION = "eu-north-1"

s3 = boto3.client("s3", region_name=REGION)

def upload_file_to_s3(local_path, s3_key):
    try:
        s3.upload_file(local_path, BUCKET_NAME, s3_key)
        print(f"✅ Uploaded: {local_path} -> s3://{BUCKET_NAME}/{s3_key}")
    except ClientError as e:
        print(f"❌ Failed to upload {local_path}: {e}")

def main():
    print(f"Starting Day 11 S3 artifacts upload to s3://{BUCKET_NAME}/...")

    # 1. Upload Model Artifacts
    model_path = os.path.join("models", "best_customer_churn_model.pkl")
    if os.path.exists(model_path):
        upload_file_to_s3(model_path, "outputs/models/best_customer_churn_model.pkl")
    else:
        print(f"⚠️ Model file not found: {model_path}")

    # Also upload validation metrics json
    val_json = "validation_output.json"
    if os.path.exists(val_json):
        upload_file_to_s3(val_json, "outputs/metrics/validation_output.json")

    # 2. Upload Key Figures & EDA Charts
    chart_dir = os.path.join("notebooks", "outputs", "eda_charts")
    if os.path.exists(chart_dir):
        png_files = glob.glob(os.path.join(chart_dir, "*.png"))
        print(f"Found {len(png_files)} charts in {chart_dir}. Uploading key figures...")
        for png_file in png_files:
            file_name = os.path.basename(png_file)
            upload_file_to_s3(png_file, f"outputs/figures/{file_name}")
    # 3. Upload Parquet Dataset for Athena Queries
    parquet_path = os.path.join("data", "processed", "retail_churn.parquet")
    if os.path.exists(parquet_path):
        upload_file_to_s3(parquet_path, "processed/retail_churn.parquet")
    else:
        print(f"⚠️ Parquet file not found: {parquet_path}")

    print("🎉 Day 11 & Day 12 S3 artifacts upload completed!")

if __name__ == "__main__":
    main()
