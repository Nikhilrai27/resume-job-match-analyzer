from careermatch_ai.domain.entities.company_profile import CompanyProfile
from careermatch_ai.domain.entities.resume import ResumeAggregate
from careermatch_ai.infrastructure.llm.llm_service import LLMService


class ATSScoringEngine:
    def __init__(self, llm_service: LLMService) -> None:
        self._llm = llm_service

    def score(self, resume: ResumeAggregate, profile: CompanyProfile) -> tuple[float, dict[str, float], list[str], list[str]]:
        result = self._llm.score_company_match(
            company_name=profile.display_name,
            sector=profile.sector,
            focus_skills=profile.focus_skills,
            preferred_certifications=profile.preferred_certifications,
            required_sections=profile.required_sections,
            min_experience=profile.minimum_experience_years,
            keywords=profile.keywords_by_weight,
            resume_skills=resume.skills,
            experience=[
                {"title": e.title, "company": e.company, "years": e.years, "bullets": e.bullets}
                for e in resume.experience
            ],
            education=[
                {"degree": e.degree, "institution": e.institution, "year": e.year}
                for e in resume.education
            ],
            projects=[
                {"name": p.name, "summary": p.summary, "technologies": p.technologies}
                for p in resume.projects
            ],
            certifications=resume.certifications,
            sections_present=resume.sections_present,
            summary=resume.summary,
        )

        overall_score = float(result.get("overall_score", 0))
        breakdown = {
            "skill_match": float(result.get("skill_match", 0)),
            "experience_relevance": float(result.get("experience_relevance", 0)),
            "education_fit": float(result.get("education_fit", 0)),
            "project_relevance": float(result.get("project_relevance", 0)),
            "certification_boost": float(result.get("certification_boost", 0)),
            "formatting": float(result.get("formatting", 0)),
        }
        matched_skills = sorted(result.get("matched_skills", []))
        missing_skills = sorted(result.get("missing_skills", []))

        return overall_score, breakdown, matched_skills, missing_skills
