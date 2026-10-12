import logging
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from api.schemas import CustomerData, PredictionResponse
from src.predict import load_saved_model, predict_customer_churn

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Global model variable
model_pipeline = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_pipeline
    logger.info("API Startup: Loading ML model...")
    try:
        model_pipeline = load_saved_model()
        logger.info("Model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load ML model: {e}")
        # We don't exit to allow the health check to report the failure
    yield


app = FastAPI(
    title="Retail Customer Churn Prediction API",
    description="API to predict retail customer churn using the validated ML model.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/")
def read_root():
    logger.info("Root endpoint called.")
    return {
        "message": "Retail Customer Churn Prediction API",
        "status": "running"
    }

@app.get("/health")
def health_check():
    logger.info("Health endpoint called.")
    if model_pipeline is not None:
        return {"status": "healthy", "model_loaded": True}
    else:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "model_loaded": False}
        )

@app.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerData):
    logger.info("Prediction endpoint called.")
    if model_pipeline is None:
        logger.error("Prediction failed: Model is not loaded.")
        raise HTTPException(status_code=503, detail="Model is not loaded.")
    
    try:
        # Convert pydantic object to dataframe (single row)
        # using .dict() for broad compatibility (works in both pydantic v1 and v2)
        input_data = pd.DataFrame([customer.dict()])
        
        # Predict using the existing prediction function
        prediction_df = predict_customer_churn(input_data, model=model_pipeline)
        
        # Extract the results
        pred_churn = int(prediction_df["predicted_churn"].iloc[0])
        prob_churn = float(prediction_df["churn_probability"].iloc[0])
        
        logger.info(f"Prediction successful: {pred_churn} ({prob_churn:.4f})")
        return PredictionResponse(
            predicted_churn=pred_churn,
            churn_probability=prob_churn
        )
    except Exception as e:
        logger.error(f"Prediction failed with exception: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during prediction.")
