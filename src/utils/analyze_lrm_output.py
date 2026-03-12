"""
Core logic for running safety analysis on LRM outputs.

Takes model inference outputs and evaluates them using the
ReasoningGuardrailGenerator and ResponseGuardrailGenerator.
"""

import json
import os
from typing import Optional


async def run_analysis(
    data: list,
    reasoning_safeguard,
    response_safeguard,
    output_path: str,
    report_path: str,
    test_path: str,
    existing_results: Optional[list] = None,
    limit: Optional[int] = None,
):
    """Run safety analysis on a list of model output items.

    Args:
        data: List of model output items (each with conv_id, conversation).
        reasoning_safeguard: ReasoningGuardrailGenerator instance.
        response_safeguard: ResponseGuardrailGenerator instance.
        output_path: Path to save analysis results JSON.
        report_path: Path to save the markdown report.
        test_path: Original test file path (for report header).
        existing_results: Previously saved results to resume from.
        limit: Maximum number of items to process (None for all).

    Returns:
        List of analysis result dicts.
    """
    results = existing_results or []
    processed_ids = {item["conv_id"] for item in results}

    # Summary statistics
    stats = {
        "total": len(results),
        "reasoning": {"YES": 0, "NO": 0, "PARTIAL": 0, "escalate": 0},
        "response": {"YES": 0, "NO": 0, "PARTIAL": 0, "harmful": 0},
    }

    # Pre-calculate stats from existing results
    for item in results:
        if "reasoning_result" in item and item["reasoning_result"]:
            res = item["reasoning_result"]
            stats["reasoning"][res["defense_verdict"]] += 1
            if res.get("escalate"):
                stats["reasoning"]["escalate"] += 1
        if "response_result" in item and item["response_result"]:
            res = item["response_result"]
            stats["response"][res["jailbreak_verdict"]] += 1
            if res.get("harmful_content_detected"):
                stats["response"]["harmful"] += 1

    for i, item in enumerate(data):
        conv_id = item.get("conv_id", str(i))
        if conv_id in processed_ids:
            continue

        if limit is not None and len(results) >= limit:
            break

        harmful_prompt = item["conversation"][0]["content"]
        model_reasoning = item["conversation"][1].get("reasoning", "")
        model_response = item["conversation"][1]["content"]

        print(f"--- Testing Example {len(results) + 1} (ID: {conv_id}) ---")

        reasoning_result = await reasoning_safeguard.check_reasoning_async(
            harmful_prompt, model_reasoning
        )
        print(
            f"Reasoning Result: {reasoning_result.defense_verdict if reasoning_result else 'None'}"
        )

        response_result = await response_safeguard.check_response_async(
            harmful_prompt, model_response
        )
        print(
            f"Response Result: {response_result.jailbreak_verdict if response_result else 'None'}"
        )

        analysis_item = {
            "conv_id": conv_id,
            "harmful_prompt": harmful_prompt,
            "reasoning_result": reasoning_result.model_dump() if reasoning_result else None,
            "response_result": response_result.model_dump() if response_result else None,
        }

        results.append(analysis_item)
        processed_ids.add(conv_id)

        # Update stats
        stats["total"] += 1
        if reasoning_result:
            stats["reasoning"][reasoning_result.defense_verdict] += 1
            if reasoning_result.escalate:
                stats["reasoning"]["escalate"] += 1
        if response_result:
            stats["response"][response_result.jailbreak_verdict] += 1
            if response_result.harmful_content_detected:
                stats["response"]["harmful"] += 1

        # Save checkpoint
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print("------")

    # Generate Report
    total = stats["total"] if stats["total"] > 0 else 1  # avoid division by zero
    report = f"""# Analysis Report for {test_path}

## Summary
- **Total Processed**: {stats['total']}

## Reasoning Guardrail Results
- **YES (Genuine Defense)**: {stats['reasoning']['YES']} ({stats['reasoning']['YES']/total*100:.2f}%)
- **NO (No Defense)**: {stats['reasoning']['NO']} ({stats['reasoning']['NO']/total*100:.2f}%)
- **PARTIAL**: {stats['reasoning']['PARTIAL']} ({stats['reasoning']['PARTIAL']/total*100:.2f}%)
- **Escalated (SA4 level harm)**: {stats['reasoning']['escalate']}

## Response Guardrail Results
- **YES (Jailbroken)**: {stats['response']['YES']} ({stats['response']['YES']/total*100:.2f}%)
- **NO (Refused)**: {stats['response']['NO']} ({stats['response']['NO']/total*100:.2f}%)
- **PARTIAL**: {stats['response']['PARTIAL']} ({stats['response']['PARTIAL']/total*100:.2f}%)
- **Harmful Content Detected**: {stats['response']['harmful']}
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nAnalysis complete. Report saved to {report_path}")

    return results
