from google.genai import types
from functions import combine_functions
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


FUNCTION_DICT = {"get_file_content": get_file_content, 
                 "get_files_info": get_files_info, 
                 "run_python_file": run_python_file, 
                 "write_file": write_file,
                 }

def call_function(function_call_part: types.FunctionCall, verbose=False):
    function_name = function_call_part.name
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    fn = FUNCTION_DICT.get(function_name)
    
    if fn is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    result = fn(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )