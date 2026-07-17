"""Agent tool for time-bounded Python subprocess execution."""

import os
import subprocess
import sys

from config import MAX_PROCESS_OUTPUT_LENGTH
from functions.path_security import resolve_in_workspace

_SAFE_ENVIRONMENT_KEYS = ("LANG", "LC_ALL", "PATH", "SYSTEMROOT", "TEMP", "TMP", "TMPDIR", "WINDIR")


def _child_environment() -> dict[str, str]:
    """Keep interpreter essentials while withholding credentials from child code."""
    environment = {key: os.environ[key] for key in _SAFE_ENVIRONMENT_KEYS if key in os.environ}
    environment.update({"PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1"})
    return environment


def _bounded_output(value: str) -> str:
    if len(value) <= MAX_PROCESS_OUTPUT_LENGTH:
        return value.rstrip()
    omitted = len(value) - MAX_PROCESS_OUTPUT_LENGTH
    return f"{value[:MAX_PROCESS_OUTPUT_LENGTH].rstrip()}\n[truncated {omitted} characters]"


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        workspace, target = resolve_in_workspace(working_directory, file_path)
        if not target.is_file():
            return f'Error: File "{file_path}" not found.'
        if target.suffix != ".py":
            return f'Error: "{file_path}" is not a Python file.'
        result = subprocess.run(
            [sys.executable, str(target), *(args or [])],
            cwd=workspace,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
            env=_child_environment(),
        )
        parts = [f"EXIT_CODE: {result.returncode}"]
        parts.append(f"STDOUT: {_bounded_output(result.stdout or '')}")
        parts.append(f"STDERR: {_bounded_output(result.stderr or '')}")
        return "\n".join(parts)
    except subprocess.TimeoutExpired:
        return "Error: Python process exceeded the 30-second timeout"
    except (OSError, ValueError) as error:
        return f"Error: executing Python file: {error}"


def schema_run_python_file(types):
    declaration = types.FunctionDeclaration(
        name="run_python_file",
        description="Run a Python file inside the workspace with a 30-second timeout.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(type=types.Type.STRING),
                "args": types.Schema(
                    type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING)
                ),
            },
            required=["file_path"],
        ),
    )
    return declaration, types.Tool(function_declarations=[declaration])
