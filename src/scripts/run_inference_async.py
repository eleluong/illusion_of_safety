"""
Entry point: Run async inference on toxic-chat dataset.

Usage:
    python -m src.scripts.run_inference_async
"""

import asyncio

from src.datasets.toxicchat import load_toxic_chat, filter_harmful
from src.services.together_llm import get_async_together_client
from src.services.localhost_llm import get_localhost_async_client
from src.utils.generate_lrm_output import run_async_inference


# --- Configuration ---
MODEL_NAME = "mistralai/Mistral-Small-24B-Instruct-2501"
MAX_CONCURRENT = 10

async def run_inference_workflow(model_name: str, max_concurrent: int, data_dir: str, base_url: str = None):
    """
    Workflow function for full dataset inference.
    """
    dataset = load_toxic_chat()
    filtered = filter_harmful(dataset)
    print(f"Total harmful items to process: {len(filtered)}")

    if base_url:
        client = get_localhost_async_client(base_url=base_url)
    else:
        client = get_async_together_client()
        
    await run_async_inference(
        client=client,
        model_name=model_name,
        items=filtered,
        max_concurrent=max_concurrent,
        data_dir=data_dir,
        enable_thinking=True,
    )

async def main():
    await run_inference_workflow(
        model_name=MODEL_NAME,
        max_concurrent=MAX_CONCURRENT,
        data_dir="data",
    )


if __name__ == "__main__":
    asyncio.run(main())
