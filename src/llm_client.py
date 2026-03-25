"""
Thin wrapper around the OpenAI API.
"""

import time
from openai import OpenAI
from src.config import OPENAI_API_KEY, MODEL_NAME

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def call_llm(prompt: str, retries: int = 3, delay: float = 2.0) -> str:
    """Send a prompt to OpenAI and return the text response."""
    client = _get_client()

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=1024,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
            else:
                print(f"[LLM ERROR] All {retries} attempts failed: {e}")
                return ""
