"""
Entry point: Run safety analysis on model inference outputs.

Usage:
    python -m src.scripts.run_analysis
"""

import asyncio
import json
import os

from src.services.groq_llm import get_groq_async_client
from src.safety_assessment import ReasoningGuardrailGenerator, ResponseGuardrailGenerator
from src.utils.analyze_lrm_output import run_analysis


# --- Configuration ---
TEST_PATH = "data/outputs/UCSC-VLAA_STAR1-R1-Distill-8B_outputs.json"

async def run_analysis_workflow(model_name: str, data_dir: str, analyzed_dir: str, report_dir: str):
    """
    Workflow function for safety analysis.
    """
    test_path = os.path.join(data_dir, f"{model_name.replace('/', '_')}_outputs.json")
    output_path = os.path.join(analyzed_dir, f"{model_name.replace('/', '_')}_analyzed.json")
    report_path = os.path.join(report_dir, f"{model_name.replace('/', '_')}_report.md")

    if not os.path.exists(test_path):
        print(f"Error: Inference output not found at {test_path}")
        return

    os.makedirs(analyzed_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)

    with open(test_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_results = []
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            existing_results = json.load(f)

    client = get_groq_async_client()
    reasoning_safeguard = ReasoningGuardrailGenerator(async_client=client)
    response_safeguard = ResponseGuardrailGenerator(async_client=client)

    await run_analysis(
        data=data,
        reasoning_safeguard=reasoning_safeguard,
        response_safeguard=response_safeguard,
        output_path=output_path,
        report_path=report_path,
        test_path=test_path,
        existing_results=existing_results,
    )

async def main():
    # Example standalone usage
    # Extract model name from test path if possible or use a default
    model_name = os.path.basename(TEST_PATH).replace("_outputs.json", "").replace("_", "/")
    
    await run_analysis_workflow(
        model_name=model_name,
        data_dir="data/outputs",
        analyzed_dir="data/analyzed",
        report_dir="data/report",
    )


if __name__ == "__main__":
    asyncio.run(main())
