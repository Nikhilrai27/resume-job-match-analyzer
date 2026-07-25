from pathlib import Path

from fastapi import Depends
from sqlalchemy.orm import Session

from careermatch_ai.application.services.company_matching_service import CompanyMatchingService
from careermatch_ai.application.services.resume_rendering_service import ResumeRenderingService
from careermatch_ai.application.use_cases.analyze_resume import AnalyzeResumeUseCase
from careermatch_ai.core.settings import get_settings
from careermatch_ai.domain.services.bullet_rewriter import BulletRewriter
from careermatch_ai.domain.services.gap_analyzer import GapAnalyzer
from careermatch_ai.infrastructure.config.company_loader import CompanyProfileLoader
from careermatch_ai.infrastructure.db.session import get_db
from careermatch_ai.infrastructure.llm.gemini_client import GeminiClient
from careermatch_ai.infrastructure.llm.groq_client import GroqClient
from careermatch_ai.infrastructure.llm.llm_service import LLMService
from careermatch_ai.infrastructure.llm.openai_client import OpenAIClient
from careermatch_ai.infrastructure.parsers.resume_parser import ResumeParser
from careermatch_ai.infrastructure.scoring.ats_engine import ATSScoringEngine


def get_llm_service() -> LLMService:
    settings = get_settings()
    fallbacks: list = []
    if settings.gemini_api_key:
        fallbacks.append(GeminiClient(api_key=settings.gemini_api_key, model=settings.gemini_model))
    if settings.openai_api_key:
        fallbacks.append(OpenAIClient(api_key=settings.openai_api_key, model=settings.openai_model))
    return LLMService(
        primary_client=GroqClient(api_key=settings.groq_api_key, model=settings.groq_model),
        fallback_clients=fallbacks,
    )


def get_analyze_resume_use_case() -> AnalyzeResumeUseCase:
    settings = get_settings()
    llm = get_llm_service()
    loader = CompanyProfileLoader(Path(settings.profiles_dir))
    matcher = CompanyMatchingService(
        loader=loader,
        scoring_engine=ATSScoringEngine(llm_service=llm),
        gap_analyzer=GapAnalyzer(llm_service=llm),
        bullet_rewriter=BulletRewriter(llm_service=llm),
        llm_service=llm,
    )
    return AnalyzeResumeUseCase(
        parser=ResumeParser(llm_service=llm),
        matcher=matcher,
    )


def get_resume_rendering_service() -> ResumeRenderingService:
    return ResumeRenderingService()


def get_database(db: Session = Depends(get_db)) -> Session:
    return db
