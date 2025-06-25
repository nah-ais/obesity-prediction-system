from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
from typing import List

# Initialize FastAPI app
app = FastAPI(title="Obesity Prediction API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model, scaler, and label encoder
try:
    with open("best_obesity_model.pkl", "rb") as f:
        model = pickle.load(f)
    
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    
    with open("target_label_encoder.pkl", "rb") as f:
        target_encoder = pickle.load(f)
    
    print("Model, scaler, and encoder loaded successfully!")
except Exception as e:
    print(f"Error loading model artifacts: {e}")
    model = None
    scaler = None
    target_encoder = None

# Define input data model
class ObesityInput(BaseModel):
    Gender: str  # "Male" or "Female"
    Age: float
    Height: float
    Weight: float
    family_history_with_overweight: str  # "yes" or "no"
    FAVC: str  # "yes" or "no" (Frequent consumption of high caloric food)
    FCVC: float  # Frequency of consumption of vegetables (1-3)
    NCP: float  # Number of main meals (1-4)
    CAEC: str  # Consumption of food between meals ("no", "Sometimes", "Frequently", "Always")
    SMOKE: str  # "yes" or "no"
    CH2O: float  # Consumption of water daily (1-3)
    SCC: str  # "yes" or "no" (Calories consumption monitoring)
    FAF: float  # Physical activity frequency (0-3)
    TUE: float  # Time using technology devices (0-2)
    CALC: str  # Consumption of alcohol ("no", "Sometimes", "Frequently", "Always")
    MTRANS: str  # Transportation used ("Walking", "Public_Transportation", "Automobile", "Bike", "Motorbike")

# Define response model
class ObesityPrediction(BaseModel):
    prediction: str
    prediction_code: int
    confidence: float

@app.get("/")
async def root():
    return {"message": "Obesity Prediction API", "status": "running"}

@app.get("/health")
async def health_check():
    if model is None:
        return {"status": "unhealthy", "message": "Model not loaded"}
    return {"status": "healthy", "message": "Model loaded successfully"}

@app.post("/predict", response_model=ObesityPrediction)
async def predict_obesity(input_data: ObesityInput):
    if model is None or scaler is None or target_encoder is None:
        raise HTTPException(status_code=500, detail="Model not loaded properly")
    
    try:
        # Convert input to DataFrame
        input_dict = input_data.dict()
        df = pd.DataFrame([input_dict])
        
        # Apply label encoding to categorical variables
        # Note: In a production system, you'd want to save and load the label encoders
        # for all categorical variables, not just recreate them
        categorical_mappings = {
            'Gender': {'Female': 0, 'Male': 1},
            'family_history_with_overweight': {'no': 0, 'yes': 1},
            'FAVC': {'no': 0, 'yes': 1},
            'CAEC': {'Always': 0, 'Frequently': 1, 'Sometimes': 2, 'no': 3},
            'SMOKE': {'no': 0, 'yes': 1},
            'SCC': {'no': 0, 'yes': 1},
            'CALC': {'Always': 0, 'Frequently': 1, 'Sometimes': 2, 'no': 3},
            'MTRANS': {'Automobile': 0, 'Bike': 1, 'Motorbike': 2, 'Public_Transportation': 3, 'Walking': 4}
        }
        
        # Apply mappings
        for col, mapping in categorical_mappings.items():
            if input_dict[col] in mapping:
                df[col] = mapping[input_dict[col]]
            else:
                raise HTTPException(status_code=400, detail=f"Invalid value for {col}: {input_dict[col]}")
        
        # Scale the features
        X_scaled = scaler.transform(df)
        
        # Make prediction
        prediction_code = model.predict(X_scaled)[0]
        prediction_proba = model.predict_proba(X_scaled)[0]
        confidence = float(np.max(prediction_proba))
        
        # Convert prediction code back to label
        prediction_label = target_encoder.inverse_transform([prediction_code])[0]
        
        return ObesityPrediction(
            prediction=prediction_label,
            prediction_code=int(prediction_code),
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/model-info")
async def get_model_info():
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    return {
        "model_type": type(model).__name__,
        "feature_count": model.n_features_in_ if hasattr(model, 'n_features_in_') else "Unknown",
        "classes": target_encoder.classes_.tolist() if target_encoder else "Unknown"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

