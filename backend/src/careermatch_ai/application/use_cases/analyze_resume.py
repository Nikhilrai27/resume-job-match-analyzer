from pathlib import Path
from uuid import uuid4

from careermatch_ai.application.services.company_matching_service import CompanyMatchingService
from careermatch_ai.domain.entities.analysis import ResumeAnalysis
from careermatch_ai.domain.entities.resume import ResumeAggregate
from careermatch_ai.infrastructure.parsers.resume_parser import ResumeParser


class AnalyzeResumeUseCase:
    def __init__(
        self,
        parser: ResumeParser,
        matcher: CompanyMatchingService,
    ) -> None:
        self._parser = parser
        self._matcher = matcher

    def execute(self, file_path: Path, resume_id: str | None = None) -> tuple[ResumeAggregate, ResumeAnalysis]:
        resume = self._parser.parse(file_path)
        company_scores = self._matcher.match(resume)
        global_gaps = sorted({gap for company in company_scores for gap in company.gaps})[:8]
        overall_ats = round(sum(company.overall_score for company in company_scores) / max(len(company_scores), 1), 2)
        analysis = ResumeAnalysis(
            resume_id=resume_id or str(uuid4()),
            ats_score=overall_ats,
            global_gaps=global_gaps,
            company_scores=company_scores,
        )
        return resume, analysis
