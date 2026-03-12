"""
Groq client factory (uses OpenAI-compatible API).
"""

import os

from dotenv import load_dotenv

load_dotenv()


def get_groq_async_client():
    """Create an async OpenAI client pointing at the Groq API."""
    from openai import AsyncOpenAI
    return AsyncOpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
    )
