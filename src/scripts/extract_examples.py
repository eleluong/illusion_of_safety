"""
Entry point: Extract representative failure examples from analysis results.

Usage:
    python -m src.scripts.extract_examples
"""

import json


def get_failure_examples(data_dir: str = "data"):
    """Load and categorize defense failure examples."""
    with open(f'{data_dir}/defense_failures_deepdive.json', 'r', encoding='utf-8') as f:
        failures = json.load(f)

    strong_failures = [f for f in failures if f['reasoning_verdict'] == 'YES']
    partial_failures = [f for f in failures if f['reasoning_verdict'] == 'PARTIAL']

    print("### Representative Failures with YES Defense")
    for f in strong_failures[:5]:
        print(f"- **{f['model']}**: {f['prompt'][:100]}...")

    print("\n### Representative Failures with PARTIAL Defense")
    for f in partial_failures[:5]:
        print(f"- **{f['model']}**: {f['prompt'][:100]}...")


if __name__ == "__main__":
    get_failure_examples()
