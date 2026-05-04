import asyncio
import re
from pathlib import Path

from app.config import settings
from app.core.exceptions import GitCloneError


class GitService:
    async def clone_repo(self, repo_url: str, target_dir: str) -> str:
        repo_path = Path(target_dir)
        repo_path.parent.mkdir(parents=True, exist_ok=True)

        if repo_path.exists():
            return str(repo_path)

        try:
            process = await asyncio.create_subprocess_exec(
                "git", "clone", "--depth", "1", repo_url, str(repo_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            _, stderr = await process.communicate()
            if process.returncode != 0:
                raise GitCloneError(stderr.decode().strip())
            return str(repo_path)
        except FileNotFoundError:
            raise GitCloneError("git is not installed or not in PATH")

    def extract_repo_name(self, repo_url: str) -> str:
        match = re.search(r"github\.com/([^/]+/[^/]+?)(?:\.git)?$", repo_url)
        if match:
            return match.group(1)
        return repo_url.rstrip("/").split("/")[-1]

    def get_repo_local_path(self, repo_name: str) -> str:
        safe_name = repo_name.replace("/", "_")
        return str(Path(settings.REPOS_DIR) / safe_name)
