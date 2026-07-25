from pathlib import Path

from careermatch_ai.domain.entities.resume import EducationEntry, ExperienceEntry, ProjectEntry, ResumeAggregate
from careermatch_ai.infrastructure.llm.llm_service import LLMService

try:
    import docx
except ImportError:
    docx = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


class ResumeParser:
    def __init__(self, llm_service: LLMService) -> None:
        self._llm = llm_service

    def parse(self, file_path: Path) -> ResumeAggregate:
        raw_text = self._extract_text(file_path)
        return self._build_resume(raw_text)

    def _extract_text(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            if pdfplumber is None:
                raise ImportError("pdfplumber is required for PDF parsing.")
            with pdfplumber.open(file_path) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)

        if suffix == ".docx":
            if docx is None:
                raise ImportError("python-docx is required for DOCX parsing.")
            document = docx.Document(file_path)
            return "\n".join(paragraph.text for paragraph in document.paragraphs)

        if suffix in {".txt", ".md"}:
            return file_path.read_text(encoding="utf-8")

        raise ValueError(f"Unsupported resume format: {suffix}")

    def _build_resume(self, raw_text: str) -> ResumeAggregate:
        data = self._llm.parse_resume(raw_text)
        return ResumeAggregate(
            candidate_name=data.get("candidate_name") or "Unknown Candidate",
            email=data.get("email") or "",
            phone=data.get("phone") or "",
            summary=data.get("summary") or "",
            skills=sorted(data.get("skills", [])),
            education=[
                EducationEntry(
                    degree=item.get("degree", ""),
                    institution=item.get("institution", ""),
                    year=item.get("year", ""),
                )
                for item in data.get("education", [])
            ],
            experience=[
                ExperienceEntry(
                    title=item.get("title", ""),
                    company=item.get("company", ""),
                    years=float(item.get("years", 0)),
                    bullets=item.get("bullets", []),
                )
                for item in data.get("experience", [])
            ],
            projects=[
                ProjectEntry(
                    name=item.get("name", ""),
                    summary=item.get("summary", ""),
                    technologies=item.get("technologies", []),
                )
                for item in data.get("projects", [])
            ],
            certifications=data.get("certifications", []),
            raw_text=raw_text,
            sections_present=data.get("sections_present", []),
        )
