import json
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.analysis.scanner import DirectoryScanner
from app.analysis.tech_stack import TechStackAnalyzer
from app.analysis.core_modules import CoreModuleAnalyzer
from app.analysis.data_flow import DataFlowAnalyzer
from app.analysis.design_patterns import DesignPatternAnalyzer
from app.analysis.reading_guide import ReadingGuideGenerator
from app.core.progress import ProgressEvent, ProgressManager
from app.core.exceptions import AnalysisError
from app.models.project import Project
from app.models.analysis_report import AnalysisReport
from app.services.git_service import GitService
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)


class ProjectAnalyzer:
    def __init__(self, db: AsyncSession, progress: ProgressManager) -> None:
        self.db = db
        self.progress = progress
        self.git = GitService()
        self.llm = LLMService()
        self.scanner = DirectoryScanner()
        self.tech_stack_analyzer = TechStackAnalyzer(self.llm)
        self.module_analyzer = CoreModuleAnalyzer(self.llm)
        self.data_flow_analyzer = DataFlowAnalyzer(self.llm)
        self.pattern_analyzer = DesignPatternAnalyzer(self.llm)
        self.guide_generator = ReadingGuideGenerator(self.llm)

    async def run_analysis(self, project_id: int, repo_url: str) -> None:
        try:
            await self._update_status(project_id, "analyzing")
            repo_name = self.git.extract_repo_name(repo_url)
            local_path = self.git.get_repo_local_path(repo_name)

            # Stage 1: Clone
            await self._emit(project_id, "cloning", 5, "Cloning repository...")
            repo_path = await self.git.clone_repo(repo_url, local_path)

            # Stage 2: Scan directory
            await self._emit(project_id, "scanning", 15, "Scanning directory structure...")
            dir_tree = self.scanner.scan(repo_path)
            file_stats = self.scanner.get_file_stats(repo_path)
            key_files = self.scanner.find_key_files(repo_path)
            key_file_contents = self._read_key_files(repo_path, key_files)

            # Stage 3: Tech stack
            await self._emit(project_id, "analyzing_tech_stack", 30, "Analyzing tech stack...")
            tech_stack = await self.tech_stack_analyzer.analyze(repo_path, key_file_contents)

            # Stage 4: Core modules
            await self._emit(project_id, "identifying_modules", 50, "Identifying core modules...")
            core_modules = await self.module_analyzer.analyze(repo_path, dir_tree, key_file_contents)

            # Stage 5: Data flow
            await self._emit(project_id, "analyzing_data_flow", 65, "Analyzing data flow...")
            data_flow = await self.data_flow_analyzer.analyze(repo_path, dir_tree, core_modules, key_file_contents)

            # Stage 6: Design patterns
            await self._emit(project_id, "detecting_patterns", 80, "Detecting design patterns...")
            design_patterns = await self.pattern_analyzer.analyze(repo_path, dir_tree, key_file_contents)

            # Stage 7: Reading guide
            await self._emit(project_id, "generating_guide", 90, "Generating reading guide...")
            reading_suggestions = await self.guide_generator.generate(repo_path, dir_tree, core_modules)

            # Stage 8: Save report
            await self._emit(project_id, "saving_report", 95, "Saving analysis report...")
            overview = await self._generate_overview(repo_name, tech_stack, core_modules)

            report = AnalysisReport(
                project_id=project_id,
                overview=overview,
                tech_stack=json.dumps(tech_stack, ensure_ascii=False),
                directory_structure=dir_tree,
                core_modules=json.dumps(core_modules, ensure_ascii=False),
                data_flow=data_flow,
                design_patterns=json.dumps(design_patterns, ensure_ascii=False),
                reading_suggestions=json.dumps(reading_suggestions, ensure_ascii=False),
            )
            self.db.add(report)
            await self._update_status(project_id, "completed")
            await self.progress.complete(project_id)

        except Exception as e:
            logger.exception("Analysis failed for project %d", project_id)
            await self._update_status(project_id, "failed", str(e))
            await self.progress.emit(project_id, ProgressEvent(stage="error", progress=0, detail=str(e)))

    async def _emit(self, project_id: int, stage: str, progress: int, detail: str) -> None:
        await self.progress.emit(project_id, ProgressEvent(stage=stage, progress=progress, detail=detail))

    async def _update_status(self, project_id: int, status: str, error_message: str | None = None) -> None:
        result = await self.db.execute(select(Project).where(Project.id == project_id))
        project = result.scalar_one_or_none()
        if project:
            project.status = status
            if error_message:
                project.error_message = error_message
            await self.db.commit()

    def _read_key_files(self, repo_path: str, key_files: list[str]) -> dict[str, str]:
        from pathlib import Path

        contents = {}
        for f in key_files:
            path = Path(repo_path) / f
            if path.exists() and path.is_file():
                try:
                    text = path.read_text(encoding="utf-8", errors="replace")
                    contents[f] = text[:5000]
                except Exception:
                    pass
        return contents

    async def _generate_overview(self, repo_name: str, tech_stack: dict, core_modules: list) -> str:
        from app.agent.prompts import OVERVIEW_PROMPT

        user_prompt = f"Project: {repo_name}\nTech Stack: {json.dumps(tech_stack, ensure_ascii=False)}\nCore Modules: {json.dumps(core_modules, ensure_ascii=False)}"
        return await self.llm.analyze(OVERVIEW_PROMPT, user_prompt)
