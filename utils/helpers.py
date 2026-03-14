import streamlit as st
import joblib
import pandas as pd
import os

@st.cache_resource
def load_model():
    """Load the trained machine learning model from disk."""
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model.pkl')
    try:
        artifact = joblib.load(model_path)
        return artifact
    except FileNotFoundError:
        return None

def predict_transaction(df, artifact):
    """Predict risk for a dataframe of transactions."""
    if artifact is None:
        return None
    
    model = artifact['model']
    features = artifact['features']
    
    # We need to process the dataframe exactly as we did in training
    # For simplicity, we assume df has exactly the columns we expect
    
    # In a real app we would call extract_features here from data_generator, 
    # but since data_generator is in utils we can just import it
    from utils.data_generator import extract_features
    
    X, _ = extract_features(df)
    
    # Ensure columns match exactly what the model expects
    X = X[features]
    
    # Make predictions
    probas = model.predict_proba(X)[:, 1]
    labels = model.predict(X)
    
    # Return as dataframe columns
    return probas, labels

def format_currency(value):
    """Format a number as currency."""
    return f"${value:,.2f}"

def calculate_kpis(df):
    """Calculate key performance indicators from transaction data."""
    if df is None or len(df) == 0:
        return {
            'total_transactions': 0,
            'suspicious_count': 0,
            'fraud_rate': 0.0,
            'total_volume': 0,
            'avg_risk_score': 0.0
        }
        
    total_tx = len(df)
    suspicious_count = df['is_suspicious'].sum() if 'is_suspicious' in df.columns else 0
    
    risk_score_col = 'risk_score' if 'risk_score' in df.columns else 'is_suspicious'
    avg_risk = df[risk_score_col].mean() if risk_score_col in df.columns else 0.0
    
    return {
        'total_transactions': total_tx,
        'suspicious_count': int(suspicious_count),
        'fraud_rate': (suspicious_count / total_tx) * 100 if total_tx > 0 else 0,
        'total_volume': df['amount'].sum(),
        'avg_risk_score': float(avg_risk)
    }
