import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_file_info

# Load environment variables from .env
load_dotenv()

# Retrieve Gemini API key
api_key = os.environ.get("GEMINI_API_KEY")

# Fail fast if key not found
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in environment.")
    sys.exit(1)

# Check if prompt argument is provided
if len(sys.argv) <= 1:
    print("ERROR: No prompt provided. Please provide a prompt as a command-line argument.")
    sys.exit(1)

# Assemble prompt from command-line args
args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
prompt = " ".join(args)

# Initialize GenAI client
client = genai.Client(api_key=api_key)


# Set a system prompt.
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info, available_functions = schema_get_file_info(types)

# Generate response
try:
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=prompt,
        config=types.GenerateContentConfig(tools=[available_functions], 
                                           system_instruction=system_prompt),
        
    )
    
    print("\nResponse:")
    function_calls = getattr(response, "function_calls", None) or []
    if function_calls:
        for function_call in function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text or "")

    # Output results
    if "--verbose" in sys.argv:
        print(f"User prompt:  {prompt}")
        print(f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
