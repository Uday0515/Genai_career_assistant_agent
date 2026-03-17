 # GenAI Career Assistant

 An AI-powered mentor that helps learners and professionals navigate Generative AI careers. The project combines LangChain, LangGraph, and Gemini 2.5 Flash to categorize user intent, search the web for up-to-date context, and deliver tailored guidance for learning, resumes, interviews, and job searches.

 ## Features
 - Multi-agent workflow built with LangGraph for routing and specialization
 - Gemini 2.5 Flash model via `langchain_google_genai`
 - Live web context using DuckDuckGo search
 - Streamlit chat UI with download buttons for Markdown/Text outputs
 - CLI entry point that saves responses to category-specific files

 ## Prerequisites
 - Python 3.10+ recommended
 - Google AI Studio API key with access to Gemini 2.5 Flash
 - Internet access for search-enabled answers

 ## Setup
 1. (Optional) Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
 2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
 3. Create a `.env` file in the project root and add your key:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```
    You can generate a key from [Google AI Studio](https://makersuite.google.com/app/apikey).

 ## Running the app
 ### Streamlit UI (recommended)
 ```bash
 streamlit run ui.py
 ```
 - Provides a chat-style interface with preset examples and download buttons.
 - Make sure the `.env` file is present before launching.

 ### CLI example
 The default script runs an example query and writes the response to a Markdown file based on the detected category.
 ```bash
 python main.py
 ```
 To run your own question:
 ```python
 from main import run_career_assistant

 run_career_assistant("Give me a mock interview for a prompt engineer role")
 ```

 ## Output files
 When invoked from `main.py`, responses are saved to category-specific filenames (e.g., `tutorial_output.md`, `resume_guidance.md`, `job_search_help.md`). The Streamlit UI offers equivalent downloads for Markdown or text.

 ## Troubleshooting
 - **Missing API key:** Ensure `GOOGLE_API_KEY` is set in `.env`.
 - **Network-dependent steps:** Web search requires internet connectivity.
 - **Dependency issues:** Re-run `pip install -r requirements.txt` inside your activated virtual environment.

 ## License
 This project is licensed under the [MIT License](LICENSE).
