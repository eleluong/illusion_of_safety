"""
JSON parsing helper for extracting structured data from LLM responses.
"""

import json
import re


def parse_json(text: str) -> dict:
    """Extract a JSON object from an LLM response, handling fenced code blocks.

    Tries three strategies in order:
    1. Direct JSON parse
    2. Strip markdown code fences and parse
    3. Find first '{' to last '}' and parse

    Args:
        text: Raw text from an LLM response.

    Returns:
        Parsed dictionary.

    Raises:
        ValueError: If no valid JSON could be extracted.
    """
    text = text.strip()

    # Attempt 1: direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Attempt 2: strip markdown code fence
    match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Attempt 3: find first '{' … last '}'
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not extract JSON from model response: {text[:300]!r}")
