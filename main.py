"""
GenAI Career Assistant 
A multi-agent system for career guidance in Generative AI
"""

import os
from typing import TypedDict
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END, START
from langchain_community.tools import DuckDuckGoSearchRun


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in your .env file")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7,
    verbose=True
)


class AgentState(TypedDict):
    query: str
    category: str
    sub_category: str
    response: str
    search_results: str


def categorize_query(state: AgentState) -> AgentState:
    query = state["query"]
    
    categorization_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a career assistant specializing in Generative AI careers.
        Categorize the user's query into one of these categories:
        1. Learning - for tutorial requests, concept explanations, coding help
        2. Resume - for resume preparation, review, optimization
        3. Interview - for interview preparation, mock interviews
        4. Job_Search - for job hunting, applications, networking
        
        Respond with ONLY the category name (Learning, Resume, Interview, or Job_Search).
        """),
        ("human", "{query}")
    ])
    
    chain = categorization_prompt | llm
    result = chain.invoke({"query": query})
    category = result.content.strip()
    
    state["category"] = category
    print(f"📋 Category: {category}")
    
    return state


def sub_categorize_learning(state: AgentState) -> AgentState:
    query = state["query"]
    
    sub_categorization_prompt = ChatPromptTemplate.from_messages([
        ("system", """For this learning-related query, determine if it's:
        1. Tutorial - user wants a complete tutorial, guide, or blog post
        2. QA - user has a specific question or coding problem
        
        Respond with ONLY 'Tutorial' or 'QA'.
        """),
        ("human", "{query}")
    ])
    
    chain = sub_categorization_prompt | llm
    result = chain.invoke({"query": query})
    sub_category = result.content.strip()
    
    state["sub_category"] = sub_category
    print(f"📌 Sub-category: {sub_category}")
    
    return state


def sub_categorize_interview(state: AgentState) -> AgentState:
    query = state["query"]
    
    sub_categorization_prompt = ChatPromptTemplate.from_messages([
        ("system", """For this interview-related query, determine if it's:
        1. Preparation - user wants interview tips, common questions, guidance
        2. Mock - user wants a mock interview simulation
        
        Respond with ONLY 'Preparation' or 'Mock'.
        """),
        ("human", "{query}")
    ])
    
    chain = sub_categorization_prompt | llm
    result = chain.invoke({"query": query})
    sub_category = result.content.strip()
    
    state["sub_category"] = sub_category
    print(f"📌 Sub-category: {sub_category}")
    
    return state


def web_search(state: AgentState) -> AgentState:
    query = state["query"]
    search_tool = DuckDuckGoSearchRun()
    search_query = f"Generative AI {query}"
    
    try:
        search_results = search_tool.run(search_query)
        state["search_results"] = search_results
        print(f"🔍 Web search completed")
    except Exception as e:
        print(f"⚠️ Search error: {e}")
        state["search_results"] = "No search results available"
    
    return state


def generate_tutorial(state: AgentState) -> AgentState:
    query = state["query"]
    search_results = state.get("search_results", "")
    
    tutorial_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert GenAI educator creating tutorials.
        Create a comprehensive, well-structured tutorial in Markdown format.
        Include:
        - Clear introduction
        - Step-by-step explanations
        - Code examples where relevant
        - Best practices
        - Common pitfalls to avoid
        - Additional resources
        
        Use the web search results to ensure current information.
        """),
        ("human", """Create a tutorial for: {query}
        
        Web search context: {search_results}
        """)
    ])
    
    chain = tutorial_prompt | llm
    result = chain.invoke({
        "query": query,
        "search_results": search_results
    })
    
    state["response"] = result.content
    print(f"✅ Tutorial generated")
    
    return state


def generate_qa_response(state: AgentState) -> AgentState:
    query = state["query"]
    search_results = state.get("search_results", "")
    
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful GenAI expert answering questions.
        Provide clear, concise answers with:
        - Direct answer to the question
        - Code examples if relevant
        - Explanation of key concepts
        - Links to documentation when available
        
        Use current information from web search results.
        """),
        ("human", """Answer this question: {query}
        
        Web search context: {search_results}
        """)
    ])
    
    chain = qa_prompt | llm
    result = chain.invoke({
        "query": query,
        "search_results": search_results
    })
    
    state["response"] = result.content
    print(f"✅ Q&A response generated")
    
    return state


def generate_resume_assistance(state: AgentState) -> AgentState:
    query = state["query"]
    
    resume_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a career coach specializing in GenAI resumes.
        Provide comprehensive resume guidance including:
        - Key skills to highlight
        - Project descriptions
        - Achievement formatting
        - ATS optimization tips
        - Industry-specific keywords
        """),
        ("human", "Resume help needed: {query}")
    ])
    
    chain = resume_prompt | llm
    result = chain.invoke({"query": query})
    
    state["response"] = result.content
    print(f"✅ Resume guidance generated")
    
    return state


def generate_interview_prep(state: AgentState) -> AgentState:
    query = state["query"]
    
    prep_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an interview coach for GenAI positions.
        Provide:
        - Common interview questions
        - How to answer behavioral questions
        - Technical concepts to review
        - Tips for virtual interviews
        - Questions to ask interviewers
        """),
        ("human", "Interview preparation for: {query}")
    ])
    
    chain = prep_prompt | llm
    result = chain.invoke({"query": query})
    
    state["response"] = result.content
    print(f"✅ Interview prep generated")
    
    return state


def generate_mock_interview(state: AgentState) -> AgentState:
    query = state["query"]
    
    mock_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are conducting a mock interview for a GenAI position.
        Generate:
        - 5-7 interview questions (mix of technical and behavioral)
        - Sample strong answers for each
        - Evaluation criteria
        - Feedback points to consider
        """),
        ("human", "Mock interview for: {query}")
    ])
    
    chain = mock_prompt | llm
    result = chain.invoke({"query": query})
    
    state["response"] = result.content
    print(f"✅ Mock interview generated")
    
    return state


def generate_job_search_help(state: AgentState) -> AgentState:
    query = state["query"]
    search_results = state.get("search_results", "")
    
    job_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a job search strategist for GenAI careers.
        Provide:
        - Job search strategies
        - Company recommendations
        - Networking tips
        - Application best practices
        - Salary negotiation guidance
        
        Use current job market information.
        """),
        ("human", """Job search help: {query}
        
        Current market context: {search_results}
        """)
    ])
    
    chain = job_prompt | llm
    result = chain.invoke({
        "query": query,
        "search_results": search_results
    })
    
    state["response"] = result.content
    print(f"✅ Job search guidance generated")
    
    return state


def route_by_category(state: AgentState) -> str:
    category = state["category"]
    
    if "Learning" in category:
        return "sub_categorize_learning"
    elif "Resume" in category:
        return "resume"
    elif "Interview" in category:
        return "sub_categorize_interview"
    elif "Job" in category or "Job_Search" in category:
        return "job_search"
    else:
        return "learning"


def route_learning_subcategory(state: AgentState) -> str:
    sub_category = state["sub_category"]
    
    if "Tutorial" in sub_category:
        return "web_search_tutorial"
    else:
        return "web_search_qa"


def route_interview_subcategory(state: AgentState) -> str:
    sub_category = state["sub_category"]
    
    if "Mock" in sub_category:
        return "mock"
    else:
        return "prep"


def create_agent_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("categorize", categorize_query)
    workflow.add_node("sub_categorize_learning", sub_categorize_learning)
    workflow.add_node("sub_categorize_interview", sub_categorize_interview)
    workflow.add_node("web_search_tutorial", web_search)
    workflow.add_node("web_search_qa", web_search)
    workflow.add_node("web_search_jobs", web_search)
    workflow.add_node("tutorial", generate_tutorial)
    workflow.add_node("qa", generate_qa_response)
    workflow.add_node("resume", generate_resume_assistance)
    workflow.add_node("prep", generate_interview_prep)
    workflow.add_node("mock", generate_mock_interview)
    workflow.add_node("job_search", generate_job_search_help)
    
    workflow.add_edge(START, "categorize")
    
    workflow.add_conditional_edges(
        "categorize",
        route_by_category,
        {
            "sub_categorize_learning": "sub_categorize_learning",
            "resume": "resume",
            "sub_categorize_interview": "sub_categorize_interview",
            "job_search": "web_search_jobs",
            "learning": "sub_categorize_learning"
        }
    )
    
    workflow.add_conditional_edges(
        "sub_categorize_learning",
        route_learning_subcategory,
        {
            "web_search_tutorial": "web_search_tutorial",
            "web_search_qa": "web_search_qa"
        }
    )
    
    workflow.add_conditional_edges(
        "sub_categorize_interview",
        route_interview_subcategory,
        {
            "mock": "mock",
            "prep": "prep"
        }
    )
    
    workflow.add_edge("web_search_tutorial", "tutorial")
    workflow.add_edge("web_search_qa", "qa")
    workflow.add_edge("web_search_jobs", "job_search")
    
    workflow.add_edge("tutorial", END)
    workflow.add_edge("qa", END)
    workflow.add_edge("resume", END)
    workflow.add_edge("prep", END)
    workflow.add_edge("mock", END)
    workflow.add_edge("job_search", END)
    
    return workflow.compile()


def run_career_assistant(user_query: str):
    print(f"\n{'='*60}")
    print(f"🤖 GenAI Career Assistant")
    print(f"{'='*60}")
    print(f"Query: {user_query}\n")
    
    agent = create_agent_graph()
    
    initial_state = {
        "query": user_query,
        "category": "",
        "sub_category": "",
        "response": "",
        "search_results": ""
    }
    
    result = agent.invoke(initial_state)
    
    print(f"\n{'='*60}")
    print(f"📊 Response:")
    print(f"{'='*60}\n")
    print(result["response"])
    print(f"\n{'='*60}\n")
    
    return result


if __name__ == "__main__":
    
    examples = [
        "Create a tutorial on how to build a RAG system with LangChain",  
        "What's the difference between GPT-4 and Claude?",                
        "Help me write a resume for a GenAI engineer position",           
        "What are common interview questions for ML positions?",          
        "Give me a mock interview for a prompt engineer role",            
        "How do I find GenAI jobs at FAANG companies?"                    
    ]
    query = examples[5]  
    
    
    result = run_career_assistant(query)
    
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
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result["response"])
    print(f"📄 Output saved to {filename}")