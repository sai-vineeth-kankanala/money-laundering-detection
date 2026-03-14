import streamlit as st
from utils.styles import apply_custom_styles
from utils.navigation import render_top_nav
import time

# Must be the first Streamlit command
st.set_page_config(
    page_title="Money Laundering Detection",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply global custom styling
apply_custom_styles()

def main():
    # Render the custom enterprise top navigation
    render_top_nav()
    
    # Main application greeting on root page
    st.markdown("<h1 style='font-size: 1.5rem; color: #FFFFFF; font-weight: 500;'>Compliance Command Center Overview</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #787B86; font-size: 0.9rem; margin-bottom: 2rem;'>Select a module from the top navigation to begin forensic monitoring.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background-color: #1E222D; padding: 20px; border-radius: 4px; border: 1px solid #2A2E39; height: 100%; border-top: 3px solid #3182CE;'>
            <h3 style='color: #FFFFFF; margin-top: 0; font-size: 1.1rem;'>Command Center</h3>
            <p style='color: #A0AEC0; font-size: 0.85rem;'>View high-level risk metrics, fraud detection rates, and transaction volume trends across the global network.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style='background-color: #1E222D; padding: 20px; border-radius: 4px; border: 1px solid #2A2E39; height: 100%; border-top: 3px solid #E53E3E;'>
            <h3 style='color: #FFFFFF; margin-top: 0; font-size: 1.1rem;'>Triage Queue</h3>
            <p style='color: #A0AEC0; font-size: 0.85rem;'>Investigate individual transactions, apply advanced forensic filters, and identify suspicious activity in real-time.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style='background-color: #1E222D; padding: 20px; border-radius: 4px; border: 1px solid #2A2E39; height: 100%; border-top: 3px solid #38A169;'>
            <h3 style='color: #FFFFFF; margin-top: 0; font-size: 1.1rem;'>Risk Networks</h3>
            <p style='color: #A0AEC0; font-size: 0.85rem;'>Analyze complex topological relationships and behavioral clusters to uncover hidden money laundering rings.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
