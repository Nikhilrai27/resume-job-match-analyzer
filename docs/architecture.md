# Architecture

## System Overview

CareerMatch AI is a resume analysis platform that uses Large Language Models (LLMs) to evaluate resumes against company profiles and job descriptions.

## High-Level Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Streamlit UI  │────▶│   FastAPI Backend │────▶│   PostgreSQL    │
│   (Frontend)    │     │   (REST API)      │     │   + pgvector    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │
                              ▼
                        ┌──────────────────┐
                        │   LLM Providers  │
                        │  (Groq/Gemini/   │
                        │   OpenAI)        │
                        └──────────────────┘
```

## Backend Architecture

### Layered Design (DDD)

```
backend/src/careermatch_ai/
├── domain/                    # Business logic (pure Python)
│   ├── entities/              # Domain models (Resume, Company, Analysis)
│   ├── services/              # Business services (GapAnalyzer, BulletRewriter)
│   └── value_objects/         # Immutable value objects (Skill)
│
├── application/               # Use cases and orchestration
│   ├── use_cases/             # Application workflows (AnalyzeResume)
│   ├── services/              # Application services
│   └── dto/                   # Data transfer objects
│
├── infrastructure/            # External integrations
│   ├── llm/                   # LLM client implementations
│   ├── parsers/               # Resume file parsers
│   ├── scoring/               # ATS scoring engine
│   ├── auth/                  # Authentication (JWT, OAuth)
│   ├── db/                    # Database models and sessions
│   └── repositories/          # Data access layer
│
├── api/                       # FastAPI routes and dependencies
│   └── routes/                # API endpoint definitions
│
└── core/                      # Configuration and settings
```

### Key Components

#### Domain Layer
- **ResumeAggregate**: Core resume data model
- **CompanyProfile**: Company-specific ATS requirements
- **ResumeAnalysis**: Analysis results with scores
- **GapAnalyzer**: Identifies skill/experience gaps
- **BulletRewriter**: Improves resume bullet points

#### Infrastructure Layer
- **LLMService**: Orchestrates multiple LLM providers with fallback
- **ResumeParser**: Extracts text from PDF/DOCX/TXT/MD files
- **ATSEngine**: Calculates ATS compatibility scores
- **Auth**: JWT tokens and Google OAuth integration

#### Application Layer
- **AnalyzeResumeUseCase**: Main workflow for resume analysis
- **CompanyMatchingService**: Matches resume against company profiles
- **ResumeRenderingService**: Generates optimized resume content

### LLM Fallback Chain

```
Primary: Groq (Llama 3) → Fallback 1: Gemini 2.0 Flash → Fallback 2: OpenAI GPT-4o-mini
```

## Data Flow

1. **Upload**: User uploads resume → Parser extracts text → LLM parses structure
2. **Analysis**: Resume matched against company profiles → LLM scores and analyzes
3. **Results**: Scores, gaps, recommendations → Frontend displays results
4. **Optimization**: LLM rewrites bullets → Generates improved resume

## Database Schema

- **users**: User accounts and authentication
- **resumes**: Uploaded resume files and extracted data
- **resume_analyses**: Analysis results per company
- **resume_embeddings**: Vector embeddings for similarity search (future)

## Deployment

- **Docker Compose**: Backend + Frontend + PostgreSQL
- **Streamlit Cloud**: Free frontend hosting
- **Railway/Render**: Full-stack deployment option

## Security

- JWT-based authentication
- Google OAuth integration
- File upload validation
- Environment variable configuration
- No secrets in codebase
