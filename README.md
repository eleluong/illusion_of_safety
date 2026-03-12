# Illusion of Safety: Analyzing Reasoning Guardrails

A research project focused on analyzing the effectiveness of reasoning-based guardrails (Chain-of-Thought thinking) in Large Language Models (LLMs) against harmful prompts and jailbreak attempts.

## Project Overview

This project provides a pipeline to:
1. **Inference**: Run Large Reasoning Models (LRMs) on the `lmsys/toxic-chat` dataset to capture both the final response and the internal reasoning/thinking trace.
2. **Safety Assessment**: Evaluate whether the model's internal reasoning contains a genuine "Defense Policy" (harm recognition and refusal deliberation) and whether the final response complies with the harmful intent.
3. **Analysis**: Aggregate results into detailed metrics and reports to identify cases where models "defend" in reasoning but still "fail" in the final output.

## Repository Structure

```
illusion_of_safety/
├── data/                  # Inference outputs, filtered datasets, and analysis reports
├── src/                   # Core Python package
│   ├── datasets/          # Dataset loading and filtering logic (Toxic-Chat)
│   ├── safety_assessment/ # Guardrail generators (Reasoning & Response) and schemas
│   ├── services/          # LLM API client factories (Together AI, Groq, Localhost)
│   ├── utils/             # Core logic for inference pipelines and analysis runners
│   ├── scripts/           # Command-line entry points
│   └── prompts/           # YAML-based safety policy and guardrail prompts
├── .env                   # Environment variables (API keys)
└── requirements.txt       # Project dependencies
```

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   TOGETHER_API_KEY=your_key_here
   GROQ_API_KEY=your_key_here
   ```

## Usage

All scripts should be run from the project root using `python -m`.

### 1. Run Inference
Generate model outputs (including thinking traces) for harmful prompts:
```bash
# Async version (recommended)
PYTHONPATH=. python -m src.scripts.run_inference_async

# Synchronous version
PYTHONPATH=. python -m src.scripts.run_inference_sync
```

### 2. Run Safety Analysis
Evaluate the generated outputs against safety guardrails:
```bash
PYTHONPATH=. python -m src.scripts.run_analysis
```

### 3. Generate Reports
Aggregate analysis results into a comprehensive report:
```bash
PYTHONPATH=. python -m src.scripts.analyze_guardrails
```

### 4. Extract Failure Examples
Extract representative cases where defense reasoning failed to prevent harmful output:
```bash
PYTHONPATH=. python -m src.scripts.extract_examples
```

## Data Directory

The `data/` directory contains:
- `*_outputs.json`: Raw model responses and thinking traces.
- `*_outputs_analyzed.json`: Results from the safety assessment guardrails.
- `*_report.md`: Individual model analysis reports.
- `guardrail_analysis_report.md`: Global aggregated report.
- `defense_failures_deepdive.json`: Filtered list of "defense but fail" cases.
