import streamlit as st

def render_top_nav():
    """Renders a custom enterprise top navigation bar and handles routing."""
    
    st.markdown("""
        <style>
        .top-nav {
            display: flex;
            align-items: center;
            background-color: #0B0E14;
            border-bottom: 1px solid #2A2E39;
            padding: 10px 24px;
            margin-bottom: 24px;
            margin-top: -3rem; /* Offset Streamlit default padding */
        }
        .nav-logo {
            display: flex;
            align-items: center;
            margin-right: 48px;
        }
        .nav-logo .icon {
            font-size: 2.4rem;
            margin-right: 12px;
            filter: drop-shadow(0 0 10px rgba(49, 130, 206, 0.4));
        }
        .nav-logo .title {
            font-size: 2.0rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FFFFFF 0%, #90CDF4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        .nav-logo .subtitle {
            font-size: 1.1rem;
            font-weight: 500;
            color: #63B3ED;
            margin-left: 16px;
            padding-left: 16px;
            border-left: 2px solid #2A2E39;
            letter-spacing: 0px;
            align-self: center;
            margin-top: 4px;
        }
        .nav-status {
            margin-left: auto;
            display: flex;
            align-items: center;
            font-size: 0.8rem;
            color: #787B86;
        }
        .status-dot {
            height: 8px;
            width: 8px;
            background-color: #38A169;
            border-radius: 50%;
            margin-right: 8px;
        }
        </style>
        
        <div class="top-nav">
            <div class="nav-logo">
                <span class="icon">🛡️</span>
                <span class="title">Money Laundering Detection</span>
                <span class="subtitle">using Machine Learning</span>
            </div>
            <div class="nav-status">
                <div class="status-dot"></div>
                SYSTEM ONLINE | V2.4.1
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # We use Streamlit columns to lay out the buttons to act as tabs
    c1, c2, c3, c4, c5, _ = st.columns([2, 2, 2, 2, 2, 6])
    
    current_page = st.session_state.get('current_page', 'Overview Dashboard')
    
    def nav_to(page_name, py_file):
        if current_page != page_name:
            st.session_state['current_page'] = page_name
            st.switch_page(py_file)

    with c1:
        if st.button("Command Center", type="primary" if current_page == 'Overview Dashboard' else "secondary", use_container_width=True):
            nav_to('Overview Dashboard', "pages/1_Overview_Dashboard.py")
    with c2:
        if st.button("Triage Queue", type="primary" if current_page == 'Transaction Monitor' else "secondary", use_container_width=True):
            nav_to('Transaction Monitor', "pages/2_Transaction_Monitor.py")
    with c3:
        if st.button("Inference Engine", type="primary" if current_page == 'Detection Engine' else "secondary", use_container_width=True):
            nav_to('Detection Engine', "pages/3_Detection_Engine.py")
    with c4:
        if st.button("Risk Networks", type="primary" if current_page == 'Risk Intelligence' else "secondary", use_container_width=True):
            nav_to('Risk Intelligence', "pages/4_Risk_Intelligence.py")
    with c5:
        if st.button("Regulatory Reports", type="primary" if current_page == 'Compliance Insights' else "secondary", use_container_width=True):
            nav_to('Compliance Insights', "pages/5_Compliance_Insights.py")
            
    st.markdown("<hr style='border: none; border-bottom: 1px solid #2A2E39; margin-top: 0; margin-bottom: 24px;'>", unsafe_allow_html=True)
