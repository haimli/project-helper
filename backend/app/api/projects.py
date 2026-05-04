import json
from typing import AsyncGenerator

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from app.core.progress import ProgressManager
from app.database import async_session_maker, get_db
from app.models.analysis_report import AnalysisReport
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectListResponse, ProjectResponse
from app.schemas.report import ReportResponse
from app.services.analyzer import ProjectAnalyzer
from app.services.cache_service import CacheService
from app.services.git_service import GitService

router = APIRouter()


@router.post("/analyze", response_model=ProjectResponse)
async def analyze_project(
    request: ProjectCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    cached = await CacheService.get_cached_project(db, request.repo_url)
    if cached:
        return cached

    existing = await db.execute(select(Project).where(Project.repo_url == request.repo_url))
    project = existing.scalar_one_or_none()
    if project:
        return project

    git = GitService()
    repo_name = git.extract_repo_name(request.repo_url)
    project = Project(repo_url=request.repo_url, repo_name=repo_name, status="pending")
    db.add(project)
    await db.commit()
    await db.refresh(project)

    progress = ProgressManager.get_instance()

    async def run():
        async with async_session_maker() as bg_db:
            from app.services.analyzer import ProjectAnalyzer
            analyzer = ProjectAnalyzer(bg_db, progress)
            await analyzer.run_analysis(project.id, request.repo_url)

    background_tasks.add_task(run)
    return project


@router.get("", response_model=ProjectListResponse)
async def list_projects(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    total_result = await db.execute(select(func.count(Project.id)))
    total = total_result.scalar() or 0
    result = await db.execute(select(Project).order_by(Project.created_at.desc()).offset(skip).limit(limit))
    items = list(result.scalars().all())
    return ProjectListResponse(items=items, total=total)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/{project_id}/report", response_model=ReportResponse)
async def get_report(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AnalysisReport).where(AnalysisReport.project_id == project_id))
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get("/{project_id}/progress")
async def stream_progress(project_id: int):
    progress = ProgressManager.get_instance()
    queue = await progress.subscribe(project_id)

    async def event_generator() -> AsyncGenerator[dict, None]:
        try:
            while True:
                event = await queue.get()
                yield {"event": "progress", "data": json.dumps(event)}
                if event.get("stage") in ("complete", "error"):
                    break
        finally:
            progress.unsubscribe(project_id, queue)

    return EventSourceResponse(event_generator())


@router.delete("/{project_id}")
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await db.delete(project)
    await db.commit()
    return {"ok": True}
