from fastapi import FastAPI, HTTPException
import sqlite3
import pandas as pd
import os

app = FastAPI(title="Predictive Transaction Intelligence API")

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "transactions.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def read_root():
    return {"message": "Predictive Transaction Intelligence API is running"}

@app.get("/api/transactions")
def get_transactions(limit: int = 10):
    """
    Fetch recent transactions from the database.
    """
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Database not found. Please run preprocessing first.")

    try:
        conn = get_db_connection()
        query = f"SELECT * FROM transactions LIMIT {limit}"
        transactions = pd.read_sql(query, conn).to_dict(orient="records")
        conn.close()
        return {"count": len(transactions), "transactions": transactions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
