# API Contract

## Base URL
`http://localhost:8000`

## Endpoints

### 1. Predict Fraud
**POST** `/predict`

**Description**: Predicts the probability of fraud for a given transaction.

**Request Body**:
```json
{
  "transaction_id": "TXN_12345",
  "customer_id": "CUST_999",
  "account_age_days": 120.5,
  "transaction_amount": 500.00,
  "channel": "Online",
  "kyc_verified_flag": 1,
  "hour": 14,
  "weekday": 3
}
```

**Response**:
```json
{
  "transaction_id": "TXN_12345",
  "risk_score": 0.05,
  "is_fraud": false,
  "prediction": 0
}
```

### 2. Get Metrics
**GET** `/metrics`

**Description**: Returns the latest model performance metrics.

**Response**:
```json
{
  "accuracy": 0.95,
  "precision": 0.88,
  "recall": 0.82,
  "f1": 0.85,
  "roc_auc": 0.92
}
```

## Example Usage

### Curl
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "transaction_id": "TXN_SAMPLE",
           "customer_id": "CUST_SAMPLE",
           "account_age_days": 200,
           "transaction_amount": 1000,
           "channel": "POS",
           "kyc_verified_flag": 1,
           "hour": 10,
           "weekday": 1
         }'
```
