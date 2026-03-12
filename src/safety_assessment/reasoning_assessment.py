"""
Reasoning guardrail assessment.

Analyses whether a model's reasoning trace contains a genuine defense policy
when the model receives a harmful prompt.
"""

import json
import logging
import os
from typing import Optional

import yaml

from .schemas import DefenseResponse
from .json_parser import parse_json

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Load reasoning guardrail prompt from YAML
# ---------------------------------------------------------------------------

_PROMPT_YAML_PATH = os.path.join(
    os.path.dirname(__file__), os.pardir, "prompts", "guardrail_prompt_reasoning.yml"
)


def _load_reasoning_prompt() -> str:
    with open(_PROMPT_YAML_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["prompt"]


REASONING_GUARDRAIL_PROMPT: str = _load_reasoning_prompt()


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class ReasoningGuardrailGenerator:
    """
    Analyses whether a model's reasoning trace contains a genuine defense policy
    when the model receives a harmful prompt.

    Inputs
    ------
    harmful_prompt   : The harmful / policy-violating user message.
    model_reasoning  : The LLM's internal chain-of-thought / thinking trace.

    Output
    ------
    DefenseResponse  : Structured verdict (YES / PARTIAL / NO) plus supporting signals.
    """

    def __init__(self, async_client=None, sync_client=None):
        self.async_client = async_client
        self.sync_client = sync_client

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_messages(self, harmful_prompt: str, model_reasoning: str) -> list:
        schema_str = json.dumps(
            DefenseResponse.model_json_schema(), ensure_ascii=False, indent=2
        )
        system_content = (
            f"{REASONING_GUARDRAIL_PROMPT}\n\n"
            "You MUST return your analysis as a JSON object that strictly follows "
            f"this schema:\n```json\n{schema_str}\n```"
        )
        user_content = (
            f"[HARMFUL_PROMPT]:\n{harmful_prompt}\n\n"
            f"[MODEL_REASONING]:\n{model_reasoning}"
        )
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ]

    # ------------------------------------------------------------------
    # Async
    # ------------------------------------------------------------------

    async def check_reasoning_async(
        self,
        harmful_prompt: str,
        model_reasoning: str,
        model: str = "openai/gpt-oss-safeguard-20b",
    ) -> Optional[DefenseResponse]:
        """
        Async: analyse whether model_reasoning contains a defense policy
        against harmful_prompt.
        """
        messages = self._build_messages(harmful_prompt, model_reasoning)
        try:
            response = await self.async_client.chat.completions.create(
                model=model,
                messages=messages,
            )
            content = response.choices[0].message.content
            parsed = parse_json(content)
            return DefenseResponse(**parsed)
        except Exception:
            logger.exception("Error during async reasoning guardrail check")
            return None

    # ------------------------------------------------------------------
    # Sync
    # ------------------------------------------------------------------

    def check_reasoning(
        self,
        harmful_prompt: str,
        model_reasoning: str,
        model: str = "openai/gpt-oss-safeguard-20b",
    ) -> Optional[DefenseResponse]:
        """
        Sync: analyse whether model_reasoning contains a defense policy
        against harmful_prompt.
        """
        messages = self._build_messages(harmful_prompt, model_reasoning)
        try:
            response = self.sync_client.chat.completions.create(
                model=model,
                messages=messages,
            )
            content = response.choices[0].message.content
            parsed = parse_json(content)
            return DefenseResponse(**parsed)
        except Exception:
            logger.exception("Error during sync reasoning guardrail check")
            return None
