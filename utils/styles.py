import streamlit as st
import base64
import os

def apply_custom_styles():
    """Apply custom CSS to give the Streamlit app a modern fintech look."""
    
    # Inject animated CSS gradient background (Abstract & Network safe)
    video_html = """
    <style>
    .video-background {
        position: fixed;
        right: 0;
        bottom: 0;
        width: 100vw; 
        height: 100vh;
        z-index: -100;
        background: linear-gradient(315deg, #0B0E14, #1a2333, #0f1c2e, #0B0E14);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    <div class="video-background"></div>
    """
    st.markdown(video_html, unsafe_allow_html=True)
        
    # We define a CSS string with professional styling
    custom_css = """
    <style>
    /* Global Background and Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    /* Modify main background layers to transparent so the video shows through */
    .stApp, .stApp > header {
        background-color: transparent !important;
    }
    
    .stApp > div {
        background-color: transparent !important;
    }
    
    html, body {
        background-color: #0B0E14 !important;
        color: #D1D4DC !important;
    }
    
    /* Hide Default Streamlit Chrome entirely */
    #scrollToTopButton {display: none;}
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    header[data-testid="stHeader"] {display: none !important;}
    footer {visibility: hidden;}
    
    /* Metrics block styling (Cards) */
    [data-testid="stMetric"] {
        background-color: #1E222D;
        border-radius: 4px;
        padding: 12px 16px;
        border: 1px solid #2A2E39;
        /* No dropshadows for flatter enterprise look */
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        color: #787B86 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetricDelta"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
    }
    
    /* Custom Risk Badge */
    .risk-high {
        background-color: transparent;
        color: #E53E3E;
        font-weight: 700;
        font-size: 0.85rem;
    }
    
    .risk-medium {
        background-color: transparent;
        color: #DD6B20;
        font-weight: 700;
        font-size: 0.85rem;
    }
    
    .risk-low {
        background-color: transparent;
        color: #38A169;
        font-weight: 700;
        font-size: 0.85rem;
    }
    
    /* Dataframes and Tables */
    [data-testid="stDataFrame"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem;
    }
    
    .dataframe {
        border-collapse: collapse;
        width: 100%;
        color: #D1D4DC;
        font-size: 0.8rem;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .dataframe th {
        background-color: #131722 !important;
        color: #787B86 !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.7rem;
        letter-spacing: 0.05em;
        border-bottom: 1px solid #2A2E39 !important;
        padding: 8px 12px !important;
    }
    
    .dataframe td {
        border-bottom: 1px solid #1E222D !important;
        padding: 8px 12px !important;
        color: #D1D4DC;
    }
    
    .suspicious-row {
        background-color: rgba(229, 62, 62, 0.08) !important;
    }
    
    /* Expander / Drawer styling for a cleaner look */
    .streamlit-expanderHeader {
        background-color: #1E222D !important;
        border-radius: 4px;
        border: 1px solid #2A2E39;
        margin-top: 8px;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Hide top padding and Streamlit toolbar for cleaner look */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 98% !important;
    }
    
    /* Custom button styling */
    .stButton > button {
        background-color: #1E222D;
        color: #D1D4DC;
        border-radius: 4px;
        border: 1px solid #2A2E39;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        transition: all 0.1s;
        padding: 4px 12px;
    }
    
    .stButton > button:hover {
        background-color: #2A2E39;
        border-color: #787B86;
        color: #FFFFFF;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #2962FF;
        color: white;
        border: none;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #1E4ED8;
    }
    
    /* Clean up select boxes and inputs */
    [data-baseweb="select"], [data-baseweb="input"] {
        background-color: #1E222D !important;
        border: 1px solid #2A2E39 !important;
    }
    
    div[data-baseweb="base-input"] > input {
        color: #D1D4DC !important;
    }
    
    /* Enhance visibility over background image */
    [data-testid="stMetric"], .dataframe, .streamlit-expanderHeader {
        background-color: rgba(30, 34, 45, 0.95) !important;
        backdrop-filter: blur(10px);
    }
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)
