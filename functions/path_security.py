"""Shared path-boundary checks for agent tools."""

from pathlib import Path


def resolve_in_workspace(working_directory: str, requested_path: str = ".") -> tuple[Path, Path]:
    """Return resolved workspace/target paths or raise on boundary escape."""
    workspace = Path(working_directory).resolve(strict=True)
    target = (workspace / requested_path).resolve(strict=False)
    if target != workspace and workspace not in target.parents:
        raise ValueError(f'Path "{requested_path}" is outside the permitted working directory')
    return workspace, target
