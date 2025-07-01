import os
import sys
from dotenv import load_dotenv
from google import genai

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

# Generate response
try:
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=prompt
    )
    
    print("\nResponse:\n" + response.text)

    # Output results
    if "--verbose" in sys.argv:
        print(f"User prompt:  {prompt}")
        print(f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)


