import pathlib
import subprocess
from typing import Tuple

from langchain_core.tools import tool

# Generated code lives under <cwd>/generated_project
PROJECT_ROOT = pathlib.Path.cwd() / "generated_project"


def normalize_project_path(path: str) -> str:
    """Normalize model-provided paths to a safe relative path under PROJECT_ROOT."""
    cleaned = (path or "").strip().replace("\\", "/")
    if not cleaned:
        raise ValueError("Path cannot be empty")

    # Drop leading slashes so "/src/index.html" does not escape to drive root on Windows.
    cleaned = cleaned.lstrip("/")

    # If the model repeats the project folder, strip it.
    project_prefix = f"{PROJECT_ROOT.name}/"
    if cleaned.startswith(project_prefix):
        cleaned = cleaned[len(project_prefix) :]

    if ".." in pathlib.PurePosixPath(cleaned).parts:
        raise ValueError("Attempt to write outside project root")

    return cleaned


def safe_path_for_project(path: str) -> pathlib.Path:
    """Resolve a path and ensure it stays inside PROJECT_ROOT."""
    root = PROJECT_ROOT.resolve()
    candidate = pathlib.Path(path.strip())

    if candidate.is_absolute():
        resolved = candidate.resolve()
    else:
        resolved = (root / normalize_project_path(path)).resolve()

    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("Attempt to write outside project root") from exc

    return resolved


@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return f"WROTE:{p}"


@tool
def read_file(path: str) -> str:
    """Reads content from a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    if not p.exists():
        return ""
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


@tool
def get_current_directory() -> str:
    """Returns the current working directory."""
    return str(PROJECT_ROOT)


@tool
def list_files(directory: str = ".") -> str:
    """Lists all files in the specified directory within the project root."""
    normalized_directory = (directory or "").strip() or "."
    p = safe_path_for_project(normalized_directory)
    if not p.is_dir():
        return f"ERROR: {p} is not a directory"
    files = [str(f.relative_to(PROJECT_ROOT)) for f in p.glob("**/*") if f.is_file()]
    return "\n".join(files) if files else "No files found."


@tool
def run_cmd(cmd: str, cwd: str = None, timeout: int = 30) -> Tuple[int, str, str]:
    """Runs a shell command in the specified directory and returns the result."""
    cwd_dir = safe_path_for_project(cwd) if cwd else PROJECT_ROOT
    res = subprocess.run(cmd, shell=True, cwd=str(cwd_dir), capture_output=True, text=True, timeout=timeout)
    return res.returncode, res.stdout, res.stderr


def init_project_root() -> str:
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return str(PROJECT_ROOT.resolve())
