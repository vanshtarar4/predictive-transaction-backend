import requests
import json

BASE_URL = "http://localhost:8000"

def test_metrics():
    print("\n=== Testing GET /metrics ===")
    response = requests.get(f"{BASE_URL}/metrics")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Precision: {data.get('precision')}")
        print(f"Recall: {data.get('recall')}")
        print(f"F1 Score: {data.get('f1_score')}")
        print("✓ PASSED")
    else:
        print(f"✗ FAILED: {response.text}")

def test_legit_transaction():
    print("\n=== Testing POST /predict (Legit) ===")
    payload = {
        "transaction_id": "LEGIT_TEST",
        "customer_id": "C_TEST",
        "account_age_days": 500,
        "transaction_amount": 50,
        "channel": "atm",
        "kyc_verified_flag": 1,
        "hour": 12,
        "weekday": 2
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Is Fraud: {data['is_fraud']}")
        print(f"Risk Score: {data['risk_score']:.4f}")
        print(f"Reason: {data['reason']}")
        if not data['is_fraud']:
            print("✓ PASSED")
        else:
            print("✗ FAILED: Should be legit")
    else:
        print(f"✗ FAILED: {response.text}")

def test_fraud_odd_hour():
    print("\n=== Testing POST /predict (Fraud - Odd Hour) ===")
    payload = {
        "transaction_id": "FRAUD_HOUR",
        "customer_id": "C_HOUR",
        "account_age_days": 100,
        "transaction_amount": 50,
        "channel": "atm",
        "kyc_verified_flag": 1,
        "hour": 3,
        "weekday": 1
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Is Fraud: {data['is_fraud']}")
        print(f"Risk Score: {data['risk_score']:.4f}")
        print(f"Reason: {data['reason']}")
        if data['is_fraud'] and "Odd Hours" in data['reason']:
            print("✓ PASSED")
        else:
            print("✗ FAILED: Should detect odd hour fraud")
    else:
        print(f"✗ FAILED: {response.text}")

def test_fraud_risky_channel():
    print("\n=== Testing POST /predict (Fraud - Risky Channel) ===")
    payload = {
        "transaction_id": "FRAUD_CHANNEL",
        "customer_id": "C_CHANNEL",
        "account_age_days": 100,
        "transaction_amount": 50,
        "channel": "web",
        "kyc_verified_flag": 0,
        "hour": 12,
        "weekday": 2
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Is Fraud: {data['is_fraud']}")
        print(f"Risk Score: {data['risk_score']:.4f}")
        print(f"Reason: {data['reason']}")
        if data['is_fraud'] and "Risky Channel" in data['reason']:
            print("✓ PASSED")
        else:
            print("✗ FAILED: Should detect risky channel fraud")
    else:
        print(f"✗ FAILED: {response.text}")

if __name__ == "__main__":
    print("=" * 50)
    print("COMPREHENSIVE API TESTING")
    print("=" * 50)
    
    test_metrics()
    test_legit_transaction()
    test_fraud_odd_hour()
    test_fraud_risky_channel()
    
    print("\n" + "=" * 50)
    print("TESTING COMPLETE")
    print("=" * 50)
