# 📊 Predictive Transaction Intelligence – Backend

This repository contains the backend implementation for the Predictive Transaction Intelligence for BFSI system.
It covers data collection, preprocessing, feature engineering, fraud detection model preparation, and REST API development.

## 🚀 Milestone 1 Deliverables

✔ Setup project structure
✔ Load & clean raw dataset
✔ Feature engineering
✔ Generate processed dataset
✔ Train–test split
✔ EDA summary report
✔ Basic API endpoint (/api/transactions)

project_root/
├── data/
│   ├── raw/                  # Original dataset
│   ├── processed/            # Cleaned & processed data
├── notebooks/                # EDA notebooks
├── src/
│   ├── preprocessing/        # Data cleaning scripts
│   ├── utils/                # Helper functions
├── docs/                     # Reports & documentation
├── configs/                  # Project configuration files
├── tests/                    # Unit tests
├── requirements.txt          # Python dependencies
└── README.md                 # Project overview


## 1. Clone repository
```bash
git clone <your-repo-link>
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

python src/preprocessing/cleaning_pipeline.py

uvicorn src.api.main:app --reload
```
