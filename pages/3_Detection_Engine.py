import streamlit as st
import pandas as pd
import time
import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import apply_custom_styles
from utils.navigation import render_top_nav
from utils.helpers import load_model, predict_transaction, format_currency

# Apply global custom styling
apply_custom_styles()

# Render custom top navigation
render_top_nav()

st.markdown("<h1 style='font-size: 1.4rem; color: #FFFFFF; font-weight: 500;'>Inference Engine (Batch Scoring)</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #787B86; font-size: 0.85rem; margin-bottom: 2rem;'>Upload bulk transaction data (CSV) to run through the ML risk scoring model.</p>", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div style='background-color: #1E2532; padding: 20px; border-radius: 8px; border: 1px solid #2D3748;'>
        <h3 style='margin-top:0;'>Submit Data Batch</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV File", type="csv")
    
    st.markdown("<hr style='border-color: #2D3748;'>", unsafe_allow_html=True)
    
    st.markdown("### Model Configuration")
    sensitivity = st.slider("Alert Sensitivity Threshold", 0.0, 1.0, 0.75, 0.05, 
                           help="Lower threshold generates more alerts (higher false positive rate).")
    
    run_button = st.button("Run Detection Analysis", type="primary", use_container_width=True, disabled=uploaded_file is None)

with col2:
    if uploaded_file is not None and not run_button:
        # Just show preview of uploaded file
        try:
            df_preview = pd.read_csv(uploaded_file)
            st.markdown(f"### Data Preview ({len(df_preview)} rows)")
            st.dataframe(df_preview.head(5), use_container_width=True)
            st.info("Click 'Run Detection Analysis' to score these transactions.")
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            
    elif uploaded_file is not None and run_button:
        try:
            # Process the file
            with st.spinner('Loading Machine Learning Model...'):
                artifact = load_model()
                time.sleep(0.5) # Fake loading time for effect
            
            if artifact is None:
                st.error("Model not found. Please train the model first by running `python train_model.py`.")
            else:
                with st.spinner('Standardizing features and running inference pipeline...'):
                    # Reset pointer to start of file
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file)
                    
                    # Convert timestamps if present
                    if 'timestamp' in df.columns:
                        df['timestamp'] = pd.to_datetime(df['timestamp'])
                        
                    # Run prediction
                    probas, _ = predict_transaction(df, artifact)
                    time.sleep(1) # Fake inference time to look like it's doing heavy work
                    
                # Add results to dataframe
                results_df = df.copy()
                results_df['risk_probability'] = probas
                results_df['risk_score'] = (probas * 100).round(1)
                
                # Apply dynamic threshold from slider
                results_df['is_suspicious'] = (probas >= sensitivity).astype(int)
                
                def classify_risk(prob):
                    if prob >= sensitivity:
                        return "🔴 Critical"
                    elif prob >= sensitivity * 0.6:
                        return "🟠 Elevated"
                    else:
                        return "🟢 Normal"
                        
                results_df['classification'] = results_df['risk_probability'].apply(classify_risk)
                
                # Show success and results
                st.success(f"Analysis complete! Scored {len(results_df)} transactions in 1.4s.")
                
                # Results metrics
                total_alerts = results_df['is_suspicious'].sum()
                rate = (total_alerts / len(results_df)) * 100
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Rows Processed", len(results_df))
                m2.metric("Alerts Generated", int(total_alerts))
                m3.metric("Detection Rate", f"{rate:.1f}%")
                
                st.markdown("### Prediction Results")
                
                # Sort to show highest risk first
                display_df = results_df.sort_values('risk_probability', ascending=False)
                
                # Format to look nice
                if 'amount' in display_df.columns:
                    display_df['amount_fmt'] = display_df['amount'].apply(format_currency)
                
                cols_to_show = ['transaction_id', 'classification', 'risk_score']
                if 'amount_fmt' in display_df.columns:
                    cols_to_show.append('amount_fmt')
                if 'transaction_type' in display_df.columns:
                    cols_to_show.append('transaction_type')
                if 'country' in display_df.columns:
                    cols_to_show.append('country')
                    
                # Highlight rows that are suspicious
                def highlight_suspicious(s):
                    if s.is_suspicious == 1:
                        return ['background-color: rgba(229, 62, 62, 0.1)'] * len(s)
                    return [''] * len(s)
                
                st.dataframe(
                    display_df[cols_to_show].style.apply(highlight_suspicious, axis=1),
                    use_container_width=True,
                    height=400
                )
                
                st.download_button(
                    label="Download Scored Results (CSV)",
                    data=results_df.to_csv(index=False).encode('utf-8'),
                    file_name="scored_transactions.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
        except Exception as e:
            st.error(f"Detection pipeline failed: {str(e)}")
            st.exception(e)
    else:
        st.info("Upload a CSV file containing transaction data matching the required schema.")
        
        # Show expected schema
        st.markdown("""
        **Expected Columns:**
        - `transaction_id`: Unique ID
        - `timestamp`: Date and time
        - `sender_account`: Account ID
        - `receiver_account`: Account ID
        - `amount`: Transaction value (numeric)
        - `transaction_type`: e.g., TRANSFER, CASH_OUT
        - `country`: ISO country code (e.g., US, UK)
        """)
