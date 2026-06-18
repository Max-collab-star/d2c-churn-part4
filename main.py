import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="D2C Customer Churn Prediction Engine",
    version="1.0.0"
)

MODEL_PATH = "production_churn_model.pkl"
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

class PredictionRequest(BaseModel):
    recency: float = Field(..., ge=0, le=365, description="Days since last order")
    frequency: int = Field(..., ge=0, description="Total historical order count")
    monetary: float = Field(..., ge=0, description="Total gross spent amount")
    complaints_count: int = Field(..., ge=0, description="Total customer support tickets logged")

class PredictionResponse(BaseModel):
    churn_prediction: int
    churn_probability: float
    risk_status: str

@app.get("/")
def read_root():
    return {
        "status": "online",
        "model_loaded": model is not None,
        "engine": "FastAPI Production System"
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_churn(payload: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model artifact pkl file not loaded properly on server.")
    
    try:
        features = np.array([[payload.recency, payload.frequency, payload.monetary, payload.complaints_count]])
        
        prediction = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0][1])
        
        if probability >= 0.55 or prediction == 1:
            status = "CRITICAL_RISK"
        elif probability >= 0.35:
            status = "MODERATE_RISK"
        else:
            status = "LOW_RISK"
            
        return PredictionResponse(
            churn_prediction=prediction,
            churn_probability=round(probability, 4),
            risk_status=status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal pipeline error during execution: {str(e)}")