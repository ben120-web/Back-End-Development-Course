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
    
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Write or overwrite a file with provided content",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Relative path to the file to write or overwrite.",
                ),
                "content": types.Schema(
                    type = types.Type.STRING,
                    description = "Content to write to the file", 
                ),
            },
            required = ["file_path", "content"],
        ),
    )
    
    available_functions = types.Tool(
    function_declarations=[
        schema_write_file,
    ]
)
    return schema_write_file, available_functions