import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os

# Configure clean logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load the saved Brain
try:
    model = joblib.load("model/fraud_model.pkl")
    scaler = joblib.load("model/scaler.pkl")
    logging.info("API: Model and Scaler loaded successfully.")
except Exception as e:
    logging.error(f"API: Failed to load model files: {e}")
    model, scaler = None, None

app = FastAPI(title="Credit Fraud Detection API")

class TransactionInput(BaseModel):
    """Matches the features our model expects"""
    Time: float
    V1: float
    V2: float
    # ... In a real app, you'd include V3-V28
    Amount: float

@app.get("/")
def health_check():
    return {"status": "Service is online", "model_loaded": model is not None}

@app.post("/predict")
def predict(data: TransactionInput):
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    try:
        # 1. Convert input to DataFrame
        input_df = pd.DataFrame([data.model_dump()])
        
        # 2. Add dummy values for missing V-features (to match shape)
        # Note: Our trained model expects 30 features
        for i in range(3, 29):
            input_df[f'V{i}'] = 0.0
            
        # 3. Apply the EXACT same scaling used in training
        input_df['Amount'] = scaler.transform(input_df[['Amount']])
        input_df['Time'] = scaler.transform(input_df[['Time']])
        
        # 4. Predict
        # Ensure column order matches training
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        
        return {
            "prediction": "Fraud" if prediction == 1 else "Safe",
            "fraud_probability": round(float(probability), 4)
        }
    except Exception as e:
        logging.error(f"API: Prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)