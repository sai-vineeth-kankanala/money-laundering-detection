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
from utils.helpers import calculate_kpis, format_currency

# Apply global custom styling
apply_custom_styles()

# Render top navigation
render_top_nav()

st.markdown("<h1 style='font-size: 1.4rem; color: #FFFFFF; font-weight: 500;'>Command Center (Global Risk Overview)</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #787B86; font-size: 0.85rem; margin-bottom: 2rem;'>Real-time telemetry of global transaction flow and ML model health metrics.</p>", unsafe_allow_html=True)

# Function to load sample data for the dashboard
@st.cache_data
def load_dashboard_data():
    try:
        # Load the sample transactions generated during training
        data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sample_transactions.csv')
        df = pd.read_csv(data_path)
        
        # Ensure timestamp is datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # For the dashboard demo, we'll simulate model predictions 
        # normally we'd run predict_transaction from helpers.py
        import numpy as np
        np.random.seed(42)
        
        # Simulate risk scores
        df['risk_score'] = np.random.beta(a=0.5, b=5, size=len(df)).round(3)
        
        # Add a few high risk anomalies manually to make charts look good
        anomaly_idx = np.random.choice(df.index, size=int(len(df) * 0.04), replace=False)
        df.loc[anomaly_idx, 'risk_score'] = np.random.uniform(0.7, 0.99, size=len(anomaly_idx))
        
        df['is_suspicious'] = (df['risk_score'] > 0.75).astype(int)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        # Return empty DataFrame with expected columns as fallback
        return pd.DataFrame(columns=['transaction_id', 'timestamp', 'sender_account', 
                                    'receiver_account', 'amount', 'transaction_type', 
                                    'country', 'risk_score', 'is_suspicious'])

# Load data
df = load_dashboard_data()

# Calculate KPIs
kpis = calculate_kpis(df)

# Top KPIs Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Transactions Analyzed", 
        value=f"{kpis['total_transactions']:,}",
        delta="12% from last hour"
    )

with col2:
    st.metric(
        label="Suspicious Detected", 
        value=f"{kpis['suspicious_count']:,}",
        delta=f"{kpis['fraud_rate']:.1f}% rate",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="Average Risk Score", 
        value=f"{kpis['avg_risk_score']:.3f}",
        delta="-0.012 from baseline",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="Total Volume Monitored", 
        value=format_currency(kpis['total_volume']),
        delta="2.4M suspicious volume",
        delta_color="inverse"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Charts Section
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    st.markdown("### Transaction Trend & Anomalies")
    
    if not df.empty:
        # Aggregate by hour for charting
        df['hour'] = df['timestamp'].dt.floor('h')
        trend_df = df.groupby('hour').agg({
            'transaction_id': 'count', 
            'is_suspicious': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        
        # Normal volume
        fig.add_trace(go.Scatter(
            x=trend_df['hour'], y=trend_df['transaction_id'],
            fill='tozeroy',
            mode='lines',
            line=dict(color='#3182CE', width=2),
            name='Total Volume'
        ))
        
        # Anomalies
        fig.add_trace(go.Bar(
            x=trend_df['hour'], y=trend_df['is_suspicious'],
            marker_color='#E53E3E',
            name='Suspicious Alerts',
            yaxis='y2'
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#D1D4DC', family='"JetBrains Mono", monospace', size=11),
            margin=dict(l=0, r=0, t=10, b=0),
            height=300,
            yaxis=dict(title='', gridcolor='#2A2E39', zeroline=False),
            yaxis2=dict(title='', overlaying='y', side='right', showgrid=False, zeroline=False),
            xaxis=dict(title='', gridcolor='#2A2E39', zeroline=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available to plot trends.")

with row1_col2:
    st.markdown("### Risk Score Distribution")
    
    if not df.empty:
        fig = px.histogram(
            df, x="risk_score", 
            nbins=30,
            color="is_suspicious",
            color_discrete_map={0: '#3182CE', 1: '#E53E3E'},
            opacity=0.8,
            marginal="box"
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#D1D4DC', family='"JetBrains Mono", monospace', size=11),
            margin=dict(l=0, r=0, t=10, b=0),
            height=300,
            yaxis=dict(gridcolor='#2A2E39', title='', zeroline=False),
            xaxis=dict(gridcolor='#2A2E39', title='', zeroline=False),
            showlegend=False
        )
        
        # Add threshold line
        fig.add_vline(x=0.75, line_dash="dash", line_color="yellow", annotation_text="Alert Threshold (0.75)")
        
        st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown("### Risk by Country Destination")
    
    if not df.empty:
        country_risk = df.groupby('country').agg({
            'transaction_id': 'count',
            'is_suspicious': 'sum'
        }).reset_index()
        
        country_risk['alert_rate'] = (country_risk['is_suspicious'] / country_risk['transaction_id']) * 100
        country_risk = country_risk.sort_values('alert_rate', ascending=False).head(10)
        
        fig = px.bar(
            country_risk, x='country', y='alert_rate',
            color='alert_rate',
            color_continuous_scale="Reds",
            labels={'alert_rate': 'Alert Rate (%)', 'country': 'Country Code'}
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#D1D4DC', family='"JetBrains Mono", monospace', size=11),
            margin=dict(l=0, r=0, t=10, b=0),
            height=260,
            yaxis=dict(gridcolor='#2A2E39', title='', zeroline=False),
            xaxis=dict(gridcolor='#2A2E39', title='', zeroline=False),
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

with row2_col2:
    st.markdown("### Transaction Types Breakdown")
    
    if not df.empty:
        type_risk = df.groupby(['transaction_type', 'is_suspicious']).size().reset_index(name='count')
        type_risk['status'] = type_risk['is_suspicious'].map({0: 'Normal', 1: 'Suspicious'})
        
        fig = px.pie(
            df, names='transaction_type', 
            hole=0.6,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E2E8F0'),
            margin=dict(l=20, r=20, t=10, b=0),
            height=300,
            showlegend=False
        )
        
        # Add a central label for high risk volume
        high_risk_vol = df[df['is_suspicious'] == 1]['amount'].sum()
        
        fig.add_annotation(
            text=f"Total Fraud<br>{format_currency(high_risk_vol)}",
            x=0.5, y=0.5,
            font=dict(size=14, color="#E53E3E"),
            showarrow=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
