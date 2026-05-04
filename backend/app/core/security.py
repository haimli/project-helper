from pathlib import Path

from app.core.exceptions import PathTraversalError


def validate_path(repo_path: str, requested_path: str) -> Path:
    base = Path(repo_path).resolve()
    target = (base / requested_path).resolve()
    if not str(target).startswith(str(base)):
        raise PathTraversalError(f"Path traversal detected: {requested_path}")
    if not target.exists():
        raise FileNotFoundError(f"Path not found: {requested_path}")
    return target
