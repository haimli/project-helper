import os
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".idea", ".vscode", "dist", "build", ".next", ".nuxt"}

KEY_FILE_NAMES = {
    "README.md", "README.rst", "README.txt", "readme.md",
    "package.json", "requirements.txt", "Pipfile", "pyproject.toml", "setup.py", "setup.cfg",
    "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "Makefile", "Dockerfile",
    "docker-compose.yml", "docker-compose.yaml",
    ".env.example", "tsconfig.json", "vite.config.ts", "vite.config.js",
    "next.config.js", "next.config.ts", "nuxt.config.ts",
    "webpack.config.js", "rollup.config.js",
}


class DirectoryScanner:
    def scan(self, repo_path: str) -> str:
        lines = []
        self._walk(Path(repo_path), "", lines)
        return "\n".join(lines)

    def _walk(self, directory: Path, prefix: str, lines: list[str]) -> None:
        entries = sorted(directory.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
        for entry in entries:
            if entry.name in SKIP_DIRS or entry.name.startswith("."):
                continue
            lines.append(f"{prefix}{entry.name}")
            if entry.is_dir():
                self._walk(entry, f"{prefix}  ", lines)

    def get_file_stats(self, repo_path: str) -> dict[str, int]:
        stats: dict[str, int] = {}
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            for f in files:
                ext = Path(f).suffix.lower()
                if ext:
                    stats[ext] = stats.get(ext, 0) + 1
        return dict(sorted(stats.items(), key=lambda x: -x[1]))

    def find_key_files(self, repo_path: str) -> list[str]:
        result = []
        base = Path(repo_path)
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            for f in files:
                if f in KEY_FILE_NAMES or f.startswith("main.") or f.startswith("app.") or f.startswith("index."):
                    rel = Path(root).relative_to(base) / f
                    result.append(str(rel).replace("\\", "/"))
        return result
