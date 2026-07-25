# CareerMatch AI

AI-powered resume analysis that evaluates resumes against major Indian IT company profiles (TCS, Infosys, Wipro, HCL, Accenture, Cognizant, Capgemini, IBM, Tech Mahindra) using LLMs.

## Quick Start

```bash
pip install -r backend/requirements.txt streamlit
export GROQ_API_KEY=gsk_your_key
streamlit run frontend_streamlit/app.py
```

## Deploy Forever (Free Options)

### Option 1: Streamlit Community Cloud (simplest, free forever)

1. **Push to GitHub:**
   ```bash
   git init && git add . && git commit -m "init"
   gh repo create careermatch-ai --public --push
   ```

2. **Deploy on** https://streamlit.io/cloud:
   - Sign in with GitHub
   - Click "New app" → select your repo
   - Main file: `frontend_streamlit/app.py`
   - Python version: 3.11
   - Under **Secrets**, add your API keys:
     ```
     GROQ_API_KEY=gsk_...
     GEMINI_API_KEY=AIza...
     OPENAI_API_KEY=sk-...
     ```
   - Click Deploy

3. Your app is live at `https://careermatch-ai.streamlit.app` — forever free.

### Option 2: Hugging Face Spaces (free, with GPU option)

1. Create a Space at https://huggingface.co/new-space
2. Choose **Streamlit** SDK
3. Push code and set secrets in Space settings

### Option 3: Railway / Render (for the full FastAPI backend too)

```bash
# Deploy backend separately if you want API access
railway up
```

## Architecture

```
frontend_streamlit/ (Streamlit)
    ↓ direct imports (no DB needed)
backend/src/careermatch_ai/
    ├── infrastructure/llm/  ← 3 LLM providers
    ├── infrastructure/parsers/
    ├── infrastructure/scoring/
    ├── domain/services/
    └── application/services/
```

The Streamlit app imports the backend services directly — no separate server required.

## LLM Fallback Chain

| Provider | Role | Key Needed |
|----------|------|------------|
| Groq (Llama 3) | Primary | `GROQ_API_KEY` |
| Gemini 2.0 Flash | Fallback 1 | `GEMINI_API_KEY` |
| OpenAI GPT-4o-mini | Fallback 2 | `OPENAI_API_KEY` |

All analysis is LLM-based: resume parsing, ATS scoring, gap analysis, bullet rewriting, recommendations.

## Local Development

```bash
# Backend API (optional, only if you need REST endpoints)
cd backend && pip install -r requirements.txt
uvicorn careermatch_ai.main:app --app-dir src --reload

# Streamlit UI
pip install streamlit
streamlit run frontend_streamlit/app.py
```

## Add a Company

Create a new YAML file in `company_profiles/`. No code changes needed.
