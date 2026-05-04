import os
import re
from pathlib import Path

from langchain_core.tools import tool

from app.core.security import validate_path


def create_project_tools(repo_path: str) -> list:
    @tool
    def read_file(file_path: str) -> str:
        """Read the content of a source file in the project.
        Args:
            file_path: Relative path from project root, e.g. 'src/main.py'
        """
        validated = validate_path(repo_path, file_path)
        content = validated.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        if len(lines) > 500:
            return "\n".join(lines[:500]) + f"\n... [truncated, file has {len(lines)} lines]"
        return content

    @tool
    def search_code(query: str, file_pattern: str = "*") -> str:
        """Search for a string or regex pattern across the project's source files.
        Args:
            query: The search string or pattern.
            file_pattern: Glob filter, e.g. '*.py', '*.ts'. Default '*' searches all.
        """
        results = []
        base = Path(repo_path)
        skip = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
        pattern = re.compile(query, re.IGNORECASE)

        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in skip]
            for f in files:
                if file_pattern != "*" and not f.endswith(file_pattern.lstrip("*")):
                    continue
                filepath = Path(root) / f
                try:
                    for i, line in enumerate(filepath.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                        if pattern.search(line):
                            rel = filepath.relative_to(base)
                            results.append(f"{rel}:{i}: {line.strip()}")
                            if len(results) >= 20:
                                return "\n".join(results)
                except Exception:
                    continue
        if not results:
            return "No matches found."
        return "\n".join(results)

    @tool
    def list_files(directory: str = ".") -> str:
        """List files and subdirectories in a directory.
        Args:
            directory: Relative path from project root. Default '.' lists the root.
        """
        validated = validate_path(repo_path, directory)
        if not validated.is_dir():
            return f"{directory} is not a directory."
        entries = []
        for entry in sorted(validated.iterdir(), key=lambda e: (not e.is_dir(), e.name)):
            if entry.name.startswith(".") or entry.name in {"node_modules", "__pycache__", ".git"}:
                continue
            size = ""
            if entry.is_file():
                try:
                    size = f" ({entry.stat().st_size} bytes)"
                except OSError:
                    pass
            kind = "DIR " if entry.is_dir() else "FILE"
            entries.append(f"{kind} {entry.name}{size}")
        if not entries:
            return "Empty directory."
        return "\n".join(entries)

    return [read_file, search_code, list_files]
