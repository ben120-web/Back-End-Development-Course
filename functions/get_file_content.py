"""Agent tool for bounded text-file reads."""

from config import MAX_FILE_CONTENT_LENGTH
from functions.path_security import resolve_in_workspace


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        _, target = resolve_in_workspace(working_directory, file_path)
        if not target.is_file():
            return f'Error: File not found or is not a regular file: "{file_path}"'
        content = target.read_text(encoding="utf-8")
        if len(content) > MAX_FILE_CONTENT_LENGTH:
            return (
                content[:MAX_FILE_CONTENT_LENGTH]
                + f'\n[File "{file_path}" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'
            )
        return content
    except (OSError, UnicodeError, ValueError) as error:
        return f"Error: {error}"


def schema_get_file_content(types):
    declaration = types.FunctionDeclaration(
        name="get_file_content",
        description="Read a UTF-8 text file inside the selected workspace.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="File path relative to the workspace.",
                )
            },
            required=["file_path"],
        ),
    )
    return declaration, types.Tool(function_declarations=[declaration])
