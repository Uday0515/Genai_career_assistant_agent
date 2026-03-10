"""
Streamlit UI for GenAI Career Assistant
"""

import streamlit as st
import os
from dotenv import load_dotenv
from main import run_career_assistant, initialize_llm

load_dotenv()

st.set_page_config(
    page_title="GenAI Career Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    st.title("🤖 GenAI Career Assistant")
    st.markdown("Your AI-powered mentor for Generative AI careers")
    
    with st.sidebar:
        st.header("📋 About")
        st.markdown("""
        This assistant helps you with:
        - 📚 **Learning**: Tutorials and Q&A
        - 📄 **Resume**: Professional guidance
        - 🎤 **Interview**: Prep and mock interviews
        - 💼 **Job Search**: Strategies and tips
        """)
        
        st.divider()
        
        st.header("🚀 Quick Examples")
        example_queries = {
            "RAG Tutorial": "Create a tutorial on how to build a RAG system with LangChain and LangGraph, including evaluation metrics",
            "GPT-4 vs Claude": "What's the difference between GPT-4 and Claude?",
            "Resume Help": "Help me write a resume for a GenAI engineer position",
            "Interview Questions": "What are common interview questions for ML positions?",
            "Mock Interview": "Give me a mock interview for a prompt engineer role",
            "Job Search": "How do I find GenAI jobs at FAANG companies?"
        }
        
        selected_example = st.selectbox(
            "Choose an example:",
            ["Custom Query"] + list(example_queries.keys())
        )
        
        if selected_example != "Custom Query":
            st.session_state.example_query = example_queries[selected_example]
        
        st.divider()
        
        if st.button("🗑️ Clear History"):
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        
        st.markdown("### ⚙️ Settings")
        st.info("Model: Gemini 2.5 Flash")
        
        if st.button("🔄 Reset Session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "category" in message:
                st.caption(f"Category: {message['category']} | Type: {message.get('sub_category', 'N/A')}")
    
    if "example_query" in st.session_state:
        prompt = st.session_state.example_query
        del st.session_state.example_query
    else:
        prompt = st.chat_input("Ask me anything about GenAI careers...")
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🔍 Analyzing your query..."):
                try:
                    result = run_career_assistant(prompt)
                    
                    category_emoji = {
                        "Learning": "📚",
                        "Resume": "📄",
                        "Interview": "🎤",
                        "Job_Search": "💼"
                    }
                    
                    emoji = category_emoji.get(result["category"], "🤖")
                    
                    st.info(f"{emoji} **Category:** {result['category']}")
                    
                    if result.get("sub_category"):
                        st.info(f"📌 **Type:** {result['sub_category']}")
                    
                    st.markdown(result["response"])
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["response"],
                        "category": result["category"],
                        "sub_category": result.get("sub_category", "")
                    })
                    
                    category = result["category"]
                    sub_category = result.get("sub_category", "")
                    
                    if "Learning" in category and "Tutorial" in sub_category:
                        filename = "tutorial_output.md"
                    elif "Learning" in category and "QA" in sub_category:
                        filename = "qa_output.md"
                    elif "Resume" in category:
                        filename = "resume_guidance.md"
                    elif "Interview" in category and "Mock" in sub_category:
                        filename = "mock_interview.md"
                    elif "Interview" in category and "Preparation" in sub_category:
                        filename = "interview_prep.md"
                    elif "Job" in category or "Job_Search" in category:
                        filename = "job_search_help.md"
                    else:
                        filename = "output.md"
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.download_button(
                            label="📥 Download as Markdown",
                            data=result["response"],
                            file_name=filename,
                            mime="text/markdown",
                            use_container_width=True
                        )
                    
                    with col2:
                        st.download_button(
                            label="📄 Download as Text",
                            data=result["response"],
                            file_name=filename.replace('.md', '.txt'),
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Make sure your GOOGLE_API_KEY is set in the .env file")
                    st.code(str(e), language="python")


if __name__ == "__main__":
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    if not GOOGLE_API_KEY:
        st.error("⚠️ GOOGLE_API_KEY not found!")
        st.markdown("""
        ### Setup Instructions:
        
        1. Create a `.env` file in your project directory
        2. Add your Google API key:
        ```
        GOOGLE_API_KEY=your_api_key_here
        ```
        3. Get your API key from: [Google AI Studio](https://makersuite.google.com/app/apikey)
        4. Restart the Streamlit app
        """)
        st.stop()
    
    main()