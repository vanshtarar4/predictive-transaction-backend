import sys
import os
import pandas as pd
import requests
import json
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.features.preprocess import load_data

DATA_PATH = 'data/processed/transactions_processed.csv'
API_URL = "http://localhost:8000/predict"

def seed_predictions():
    print("Loading data...")
    X, y = load_data(DATA_PATH)
    
    # Take a sample of 100 rows
    sample = X.sample(100, random_state=42)
    
    # We need to add back the ID columns for the API input if they were dropped in load_data
    # But load_data drops them. 
    # Let's read the CSV directly to get IDs
    df_full = pd.read_csv(DATA_PATH)
    sample_full = df_full.loc[sample.index]
    
    print(f"Sending {len(sample_full)} predictions to API (simulated)...")
    
    # Since we can't easily run the API server and this script concurrently in this environment 
    # without blocking or complex background management, 
    # we will simulate the DB insertion by importing the logic or just inserting directly.
    # BUT the task asked to "Run predictions on test set and insert sample rows".
    # The API handles insertion.
    # I will insert directly into SQLite to fulfill the requirement without needing the API server running.
    
    import sqlite3
    from src.api.main import init_db, DB_PATH, model, predict, TransactionInput
    import joblib
    
    # Ensure DB exists
    init_db()
    
    # Load model if not loaded (it's global in main.py but we are importing)
    # We need to manually load it because we are not running the app lifespan
    model_path = 'models/fraud_model.pkl'
    loaded_model = joblib.load(model_path)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    count = 0
    for _, row in sample_full.iterrows():
        # Prepare input for model
        input_df = pd.DataFrame([{
            'account_age_days': row['account_age_days'],
            'transaction_amount': row['transaction_amount'],
            'channel': row['channel'],
            'kyc_verified_flag': row['kyc_verified_flag'],
            'hour': row['hour'],
            'weekday': row['weekday']
        }])
        
        # Predict
        risk_score = float(loaded_model.predict_proba(input_df)[:, 1][0])
        prediction = int(loaded_model.predict(input_df)[0])
        
        # Insert
        features = input_df.to_dict(orient='records')[0]
        cursor.execute('''
            INSERT INTO model_predictions 
            (transaction_id, customer_id, features_json, risk_score, prediction, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            row['transaction_id'],
            row['customer_id'],
            json.dumps(features),
            risk_score,
            prediction,
            pd.Timestamp.now().isoformat()
        ))
        count += 1
        
    conn.commit()
    conn.close()
    print(f"Successfully inserted {count} predictions into {DB_PATH}")

if __name__ == "__main__":
    seed_predictions()
