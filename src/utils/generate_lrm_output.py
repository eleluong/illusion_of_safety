"""
Core logic for generating LRM (Language Reasoning Model) outputs.

Handles async inference over toxic-chat items, response parsing,
checkpoint saving, and progress tracking.
"""

import asyncio
import json
import os
import threading
from typing import List

from tqdm import tqdm


def save_outputs(outputs: list, model_name: str, data_dir: str = "data"):
    """Save inference outputs to a JSON file.

    Args:
        outputs: List of inference result dicts.
        model_name: Model identifier (e.g. "Qwen/Qwen3.5-397B-A17B").
        data_dir: Directory to save output files in.
    """
    path = os.path.join(data_dir, f'{model_name.replace("/", "_")}_outputs.json')
    with open(path, 'w') as f:
        json.dump(outputs, f, indent=4, ensure_ascii=False)


def load_outputs(model_name: str, data_dir: str = "data") -> list:
    """Load previously saved inference outputs.

    Args:
        model_name: Model identifier.
        data_dir: Directory to load output files from.

    Returns:
        List of previously saved outputs, or empty list if none exist.
    """
    path = os.path.join(data_dir, f'{model_name.replace("/", "_")}_outputs.json')
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []


async def inference(client, model_name: str, item: dict, enable_thinking: bool = True):
    """Run a single async inference call.

    Args:
        client: Async LLM client (Together/OpenAI compatible).
        model_name: Model to use for inference.
        item: Dataset item with 'user_input' key.
        enable_thinking: Whether to enable thinking mode.

    Returns:
        Raw API response object.
    """
    extra_body = {}
    if enable_thinking:
        extra_body = {'chat_template_kwargs': {'enable_thinking': True}}

    response = await client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": item['user_input']}
        ],
        stream=False,
        max_tokens=10000,
        extra_body=extra_body,
    )
    return response


def parse_reasoning_response(raw_response):
    """Parse reasoning and response content from an API response.

    Handles both <think> tags and reasoning_content attribute patterns.

    Args:
        raw_response: Raw API response object.

    Returns:
        Tuple of (response_text, reasoning_text) or None if incomplete.
    """
    response = raw_response.choices[0].message.content

    if "<think>" in response:
        if "</think>" not in response:
            return None
        reasoning = response.split("<think>")[1].split("</think>")[0]
        response = response.split("<think>")[1].split("</think>")[1]
    elif "</think>" in response:
        reasoning = response.split("</think>")[0]
        response = response.split("</think>")[1]
    elif "reasoning_content" in dir(raw_response.choices[0].message):
        reasoning = getattr(raw_response.choices[0].message, 'reasoning_content', None)
    else:
        reasoning = getattr(raw_response.choices[0].message, 'reasoning', None)

    return response, reasoning


async def process_item(client, model_name: str, item: dict, outputs: list,
                       semaphore: asyncio.Semaphore, lock: threading.Lock,
                       data_dir: str = "data", enable_thinking: bool = True):
    """Process a single dataset item with concurrency control.

    Args:
        client: Async LLM client.
        model_name: Model to use.
        item: Dataset item.
        outputs: Shared list of results (thread-safe via lock).
        semaphore: Concurrency limiter.
        lock: Threading lock for safe list access.
        data_dir: Directory for checkpoint saves.
        enable_thinking: Whether to enable thinking mode.

    Returns:
        Result dict or None on error/skip.
    """
    async with semaphore:
        try:
            # Re-check if already processed (could have been added while waiting)
            with lock:
                if item['conv_id'] in [x['conv_id'] for x in outputs]:
                    return None

            raw_response = await inference(client, model_name, item, enable_thinking)
            result = parse_reasoning_response(raw_response)

            if result is None:
                return None

            response, reasoning = result

            temp = {
                'conv_id': item['conv_id'],
                'conversation': [
                    {"role": "user", "content": item['user_input']},
                    {"role": "assistant", "content": response, "reasoning": reasoning}
                ]
            }

            with lock:
                outputs.append(temp)
                if len(outputs) % 5 == 0:
                    save_outputs(outputs, model_name, data_dir)
            return temp

        except Exception as e:
            print(f"Error processing {item['conv_id']}: {e}")
            return None


async def run_async_inference(client, model_name: str, items: list,
                              max_concurrent: int = 10, data_dir: str = "data",
                              enable_thinking: bool = True):
    """Run async inference over a list of dataset items.

    Args:
        client: Async LLM client.
        model_name: Model to use.
        items: List of dataset items to process.
        max_concurrent: Maximum number of concurrent requests.
        data_dir: Directory for saving outputs.
        enable_thinking: Whether to enable thinking mode.

    Returns:
        List of all outputs (including previously saved ones).
    """
    outputs = load_outputs(model_name, data_dir)

    # Filter out already processed items
    to_process = [item for item in items if item['conv_id'] not in [x['conv_id'] for x in outputs]]
    print(f"Items remaining to process: {len(to_process)}")

    if not to_process:
        print("All items already processed.")
        return outputs

    semaphore = asyncio.Semaphore(max_concurrent)
    lock = threading.Lock()

    tasks = [
        process_item(client, model_name, item, outputs, semaphore, lock, data_dir, enable_thinking)
        for item in to_process
    ]

    for f in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        await f

    save_outputs(outputs, model_name, data_dir)
    print("Inference complete.")
    return outputs
