"""
Dataset loading utilities for the lmsys/toxic-chat dataset.
"""

from datasets import load_dataset


def load_toxic_chat(split: str = "test"):
    """Load the toxic-chat dataset (toxicchat0124 config).

    Args:
        split: Dataset split to load (default: "test").

    Returns:
        The requested split of the toxic-chat dataset.
    """
    ds = load_dataset("lmsys/toxic-chat", "toxicchat0124")
    return ds[split]


def filter_harmful(dataset):
    """Filter dataset items that are toxic or jailbreaking attempts.

    Args:
        dataset: A toxic-chat dataset split.

    Returns:
        List of items where toxicity == 1 or jailbreaking == 1.
    """
    filtered = []
    for item in dataset:
        try:
            if item["toxicity"] == 1 or item["jailbreaking"] == 1:
                filtered.append(item)
        except Exception as e:
            print(e)
            continue
    return filtered
