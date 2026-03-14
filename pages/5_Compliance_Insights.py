import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

st.markdown("<h1 style='font-size: 1.4rem; color: #FFFFFF; font-weight: 500;'>Compliance Command Executive Summary</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #787B86; font-size: 0.85rem; margin-bottom: 2rem;'>High-level reporting and regulatory compliance summaries for Chief Risk Officers (CROs).</p>", unsafe_allow_html=True)

@st.cache_data
def load_compliance_data():
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sample_transactions.csv')
        df = pd.read_csv(data_path)
        
        # Simulate predictions
        import numpy as np
        np.random.seed(42)
        df['risk_score'] = np.random.beta(a=0.5, b=5, size=len(df)).round(3) * 100
        df['is_suspicious'] = (df['risk_score'] >= 75).astype(int)
        
        return df
    except Exception:
        return pd.DataFrame()

df = load_compliance_data()

if df.empty:
    st.warning("No data available to generate insights.")
else:
    # Summary Metrics
    total_tx = len(df)
    suspicious_tx = df['is_suspicious'].sum()
    fraud_rate = (suspicious_tx / total_tx) * 100
    
    total_volume = df['amount'].sum()
    fraud_volume = df[df['is_suspicious'] == 1]['amount'].sum()
    fraud_volume_pct = (fraud_volume / total_volume) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='background-color: #1E222D; padding: 16px; border-radius: 4px; border: 1px solid #2A2E39;'>
            <h4 style='color: #787B86; margin-top: 0; font-size: 0.8rem; text-transform: uppercase;'>Suspicious Activity Rate</h4>
            <h2 style='color: #FFFFFF; font-family: "JetBrains Mono", monospace; font-size: 2.2rem; margin: 8px 0;'>{fraud_rate:.2f}%</h2>
            <p style='color: #E53E3E; margin: 0; font-family: "JetBrains Mono", monospace; font-size: 0.8rem;'>▲ 0.14% from last quarter</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style='background-color: #1E222D; padding: 16px; border-radius: 4px; border: 1px solid #2A2E39;'>
            <h4 style='color: #787B86; margin-top: 0; font-size: 0.8rem; text-transform: uppercase;'>Value at Risk (VaR)</h4>
            <h2 style='color: #FFFFFF; font-family: "JetBrains Mono", monospace; font-size: 2.2rem; margin: 8px 0;'>{format_currency(fraud_volume)}</h2>
            <p style='color: #E53E3E; margin: 0; font-family: "JetBrains Mono", monospace; font-size: 0.8rem;'>▲ {fraud_volume_pct:.1f}% of total volume</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style='background-color: #1E222D; padding: 16px; border-radius: 4px; border: 1px solid #2A2E39;'>
            <h4 style='color: #787B86; margin-top: 0; font-size: 0.8rem; text-transform: uppercase;'>Regulatory Filings (SARs)</h4>
            <h2 style='color: #FFFFFF; font-family: "JetBrains Mono", monospace; font-size: 2.2rem; margin: 8px 0;'>142</h2>
            <p style='color: #38A169; margin: 0; font-family: "JetBrains Mono", monospace; font-size: 0.8rem;'>▼ 12 pending review</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    row2_col1, row2_col2 = st.columns([2, 1])
    
    with row2_col1:
        st.markdown("### Risk Segmentation")
        
        # Segment by Risk Level
        risk_counts = {
            'High (75-100)': len(df[df['risk_score'] >= 75]),
            'Medium (40-74)': len(df[(df['risk_score'] >= 40) & (df['risk_score'] < 75)]),
            'Low (0-39)': len(df[df['risk_score'] < 40])
        }
        
        segment_df = pd.DataFrame(list(risk_counts.items()), columns=['Risk Level', 'Count'])
        
        fig = px.pie(
            segment_df, 
            values='Count', 
            names='Risk Level',
            color='Risk Level',
            color_discrete_map={
                'High (75-100)': '#E53E3E',   # Red
                'Medium (40-74)': '#DD6B20',  # Orange
                'Low (0-39)': '#38A169'       # Green
            },
            hole=0.4
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#D1D4DC', family='"JetBrains Mono", monospace', size=11),
            margin=dict(l=0, r=0, t=10, b=0),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with row2_col2:
        st.markdown("### Regulatory Reports")
        
        st.markdown("""
        <div style='background-color: #1A202C; padding: 12px; border-radius: 4px; border-left: 3px solid #2962FF; margin-bottom: 12px;'>
            <h4 style='margin: 0; color: #FFFFFF; font-size: 0.9rem;'>Q3 AML Compliance Report</h4>
            <p style='margin: 4px 0 0 0; color: #787B86; font-size: 0.75rem;'>Generated: Oct 01, 2026</p>
        </div>
        
        <div style='background-color: #1A202C; padding: 12px; border-radius: 4px; border-left: 3px solid #2962FF; margin-bottom: 12px;'>
            <h4 style='margin: 0; color: #FFFFFF; font-size: 0.9rem;'>FinCEN CTR Export</h4>
            <p style='margin: 4px 0 0 0; color: #787B86; font-size: 0.75rem;'>Currency Transaction Reports > $10k</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.button("Generate New SAR Batch", use_container_width=True)
        st.button("Download Full Audit Log (.CSV)", use_container_width=True)
