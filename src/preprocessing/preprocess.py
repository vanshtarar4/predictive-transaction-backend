"""
Milestone 1 - Data Preprocessing Script
---------------------------------------
This script performs all preprocessing steps:
✔ Load raw dataset
✔ Handle missing values
✔ Remove duplicates
✔ Normalize transaction amount
✔ Standardize timestamp
✔ Encode categorical variables
✔ Feature Engineering (optional but recommended)
✔ Save processed dataset
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
RAW_FILE = os.path.join(BASE_DIR, "data", "raw", "transactions.csv")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

# Create processed directory if not exists
os.makedirs(PROCESSED_DIR, exist_ok=True)


def load_raw_data():
    """Load raw CSV file"""
    print(f"📂 Loading raw data from: {RAW_FILE}")
    return pd.read_csv(RAW_FILE)


def clean_data(df):
    """Apply cleaning operations"""
    print("🧹 Cleaning data...")

    # Handle missing values
    df['kyc_verified'] = df['kyc_verified'].fillna('No')
    df = df.dropna(subset=['transaction_amount'])

    # Remove duplicates
    df = df.drop_duplicates(subset=['transaction_id'])

    # Normalize transaction_amount (remove commas, ₹ symbol)
    df['transaction_amount'] = (
        df['transaction_amount']
        .astype(str)
        .str.replace(',', '', regex=False)
        .str.replace('₹', '', regex=False)
        .astype(float)
    )

    # Convert timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Encode categorical variables
    df['channel'] = df['channel'].astype(str).str.title().str.strip()
    df['kyc_verified_flag'] = df['kyc_verified'].str.lower().map(lambda x: 1 if x in ['yes', 'y', 'true', '1'] else 0)

    # Optional Feature Engineering
    df['hour'] = df['timestamp'].dt.hour
    df['weekday'] = df['timestamp'].dt.weekday

    return df


def save_processed_data(df):
    """Save cleaned dataset"""
    processed_path = os.path.join(PROCESSED_DIR, 'transactions_processed.csv')
    df.to_csv(processed_path, index=False)
    print(f"💾 Processed data saved to: {processed_path}")
    return processed_path


def train_test_split_data(df):
    """Split data"""
    if 'is_fraud' not in df.columns:
        raise ValueError("❌ 'is_fraud' column missing!")

    train, test = train_test_split(df, test_size=0.2, stratify=df['is_fraud'], random_state=42)

    train.to_csv(os.path.join(PROCESSED_DIR, 'train.csv'), index=False)
    test.to_csv(os.path.join(PROCESSED_DIR, 'test.csv'), index=False)
    print("📊 Train and test datasets created.")


def run_pipeline():
    """Run full preprocessing pipeline"""
    print("\n🚀 Starting Preprocessing Pipeline...")

    df = load_raw_data()
    df = clean_data(df)
    save_processed_data(df)
    train_test_split_data(df)
    insert_data(df)
    print("\n🎯 Preprocessing Completed Successfully!\n")

def insert_data(df):
    """Insert cleaned data into database"""
    from src.utils.db_connection import get_db_connection

    # Drop original 'kyc_verified' since DB doesn't contain it
    if 'kyc_verified' in df.columns:
        df = df.drop(columns=['kyc_verified'])

    conn = get_db_connection()
    df.to_sql('transactions', conn, if_exists='append', index=False)
    conn.close()
    print("📥 Cleaned data inserted into DB.")


if __name__ == "__main__":
    run_pipeline()
