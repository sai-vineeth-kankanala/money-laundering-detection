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

st.markdown("<h1 style='font-size: 1.4rem; color: #FFFFFF; font-weight: 500;'>Risk Networks (Topology & Clustering)</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #787B86; font-size: 0.85rem; margin-bottom: 2rem;'>Deep-dive analytics into high-risk entities, behavioral anomalies, and transaction clustering.</p>", unsafe_allow_html=True)

@st.cache_data
def load_risk_data():
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
        df['is_suspicious'] = (df['risk_score'] >= 75).astype(int)
        
        return df
    except Exception:
        return pd.DataFrame()

df = load_risk_data()

if df.empty:
    st.warning("No data available.")
else:
    tab1, tab2 = st.tabs(["Entity Risk Profiling", "Behavioral Clusters"])
    
    with tab1:
        st.markdown("### Top High-Risk Accounts")
        
        col1, col2 = st.columns([1, 1])
        
        # Calculate risk per sender
        sender_risk = df.groupby('sender_account').agg(
            total_tx=('transaction_id', 'count'),
            suspicious_tx=('is_suspicious', 'sum'),
            avg_risk=('risk_score', 'mean'),
            total_volume=('amount', 'sum')
        ).reset_index()
        
        sender_risk = sender_risk[sender_risk['suspicious_tx'] > 0]
        sender_risk = sender_risk.sort_values(['suspicious_tx', 'avg_risk'], ascending=[False, False]).head(10)
        
        with col1:
            fig = px.bar(
                sender_risk, 
                x='suspicious_tx', 
                y='sender_account', 
                orientation='h',
                color='avg_risk',
                color_continuous_scale='Reds',
                labels={'suspicious_tx': 'Suspicious Transactions', 'sender_account': 'Account ID', 'avg_risk': 'Avg Risk'}
            )
            
            fig.update_layout(
                yaxis={'categoryorder':'total ascending'},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#D1D4DC', family='"JetBrains Mono", monospace', size=11),
                height=350,
                margin=dict(l=0, r=0, t=10, b=0),
                coloraxis_showscale=False,
                xaxis=dict(gridcolor='#2A2E39', zeroline=False),
                yaxis_title=""
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            display_accounts = sender_risk.copy()
            display_accounts['total_volume'] = display_accounts['total_volume'].apply(format_currency)
            display_accounts['avg_risk'] = display_accounts['avg_risk'].apply(lambda x: f"{x:.1f}")
            
            st.dataframe(
                display_accounts[['sender_account', 'suspicious_tx', 'avg_risk', 'total_volume']],
                use_container_width=True,
                hide_index=True,
                height=350
            )
            
    with tab2:
        st.markdown("### Transaction Clustering (Amount vs Time)")
        
        # Create a scatter plot to identify structural clusters
        # e.g., smurfing (many small transactions over time)
        
        # Just plot a sample to avoid overloading
        sample_df = df.sample(min(2000, len(df)), random_state=42)
        sample_df['hour'] = pd.to_datetime(sample_df['timestamp']).dt.hour
        
        fig = px.scatter(
            sample_df,
            x='hour',
            y='amount',
            color='is_suspicious',
            size='risk_score',
            hover_data=['transaction_id', 'sender_account', 'transaction_type'],
            color_discrete_map={0: 'rgba(49, 130, 206, 0.5)', 1: 'rgba(229, 62, 62, 0.9)'},
            log_y=True,
            labels={'amount': 'Transaction Amount (Log Scale)', 'hour': 'Hour of Day'}
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#D1D4DC', family='"JetBrains Mono", monospace', size=11),
            height=500,
            xaxis=dict(gridcolor='#2A2E39', tickmode='linear', tick0=0, dtick=2, zeroline=False),
            yaxis=dict(gridcolor='#2A2E39', zeroline=False),
            legend=dict(title='', orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Add annotation for hypothetical cluster
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=0, y0=3.8, x1=4, y1=4.2,
            line_color="yellow",
            line_width=2,
            line_dash="dash",
        )
        
        fig.add_annotation(
            x=2, y=4.4,
            text="High-Risk Late Night Transfers",
            showarrow=False,
            font=dict(color="yellow")
        )
        
        st.plotly_chart(fig, use_container_width=True)
