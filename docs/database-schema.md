# Database Schema

## Core Tables

### `users`

- `id` UUID/string primary key
- `email` unique
- `password_hash`
- `full_name`
- `oauth_provider`
- `created_at`

### `resumes`

- `id` UUID/string primary key
- `user_id` foreign key to `users`
- `original_filename`
- `storage_path`
- `extracted_text`
- `optimized_resume_markdown`
- `created_at`

### `resume_analyses`

- `id` UUID/string primary key
- `resume_id` foreign key to `resumes`
- `company_slug`
- `overall_score`
- `explanation_json`
- `created_at`

### `resume_embeddings`

- `id` UUID/string primary key
- `resume_id` foreign key to `resumes`
- `embedding` vector(384) using `pgvector`

## Recommended Migrations

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE INDEX IF NOT EXISTS idx_resume_analyses_company_slug ON resume_analyses(company_slug);
CREATE INDEX IF NOT EXISTS idx_resume_embeddings_vector ON resume_embeddings USING ivfflat (embedding vector_cosine_ops);
```

## Future Tables

- `job_descriptions`
- `analysis_jobs`
- `resume_exports`
- `audit_logs`
