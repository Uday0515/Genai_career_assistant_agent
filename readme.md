# GenAI Career Assistant

An AI agent that helps with career guidance in the GenAI field. I built this to understand how to structure agent workflows with LangGraph and integrate external tools like web search.

## What it does

The system routes career-related queries to specialized handlers:
- **Learning**: Creates tutorials or answers technical questions about GenAI concepts
- **Resume**: Provides guidance on building resumes for GenAI roles
- **Interview**: Helps with interview prep or runs mock interviews
- **Job Search**: Suggests strategies for finding GenAI positions

## Why I built this

I wanted to learn how to build an actual AI agent (not just a chatbot wrapper). The main challenges I tackled:

1. **Workflow routing** - How do you make an agent decide which path to take?
2. **Tool integration** - Can I give the agent access to real-time web search?
3. **Specialized responses** - How do I generate domain-specific content instead of generic answers?

## How it works

```
User asks a question
  ↓
Agent categorizes it (Learning, Resume, Interview, Job Search)
  ↓
If it's a Learning or Job Search query, agent searches the web
  ↓
Agent generates a specialized response based on the category
```

The agent uses LangGraph for workflow management. Each category gets its own prompt template, which is why a resume question gets different treatment than a tutorial request.

## Tech choices

**LangChain/LangGraph**: I needed conditional routing and state management. LangGraph made this clean with its graph-based approach.

**Gemini 2.5 Flash**: Fast enough for real-time responses, free tier is generous (1500 req/day). I experimented with temperature settings - 0.7 worked best for balancing accuracy and creativity.

**DuckDuckGo Search**: Doesn't need an API key, unlike Google Search. I use it for Learning and Job Search queries to get current information.

**Streamlit**: Quick way to add a UI without building a full React frontend. Kept the core logic separate in `main.py` so it works as both CLI and web app.

## Setup

Clone and install dependencies:
```bash
git clone https://github.com/Uday0515/Genai_career_assistant_agent.git
cd Genai_career_assistant_agent
pip install -r requirements.txt
```

Add your Gemini API key to `.env`:
```
GOOGLE_API_KEY=your_key_here
```

Run it:
```bash
# Web interface
streamlit run ui.py

# Or use the CLI
python main.py
```

## Project structure

```
main.py          # Core agent logic - categorization, routing, generation
ui.py            # Streamlit interface that imports from main.py
requirements.txt # Dependencies
```

I separated the UI from the logic so the agent can be used programmatically or through the web interface.

## Example usage

**Tutorial request:**
> "Create a tutorial on building RAG systems with LangChain"

Agent flow: Categorize → Learning → Tutorial → Search web → Generate tutorial with code examples

**Interview prep:**
> "Mock interview for prompt engineer role"

Agent flow: Categorize → Interview → Mock → Generate Q&A with sample answers

## What I learned

**Routing is harder than it looks**: Getting the agent to consistently categorize queries correctly took prompt iteration. I ended up being very explicit in the system prompts.

**Web search quality matters**: DuckDuckGo sometimes returns irrelevant results. I prepend "Generative AI" to search queries to improve relevance.

**Separating concerns helps**: Keeping `main.py` as pure logic and `ui.py` as just interface made debugging much easier.

**Cost adds up**: Even with free tier, I needed to track API calls. ~4 calls per query means I can handle about 375 queries/day on Gemini's free tier.

## Limitations

- Only works with Gemini (no OpenAI/Anthropic support yet)
- No conversation history - each query is independent
- Web search only uses DuckDuckGo
- Responses overwrite files instead of appending

## Future improvements

Things I want to add:
- [ ] Support multiple LLM providers
- [ ] Add conversation memory using vector storage
- [ ] More tools (Wikipedia for research, Calculator for technical questions)
- [ ] Deploy to Streamlit Cloud so it's publicly accessible
- [ ] Better error handling when search fails

## Running it yourself

The code is designed to be modified. Some ideas:
- Change the categories in `categorize_query()` to fit your domain
- Add new tools in the workflow graph
- Modify the prompt templates to change response style
- Swap out Gemini for a different LLM

## Why "agent" not "chatbot"

A chatbot just responds to messages. This system:
1. Analyzes queries to decide routing
2. Uses external tools (web search)
3. Maintains state across multiple steps
4. Generates specialized outputs per domain

That's what makes it an agent.

---

Built while learning about AI agents and LangGraph. Feel free to fork and adapt for your use case.