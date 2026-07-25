# Project Structure

## Backend (Python/FastAPI)

```
backend/
├── src/careermatch_ai/
│   ├── api/                    # FastAPI routes and dependencies
│   │   ├── routes/             # API endpoint definitions
│   │   ├── dependencies.py     # Dependency injection
│   │   └── router.py           # Route assembly
│   │
│   ├── application/            # Use cases and orchestration
│   │   ├── dto/                # Data transfer objects (schemas)
│   │   ├── services/           # Application services
│   │   └── use_cases/          # Application workflows
│   │
│   ├── core/                   # Configuration and settings
│   │   └── settings.py         # Environment-based configuration
│   │
│   ├── domain/                 # Business logic (pure Python)
│   │   ├── entities/           # Domain models
│   │   ├── services/           # Business services
│   │   └── value_objects/      # Immutable value objects
│   │
│   └── infrastructure/         # External integrations
│       ├── auth/               # Authentication (JWT, OAuth)
│       ├── config/             # Configuration loaders
│       ├── db/                 # Database models and sessions
│       ├── llm/                # LLM client implementations
│       ├── parsers/            # Resume file parsers
│       ├── repositories/       # Data access layer
│       └── scoring/            # ATS scoring engine
│
├── migrations/                 # Alembic database migrations
├── requirements.txt            # Python dependencies
└── Dockerfile                  # Backend container
```

## Frontend (Streamlit)

```
frontend_streamlit/
├── app.py                      # Main Streamlit application
└── Dockerfile                  # Frontend container
```

## Configuration

```
company_profiles/              # Company-specific ATS rules (YAML)
├── tcs.yaml
├── infosys.yaml
├── wipro.yaml
├── hcl.yaml
├── accenture.yaml
├── cognizant.yaml
├── capgemini.yaml
├── ibm.yaml
└── tech_mahindra.yaml
```

## Infrastructure

```
infra/
└── nginx/                      # Reverse proxy configuration
```

## Documentation

```
docs/
├── architecture.md             # System architecture overview
├── project-structure.md        # This file
├── roadmap.md                  # Development roadmap
└── deployment-architecture.md  # Deployment guide
```
