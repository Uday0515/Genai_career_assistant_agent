"""
GenAI Career Assistant - Streamlit UI
A beautiful interface for the multi-agent career guidance system
"""

import streamlit as st
import os
from typing import Dict
from dotenv import load_dotenv
from main import create_agent_graph, AgentState

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="GenAI Career Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Header styling */
    .header-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .subtitle {
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        font-size: 1.2rem;
        font-weight: 300;
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        animation: fadeIn 1s ease-out;
    }
    
    /* Message bubbles */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        max-width: 80%;
        float: right;
        clear: both;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.5s ease-out;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        max-width: 80%;
        float: left;
        clear: both;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
        animation: slideInLeft 0.5s ease-out;
    }
    
    /* Category badges */
    .category-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.5rem;
        animation: pulse 2s infinite;
    }
    
    .learning-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .resume-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .interview-badge {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    .job-badge {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #667eea !important;
    }
    
    /* Markdown content in responses */
    .assistant-message h1, .assistant-message h2, .assistant-message h3 {
        color: white;
        margin-top: 1rem;
    }
    
    .assistant-message code {
        background: rgba(255, 255, 255, 0.2);
        padding: 0.2rem 0.4rem;
        border-radius: 5px;
    }
    
    .assistant-message pre {
        background: rgba(0, 0, 0, 0.2);
        padding: 1rem;
        border-radius: 10px;
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'agent' not in st.session_state:
    st.session_state.agent = create_agent_graph()

def get_category_badge(category: str, sub_category: str = "") -> str:
    """Generate HTML badge for category"""
    badge_class = ""
    badge_text = category
    
    if "Learning" in category:
        badge_class = "learning-badge"
        if sub_category:
            badge_text = f"{category} - {sub_category}"
    elif "Resume" in category:
        badge_class = "resume-badge"
    elif "Interview" in category:
        badge_class = "interview-badge"
        if sub_category:
            badge_text = f"{category} - {sub_category}"
    elif "Job" in category:
        badge_class = "job-badge"
    
    return f'<span class="category-badge {badge_class}">{badge_text}</span>'

def process_query(query: str) -> Dict:
    """Process user query through the agent"""
    initial_state = {
        "query": query,
        "category": "",
        "sub_category": "",
        "response": "",
        "search_results": ""
    }
    
    result = st.session_state.agent.invoke(initial_state)
    return result

# Header
st.markdown("""
<div class="header-container">
    <h1 class="main-title">🤖 GenAI Career Assistant</h1>
    <p class="subtitle">Your AI-powered guide for Generative AI careers</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 What I Can Help With")
    
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <h4 style="color: white;">📚 Learning</h4>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
        • Tutorials & Guides<br>
        • Q&A Support<br>
        • Code Examples
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <h4 style="color: white;">📄 Resume</h4>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
        • Resume Review<br>
        • ATS Optimization<br>
        • Skills Highlighting
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <h4 style="color: white;">💼 Interview</h4>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
        • Interview Prep<br>
        • Mock Interviews<br>
        • Common Questions
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <h4 style="color: white;">🔍 Job Search</h4>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
        • Job Strategies<br>
        • Company Research<br>
        • Networking Tips
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.7); font-size: 0.8rem;">
        <p>Powered by LangGraph & Gemini</p>
    </div>
    """, unsafe_allow_html=True)

# Main chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
    else:
        category_badge = get_category_badge(
            message.get("category", ""), 
            message.get("sub_category", "")
        )
        st.markdown(f'<div class="assistant-message">🤖 {category_badge}<br><br>{message["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Quick action buttons
st.markdown("### 💡 Quick Start Examples")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📚 RAG Tutorial", use_container_width=True):
        query = "Create a tutorial on how to build a RAG system with LangChain"
        st.session_state.messages.append({"role": "user", "content": query})
        st.rerun()

with col2:
    if st.button("📄 Resume Help", use_container_width=True):
        query = "Help me write a resume for a GenAI engineer position"
        st.session_state.messages.append({"role": "user", "content": query})
        st.rerun()

with col3:
    if st.button("💼 Interview Prep", use_container_width=True):
        query = "What are common interview questions for ML positions?"
        st.session_state.messages.append({"role": "user", "content": query})
        st.rerun()

with col4:
    if st.button("🔍 Job Search", use_container_width=True):
        query = "How do I find GenAI jobs at FAANG companies?"
        st.session_state.messages.append({"role": "user", "content": query})
        st.rerun()

# Chat input
st.markdown("### 💬 Ask Me Anything")
user_input = st.text_area(
    "Type your question here...",
    placeholder="e.g., How do I prepare for a prompt engineering interview?",
    label_visibility="collapsed",
    height=100
)

col1, col2, col3 = st.columns([3, 1, 1])
with col2:
    submit_button = st.button("🚀 Send", use_container_width=True)

# Process user input
if submit_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show processing spinner
    with st.spinner("🤔 Thinking..."):
        # Process query
        result = process_query(user_input)
        
        # Add assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response"],
            "category": result.get("category", ""),
            "sub_category": result.get("sub_category", "")
        })
    
    # Rerun to update chat
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.8); padding: 1rem;">
    <p style="font-size: 0.9rem;">
        Built with ❤️ using Streamlit, LangGraph, and Google Gemini
    </p>
</div>
""", unsafe_allow_html=True)
