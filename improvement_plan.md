# Plan to Improve "Illusion of Safety"

Based on the current state of the paper and repository, here is a structured guide on how to improve the experiments, the codebase, and the analysis of Large Reasoning Models (LRMs) safety misalignment.

## 1. Deep Dive into "PARTIAL" Defenses (Defense Collapse)
Currently, a large portion of defense failures fall under the `PARTIAL` category (e.g., Kimi-K2.5 has a 35% collapse rate for PARTIAL defenses). 

**Actionable Steps:**
1. **Refine the Judge Prompt:** Update `src/prompts/guardrail_prompt_reasoning.yml` to further classify the `PARTIAL` verdict into sub-categories:
   - **Softened Compliance:** Acknowledges harm but provides the harmful information with a disclaimer.
   - **Refusal Drift:** Starts with a refusal but drifts into providing helpful, adjacent information that satisfies the harmful intent.
   - **Information Redaction:** Provides the steps but explicitly omits a critical component (e.g., leaving out a specific chemical).
2. **Re-run Evaluation:** Run the updated judge on the existing `data/analyzed/*_analyzed.json` to generate a stacked bar chart showing the composition of `PARTIAL` failures across models.
3. **Drafting:** Add a new subsection in the paper detailing the taxonomy of Defense Collapse.

## 2. Formalize the "Test-Time Interventions" (SafeSlider / Budget Forcing)
The LaTeX draft mentions *SafeSlider* and *Budget Forcing*, and the code `src/utils/generate_lrm_output.py` already includes `budget_forcing_inference`.

**Actionable Steps:**
1. **Run Ablation Studies:** Execute `run_inference_async.py` with `use_budget_forcing=True` while varying the `remind_after_n_tokens` parameter (e.g., 500, 1000, 2000 tokens).
2. **Test Prompt Variations:** Experiment with different `remind_phrase` values to see if an authoritative prompt ("STOP. This is unsafe.") works better than an inquisitive one ("Wait, is this safe?").
3. **Analyze "Rescue Rate":** Calculate how often the intervention successfully converts a likely "Defense Omission" into a "Successful Defense".
4. **Drafting:** Complete Section 6 in the paper ("Test-time scaling for Safety LRMs") using these empirical results.

## 3. Expand the Evaluation Benchmark
Currently, the evaluation relies entirely on 362 prompts from ToxicChat. This limits the generalizability of the findings.

**Actionable Steps:**
1. **Incorporate JailbreakBench/AdvBench:** Test if complex, cognitively demanding attacks (like ciphers or complex roleplay) increase the **Defense Omission Rate (DOR)** by consuming the model's reasoning capacity.
2. **Test for Over-refusal (XSTest):** Evaluate if LRMs hallucinate safety risks on benign prompts. Define and measure a "False Defense Rate".
3. **Drafting:** Update the "Benchmark Setup" section to include these diverse datasets and present the findings in a comparative table.

## 4. Analyze Reasoning Trace Dynamics
The current methodology treats the reasoning trace as a static block of text. However, reasoning is temporal.

**Actionable Steps:**
1. **Sequence Analysis:** Write a script to analyze *where* the defense occurs in the trace (beginning, middle, or end). 
2. **Self-Correction Markers:** Count transition markers like "Wait," "Actually," or "On second thought" and correlate their frequency with the final `YES`/`NO` answer safety verdict.
3. **Drafting:** Add a discussion point on whether early harm recognition leads to higher defense success compared to late realization.

## 5. Reasoning-Specific Red Teaming
Standard harmful prompts target the *response*. We can design attacks that specifically target the *reasoning* process.

**Actionable Steps:**
1. **Design "Cognitive Overload" Prompts:** Create prompts that embed a harmful request within a complex logic puzzle or math problem, forcing the model to allocate most of its token budget to task-solving, increasing the likelihood of Defense Omission.
2. **Evaluate:** Measure if these reasoning-specific attacks bypass defenses more effectively than standard jailbreaks.

---

### Suggested Order of Execution
1. **Quick Win:** Implement Step 1 (Refining the `PARTIAL` judge) since the data is already generated and only requires re-running the LLM judge.
2. **Core Contribution:** Execute Step 2 (Budget Forcing ablations) to solidify the intervention methodology proposed in the paper.
3. **Expansion:** Run Step 3 (New datasets) to make the paper's claims more robust before submission.
