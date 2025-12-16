import pytest
from fastapi.testclient import TestClient
from src.api.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_get_metrics(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "accuracy" in data
    assert "roc_auc" in data

def test_predict_legit(client):
    payload = {
        "transaction_id": "TXN_TEST_001",
        "customer_id": "CUST_TEST_001",
        "account_age_days": 365.0,
        "transaction_amount": 50.0,
        "channel": "Online",
        "kyc_verified_flag": 1,
        "hour": 12,
        "weekday": 2
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["transaction_id"] == "TXN_TEST_001"
    assert "risk_score" in data
    assert "is_fraud" in data
    assert isinstance(data["is_fraud"], bool)

def test_predict_invalid_input(client):
    payload = {
        "transaction_id": "TXN_TEST_002",
        # Missing fields
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
