"""CLI for the workspace-bounded Gemini coding agent."""

import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import DEFAULT_MODEL
from functions.call_function import call_function
from functions.combine_functions import combine_all_function_declarations

SYSTEM_PROMPT = """You are a coding agent operating inside a restricted workspace.
Plan briefly, inspect relevant files, make the smallest useful change, and run
available tests. All tool paths must be relative to the workspace. Never attempt
to bypass the workspace boundary or access credentials.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="+", help="Task for the coding agent")
    parser.add_argument("--workspace", default="./calculator")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--max-iterations", type=int, default=20)
    parser.add_argument(
        "--model",
        default=os.environ.get("GEMINI_MODEL", DEFAULT_MODEL),
        help="Stable Gemini model identifier (or set GEMINI_MODEL)",
    )
    return parser.parse_args()


def main() -> int:
    load_dotenv()
    args = parse_args()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY is not set")

    client = genai.Client(api_key=api_key)
    tools = combine_all_function_declarations(types)
    messages: list[types.Content | str] = [" ".join(args.prompt)]

    for _ in range(args.max_iterations):
        response = client.models.generate_content(
            model=args.model,
            contents=messages,
            config=types.GenerateContentConfig(tools=[tools], system_instruction=SYSTEM_PROMPT),
        )
        messages.extend(candidate.content for candidate in response.candidates)
        if response.text and not response.function_calls:
            print(response.text)
            return 0

        function_responses = [
            call_function(call, args.verbose, args.workspace)
            for call in response.function_calls or []
        ]
        if function_responses:
            messages.append(
                types.Content(role="user", parts=[r.parts[0] for r in function_responses])
            )
        if args.verbose and response.usage_metadata:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")

    raise SystemExit(f"Agent exceeded {args.max_iterations} iterations")


if __name__ == "__main__":
    raise SystemExit(main())
