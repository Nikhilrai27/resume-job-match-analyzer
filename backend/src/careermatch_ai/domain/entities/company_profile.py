from dataclasses import dataclass, field


@dataclass(frozen=True)
class ATSWeights:
    skill_match: float
    experience_relevance: float
    education_fit: float
    project_relevance: float
    certification_boost: float
    formatting: float


@dataclass(frozen=True)
class CompanyProfile:
    slug: str
    display_name: str
    sector: str
    focus_skills: list[str]
    preferred_certifications: list[str]
    required_sections: list[str]
    preferred_keywords: list[str]
    ats_weights: ATSWeights
    minimum_experience_years: int = 0
    keywords_by_weight: dict[str, float] = field(default_factory=dict)
