"""
Database Connection Script (Milestone 1)
---------------------------------------
This sets up a basic SQLite database connection.
Schema will be used to store processed transactions.
"""

import sqlite3
import os

DB_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(DB_DIR, "data", "processed", "transactions.db")

def get_db_connection():
    """Creates a database connection (SQLite for now)"""
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_table():
    """Creates transaction table if not exists"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            customer_id TEXT,
            account_age_days INTEGER,
            transaction_amount REAL,
            channel TEXT,
            timestamp TEXT,
            is_fraud INTEGER,
            kyc_verified_flag INTEGER,
            hour INTEGER,
            weekday INTEGER
        );
    """)

    conn.commit()
    conn.close()
    print("🗄️ Database schema created (if not already).")

if __name__ == "__main__":
    create_table()
    print(f"📚 DB setup complete: {DB_PATH}")
