"""
Response guardrail assessment.

Analyses whether a model's final response contains harmful content or fulfills
the harmful intent of the user prompt.
"""

import json
import logging
import os
from typing import Optional

import yaml

from .schemas import ResponseGuardrailResponse
from .json_parser import parse_json

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Load response guardrail prompt from YAML
# ---------------------------------------------------------------------------

_RESPONSE_PROMPT_YAML_PATH = os.path.join(
    os.path.dirname(__file__), os.pardir, "prompts", "guardrail_prompt_response.yml"
)


def _load_response_prompt() -> str:
    with open(_RESPONSE_PROMPT_YAML_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["prompt"]


RESPONSE_GUARDRAIL_PROMPT: str = _load_response_prompt()


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class ResponseGuardrailGenerator:
    """
    Analyses whether a model's final response contains harmful content or fulfills
    the harmful intent of the user prompt.

    Inputs
    ------
    harmful_prompt  : The harmful / policy-violating user message.
    model_response   : The LLM's final generated message.

    Output
    ------
    ResponseGuardrailResponse : Structured verdict (YES / NO / PARTIAL) plus rationale.
    """

    def __init__(self, async_client=None, sync_client=None):
        self.async_client = async_client
        self.sync_client = sync_client

    def _build_messages(self, harmful_prompt: str, model_response: str) -> list:
        schema_str = json.dumps(
            ResponseGuardrailResponse.model_json_schema(), ensure_ascii=False, indent=2
        )
        system_content = (
            f"{RESPONSE_GUARDRAIL_PROMPT}\n\n"
            "You MUST return your analysis as a JSON object that strictly follows "
            f"this schema:\n```json\n{schema_str}\n```"
        )
        user_content = (
            f"[HARMFUL_PROMPT]:\n{harmful_prompt}\n\n"
            f"[MODEL_RESPONSE]:\n{model_response}"
        )
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ]

    async def check_response_async(
        self,
        harmful_prompt: str,
        model_response: str,
        model: str = "openai/gpt-oss-safeguard-20b",
    ) -> Optional[ResponseGuardrailResponse]:
        """
        Async: analyse whether model_response fulfills harmful_prompt.
        """
        messages = self._build_messages(harmful_prompt, model_response)
        try:
            response = await self.async_client.chat.completions.create(
                model=model,
                messages=messages,
            )
            content = response.choices[0].message.content
            parsed = parse_json(content)
            return ResponseGuardrailResponse(**parsed)
        except Exception:
            logger.exception("Error during async response guardrail check")
            return None

    def check_response(
        self,
        harmful_prompt: str,
        model_response: str,
        model: str = "openai/gpt-oss-safeguard-20b",
    ) -> Optional[ResponseGuardrailResponse]:
        """
        Sync: analyse whether model_response fulfills harmful_prompt.
        """
        messages = self._build_messages(harmful_prompt, model_response)
        try:
            response = self.sync_client.chat.completions.create(
                model=model,
                messages=messages,
            )
            content = response.choices[0].message.content
            parsed = parse_json(content)
            return ResponseGuardrailResponse(**parsed)
        except Exception:
            logger.exception("Error during sync response guardrail check")
            return None
