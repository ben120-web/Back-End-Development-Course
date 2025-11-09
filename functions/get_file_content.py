import os

from config import MAX_FILE_CONTENT_LENGTH

def get_file_content(working_directory, file_path):
    try:
        # Convert both to absolute paths.
        abs_work = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        abs_work_with_sep = abs_work if abs_work.endswith(os.sep) else abs_work + os.sep
        is_inside = full_path.startswith(abs_work_with_sep)

        if not is_inside:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_path, "r", encoding="utf-8") as source:
            content = source.read()

        if len(content) > MAX_FILE_CONTENT_LENGTH:
            truncated_content = content[:MAX_FILE_CONTENT_LENGTH]
            return truncated_content + f'[...File "{file_path}" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'

        return content

    except Exception as exc:
        return f'Error: {exc}'
    
def schema_get_file_content(types):
    schema_get_file_content = types.FunctionDeclaration(
        name = "get_file_content",
        description = "Read the content of a file.",
        parameters = types.Schema(
            type = types.Type.OBJECT,
            properties = {
                "file_path": types.Schema(
                    type = types.Type.STRING,
                    description = "The file to read content from",
                )
            },
            required = ["file_path"],
        )
    )
    
    available_functions = types.Tool(
        function_declarations = [
            schema_get_file_content,
        ]
    )
    
    return schema_get_file_content, available_functions