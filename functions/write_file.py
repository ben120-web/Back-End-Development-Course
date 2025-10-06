import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_work = os.path.abspath(working_directory)
        if not os.path.isdir(abs_work):
            return f'Error: Working directory does not exist: "{working_directory}"'

        full_path = os.path.abspath(os.path.join(abs_work, file_path))
        abs_work_with_sep = abs_work if abs_work.endswith(os.sep) else abs_work + os.sep

        if not full_path.startswith(abs_work_with_sep):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        parent_dir = os.path.dirname(full_path)
        if parent_dir and not os.path.isdir(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(full_path, 'w', encoding='utf-8') as target:
            target.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as exc:
        return f'Error: {exc}'

def schema_write_file(types):
    
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )
    
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)
    return schema_get_files_info, available_functions