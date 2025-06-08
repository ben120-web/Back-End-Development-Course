import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=api_key)

response = client.models.generate_content(model='gemini-2.0-flash-001', contents="Why is Boot.Dev such a great place to learn backend development? Use one paragrapgh minimum")

print(response.text)

print(response.usage_metadata.prompt_token_count)
print(response.usage_metadata.candidates_token_count)