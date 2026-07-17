"""Agent tool for bounded directory listings."""

from functions.path_security import resolve_in_workspace


def get_files_info(working_directory: str, directory: str | None = None) -> str:
    requested = directory or "."
    try:
        _, target = resolve_in_workspace(working_directory, requested)
        if not target.is_dir():
            return f'Error: "{requested}" is not a directory'
        lines = []
        for entry in sorted(target.iterdir(), key=lambda item: item.name.lower()):
            size = entry.stat().st_size
            lines.append(f"- {entry.name}: file_size={size} bytes, is_dir={entry.is_dir()}")
        return "\n".join(lines)
    except (OSError, ValueError) as error:
        return f"Error: {error}"


def schema_get_file_info(types):
    declaration = types.FunctionDeclaration(
        name="get_files_info",
        description="List files and sizes inside a workspace directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={"directory": types.Schema(type=types.Type.STRING)},
        ),
    )
    return declaration, types.Tool(function_declarations=[declaration])
