"""Agent tool for time-bounded Python subprocess execution."""

import subprocess
import sys

from functions.path_security import resolve_in_workspace


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
        )
        parts = [f"EXIT_CODE: {result.returncode}"]
        parts.append(f"STDOUT: {(result.stdout or '').rstrip()}")
        parts.append(f"STDERR: {(result.stderr or '').rstrip()}")
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
