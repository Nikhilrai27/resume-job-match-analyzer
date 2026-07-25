import json
from pathlib import Path

from sqlalchemy.orm import Session

from careermatch_ai.domain.entities.analysis import ResumeAnalysis
from careermatch_ai.domain.entities.resume import ResumeAggregate
from careermatch_ai.infrastructure.db.models.analysis import ResumeAnalysisModel
from careermatch_ai.infrastructure.db.models.resume import ResumeModel


class ResumeRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def save_resume(self, user_id: str, filename: str, file_path: Path, resume: ResumeAggregate, optimized_markdown: str) -> ResumeModel:
        record = ResumeModel(
            user_id=user_id,
            original_filename=filename,
            storage_path=str(file_path),
            extracted_text=resume.raw_text,
            optimized_resume_markdown=optimized_markdown,
        )
        self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record

    def save_analysis(self, resume_record: ResumeModel, analysis: ResumeAnalysis) -> None:
        for item in analysis.company_scores:
            row = ResumeAnalysisModel(
                resume_id=resume_record.id,
                company_slug=item.company_slug,
                overall_score=item.overall_score,
                explanation_json=json.dumps(
                    {
                        "score_breakdown": item.score_breakdown,
                        "matched_skills": item.matched_skills,
                        "missing_skills": item.missing_skills,
                        "gaps": item.gaps,
                        "recommendations": item.recommendations,
                        "rewritten_bullets": item.rewritten_bullets,
                    }
                ),
            )
            self._db.add(row)
        self._db.commit()

    def get_resume_for_user(self, resume_id: str, user_id: str) -> ResumeModel | None:
        return (
            self._db.query(ResumeModel)
            .filter(ResumeModel.id == resume_id, ResumeModel.user_id == user_id)
            .one_or_none()
        )
