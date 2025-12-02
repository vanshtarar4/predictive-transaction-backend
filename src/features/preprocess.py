import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin

# Define feature groups
NUMERIC_FEATURES = ['account_age_days', 'transaction_amount', 'hour', 'weekday']
CATEGORICAL_FEATURES = ['channel']
BINARY_FEATURES = ['kyc_verified_flag']

def get_preprocessing_pipeline():
    """
    Returns a scikit-learn ColumnTransformer for preprocessing.
    """
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    binary_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERIC_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES),
            ('bin', binary_transformer, BINARY_FEATURES)
        ],
        remainder='drop' # Drop ID columns and original timestamp
    )

    return preprocessor

def load_data(filepath):
    """
    Load data and return X, y.
    """
    df = pd.read_csv(filepath)
    
    # Ensure correct types
    # (Add any specific type conversion if needed here)
    
    X = df.drop(columns=['is_fraud'])
    y = df['is_fraud']
    
    return X, y
