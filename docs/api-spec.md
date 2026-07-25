# API Specification

Base path: `/api/v1`

## Auth

### `POST /auth/register`

Request:

```json
{
  "email": "user@example.com",
  "password": "strong-password",
  "full_name": "Aarav Singh"
}
```

Response: `201 Created`

### `POST /auth/login`

Request:

```json
{
  "email": "user@example.com",
  "password": "strong-password"
}
```

Response:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

### `POST /auth/google`

Request:

```json
{
  "id_token": "google-id-token"
}
```

## Resumes

### `POST /resumes/upload`

Multipart form:

- `file`

Authorization:

- `Bearer <jwt>`

### `POST /resumes/analyze`

Multipart form:

- `file`

Authorization:

- `Bearer <jwt>`

Response:

```json
{
  "resume_id": "uuid",
  "ats_score": 84.5,
  "global_gaps": ["Missing certifications"],
  "companies": [
    {
      "company_slug": "accenture",
      "overall_score": 88.0,
      "score_breakdown": {
        "skill_match": 90.0,
        "experience_relevance": 85.0,
        "education_fit": 100.0,
        "project_relevance": 75.0,
        "certification_boost": 40.0,
        "formatting": 100.0
      },
      "matched_skills": ["python", "sql"],
      "missing_skills": ["power bi"],
      "gaps": ["Relevant certifications are missing"],
      "recommendations": ["Add evidence of these Accenture skills: power bi"],
      "rewritten_bullets": ["Optimized ETL pipeline by delivering measurable business impact."]
    }
  ],
  "generated_resume_markdown": "# Candidate Name"
}
```

### `GET /resumes/{resume_id}/download?format=md`

Authorization:

- `Bearer <jwt>`

Response:

```json
{
  "filename": "optimized-resume-uuid.md",
  "content": "# Candidate Name",
  "media_type": "text/markdown"
}
```

## Health

### `GET /health`

Response:

```json
{
  "status": "ok"
}
```
