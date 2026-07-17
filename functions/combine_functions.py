from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_file_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


def combine_all_function_declarations(types):
    d1, _ = schema_get_file_info(types)
    d2, _ = schema_get_file_content(types)
    d3, _ = schema_run_python_file(types)
    d4, _ = schema_write_file(types)

    available_functions = types.Tool(function_declarations=[d1, d2, d3, d4])
    return available_functions
