import json
import logging

from careermatch_ai.infrastructure.llm.base import LLMClient
from careermatch_ai.infrastructure.llm.prompts import (
    ATS_SCORE_SYSTEM,
    ATS_SCORE_USER,
    BULLET_REWRITE_SYSTEM,
    BULLET_REWRITE_USER,
    GAP_ANALYSIS_SYSTEM,
    GAP_ANALYSIS_USER,
    RECOMMENDATIONS_SYSTEM,
    RECOMMENDATIONS_USER,
    RESUME_PARSE_SYSTEM,
    RESUME_PARSE_USER,
)

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self, primary_client: LLMClient, fallback_clients: list[LLMClient] | None = None) -> None:
        self._primary = primary_client
        self._fallbacks = fallback_clients or []

    def _call(self, system: str, user: str, json_mode: bool = True) -> dict | list | str:
        clients = [self._primary, *self._fallbacks]

        last_error: Exception | None = None
        for client in clients:
            try:
                raw = client.generate(system, user, json_mode=json_mode)
                if not raw or not raw.strip():
                    raise ValueError("Empty response from LLM")
                cleaned = raw.strip()
                if cleaned.startswith("```"):
                    cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
                    cleaned = cleaned.rsplit("```", 1)[0] if "```" in cleaned else cleaned
                parsed = json.loads(cleaned)
                return parsed
            except Exception as exc:
                last_error = exc
                logger.warning("LLM call failed for %s: %s", type(client).__name__, exc)
                continue

        raise RuntimeError("All LLM clients failed") from last_error

    def parse_resume(self, resume_text: str) -> dict:
        return self._call(RESUME_PARSE_SYSTEM, RESUME_PARSE_USER.format(resume_text=resume_text))

    def score_company_match(
        self,
        company_name: str,
        sector: str,
        focus_skills: list[str],
        preferred_certifications: list[str],
        required_sections: list[str],
        min_experience: int,
        keywords: dict[str, float],
        resume_skills: list[str],
        experience: list[dict],
        education: list[dict],
        projects: list[dict],
        certifications: list[str],
        sections_present: list[str],
        summary: str,
    ) -> dict:
        user = ATS_SCORE_USER.format(
            company_name=company_name,
            sector=sector,
            focus_skills=focus_skills,
            preferred_certifications=preferred_certifications,
            required_sections=required_sections,
            min_experience=min_experience,
            keywords=keywords,
            resume_skills=resume_skills,
            experience=experience,
            education=education,
            projects=projects,
            certifications=certifications,
            sections_present=sections_present,
            summary=summary,
        )
        return self._call(ATS_SCORE_SYSTEM, user)

    def analyze_gaps(
        self,
        company_name: str,
        sector: str,
        required_sections: list[str],
        focus_skills: list[str],
        preferred_certifications: list[str],
        min_experience: int,
        resume_skills: list[str],
        experience: list[dict],
        sections_present: list[str],
        certifications: list[str],
        has_summary: bool,
        project_count: int,
        missing_skills: list[str],
    ) -> list[str]:
        user = GAP_ANALYSIS_USER.format(
            company_name=company_name,
            sector=sector,
            required_sections=required_sections,
            focus_skills=focus_skills,
            preferred_certifications=preferred_certifications,
            min_experience=min_experience,
            resume_skills=resume_skills,
            experience=experience,
            sections_present=sections_present,
            certifications=certifications,
            has_summary=str(has_summary),
            project_count=project_count,
            missing_skills=missing_skills,
        )
        result = self._call(GAP_ANALYSIS_SYSTEM, user)
        return result if isinstance(result, list) else result.get("gaps", [])

    def rewrite_bullets(self, bullets: list[str]) -> list[dict]:
        result = self._call(
            BULLET_REWRITE_SYSTEM,
            BULLET_REWRITE_USER.format(bullets="\n".join(f"- {b}" for b in bullets)),
        )
        if isinstance(result, list):
            return result
        return result.get("rewritten_bullets", [])

    def generate_recommendations(
        self,
        company_name: str,
        missing_skills: list[str],
        gaps: list[str],
        resume_skills: list[str],
    ) -> list[str]:
        user = RECOMMENDATIONS_USER.format(
            company_name=company_name,
            missing_skills=missing_skills,
            gaps=gaps,
            resume_skills=resume_skills,
        )
        result = self._call(RECOMMENDATIONS_SYSTEM, user)
        if isinstance(result, list):
            return result
        return result.get("recommendations", [])

    def match_job_description(
        self,
        job_text: str,
        resume_skills: list[str],
        experience: list[dict],
        education: list[dict],
        projects: list[dict],
        certifications: list[str],
        sections_present: list[str],
        summary: str,
    ) -> dict:
        user = ATS_SCORE_USER.format(
            company_name="Custom Job",
            sector="General",
            focus_skills=[],
            preferred_certifications=[],
            required_sections=["Summary", "Skills", "Experience", "Education"],
            min_experience=0,
            keywords={},
            resume_skills=resume_skills,
            experience=experience,
            education=education,
            projects=projects,
            certifications=certifications,
            sections_present=sections_present,
            summary=summary + f"\n\nJob Description:\n{job_text}",
        )
        return self._call(ATS_SCORE_SYSTEM, user)
