"""
Localhost (vLLM / compatible) client factory.
"""

import os

from dotenv import load_dotenv

load_dotenv()


def get_localhost_async_client(base_url: str = "http://localhost:8000/v1", api_key: str = ""):
    """Create an async OpenAI client pointing at a local server.

    Args:
        base_url: Base URL of the local OpenAI-compatible server.
        api_key: API key (usually empty for local servers).
    """
    from openai import AsyncOpenAI
    return AsyncOpenAI(api_key=api_key, base_url=base_url)
