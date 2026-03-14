import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import os
import sys

# Add current dir to path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.data_generator import generate_transactions, extract_features

def main():
    print("Generating synthetic transaction data...")
    # Generate 50,000 transactions with 5% anomalies
    df = generate_transactions(n_samples=50000, anomaly_fraction=0.05)
    
    # Save a small sample for the user to upload later (e.g., 500 rows)
    sample_df = df.sample(500, random_state=42).reset_index(drop=True)
    # Remove the target column to simulate an unlabeled upload, but keep transaction data
    sample_df_unlabeled = sample_df.drop(columns=['is_suspicious'])
    sample_df_unlabeled.to_csv('sample_transactions.csv', index=False)
    print("Saved 'sample_transactions.csv' for testing.")
    
    print("Extracting features...")
    X, mappings = extract_features(df)
    y = df['is_suspicious']
    
    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Training Random Forest Classifier model...")
    # We use class_weight='balanced' because money laundering is highly imbalanced
    model = RandomForestClassifier(
        n_estimators=100, 
        max_depth=10, 
        class_weight='balanced', 
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    print("\nModel Evaluation:")
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    print(classification_report(y_test, y_pred))
    print(f"ROC AUC Score: {roc_auc_score(y_test, y_proba):.4f}")
    
    # Save model and mappings together
    artifact = {
        'model': model,
        'mappings': mappings,
        'features': mappings['features']
    }
    
    joblib.dump(artifact, 'model.pkl')
    print("\nSaved model and artifacts to 'model.pkl'.")
    print("Training Complete!")

if __name__ == "__main__":
    main()
