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

## 1. Clone repository
```bash
git clone https://github.com/vanshtarar4/predictive-transaction-backend
cd predictive-transaction-backend
```
## 2. Create virtual environment
```bash
python -m venv .venv
```
## Activate environment
## Windows:
```bash
.venv\Scripts\activate
```
## Linux/Mac:
```bash
source .venv/bin/activate
```

## 3. Install dependencies
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
