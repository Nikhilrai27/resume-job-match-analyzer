from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class GoogleAuthRequest(BaseModel):
    id_token: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    created_at: datetime


class ScoreBreakdownResponse(BaseModel):
    skill_match: float
    experience_relevance: float
    education_fit: float
    project_relevance: float
    certification_boost: float
    formatting: float


class CompanyScoreResponse(BaseModel):
    company_slug: str
    overall_score: float
    score_breakdown: ScoreBreakdownResponse
    matched_skills: list[str]
    missing_skills: list[str]
    gaps: list[str]
    recommendations: list[str]
    rewritten_bullets: list[str]


class ResumeAnalysisResponse(BaseModel):
    resume_id: str
    ats_score: float
    global_gaps: list[str]
    companies: list[CompanyScoreResponse]
    generated_resume_markdown: str


class ResumeUploadResponse(BaseModel):
    resume_id: str
    filename: str
    status: str


class PaginatedResponse(BaseModel):
    items: list[Any]
    total: int


class ResumeExportResponse(BaseModel):
    filename: str
    content: str
    media_type: str
