# Data Analysis Agent

An agentic AI system built with LangGraph and LangChain that can load CSV data,
run pandas analysis, and answer questions using the ReAct reasoning pattern.

## Setup

1. Clone the repo
git clone https://github.com/yourusername/agentic-ai.git

cd agentic-ai

2. Create a virtual environment
python -m venv venv

source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Add your API keys
cp .env.example .env
Edit .env and add your GROQ_API_KEY

5. Run the app
uvicorn app:app --reload

6. Open http://127.0.0.1:8000

## Tech Stack
- LangGraph — agent state machine
- LangChain — tool binding and LLM interface  
- Groq (Llama 3.3 70b) — LLM backend
- FastAPI — backend API
- Pandas — data analysis
