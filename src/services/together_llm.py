"""
Together AI client factory.
"""

import os

from dotenv import load_dotenv

load_dotenv()


def get_together_client():
    """Create a synchronous Together client."""
    from together import Together
    return Together()


def get_async_together_client():
    """Create an asynchronous Together client."""
    from together import AsyncTogether
    return AsyncTogether()
