import sqlite3
import pandas as pd

try:
    conn = sqlite3.connect('data/processed/transactions.db')
    print("\n=== Recent Fraud Alerts ===")
    alerts = pd.read_sql_query("SELECT * FROM fraud_alerts ORDER BY created_at DESC LIMIT 5", conn)
    print(alerts)
    print("\n=== Recent Model Predictions ===")
    preds = pd.read_sql_query("SELECT * FROM model_predictions ORDER BY created_at DESC LIMIT 5", conn)
    print(preds)
    conn.close()
except Exception as e:
    print(f"Error reading DB: {e}")
