import requests
import json
import time

BASE_URL = "http://localhost:8000/predict"

def send_txn(name, data):
    print(f"\n--- Testing: {name} ---")
    try:
        response = requests.post(BASE_URL, json=data)
        if response.status_code == 200:
            res = response.json()
            print(f"Prediction: {'FRAUD' if res['is_fraud'] else 'LEGIT'}")
            print(f"Risk Score: {res['risk_score']:.4f}")
            if res['reason']:
                print(f"Reason: {res['reason']}")
            else:
                print("Reason: N/A")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Failed: {e}")

def run_tests():
    # 1. Legit Transaction
    # Normal hour, normal amount, verified, safe channel
    legit_txn = {
        "transaction_id": "TEST_LEGIT_001",
        "customer_id": "C_LEGIT",
        "account_age_days": 500,
        "transaction_amount": 50.0,
        "channel": "atm",
        "kyc_verified_flag": 1,
        "hour": 12,
        "weekday": 2
    }
    send_txn("Legit Transaction", legit_txn)

    # 2. Setup for High Amount Rule (Establish history)
    # We need to insert a few 'normal' transactions for a user first.
    # Note: The rule check logic does Avg > 0.
    setup_txn = {
        "transaction_id": "TEST_SETUP_001",
        "customer_id": "C_HIGHVAL",
        "account_age_days": 500,
        "transaction_amount": 100.0, # Avg will be around 100
        "channel": "atm",
        "kyc_verified_flag": 1,
        "hour": 12,
        "weekday": 2
    }
    send_txn("Setup History for User C_HIGHVAL (Amount $100)", setup_txn)
    
    # 3. High Amount Fraud
    # Amount 600 > 5 * 100
    high_amount_txn = {
        "transaction_id": "TEST_HIGHVAL_001",
        "customer_id": "C_HIGHVAL",
        "account_age_days": 500,
        "transaction_amount": 600.0,
        "channel": "atm",
        "kyc_verified_flag": 1,
        "hour": 12,
        "weekday": 2
    }
    send_txn("High Amount Rule (>5x Avg)", high_amount_txn)

    # 4. Odd Hour Rule
    odd_hour_txn = {
        "transaction_id": "TEST_ODD_001",
        "customer_id": "C_ODD",
        "account_age_days": 500,
        "transaction_amount": 50.0,
        "channel": "atm",
        "kyc_verified_flag": 1,
        "hour": 3, # 03:00 -> Rule Trigger
        "weekday": 2
    }
    send_txn("Odd Hour Rule (03:00)", odd_hour_txn)

    # 5. Risky Channel Rule
    risky_txn = {
        "transaction_id": "TEST_RISKY_001",
        "customer_id": "C_RISKY",
        "account_age_days": 10,
        "transaction_amount": 50.0,
        "channel": "unknown", # Risky
        "kyc_verified_flag": 0, # Not Verified
        "hour": 12,
        "weekday": 2
    }
    send_txn("Risky Channel + Unverified Rule", risky_txn)

if __name__ == "__main__":
    run_tests()
