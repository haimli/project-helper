from datetime import datetime

from sqlalchemy import Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), unique=True)
    overview: Mapped[str] = mapped_column(Text, nullable=False)
    tech_stack: Mapped[str] = mapped_column(Text, nullable=False)
    directory_structure: Mapped[str] = mapped_column(Text, nullable=False)
    core_modules: Mapped[str] = mapped_column(Text, nullable=False)
    data_flow: Mapped[str] = mapped_column(Text, nullable=False)
    design_patterns: Mapped[str] = mapped_column(Text, nullable=False)
    reading_suggestions: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    project: Mapped["Project"] = relationship(back_populates="analysis_report")
