from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from careermatch_ai.infrastructure.db.base import Base


class ResumeAnalysisModel(Base):
    __tablename__ = "resume_analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), index=True)
    company_slug: Mapped[str] = mapped_column(String(100), index=True)
    overall_score: Mapped[float] = mapped_column(Float)
    explanation_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    resume = relationship("ResumeModel", back_populates="analyses")
