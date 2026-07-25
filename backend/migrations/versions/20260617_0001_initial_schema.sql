CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    oauth_provider VARCHAR(50),
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS resumes (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id),
    original_filename VARCHAR(255) NOT NULL,
    storage_path TEXT NOT NULL,
    extracted_text TEXT NOT NULL,
    optimized_resume_markdown TEXT,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS resume_analyses (
    id VARCHAR(36) PRIMARY KEY,
    resume_id VARCHAR(36) NOT NULL REFERENCES resumes(id),
    company_slug VARCHAR(100) NOT NULL,
    overall_score DOUBLE PRECISION NOT NULL,
    explanation_json TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS resume_embeddings (
    id VARCHAR(36) PRIMARY KEY,
    resume_id VARCHAR(36) NOT NULL REFERENCES resumes(id),
    embedding vector(384)
);

CREATE INDEX IF NOT EXISTS idx_resume_analyses_company_slug ON resume_analyses(company_slug);
CREATE INDEX IF NOT EXISTS idx_resume_embeddings_vector ON resume_embeddings USING ivfflat (embedding vector_cosine_ops);
