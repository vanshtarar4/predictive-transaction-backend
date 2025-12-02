import sys
import os
import pandas as pd
import numpy as np
import joblib
import shap
from sklearn.pipeline import Pipeline

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))
from src.features.preprocess import load_data

# Load Data and Model
DATA_PATH = 'data/processed/transactions_processed.csv'
MODEL_PATH = 'models/fraud_model.pkl'

print("Loading data and model...")
X, y = load_data(DATA_PATH)
model = joblib.load(MODEL_PATH)

# Prepare data for SHAP
preprocessor = model.named_steps['preprocessor']
classifier = model.named_steps['classifier']

print("Transforming data...")
X_transformed = preprocessor.transform(X)
print(f"X_transformed shape: {X_transformed.shape}")

# Sample
X_sample = X_transformed[:100] if X_transformed.shape[0] > 100 else X_transformed
if hasattr(X_sample, "toarray"):
    X_sample_dense = X_sample.toarray()
else:
    X_sample_dense = X_sample

print(f"X_sample_dense shape: {X_sample_dense.shape}")

# Explainer
print("Calculating SHAP values...")
explainer = shap.TreeExplainer(classifier)
shap_values = explainer.shap_values(X_sample_dense)

print(f"shap_values type: {type(shap_values)}")

if isinstance(shap_values, list):
    print(f"shap_values is a list of length: {len(shap_values)}")
    for i, arr in enumerate(shap_values):
        print(f"  Item {i} shape: {np.array(arr).shape}")
        
    # Verify we can access [1]
    if len(shap_values) > 1:
        vals = shap_values[1]
        print(f"Selected vals (class 1) shape: {vals.shape}")
        
        # Check compatibility with summary_plot
        print(f"Compatible with X_sample ({X_sample_dense.shape})? {vals.shape == X_sample_dense.shape}")
else:
    print(f"shap_values shape: {shap_values.shape}")
    print(f"Compatible with X_sample ({X_sample_dense.shape})? {shap_values.shape == X_sample_dense.shape}")

print("Done.")
