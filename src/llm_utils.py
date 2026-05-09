from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Read provider from .env
PROVIDER = os.getenv("LLM_PROVIDER")
if not PROVIDER:
    raise ValueError("LLM_PROVIDER is not set")

PROVIDER = PROVIDER.strip().lower()

# Initialize client
if PROVIDER == "openai":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)
    MODEL = "gpt-4o-mini"

elif PROVIDER == "openrouter":
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENROUTER_API_KEY")

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )
    MODEL = "openai/gpt-4o-mini"

else:
    raise ValueError("Invalid LLM_PROVIDER")


def call_llm(prompt):
    """
    Send prompt to LLM and return response.

    Parameters:
        prompt (str): Input prompt

    Returns:
        str: Model response
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Battery expert. Be precise."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2  # low randomness → consistent outputs
    )

    return response.choices[0].message.content