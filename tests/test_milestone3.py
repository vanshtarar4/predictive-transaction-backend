import pytest
from fastapi.testclient import TestClient
from src.api.main import app, init_db, DB_PATH
import os
import sqlite3

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()
    yield

def test_predict_legit(client):
    # Normal transaction
    payload = {
        "transaction_id": "TEST_LEGIT_001",
        "customer_id": "C_TEST",
        "account_age_days": 1000,
        "transaction_amount": 50,
        "channel": "atm",
        "kyc_verified_flag": 1,
        "hour": 12,
        "weekday": 1
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_fraud"] is False
    assert data["reason"] == "Legit"

def test_predict_rule_fraud_odd_hour(client):
    # Fraud by Rule: Odd Hour
    payload = {
        "transaction_id": "TEST_FRAUD_RULE_001",
        "customer_id": "C_TEST",
        "account_age_days": 100,
        "transaction_amount": 50,
        "channel": "atm",
        "kyc_verified_flag": 1,
        "hour": 3, # Odd Hour
        "weekday": 1
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_fraud"] is True
    assert "Odd Hours" in data["reason"]
    
    # Verify DB insertion
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM fraud_alerts WHERE transaction_id=?", ("TEST_FRAUD_RULE_001",))
    row = c.fetchone()
    conn.close()
    assert row is not None

def test_predict_ml_or_rule_fraud(client):
    # Should trigger flow even if ML is unsure, if rules trigger
    payload = {
        "transaction_id": "TEST_FRAUD_COMBIMED",
        "customer_id": "C_TEST_RISKY",
        "account_age_days": 1,
        "transaction_amount": 10000, # High amount
        "channel": "web", # Risky
        "kyc_verified_flag": 0, # Unverified
        "hour": 3, # Odd
        "weekday": 1
    }
    # This should trigger multiple rules and likely ML
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_fraud"] is True
    # Reason should contain details. It might have LLM explanation too if key works.
    print(f"Reason: {data['reason']}")
