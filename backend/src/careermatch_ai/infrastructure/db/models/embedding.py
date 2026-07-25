from uuid import uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from careermatch_ai.infrastructure.db.base import Base

try:
    from pgvector.sqlalchemy import Vector
except ImportError:  # pragma: no cover
    Vector = None


class ResumeEmbeddingModel(Base):
    __tablename__ = "resume_embeddings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), index=True)
    if Vector is not None:  # pragma: no branch
        embedding: Mapped[list[float]] = mapped_column(Vector(384))
