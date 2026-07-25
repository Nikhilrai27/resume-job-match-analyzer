# Deployment Architecture

## Runtime Topology

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Streamlit UI  │────▶│   FastAPI Backend │────▶│   PostgreSQL    │
│   (Port 8501)   │     │   (Port 8000)     │     │   (Port 5432)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │
                              ▼
                        ┌──────────────────┐
                        │   LLM Providers  │
                        │  (External APIs) │
                        └──────────────────┘
```

## Services

- **frontend**: Streamlit web application (Python)
- **backend**: FastAPI REST API service (Python)
- **db**: PostgreSQL with pgvector extension

## Request Flow

1. User authenticates via email/password or Google OAuth
2. Frontend uploads resume to FastAPI backend
3. Backend stores the file, parses it using LLM
4. Backend scores resume against 9 company profiles
5. Backend returns analysis results and optimized resume
6. Frontend renders scorecards, gaps, and recommendations

## Local Development

```bash
# Start all services
docker-compose up --build

# Access points
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- Database: localhost:5432
```

## Production Considerations

- Use managed PostgreSQL (AWS RDS, Google Cloud SQL)
- Store uploaded files in object storage (S3, GCS)
- Add Redis for caching LLM responses
- Implement rate limiting on API endpoints
- Add monitoring and logging (Prometheus, Grafana)
- Use HTTPS for all external communication

## Scaling

- Stateless backend services (horizontal scaling)
- Background workers for heavy analysis tasks
- Database connection pooling
- CDN for static assets
- Load balancer for multiple backend instances

## Security

- JWT-based authentication
- Google OAuth integration
- Environment variable configuration
- No secrets in codebase
- File upload validation and size limits
