import os
import json
import joblib
import pandas as pd
import sqlite3
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'fraud_model.pkl')
METRICS_PATH = os.path.join(BASE_DIR, 'models', 'metrics.json')
DB_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'transactions.db')

# Global model variable
model = None

def init_db():
    """Initialize SQLite database and table."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS model_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            customer_id TEXT,
            features_json TEXT,
            risk_score REAL,
            prediction INTEGER,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model and init DB
    global model
    try:
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded from {MODEL_PATH}")
    except Exception as e:
        print(f"Error loading model: {e}")
    
    init_db()
    print(f"Database initialized at {DB_PATH}")
    
    yield
    # Clean up if needed

app = FastAPI(title="Fraud Detection API", lifespan=lifespan)

class TransactionInput(BaseModel):
    transaction_id: str
    customer_id: str
    account_age_days: float
    transaction_amount: float
    channel: str
    kyc_verified_flag: int
    hour: int
    weekday: int

class PredictionOutput(BaseModel):
    transaction_id: str
    risk_score: float
    is_fraud: bool
    prediction: int

@app.get("/metrics")
def get_metrics():
    if not os.path.exists(METRICS_PATH):
        raise HTTPException(status_code=404, detail="Metrics not found")
    with open(METRICS_PATH, 'r') as f:
        return json.load(f)

@app.post("/predict", response_model=PredictionOutput)
def predict(txn: TransactionInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Prepare input dataframe
    input_data = {
        'account_age_days': [txn.account_age_days],
        'transaction_amount': [txn.transaction_amount],
        'channel': [txn.channel],
        'kyc_verified_flag': [txn.kyc_verified_flag],
        'hour': [txn.hour],
        'weekday': [txn.weekday]
    }
    df = pd.DataFrame(input_data)
    
    # Predict
    try:
        risk_score = float(model.predict_proba(df)[:, 1][0])
        prediction = int(model.predict(df)[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
    
    # Persist
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO model_predictions 
            (transaction_id, customer_id, features_json, risk_score, prediction, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            txn.transaction_id,
            txn.customer_id,
            json.dumps(input_data),
            risk_score,
            prediction,
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")
        # We don't fail the request if DB write fails, just log it (or could fail depending on requirements)
    
    return {
        "transaction_id": txn.transaction_id,
        "risk_score": risk_score,
        "is_fraud": bool(prediction == 1),
        "prediction": prediction
    }
