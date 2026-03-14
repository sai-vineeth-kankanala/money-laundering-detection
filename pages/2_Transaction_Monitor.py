import streamlit as st
import pandas as pd
import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import apply_custom_styles
from utils.navigation import render_top_nav
from utils.helpers import format_currency

# Apply global custom styling
apply_custom_styles()

# Render custom top navigation
render_top_nav()

st.markdown("<h1 style='font-size: 1.4rem; color: #FFFFFF; font-weight: 500;'>Triage Queue (Transaction Monitor)</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #787B86; font-size: 0.85rem; margin-bottom: 1rem;'>Filter, sort, and investigate transactions. Higher risk scores are highlighted for immediate compliance review.</p>", unsafe_allow_html=True)

# Cache data loading
@st.cache_data
def load_and_score_data():
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sample_transactions.csv')
        df = pd.read_csv(data_path)
        
        # Simulate predictions for demo
        import numpy as np
        np.random.seed(42)
        df['risk_score'] = np.random.beta(a=0.5, b=5, size=len(df)).round(3) * 100
        
        # Inject anomalies
        anomaly_idx = np.random.choice(df.index, size=int(len(df) * 0.05), replace=False)
        df.loc[anomaly_idx, 'risk_score'] = np.random.uniform(75, 99, size=len(anomaly_idx))
        
        # Add risk badges
        def get_risk_badge(score):
            if score >= 75:
                return '🔴 High'
            elif score >= 40:
                return '🟠 Medium'
            else:
                return '🟢 Low'
                
        df['risk_level'] = df['risk_score'].apply(get_risk_badge)
        
        # Format timestamps
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Fix column order
        cols = ['transaction_id', 'timestamp', 'sender_account', 'receiver_account', 
                'amount', 'transaction_type', 'country', 'risk_score', 'risk_level']
        
        return df[cols].sort_values('risk_score', ascending=False)
        
    except Exception as e:
        st.error(f"Data not available yet: {str(e)}")
        return pd.DataFrame()

df = load_and_score_data()

# Utility Bar for Filters
st.markdown("### 🔍 Filter and Triage Utility")

with st.expander("Advanced Filters & Export", expanded=True):
    fc1, fc2, fc3, fc4 = st.columns(4)
    
    with fc1:
        search_id = st.text_input("Search TXN ID or Account")
    
    with fc2:
        if not df.empty:
            types = ['All'] + list(df['transaction_type'].unique())
            selected_type = st.selectbox("Transaction Type", types)
        else:
            selected_type = 'All'
            
    with fc3:
        if not df.empty:
            risk_filter = st.slider("Minimum Risk Score Threshold", 0, 100, 50, help="Filter out low-risk transactions")
        else:
            risk_filter = 0
            
    with fc4:
        if not df.empty:
            amt_min, amt_max = st.slider("Amount Range ($)", min_value=0, max_value=1000000, value=(0, 1000000), step=5000)
        else:
            amt_min, amt_max = 0, 1000000
            
    # Export Button Row
    ec1, ec2 = st.columns([8, 2])
    with ec2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("📥 Export Grid to CSV", use_container_width=True)

# Apply filters
if not df.empty:
    filtered_df = df.copy()
    
    if search_id:
        # Case insensitive search across multiple columns
        mask = (
            filtered_df['transaction_id'].str.contains(search_id, case=False, na=False) |
            filtered_df['sender_account'].str.contains(search_id, case=False, na=False) |
            filtered_df['receiver_account'].str.contains(search_id, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
        
    # Apply risk filter
    filtered_df = filtered_df[filtered_df['risk_score'] >= risk_filter]
    
    # Apply type filter
    if selected_type != 'All':
        filtered_df = filtered_df[filtered_df['transaction_type'] == selected_type]
        
    # Apply amount filter
    filtered_df = filtered_df[(filtered_df['amount'] >= amt_min) & (filtered_df['amount'] <= amt_max)]
    
    st.markdown(f"**Showing {len(filtered_df)} transactions out of {len(df)} total.**")
    
    # Format currency for display
    display_df = filtered_df.copy()
    display_df['amount'] = display_df['amount'].apply(format_currency)
    display_df['risk_score'] = display_df['risk_score'].apply(lambda x: f"{x:.1f}")
    
    # Native Streamlit Dataframe with highlighting
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=600,
        column_config={
            "transaction_id": st.column_config.TextColumn("Transaction ID"),
            "timestamp": st.column_config.DatetimeColumn("Date/Time", format="YYYY-MM-DD HH:mm"),
            "sender_account": "Sender",
            "receiver_account": "Receiver",
            "amount": "Value ($)",
            "transaction_type": "Type",
            "country": "Country",
            "risk_score": st.column_config.NumberColumn("Risk Score", help="0-100 ML Score"),
            "risk_level": "Severity",
        }
    )
elif df.empty:
    st.warning("No transactions loaded. Did you train the model and generate data?")
