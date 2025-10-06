import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []

    try:
        abs_work = os.path.abspath(working_directory)
        if not os.path.isdir(abs_work):
            return f'Error: Working directory does not exist: "{working_directory}"'

        full_path = os.path.abspath(os.path.join(abs_work, file_path))
        abs_work_with_sep = abs_work if abs_work.endswith(os.sep) else abs_work + os.sep

        if not full_path.startswith(abs_work_with_sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" not found.'

        if not full_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        result = subprocess.run(
            ['python3', full_path, *args],
            cwd=abs_work,
            capture_output=True,
            text=True,
            check=False,
            timeout=30
        )

        stdout_text = result.stdout or ""
        stderr_text = result.stderr or ""

        if result.returncode == 0 and not stdout_text and not stderr_text:
            return "No output produced."

        lines = []
        if result.returncode != 0:
            lines.append(f'Error: Process exited with code {result.returncode}')

        lines.append(f'STDOUT: {stdout_text.rstrip()}')
        lines.append(f'STDERR: {stderr_text.rstrip()}')

        return "\n".join(lines)

    except Exception as exc:
        return f"Error: executing Python file: {exc}"

def schema_run_python_file():
    