from careermatch_ai.domain.entities.analysis import ScoreExplanation
from careermatch_ai.domain.entities.resume import ResumeAggregate
from careermatch_ai.domain.services.bullet_rewriter import BulletRewriter
from careermatch_ai.domain.services.gap_analyzer import GapAnalyzer
from careermatch_ai.infrastructure.config.company_loader import CompanyProfileLoader
from careermatch_ai.infrastructure.llm.llm_service import LLMService
from careermatch_ai.infrastructure.scoring.ats_engine import ATSScoringEngine


class CompanyMatchingService:
    def __init__(
        self,
        loader: CompanyProfileLoader,
        scoring_engine: ATSScoringEngine,
        gap_analyzer: GapAnalyzer,
        bullet_rewriter: BulletRewriter,
        llm_service: LLMService,
    ) -> None:
        self._loader = loader
        self._scoring_engine = scoring_engine
        self._gap_analyzer = gap_analyzer
        self._bullet_rewriter = bullet_rewriter
        self._llm = llm_service

    def match(self, resume: ResumeAggregate) -> list[ScoreExplanation]:
        explanations: list[ScoreExplanation] = []
        all_bullets = [bullet for experience in resume.experience for bullet in experience.bullets]
        rewrites = self._bullet_rewriter.rewrite(all_bullets[:5])

        for profile in self._loader.load_all():
            score, breakdown, matched_skills, missing_skills = self._scoring_engine.score(resume, profile)
            gaps = self._gap_analyzer.analyze(resume, profile, missing_skills)
            recommendations = self._llm.generate_recommendations(
                company_name=profile.display_name,
                missing_skills=missing_skills,
                gaps=gaps,
                resume_skills=resume.skills,
            )
            explanations.append(
                ScoreExplanation(
                    company_slug=profile.slug,
                    overall_score=score,
                    score_breakdown=breakdown,
                    matched_skills=matched_skills,
                    missing_skills=missing_skills,
                    gaps=gaps,
                    recommendations=recommendations,
                    rewritten_bullets=[item.rewritten for item in rewrites],
                )
            )

        return sorted(explanations, key=lambda item: item.overall_score, reverse=True)
