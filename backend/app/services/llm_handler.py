import os
from openai import OpenAI, APIError, RateLimitError, AuthenticationError
from typing import List, Dict
from app.config import get_settings

# Initialize OpenAI client
try:
    api_key = get_settings().openai_api_key
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
    client = OpenAI(api_key=api_key)
except ValueError as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None

# Load the system prompt from the template file
def load_system_prompt():
    try:
        with open("app/templates/base_chat_prompt.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "You are a helpful assistant." # Fallback prompt

SYSTEM_PROMPT = load_system_prompt()

def get_llm_response(message: str, history: List[Dict[str, str]]) -> str:
    """
    Generates a response from the LLM based on the user's message and conversation history.
    """
    if not client:
        return "LLM service is not configured. Please set the OPENAI_API_KEY."

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=256,
        )
        reply = response.choices[0].message.content
        return reply.strip() if reply else "I'm sorry, I could not generate a response."

    except AuthenticationError:
        return "Authentication with OpenAI failed. Please check your API key."
    except RateLimitError:
        return "Rate limit exceeded. Please try again later."
    except APIError as e:
        return f"An OpenAI API error occurred: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
