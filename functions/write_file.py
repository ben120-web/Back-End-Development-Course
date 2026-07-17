"""Agent tool for bounded text-file writes."""

from functions.path_security import resolve_in_workspace


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        _, target = resolve_in_workspace(working_directory, file_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        # Resolve again after creating parents to catch symlinked directories.
        _, target = resolve_in_workspace(working_directory, file_path)
        target.write_text(content, encoding="utf-8")
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except (OSError, UnicodeError, ValueError) as error:
        return f"Error: {error}"


def schema_write_file(types):
    declaration = types.FunctionDeclaration(
        name="write_file",
        description="Write or overwrite a UTF-8 file inside the selected workspace.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(type=types.Type.STRING),
                "content": types.Schema(type=types.Type.STRING),
            },
            required=["file_path", "content"],
        ),
    )
    return declaration, types.Tool(function_declarations=[declaration])
