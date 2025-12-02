# Features Documentation

## Dataset Structure
The dataset `data/processed/transactions_processed.csv` contains the following columns:

| Column | Type | Description | Usage |
|dev|---|---|---|
| `transaction_id` | String | Unique identifier for the transaction | **Ignored** (ID) |
| `customer_id` | String | Unique identifier for the customer | **Ignored** (ID) |
| `kyc_verified` | String | KYC status (Yes/No) | **Ignored** (Redundant with `kyc_verified_flag`) |
| `account_age_days` | Float | Age of the account in days | **Feature** (Numerical) |
| `transaction_amount` | Float | Amount of the transaction | **Feature** (Numerical) |
| `channel` | String | Transaction channel (e.g., Online, POS) | **Feature** (Categorical) |
| `timestamp` | String | Timestamp of transaction | **Ignored** (Used to extract time features) |
| `is_fraud` | Integer | Target variable (0 = Legitimate, 1 = Fraud) | **Target** |
| `kyc_verified_flag` | Integer | Binary flag for KYC (1=Yes, 0=No) | **Feature** (Binary) |
| `hour` | Integer | Hour of the day (0-23) | **Feature** (Numerical/Cyclical) |
| `weekday` | Integer | Day of the week (0-6) | **Feature** (Numerical/Categorical) |

## Preprocessing Logic
1. **Drop**: `transaction_id`, `customer_id`, `timestamp`, `kyc_verified`.
2. **Imputation**:
   - Numerical: Median strategy.
   - Categorical: Most frequent strategy.
3. **Encoding**:
   - `channel`: One-Hot Encoding.
   - `hour`, `weekday`: Treated as numerical (or could be cyclical, but simple numerical for RF is often fine).
4. **Scaling**: Standard Scaler for numerical features (optional for RF but good for interpretability/consistency).
