from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.analysis_report import AnalysisReport


class CacheService:
    @staticmethod
    async def get_cached_project(db: AsyncSession, repo_url: str) -> Project | None:
        result = await db.execute(select(Project).where(Project.repo_url == repo_url))
        project = result.scalar_one_or_none()
        if project and project.status == "completed":
            return project
        return None

    @staticmethod
    async def get_cached_report(db: AsyncSession, project_id: int) -> AnalysisReport | None:
        result = await db.execute(select(AnalysisReport).where(AnalysisReport.project_id == project_id))
        return result.scalar_one_or_none()
