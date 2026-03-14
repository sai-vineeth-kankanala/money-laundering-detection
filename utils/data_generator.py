import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_transactions(n_samples=10000, anomaly_fraction=0.03):
    """
    Generate synthetic transactions data simulating a financial environment.
    Creates both normal transactions and suspicious (money laundering) patterns.
    """
    np.random.seed(42)
    random.seed(42)
    
    # Configuration
    countries = ['US', 'UK', 'CA', 'AU', 'DE', 'FR', 'SG', 'AE', 'KY', 'PA']
    # KY (Cayman Islands) and PA (Panama) are sometimes considered high-risk in synthetic datasets
    high_risk_countries = ['KY', 'PA', 'AE']
    
    transaction_types = ['TRANSFER', 'CASH_OUT', 'CASH_IN', 'PAYMENT', 'DEBIT']
    
    # Generate base data
    data = {
        'transaction_id': [f"TRX-{i:07d}" for i in range(n_samples)],
        'timestamp': [datetime.now() - timedelta(minutes=random.randint(0, 30*24*60)) for _ in range(n_samples)],
        'sender_account': [f"ACC-{random.randint(1000, 9999)}" for _ in range(n_samples)],
        'receiver_account': [f"ACC-{random.randint(1000, 9999)}" for _ in range(n_samples)],
        'amount': np.random.lognormal(mean=5.0, sigma=1.5, size=n_samples).round(2),
        'transaction_type': np.random.choice(transaction_types, n_samples, p=[0.4, 0.2, 0.2, 0.15, 0.05]),
        'country': np.random.choice(countries, n_samples, p=[0.4, 0.15, 0.1, 0.05, 0.1, 0.05, 0.05, 0.05, 0.025, 0.025]),
        'is_suspicious': np.zeros(n_samples, dtype=int)
    }
    
    df = pd.DataFrame(data)
    
    # Avoid self-transfers initially
    df.loc[df['sender_account'] == df['receiver_account'], 'receiver_account'] = "ACC-9999"
    
    # Inject suspicious patterns
    n_anomalies = int(n_samples * anomaly_fraction)
    anomaly_indices = np.random.choice(df.index, n_anomalies, replace=False)
    
    for i, idx in enumerate(anomaly_indices):
        pattern_type = i % 4
        
        if pattern_type == 0:
            # Structuring (Smurfing): Just below reporting threshold (e.g., $10,000)
            df.at[idx, 'amount'] = round(random.uniform(9500, 9999), 2)
            df.at[idx, 'transaction_type'] = 'CASH_IN'
        elif pattern_type == 1:
            # High-risk country transfer
            df.at[idx, 'country'] = random.choice(high_risk_countries)
            df.at[idx, 'amount'] = round(random.uniform(50000, 500000), 2)
            df.at[idx, 'transaction_type'] = 'TRANSFER'
        elif pattern_type == 2:
            # Unusually large round number transfer
            df.at[idx, 'amount'] = float(random.choice([50000, 100000, 250000, 500000, 1000000]))
            df.at[idx, 'transaction_type'] = 'TRANSFER'
        elif pattern_type == 3:
            # Rapid movement (in this synthetic set, we simulate by high amounts with CASH_OUT)
            df.at[idx, 'amount'] = round(random.uniform(20000, 100000), 2)
            df.at[idx, 'transaction_type'] = 'CASH_OUT'
            
        df.at[idx, 'is_suspicious'] = 1
        
    # Sort by timestamp
    df = df.sort_values('timestamp').reset_index(drop=True)
    return df

def extract_features(df):
    """
    Extract ML features from raw transaction data.
    """
    df_features = df.copy()
    
    # Time based features
    df_features['hour'] = df_features['timestamp'].dt.hour
    df_features['day_of_week'] = df_features['timestamp'].dt.dayofweek
    df_features['is_weekend'] = df_features['day_of_week'].isin([5, 6]).astype(int)
    
    # Amount features
    # Log transform to handle right-skewed amounts
    df_features['amount_log'] = np.log1p(df_features['amount'])
    
    # Is amount a round number? (e.g., 50000.00)
    df_features['is_round_amount'] = (df_features['amount'] % 1000 == 0).astype(int)
    
    # Categorical encoding (simplified for Random Forest)
    # Target encoding or dummy variables
    high_risk_countries = ['KY', 'PA', 'AE']
    df_features['is_high_risk_country'] = df_features['country'].isin(high_risk_countries).astype(int)
    
    # Replace categorical with simple numerics for the model
    type_mapping = {t: i for i, t in enumerate(df_features['transaction_type'].unique())}
    df_features['type_encoded'] = df_features['transaction_type'].map(type_mapping)
    
    # Select final features for model
    features = [
        'amount_log', 
        'is_round_amount', 
        'hour', 
        'is_weekend', 
        'is_high_risk_country', 
        'type_encoded'
    ]
    
    X = df_features[features]
    
    # Keep mappings for later use if needed
    mappings = {
        'type_mapping': type_mapping,
        'features': features
    }
    
    return X, mappings
