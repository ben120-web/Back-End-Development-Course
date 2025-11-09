import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.combine_functions import combine_all_function_declarations
from functions.call_function import call_function

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
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = combine_all_function_declarations(types)

messages = [prompt]

# Generate response
try:
    
    max_iterations = 20
    
    for iteration in range(max_iterations):
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], 
                                            system_instruction=system_prompt),
            
        )
        
        # Update the next prompt, with the response of the model.
        for candidate in response.candidates:
            messages.append(candidate.content)
            
        
        if response.text and not response.function_calls:
            print("Final response:")
            print(response.text)
            break  # Exit the loop
        
        # If not done, we must have function calls to handle.
        function_calls = getattr(response, "function_calls", None) or []
    
        function_responses = []
        
        for function_call in function_calls:
            
            
            fc_result = call_function(function_call, verbose="--verbose" in sys.argv)
            function_responses.append(fc_result.parts[0])

            try:
                payload = fc_result.parts[0].function_response.response
            except Exception:
                raise RuntimeError("Function call result missing function_response.response")

            result_text = payload.get("result", "")
            print(result_text)  # always print so tests can match output
        
        if function_responses:    
            messages.append(types.Content(
                role = "user",
                parts = function_responses
            ))
                            
        # Output results
        if "--verbose" in sys.argv:
            print(f"User prompt:  {prompt}")
            print(f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
