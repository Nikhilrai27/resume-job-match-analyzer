from careermatch_ai.domain.entities.company_profile import CompanyProfile
from careermatch_ai.domain.entities.resume import ResumeAggregate
from careermatch_ai.infrastructure.llm.llm_service import LLMService


class GapAnalyzer:
    def __init__(self, llm_service: LLMService) -> None:
        self._llm = llm_service

    def analyze(self, resume: ResumeAggregate, profile: CompanyProfile, missing_skills: list[str]) -> list[str]:
        return self._llm.analyze_gaps(
            company_name=profile.display_name,
            sector=profile.sector,
            required_sections=profile.required_sections,
            focus_skills=profile.focus_skills,
            preferred_certifications=profile.preferred_certifications,
            min_experience=profile.minimum_experience_years,
            resume_skills=resume.skills,
            experience=[
                {"title": e.title, "company": e.company, "years": e.years, "bullets": e.bullets}
                for e in resume.experience
            ],
            sections_present=resume.sections_present,
            certifications=resume.certifications,
            has_summary=bool(resume.summary.strip()),
            project_count=len(resume.projects),
            missing_skills=missing_skills,
        )
