# Testing Strategy

## Coverage Goal

- Minimum line coverage: 80%

## Test Pyramid

- Unit tests for company loader, ATS engine, gap analyzer, and bullet rewriting
- Integration tests for FastAPI routes and repository flows
- Frontend component and page tests
- Contract tests for API payloads

## Recommended Additions

- Snapshot tests for generated ATS-optimized resumes
- End-to-end upload and analysis test with Playwright
- Migration tests for PostgreSQL schema and pgvector indexes
- Security tests for JWT and OAuth flows
