"""
Entry point: Run synchronous inference on toxic-chat dataset.

Usage:
    python -m src.scripts.run_inference_sync
"""

import json
import os

from tqdm import tqdm

from src.datasets.toxicchat import load_toxic_chat, filter_harmful
from src.services.together_llm import get_together_client
from src.utils.generate_lrm_output import save_outputs, load_outputs, parse_reasoning_response


# --- Configuration ---
# model_name = "zai-org/GLM-5"
model_name = "Qwen/Qwen3.5-397B-A17B"
# model_name = "openai/gpt-oss-120b"
# model_name = "moonshotai/Kimi-K2.5"


def sync_inference(client, model_name: str, item: dict):
    """Run a single synchronous inference call."""
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": item['user_input']}
        ],
        stream=False,
        max_tokens=10000,
    )
    return response


def main():
    dataset = load_toxic_chat()
    filtered = filter_harmful(dataset)
    print(f"Total filtered items: {len(filtered)}")

    client = get_together_client()
    outputs = load_outputs(model_name, data_dir="data")

    for item in tqdm(filtered):
        try:
            if item['conv_id'] in [x['conv_id'] for x in outputs]:
                continue

            raw_response = sync_inference(client, model_name, item)
            result = parse_reasoning_response(raw_response)

            if result is None:
                continue

            response, reasoning = result

            temp = {
                'conv_id': item['conv_id'],
                'conversation': [
                    {"role": "user", "content": item['user_input']},
                    {"role": "assistant", "content": response, "reasoning": reasoning}
                ]
            }
            outputs.append(temp)
        except Exception as e:
            print(e)
            continue

        if len(outputs) % 5 == 0:
            save_outputs(outputs, model_name, data_dir="data")

    save_outputs(outputs, model_name, data_dir="data")


if __name__ == "__main__":
    main()
