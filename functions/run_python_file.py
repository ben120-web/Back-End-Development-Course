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

        lines = []
        if result.returncode != 0:
            lines.append(f'Error: Process exited with code {result.returncode}')

        lines.append(f'STDOUT: {stdout_text.rstrip()}')
        lines.append(f'STDERR: {stderr_text.rstrip()}')

        return "\n".join(lines)

    except Exception as exc:
        return f"Error: executing Python file: {exc}"
    
def schema_run_python_file(types):
    schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Run a Python File",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "Runs a given python file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description = "Optional CLI argument"
            ),
        },
        required = ["file_path"],
    )
)
    
    available_functions = types.Tool(
        function_declarations = [
            schema_run_python_file,
        ]
    )
    
    return schema_run_python_file, available_functions