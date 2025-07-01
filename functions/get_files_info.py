import os

def get_files_info(working_directory, directory=None):
    try:
        display_dir = directory if directory is not None else "."
        full_path = os.path.join(working_directory, display_dir)

        real_working_dir = os.path.realpath(working_directory)
        real_full_path = os.path.realpath(full_path)

        # Secure: prevent path escaping
        if os.path.commonpath([real_full_path, real_working_dir]) != real_working_dir:
            return f'Error: Cannot list "{display_dir}" as it is outside the permitted working directory'

        if not os.path.isdir(real_full_path):
            return f'Error: "{display_dir}" is not a directory'

        result_lines = []
        for entry in os.listdir(real_full_path):  # <- unsorted, to match real order
            entry_path = os.path.join(real_full_path, entry)
            is_dir = os.path.isdir(entry_path)
            try:
                size = os.path.getsize(entry_path)
            except Exception:
                size = "unknown"
            result_lines.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: {e}"
