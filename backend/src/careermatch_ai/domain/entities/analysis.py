from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScoreExplanation:
    company_slug: str
    overall_score: float
    score_breakdown: dict[str, float]
    matched_skills: list[str]
    missing_skills: list[str]
    gaps: list[str]
    recommendations: list[str]
    rewritten_bullets: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ResumeAnalysis:
    resume_id: str
    ats_score: float
    global_gaps: list[str]
    company_scores: list[ScoreExplanation]
