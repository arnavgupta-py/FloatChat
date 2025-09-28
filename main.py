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


# --- THEME, ANIMATIONS, & STYLE INJECTION ---
def apply_premium_theme():
    """Injects custom CSS for a premium, ocean-themed UI with animations."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&family=Playfair+Display:ital,wght@0,700&family=JetBrains+Mono:wght@400&display=swap');
            
            :root {
                --primary-deep-blue: #02040a; --accent-cyan: #00f2fe;
                --accent-glow: rgba(0, 242, 254, 0.6); --text-primary: #e6f1ff;
                --text-secondary: #a7c0e0; --surface-glass: rgba(11, 26, 58, 0.6);
                --border-color: rgba(66, 151, 160, 0.3); --font-sans: 'Montserrat', sans-serif;
                --font-serif: 'Playfair Display', serif; --font-mono: 'JetBrains Mono', monospace;
            }
            
            @keyframes slideUp { 
                0% { opacity: 0; transform: translateY(15px); } 
                100% { opacity: 1; transform: translateY(0); } 
            }

            [data-testid="stAppViewContainer"] {
                background: radial-gradient(circle at 50% 20%, #002b40, #000814 80%);
            }
            
            /* --- Sidebar Styling & Scroll --- */
            [data-testid="stSidebar"] > div:first-child {
                background: var(--surface-glass); backdrop-filter: blur(15px);
                border-right: 1px solid var(--border-color);
                max-height: 95vh; overflow-y: auto;
            }
            .sidebar-title { 
                font-family: var(--font-sans); font-weight: 600; font-size: 1.2rem; 
                color: var(--accent-cyan); animation: slideUp 0.5s ease-out; 
            }
            .metric-card { 
                background: rgba(2, 4, 10, 0.6); border: 1px solid var(--border-color); 
                border-radius: 16px; padding: 1rem; text-align: center; 
                animation: slideUp 0.6s ease-out;
            }
            .metric-card-value { 
                font-family: var(--font-sans); font-weight: 700; font-size: 2rem; 
                color: var(--text-primary); text-shadow: 0 0 5px var(--accent-glow); 
            }
            .metric-card-label { font-family: var(--font-sans); font-size: 0.8rem; color: var(--text-secondary); }
            .timestamp-label { 
                font-family: var(--font-sans); font-size: 0.8rem; color: var(--text-secondary); 
                text-align: center; margin-top: 1rem; animation: slideUp 0.7s ease-out; 
            }
            [data-testid="stSidebar"] .stButton button { 
                transition: all 0.3s ease-in-out; 
                animation: slideUp 0.8s ease-out; 
            }
            [data-testid="stSidebar"] .stButton button:hover { 
                transform: scale(1.05); border-color: var(--accent-cyan); 
                box-shadow: 0 0 15px var(--accent-glow); 
            }
            
            /* --- Chat Styling & Animations --- */
            .floatchat-title { font-family: var(--font-serif); font-size: 3.5rem; color: var(--text-primary); text-shadow: 0 0 25px var(--accent-glow); }
            .floatchat-subtitle { font-family: var(--font-sans); font-weight: 300; font-size: 1.1rem; color: var(--text-secondary); margin-top: -1rem; }
            [data-testid="stChatMessage"] {
                background: var(--surface-glass); border: 1px solid var(--border-color);
                border-radius: 20px; backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                animation: slideUp 0.5s ease-out forwards;
                animation-delay: 0.1s;
                opacity: 0;
            }
        </style>
    """, unsafe_allow_html=True)


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

    with st.spinner("Consulting the deep currents of data..."):
        time.sleep(1)
        
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

st.markdown(
    '<div style="text-align: center;"><h1 class="floatchat-title">FloatChat</h1>'
    '<p class="floatchat-subtitle">The Thinking Ocean</p></div>', 
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown('<h3 class="sidebar-title">Live Status</h3>', unsafe_allow_html=True)
    st.markdown(
        '<div class="metric-card"><div class="metric-card-value">3,847</div>'
        '<div class="metric-card-label">Active Floats</div></div>', 
        unsafe_allow_html=True
    )
    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="metric-card"><div class="metric-card-value">152</div>'
        '<div class="metric-card-label">New Profiles (24h)</div></div>', 
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="timestamp-label">Data updated on:<br>28 Sep 2025 at 14:30 UTC</p>', 
        unsafe_allow_html=True
    )
    st.divider()

    st.markdown('<h3 class="sidebar-title">Chat Controls</h3>', unsafe_allow_html=True)
    if st.button("Clear Chat", help="Clear the conversation history", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.subheader("Try These Questions:")
    
    def set_selected_question(question):
        st.session_state.selected_question = question

    for i, question in enumerate(HARDCODED_QUESTIONS):
        # Use a more robust key and trim the question for display
        display_text = (question[:70] + '...') if len(question) > 70 else question
        st.button(
            display_text,
            key=f"hardcoded_q_{i}",
            on_click=set_selected_question,
            args=(question,),
            use_container_width=True
        )


tab1, tab2 = st.tabs(["**Chatbot**", "**Trends Dashboard**"])

with tab1:
    if "selected_question" in st.session_state:
        prompt = st.session_state.selected_question
        del st.session_state.selected_question
        handle_chat_prompt(prompt)
        st.rerun()

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
                    label="Download Data as CSV",
                    data=csv,
                    file_name=f"float_chat_data_{i}.csv",
                    mime="text/csv",
                    key=f"download_{i}"
                )

            if is_assistant:
                with st.expander("Show thought process..."):
                    st.markdown(
                        message["xai_details"], unsafe_allow_html=True
                    )

    if user_input := st.chat_input("Ask a question about ARGO ocean data..."):
        handle_chat_prompt(user_input)
        st.rerun()

with tab2:
    st.header("Analyze Historical Trends")
    st.info(
        "This dashboard uses the Parquet data archive for deep "
        "time-series analysis and forecasting."
    )
    historical_data = get_hardcoded_data()

    col1, col2 = st.columns(2)
    with col1:
        selected_region = st.selectbox(
            "Select a Region:", options=historical_data['region'].unique()
        )
    with col2:
        selected_parameter = st.selectbox(
            "Select a Parameter:",
            options=historical_data['parameter'].unique()
        )

    if st.button("Run Analysis", use_container_width=True):
        with st.spinner("Performing time-series analysis..."):
            decomp_fig, forecast_fig = run_time_series_analysis(
                historical_data, selected_region, selected_parameter
            )

            st.subheader("Time-Series Decomposition")
            st.markdown(
                "This plot breaks down the data into its core components: "
                "the long-term **Trend**, repeating **Seasonal** patterns, "
                "and random **Residuals**."
            )
            st.plotly_chart(decomp_fig, use_container_width=True)

            st.subheader("12-Month Forecast")
            st.markdown(
                "This plot shows historical data, a 12-month forecast, "
                "and its uncertainty interval, generated using the Prophet model."
            )
            st.plotly_chart(forecast_fig, use_container_width=True)