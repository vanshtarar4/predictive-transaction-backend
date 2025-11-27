# 📊 Predictive Transaction Intelligence – Backend

This repository contains the backend implementation for a **Predictive Transaction Intelligence** system in the **BFSI** domain.

It covers:

- Data collection & loading  
- Preprocessing & cleaning pipelines  
- Feature engineering  
- Fraud detection model preparation  
- REST API development with **FastAPI**

---

## 🚀 Milestone 1 – Completed Deliverables

- ✅ Project structure setup  
- ✅ Load & clean raw dataset  
- ✅ Feature engineering  
- ✅ Generate processed dataset  
- ✅ Train–test split  
- ✅ EDA summary (notebooks & reports)  
- ✅ Basic API endpoint: `/api/transactions`  

---

## 📁 Project Structure

```text
project_root/
├── data/
│   ├── raw/                  # Original dataset
│   └── processed/            # Cleaned & processed data
├── notebooks/                # EDA notebooks
├── src/
│   ├── preprocessing/        # Data cleaning & feature engineering scripts
│   ├── utils/                # Helper functions
│   └── api/                  # FastAPI application (main API entrypoint)
├── docs/                     # Reports & documentation
├── configs/                  # Project configuration files (e.g. .env templates)
├── tests/                    # Unit tests
├── requirements.txt          # Python dependencies
└── README.md                 # Project overview
```

> Note: The main FastAPI app is run from `src/api/main.py` (see run instructions below).

---

## 🔧 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/vanshtarar4/predictive-transaction-backend.git
cd predictive-transaction-backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Main dependencies include:

- `pandas`, `numpy` – data handling
- `scikit-learn` – modeling & preprocessing
- `fastapi`, `uvicorn` – backend API
- `matplotlib`, `seaborn` – visualization / EDA
- `pytest` – testing
- `python-dotenv` – environment variables
- `sqlalchemy` – database integration (if used)

---

## 📂 Data Processing Workflow

Run the preprocessing / cleaning pipeline:

```bash
python src/preprocessing/cleaning_pipeline.py
```

This script is responsible for:

- Loading data from `data/raw/`
- Cleaning & transforming data
- Performing feature engineering
- Saving outputs into `data/processed/`

(Adjust this section as your pipeline evolves.)

---

## 🌐 Running the API

Start the FastAPI server with Uvicorn:

```bash
uvicorn src.api.main:app --reload
```

By default, the server will be available at:

- API root: `http://localhost:8000`
- Interactive docs (Swagger UI): `http://localhost:8000/docs`
- ReDoc docs: `http://localhost:8000/redoc`

---

## 📡 API Overview

Core endpoints (current & planned):

- `GET /api/transactions` – list transactions  
- `POST /api/transactions` – create / ingest transaction records  
- `GET /api/transactions/{id}` – get transaction by ID  
- `GET /api/predictions/{transaction_id}` – get fraud probability / risk score for a given transaction (planned)  

You can document your endpoints using FastAPI’s automatic OpenAPI docs and add more details here as the API grows.

---

## 🧠 Predictive / Fraud Detection Model

The ML part of this backend focuses on **fraud detection / risk scoring** for financial transactions.

Typical flow:

1. Preprocess raw transaction data (cleaning, encoding, scaling, feature engineering).
2. Train models using `scikit-learn` (e.g. Logistic Regression, Random Forest, XGBoost, etc.).
3. Save the trained model and load it inside the API layer.
4. Expose prediction endpoints that:
   - Accept transaction payloads
   - Run them through the preprocessing pipeline
   - Return a fraud probability or risk score

(You can add model details and metrics here once finalized.)

---

## 🧪 Testing

Run tests with:

```bash
pytest
```

Add more unit tests under the `tests/` directory for:

- Data preprocessing functions  
- Model training / inference utilities  
- API routes and response validation  

---

## 💼 Internship Context

This project was developed as part of my **Infosys internship** to explore:

- Designing and implementing production-style backend APIs in Python with **FastAPI**  
- Building end-to-end ML workflows for **fraud detection** in BFSI  
- Structuring a data/ML project with clear separation of concerns (data, models, API)  
- Writing testable and maintainable code for analytics-driven systems  

---
