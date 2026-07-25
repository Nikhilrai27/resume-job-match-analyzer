from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from careermatch_ai.api.dependencies import get_analyze_resume_use_case, get_database, get_resume_rendering_service
from careermatch_ai.application.dto.schemas import ResumeAnalysisResponse, ResumeExportResponse, ResumeUploadResponse
from careermatch_ai.application.services.resume_rendering_service import ResumeRenderingService
from careermatch_ai.application.use_cases.analyze_resume import AnalyzeResumeUseCase
from careermatch_ai.core.settings import get_settings
from careermatch_ai.infrastructure.auth.current_user import get_current_user
from careermatch_ai.infrastructure.db.models.user import UserModel
from careermatch_ai.infrastructure.repositories.resume_repository import ResumeRepository


router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    file: UploadFile = File(...),
    use_case: AnalyzeResumeUseCase = Depends(get_analyze_resume_use_case),
    renderer: ResumeRenderingService = Depends(get_resume_rendering_service),
    db: Session = Depends(get_database),
    current_user: UserModel = Depends(get_current_user),
) -> ResumeAnalysisResponse:
    settings = get_settings()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    target_path = Path(settings.upload_dir) / f"{uuid4()}-{file.filename}"
    target_path.write_bytes(await file.read())

    repository = ResumeRepository(db)
    resume, initial_analysis = use_case.execute(target_path)
    optimized_markdown = renderer.render_markdown(resume, initial_analysis)
    resume_record = repository.save_resume(current_user.id, file.filename, target_path, resume, optimized_markdown)
    resume, analysis = use_case.execute(target_path, resume_id=resume_record.id)
    optimized_markdown = renderer.render_markdown(resume, analysis)
    resume_record.optimized_resume_markdown = optimized_markdown
    db.add(resume_record)
    db.commit()
    repository.save_analysis(resume_record, analysis)

    companies = [
        {
            "company_slug": item.company_slug,
            "overall_score": item.overall_score,
            "score_breakdown": item.score_breakdown,
            "matched_skills": item.matched_skills,
            "missing_skills": item.missing_skills,
            "gaps": item.gaps,
            "recommendations": item.recommendations,
            "rewritten_bullets": item.rewritten_bullets,
        }
        for item in analysis.company_scores
    ]

    return ResumeAnalysisResponse(
        resume_id=analysis.resume_id,
        ats_score=analysis.ats_score,
        global_gaps=analysis.global_gaps,
        companies=companies,
        generated_resume_markdown=optimized_markdown,
    )


@router.post("/upload", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume_only(
    file: UploadFile = File(...),
    db: Session = Depends(get_database),
    current_user: UserModel = Depends(get_current_user),
) -> ResumeUploadResponse:
    settings = get_settings()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    target_path = Path(settings.upload_dir) / f"{uuid4()}-{file.filename}"
    target_path.write_bytes(await file.read())

    from careermatch_ai.infrastructure.parsers.resume_parser import ResumeParser
    from careermatch_ai.infrastructure.llm.llm_service import LLMService

    llm_service = LLMService()
    parser = ResumeParser(llm_service)
    resume = parser.parse(target_path)

    repository = ResumeRepository(db)
    resume_record = repository.save_resume(
        user_id=current_user.id,
        filename=file.filename,
        file_path=target_path,
        resume=resume,
        optimized_markdown="",
    )

    return ResumeUploadResponse(
        resume_id=resume_record.id,
        filename=file.filename,
        status="uploaded",
    )


@router.get("/{resume_id}/download", response_model=ResumeExportResponse)
async def download_optimized_resume(
    resume_id: str,
    format: str = Query(default="md", pattern="^(md|txt)$"),
    db: Session = Depends(get_database),
    current_user: UserModel = Depends(get_current_user),
) -> ResumeExportResponse:
    repository = ResumeRepository(db)
    resume_record = repository.get_resume_for_user(resume_id, current_user.id)
    if resume_record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    content = resume_record.optimized_resume_markdown or ""
    media_type = "text/markdown"
    filename = f"optimized-resume-{resume_id}.md"

    if format == "txt":
        content = content.replace("# ", "").replace("## ", "").replace("### ", "")
        media_type = "text/plain"
        filename = f"optimized-resume-{resume_id}.txt"

    return ResumeExportResponse(
        filename=filename,
        content=content,
        media_type=media_type,
    )
