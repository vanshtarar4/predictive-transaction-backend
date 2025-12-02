import sys
import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.features.preprocess import get_preprocessing_pipeline, load_data

DATA_PATH = 'data/processed/transactions_processed.csv'
MODELS_DIR = 'models'
METRICS_PATH = os.path.join(MODELS_DIR, 'metrics.json')
MODEL_PATH = os.path.join(MODELS_DIR, 'fraud_model.pkl')
ENCODER_PATH = os.path.join(MODELS_DIR, 'scaler_encoders.pkl')

def train():
    print("Loading data...")
    X, y = load_data(DATA_PATH)
    
    # Class balance
    print("Class balance:")
    print(y.value_counts(normalize=True))
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    
    # Pipeline
    preprocessor = get_preprocessing_pipeline()
    clf = RandomForestClassifier(
        n_estimators=200, 
        class_weight='balanced', 
        random_state=42,
        n_jobs=-1
    )
    
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', clf)
    ])
    
    # CV
    print("Running 5-fold CV...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
    scores = cross_validate(model, X_train, y_train, cv=cv, scoring=scoring)
    
    metrics = {
        'accuracy': float(np.mean(scores['test_accuracy'])),
        'precision': float(np.mean(scores['test_precision'])),
        'recall': float(np.mean(scores['test_recall'])),
        'f1': float(np.mean(scores['test_f1'])),
        'roc_auc': float(np.mean(scores['test_roc_auc']))
    }
    
    print("CV Metrics:", json.dumps(metrics, indent=2))
    
    # Train final model
    print("Training final model...")
    model.fit(X_train, y_train)
    
    # Test evaluation
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print("\nTest Set Report:")
    print(classification_report(y_test, y_pred))
    print(f"Test AUC: {roc_auc_score(y_test, y_prob):.4f}")
    
    # Save artifacts
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Save full pipeline (includes preprocessor and model)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    
    # Save metrics
    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to {METRICS_PATH}")
    
    # Save version info
    import datetime
    import subprocess
    try:
        git_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8')
    except:
        git_hash = "unknown"
        
    version_info = {
        'timestamp': datetime.datetime.now().isoformat(),
        'git_hash': git_hash
    }
    with open(os.path.join(MODELS_DIR, 'model_version.txt'), 'w') as f:
        json.dump(version_info, f, indent=2)

if __name__ == "__main__":
    train()
