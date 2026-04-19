import os
from dotenv import load_dotenv
from google import genai
import time

# Load .env from backend folder explicitly
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Debug check
print("API KEY:", api_key)

# Fail fast if missing
if not api_key:
    raise ValueError("❌ API key not found. Check your .env file")

# Initialize client with key
client = genai.Client(api_key=api_key)


def generate_response(prompt: str, history=None) -> str:
    if history:
        history_text = "Previous conversation:\n"
        for msg in history:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            history_text += f"{role.capitalize()}: {content}\n"
        prompt = f"{history_text}\nCurrent Request:\n{prompt}"

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text

        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                print(f"LLM 503 error, retrying in {attempt + 2}s...")
                time.sleep(attempt + 2)
                continue

            # 🔥 Fallback to gemini-1.5-pro (better than flash)
            print(f"Trying fallback model gemini-1.5-pro due to: {str(e)}")
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-pro",
                    contents=prompt,
                )
                return response.text

            except Exception as final_e:
                return f"Error connecting to LLM (even after fallback): {str(final_e)}"