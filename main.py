# main.py

import streamlit as st
import time
import pandas as pd
from query import (
    HARDCODED_QUESTIONS,
    HARDCODED_RESPONSES,
    HARDCODED_XAI,
    DEFAULT_XAI_DETAILS
)
from trend import get_hardcoded_data, run_time_series_analysis


# --- Page Configuration (First command) ---
st.set_page_config(
    page_title="FloatChat - The Thinking Ocean",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --- PREMIUM OCEAN THEME WITH ADVANCED ANIMATIONS ---
def apply_premium_theme():
    """Injects premium CSS for an immersive ocean-themed UI with advanced animations."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@200;300;400;600;700;900&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=JetBrains+Mono:wght@300;400;600&display=swap');
            
            :root {
                --primary-deep: #000814;
                --ocean-dark: #001d3d;
                --ocean-mid: #003566;
                --ocean-light: #006494;
                --accent-cyan: #00f2fe;
                --accent-aqua: #4ecdc4;
                --accent-foam: #a8dadc;
                --glow-cyan: rgba(0, 242, 254, 0.8);
                --glow-soft: rgba(78, 205, 196, 0.4);
                --text-primary: #f1faee;
                --text-secondary: #a8dadc;
                --text-dim: #6c8ea0;
                --surface-glass: rgba(0, 29, 61, 0.4);
                --surface-dark: rgba(0, 8, 20, 0.8);
                --border-subtle: rgba(78, 205, 196, 0.2);
                --border-glow: rgba(0, 242, 254, 0.5);
                --font-display: 'Bebas Neue', sans-serif;
                --font-serif: 'Playfair Display', serif;
                --font-sans: 'Montserrat', sans-serif;
                --font-mono: 'JetBrains Mono', monospace;
            }
            
            /* Keyframe Animations */
            @keyframes waveMotion {
                0%, 100% { transform: translateX(0) translateY(0) rotate(0deg); }
                25% { transform: translateX(-20px) translateY(-5px) rotate(-1deg); }
                50% { transform: translateX(15px) translateY(3px) rotate(1deg); }
                75% { transform: translateX(-10px) translateY(-3px) rotate(-0.5deg); }
            }
            
            @keyframes floatBubble {
                0% { transform: translateY(100vh) translateX(0) scale(0); opacity: 0; }
                10% { opacity: 0.4; transform: translateY(90vh) translateX(10px) scale(0.8); }
                50% { opacity: 0.6; transform: translateY(50vh) translateX(-20px) scale(1); }
                90% { opacity: 0.3; transform: translateY(10vh) translateX(10px) scale(0.9); }
                100% { transform: translateY(-10vh) translateX(0) scale(0.6); opacity: 0; }
            }
            
            @keyframes shimmer {
                0% { background-position: -1000px 0; }
                100% { background-position: 1000px 0; }
            }
            
            @keyframes pulseGlow {
                0%, 100% { box-shadow: 0 0 20px var(--glow-soft), inset 0 0 20px rgba(0, 242, 254, 0.1); }
                50% { box-shadow: 0 0 40px var(--glow-cyan), inset 0 0 30px rgba(0, 242, 254, 0.2); }
            }
            
            @keyframes rippleEffect {
                0% { transform: scale(0.8); opacity: 1; }
                100% { transform: scale(2); opacity: 0; }
            }
            
            @keyframes slideInFromOcean {
                0% { 
                    opacity: 0; 
                    transform: translateY(50px) scale(0.9); 
                    filter: blur(10px);
                }
                50% { filter: blur(3px); }
                100% { 
                    opacity: 1; 
                    transform: translateY(0) scale(1); 
                    filter: blur(0);
                }
            }
            
            @keyframes deepBreath {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            @keyframes currentFlow {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            /* Animated Ocean Background */
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(180deg, 
                    var(--primary-deep) 0%,
                    var(--ocean-dark) 20%,
                    var(--ocean-mid) 60%,
                    var(--ocean-light) 100%);
                position: relative;
                overflow: hidden;
            }
            
            [data-testid="stAppViewContainer"]::before {
                content: '';
                position: fixed;
                top: 0;
                left: -100%;
                width: 300%;
                height: 100%;
                background: linear-gradient(
                    90deg,
                    transparent,
                    rgba(0, 242, 254, 0.03),
                    transparent
                );
                animation: currentFlow 20s ease-in-out infinite;
                pointer-events: none;
                z-index: 1;
            }
            
            /* Floating Bubble Particles */
            [data-testid="stAppViewContainer"]::after {
                content: '';
                position: fixed;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                pointer-events: none;
                background-image: 
                    radial-gradient(circle at 20% 80%, rgba(78, 205, 196, 0.3) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(0, 242, 254, 0.2) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(168, 218, 220, 0.2) 0%, transparent 50%);
                animation: floatBubble 25s ease-in-out infinite;
                z-index: 1;
            }
            
            /* Sidebar Premium Styling */
            [data-testid="stSidebar"] > div:first-child {
                background: linear-gradient(135deg, 
                    var(--surface-dark) 0%,
                    var(--surface-glass) 100%);
                backdrop-filter: blur(20px) saturate(180%);
                border-right: 1px solid var(--border-glow);
                box-shadow: 
                    inset 0 0 40px rgba(0, 242, 254, 0.05),
                    0 0 80px rgba(0, 242, 254, 0.1);
                max-height: 95vh;
                overflow-y: auto;
                position: relative;
            }
            
            /* Animated Sidebar Title */
            .sidebar-title {
                font-family: var(--font-display);
                font-size: 1.8rem;
                letter-spacing: 2px;
                background: linear-gradient(90deg, 
                    var(--accent-cyan), 
                    var(--accent-aqua), 
                    var(--accent-cyan));
                background-size: 200% auto;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: shimmer 3s linear infinite;
                text-transform: uppercase;
                text-shadow: 0 0 30px var(--glow-cyan);
                margin-bottom: 1.5rem;
            }
            
            /* Premium Metric Cards */
            .metric-card {
                background: linear-gradient(135deg, 
                    var(--surface-glass) 0%, 
                    rgba(0, 100, 148, 0.2) 100%);
                border: 1px solid var(--border-subtle);
                border-radius: 20px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                position: relative;
                overflow: hidden;
                animation: slideInFromOcean 0.8s ease-out forwards, pulseGlow 4s ease-in-out infinite;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }
            
            .metric-card::before {
                content: '';
                position: absolute;
                top: -50%;
                right: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(
                    circle,
                    rgba(0, 242, 254, 0.1) 0%,
                    transparent 70%
                );
                animation: rippleEffect 3s ease-out infinite;
            }
            
            .metric-card:hover {
                transform: translateY(-5px) scale(1.02);
                box-shadow: 
                    0 15px 40px rgba(0, 242, 254, 0.3),
                    inset 0 0 30px rgba(0, 242, 254, 0.1);
                border-color: var(--accent-cyan);
            }
            
            .metric-card-value {
                font-family: var(--font-display);
                font-size: 3rem;
                letter-spacing: 1px;
                background: linear-gradient(180deg, var(--text-primary) 0%, var(--accent-cyan) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 
                    0 0 20px var(--glow-cyan),
                    0 0 40px var(--glow-soft);
                animation: deepBreath 3s ease-in-out infinite;
            }
            
            .metric-card-label {
                font-family: var(--font-sans);
                font-weight: 300;
                font-size: 0.9rem;
                color: var(--text-secondary);
                text-transform: uppercase;
                letter-spacing: 2px;
                margin-top: 0.5rem;
            }
            
            /* Chat Title Animation */
            .floatchat-title {
                font-family: var(--font-display);
                font-size: 5rem;
                letter-spacing: 5px;
                background: linear-gradient(90deg, 
                    var(--accent-foam) 0%,
                    var(--accent-cyan) 25%,
                    var(--accent-aqua) 50%,
                    var(--accent-cyan) 75%,
                    var(--accent-foam) 100%);
                background-size: 200% auto;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: shimmer 4s linear infinite, waveMotion 6s ease-in-out infinite;
                text-shadow: 
                    0 0 40px var(--glow-cyan),
                    0 0 80px var(--glow-soft),
                    0 0 120px rgba(0, 242, 254, 0.3);
                text-transform: uppercase;
            }
            
            .floatchat-subtitle {
                font-family: var(--font-serif);
                font-weight: 300;
                font-style: italic;
                font-size: 1.3rem;
                color: var(--text-secondary);
                opacity: 0;
                animation: slideInFromOcean 1.2s ease-out 0.3s forwards;
                letter-spacing: 3px;
            }
            
            /* Premium Chat Messages */
            [data-testid="stChatMessage"] {
                background: linear-gradient(135deg, 
                    var(--surface-glass) 0%,
                    rgba(0, 100, 148, 0.15) 100%);
                border: 1px solid var(--border-subtle);
                border-radius: 24px;
                backdrop-filter: blur(15px) saturate(150%);
                box-shadow: 
                    0 8px 32px rgba(0, 0, 0, 0.4),
                    inset 0 0 20px rgba(0, 242, 254, 0.05);
                margin-bottom: 1.5rem;
                padding: 1.5rem;
                position: relative;
                overflow: hidden;
                animation: slideInFromOcean 0.6s ease-out forwards;
                opacity: 0;
            }
            
            [data-testid="stChatMessage"]:nth-child(even) {
                background: linear-gradient(135deg, 
                    rgba(0, 100, 148, 0.15) 0%,
                    var(--surface-glass) 100%);
                animation-delay: 0.1s;
            }
            
            [data-testid="stChatMessage"]::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(
                    90deg,
                    transparent,
                    rgba(0, 242, 254, 0.1),
                    transparent
                );
                animation: shimmer 3s ease-in-out infinite;
            }
            
            /* Enhanced Buttons */
            .stButton > button {
                background: linear-gradient(135deg, 
                    var(--ocean-mid) 0%, 
                    var(--ocean-light) 100%);
                border: 1px solid var(--border-subtle);
                border-radius: 12px;
                color: var(--text-primary);
                font-family: var(--font-sans);
                font-weight: 600;
                letter-spacing: 1px;
                padding: 0.8rem 1.5rem;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                position: relative;
                overflow: hidden;
                text-transform: uppercase;
                font-size: 0.85rem;
            }
            
            .stButton > button::before {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
                background: radial-gradient(circle, var(--accent-cyan) 0%, transparent 70%);
                transform: translate(-50%, -50%);
                transition: width 0.5s, height 0.5s;
            }
            
            .stButton > button:hover::before {
                width: 300px;
                height: 300px;
            }
            
            .stButton > button:hover {
                transform: translateY(-3px) scale(1.05);
                box-shadow: 
                    0 10px 30px rgba(0, 242, 254, 0.4),
                    inset 0 0 20px rgba(0, 242, 254, 0.2);
                border-color: var(--accent-cyan);
                background: linear-gradient(135deg, 
                    var(--ocean-light) 0%, 
                    var(--accent-aqua) 100%);
            }
            
            /* Chat Input Premium Styling */
            [data-testid="stChatInput"] > div {
                background: linear-gradient(135deg, 
                    var(--surface-glass) 0%,
                    rgba(0, 100, 148, 0.2) 100%);
                border: 1px solid var(--border-glow);
                border-radius: 20px;
                backdrop-filter: blur(15px);
                box-shadow: 
                    0 4px 20px rgba(0, 0, 0, 0.3),
                    inset 0 0 30px rgba(0, 242, 254, 0.05);
                animation: pulseGlow 4s ease-in-out infinite;
            }
            
            /* Expander Styling */
            .streamlit-expanderHeader {
                background: linear-gradient(90deg, 
                    var(--surface-glass) 0%, 
                    rgba(0, 100, 148, 0.1) 100%);
                border-radius: 12px;
                border: 1px solid var(--border-subtle);
                transition: all 0.3s ease;
            }
            
            .streamlit-expanderHeader:hover {
                background: linear-gradient(90deg, 
                    rgba(0, 100, 148, 0.2) 0%, 
                    var(--surface-glass) 100%);
                border-color: var(--accent-cyan);
                box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
            }
            
            /* Tabs Premium Styling */
            .stTabs [data-baseweb="tab-list"] {
                background: linear-gradient(90deg, 
                    var(--surface-glass) 0%,
                    rgba(0, 100, 148, 0.1) 100%);
                border-radius: 16px;
                padding: 0.5rem;
                border: 1px solid var(--border-subtle);
                backdrop-filter: blur(10px);
            }
            
            .stTabs [data-baseweb="tab"] {
                background: transparent;
                color: var(--text-secondary);
                border-radius: 12px;
                transition: all 0.3s ease;
                font-family: var(--font-sans);
                font-weight: 600;
                letter-spacing: 1px;
            }
            
            .stTabs [data-baseweb="tab"]:hover {
                background: rgba(0, 242, 254, 0.1);
                color: var(--accent-cyan);
            }
            
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, 
                    var(--ocean-mid) 0%, 
                    var(--ocean-light) 100%);
                color: var(--text-primary);
                box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
            }
            
            /* DataFrame Styling */
            .stDataFrame {
                border-radius: 16px;
                overflow: hidden;
                border: 1px solid var(--border-subtle);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            }
            
            /* Scrollbar Styling */
            ::-webkit-scrollbar {
                width: 12px;
                height: 12px;
            }
            
            ::-webkit-scrollbar-track {
                background: var(--surface-dark);
                border-radius: 10px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(180deg, 
                    var(--ocean-light) 0%, 
                    var(--ocean-mid) 100%);
                border-radius: 10px;
                border: 2px solid var(--surface-dark);
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(180deg, 
                    var(--accent-aqua) 0%, 
                    var(--ocean-light) 100%);
            }
            
            /* Loading Spinner Enhancement */
            .stSpinner > div {
                border-color: var(--accent-cyan) transparent transparent transparent;
            }
            
            /* Timestamp Label */
            .timestamp-label {
                font-family: var(--font-mono);
                font-size: 0.75rem;
                color: var(--text-dim);
                text-align: center;
                margin-top: 1.5rem;
                padding: 0.5rem;
                background: var(--surface-glass);
                border-radius: 8px;
                border: 1px solid var(--border-subtle);
                animation: slideInFromOcean 1s ease-out 0.5s forwards;
                opacity: 0;
            }
            
            /* Wave Animation Overlay */
            .wave-overlay {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 150px;
                background: linear-gradient(180deg, 
                    transparent 0%, 
                    rgba(0, 100, 148, 0.1) 100%);
                pointer-events: none;
                z-index: 2;
                animation: waveMotion 8s ease-in-out infinite;
            }
            
            /* Plotly Chart Container Enhancement */
            .js-plotly-plot {
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
                border: 1px solid var(--border-subtle);
                animation: slideInFromOcean 0.8s ease-out forwards;
            }
            
            /* Info Box Styling */
            .stInfo {
                background: linear-gradient(135deg, 
                    rgba(78, 205, 196, 0.1) 0%,
                    var(--surface-glass) 100%);
                border: 1px solid var(--accent-aqua);
                border-radius: 16px;
                color: var(--text-primary);
                animation: slideInFromOcean 0.6s ease-out forwards;
            }
            
            /* Success/Warning/Error Messages */
            .stSuccess, .stWarning, .stError {
                border-radius: 16px;
                backdrop-filter: blur(10px);
                animation: slideInFromOcean 0.5s ease-out forwards;
            }
        </style>
        <div class="wave-overlay"></div>
    """, unsafe_allow_html=True)


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []


def handle_chat_prompt(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    assistant_message = {
        "role": "assistant",
        "content": (
            f"You asked: '{prompt}'. I'm currently processing this. "
            "(Assistant placeholder response)"
        ),
        "xai_details": HARDCODED_XAI.get(prompt, DEFAULT_XAI_DETAILS)
    }

    response_obj = HARDCODED_RESPONSES.get(prompt)

    with st.spinner("🌊 Diving into the ocean depths of data..."):
        time.sleep(1.5)  # Slightly longer for dramatic effect
        
        if response_obj:
            response_type = response_obj["type"]
            assistant_message["content"] = response_obj.get(
                "text_summary", response_obj.get("data", "")
            )

            if "dataframe" in response_obj:
                assistant_message["dataframe"] = response_obj["dataframe"]

            if response_type == "plot":
                plot_function = response_obj["plot_function"]
                assistant_message["plot_fig"] = plot_function(
                    response_obj["dataframe"]
                )

    st.session_state.messages.append(assistant_message)


# --- Main App Execution ---
apply_premium_theme()

# Animated Header
st.markdown(
    '''<div style="text-align: center; margin-bottom: 3rem;">
        <h1 class="floatchat-title">FloatChat</h1>
        <p class="floatchat-subtitle">Where Data Meets the Deep</p>
    </div>''', 
    unsafe_allow_html=True
)

# Sidebar with Premium Elements
with st.sidebar:
    st.markdown('<h3 class="sidebar-title">Ocean Pulse</h3>', unsafe_allow_html=True)
    
    # Animated Metric Cards
    st.markdown(
        '''<div class="metric-card">
            <div class="metric-card-value">3,847</div>
            <div class="metric-card-label">Active Floats</div>
        </div>''', 
        unsafe_allow_html=True
    )
    
    st.markdown(
        '''<div class="metric-card">
            <div class="metric-card-value">152</div>
            <div class="metric-card-label">New Profiles</div>
        </div>''', 
        unsafe_allow_html=True
    )
    
    st.markdown(
        '''<div class="metric-card">
            <div class="metric-card-value">28.1°C</div>
            <div class="metric-card-label">Avg Ocean Temp</div>
        </div>''', 
        unsafe_allow_html=True
    )
    
    st.markdown(
        '<p class="timestamp-label">🕐 Last sync: 28 Sep 2025 14:30 UTC</p>', 
        unsafe_allow_html=True
    )
    
    st.divider()
    
    st.markdown('<h3 class="sidebar-title">Command Bridge</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Clear", help="Reset conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("📊 Export", help="Export chat data", use_container_width=True):
            st.info("Export feature coming soon!")
    
    st.divider()
    
    st.markdown('<h3 class="sidebar-title">Quick Queries</h3>', unsafe_allow_html=True)
    
    def set_selected_question(question):
        st.session_state.selected_question = question

    for i, question in enumerate(HARDCODED_QUESTIONS):
        display_text = (question[:65] + '...') if len(question) > 65 else question
        st.button(
            f"🌊 {display_text}",
            key=f"hardcoded_q_{i}",
            on_click=set_selected_question,
            args=(question,),
            use_container_width=True
        )


# Main Content Tabs
tab1, tab2, tab3 = st.tabs(["🤖 **Ocean Assistant**", "📈 **Trend Analysis**", "🗺️ **Global View**"])

with tab1:
    if "selected_question" in st.session_state:
        prompt = st.session_state.selected_question
        del st.session_state.selected_question
        handle_chat_prompt(prompt)
        st.rerun()

    # Chat Messages with Enhanced Styling
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            is_assistant = message["role"] == "assistant"
            question_key = st.session_state.messages[i-1].get("content") if i > 0 else None
            response_obj = HARDCODED_RESPONSES.get(question_key)
            is_table = (
                is_assistant and response_obj and
                response_obj["type"] == "table"
            )

            if is_table:
                st.markdown(message["content"])
                st.dataframe(message["dataframe"], use_container_width=True)
            else:
                st.markdown(message["content"])

            if "plot_fig" in message:
                st.plotly_chart(
                    message["plot_fig"], use_container_width=True,
                    key=f"plotly_{i}"
                )
            
            if "dataframe" in message:
                csv = message["dataframe"].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"ocean_data_{i}.csv",
                    mime="text/csv",
                    key=f"download_{i}"
                )

            if is_assistant:
                with st.expander("🧠 Thought Process"):
                    st.markdown(
                        message["xai_details"], unsafe_allow_html=True
                    )

    # Premium Chat Input
    if user_input := st.chat_input("🌊 Ask about the ocean's secrets..."):
        handle_chat_prompt(user_input)
        st.rerun()

with tab2:
    st.markdown("### 📊 Deep Ocean Trend Analysis")
    st.info(
        "🌊 Explore temporal patterns in ocean data using advanced time-series analysis "
        "and machine learning forecasting models."
    )
    
    historical_data = get_hardcoded_data()

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        selected_region = st.selectbox(
            "🗺️ Ocean Region:", 
            options=historical_data['region'].unique()
        )
    with col2:
        selected_parameter = st.selectbox(
            "📏 Parameter:",
            options=historical_data['parameter'].unique()
        )
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🔍 Analyze", use_container_width=True)

    if analyze_btn:
        with st.spinner("🌊 Analyzing oceanic patterns..."):
            decomp_fig, forecast_fig = run_time_series_analysis(
                historical_data, selected_region, selected_parameter
            )

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 🔄 Seasonal Decomposition")
                st.caption("Revealing hidden patterns in ocean data")
                st.plotly_chart(decomp_fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 🔮 12-Month Forecast")
                st.caption("ML-powered predictions using Prophet")
                st.plotly_chart(forecast_fig, use_container_width=True)

with tab3:
    st.markdown("### 🌍 Global Ocean Monitoring")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌡️ Global SST Anomaly", "+0.3°C", "↑ 0.1°C from last month")
    with col2:
        st.metric("🧊 Arctic Ice Coverage", "4.2M km²", "↓ 5% year-over-year")
    with col3:
        st.metric("🌪️ Active Cyclones", "2", "Pacific & Atlantic")
    
    st.markdown("---")
    st.info("🗺️ Interactive global ocean visualization coming soon! Track float trajectories, temperature anomalies, and current patterns in real-time.")