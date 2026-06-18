import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import os

load_dotenv()

from agents.graph import agent

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Data Analysis Agent",
    page_icon="🤖",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f5f5f0; }
    .stTextInput > div > div > input {
        border-radius: 24px;
        border: 1px solid #d3d1c7;
        padding: 10px 16px;
    }
    .stButton > button {
        border-radius: 24px;
        background-color: #534AB7;
        color: white;
        border: none;
        padding: 10px 24px;
        font-size: 14px;
    }
    .stButton > button:hover {
        background-color: #3C3489;
        color: white;
    }
    .user-msg {
        background-color: #534AB7;
        color: white;
        padding: 12px 16px;
        border-radius: 12px 12px 2px 12px;
        margin: 8px 0;
        margin-left: 20%;
        font-size: 14px;
    }
    .agent-msg {
        background-color: #f1efe8;
        color: #2c2c2a;
        padding: 12px 16px;
        border-radius: 12px 12px 12px 2px;
        margin: 8px 0;
        margin-right: 20%;
        font-size: 14px;
    }
    .steps-badge {
        font-size: 11px;
        color: #888780;
        margin-left: 4px;
        margin-top: -4px;
    }
    .thinking-msg {
        background-color: #faeeda;
        color: #854F0B;
        padding: 10px 16px;
        border-radius: 12px;
        margin: 8px 0;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown("## 🤖 Data Analysis Agent")
st.markdown("*Powered by LangGraph · ReAct architecture · Llama 3.3 70b*")
st.divider()

# ── Session state for chat history ───────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False

# ── Display chat history ──────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="agent-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        if "steps" in msg:
            st.markdown(f'<div class="steps-badge">🔄 {msg["steps"]} reasoning steps</div>', unsafe_allow_html=True)

# ── Suggestion buttons ────────────────────────────────────────
st.markdown("**Quick questions:**")
col1, col2, col3, col4 = st.columns(4)

suggestion = None
with col1:
    if st.button("📂 Load CSV"):
        suggestion = "Load the sales CSV and summarize it"
with col2:
    if st.button("🌍 By Region"):
        suggestion = "What is the total sales by region?"
with col3:
    if st.button("📅 Top Months"):
        suggestion = "Show me the top 3 months by revenue"
with col4:
    if st.button("🔍 Anomalies"):
        suggestion = "Are there any anomalies in the data?"

# ── Text input ────────────────────────────────────────────────
with st.form(key="chat_form", clear_on_submit=True):
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            label="message",
            placeholder="Ask about your data...",
            label_visibility="collapsed"
        )
    with col_btn:
        submitted = st.form_submit_button("Send")

# ── Handle input ──────────────────────────────────────────────
def run_agent(message: str):
    st.session_state.messages.append({"role": "user", "content": message})

    with st.spinner("Agent is thinking and using tools..."):
        try:
            result = agent.invoke({"messages": [HumanMessage(content=message)]})
            final = result["messages"][-1]
            answer = final.content
            steps = len(result["messages"])
            st.session_state.messages.append({
                "role": "agent",
                "content": answer,
                "steps": steps
            })
        except Exception as e:
            st.session_state.messages.append({
                "role": "agent",
                "content": f"Error: {str(e)}"
            })

    st.rerun()

# Handle suggestion button click
if suggestion:
    run_agent(suggestion)

# Handle form submit
if submitted and user_input.strip():
    run_agent(user_input.strip())

# ── Empty state ───────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="agent-msg">
        Hi! I'm your data analysis agent. I can load CSV files, run pandas analysis,
        and answer questions about your data. Try clicking a quick question above or type below!
    </div>
    """, unsafe_allow_html=True)