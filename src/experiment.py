"""
Parallel experiment runner.
Fires all 600 LLM calls concurrently using ThreadPoolExecutor.
Results are collected and saved once all calls complete.
"""

import json
import os
import csv
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.config import DOMAINS, SHOT_COUNTS, QUALITY_LEVELS, TEST_CASES_PER_CELL, RESULTS_DIR
from src.test_cases import ALL_CASES
from src.few_shot_examples import get_examples
from src.prompts import build_prompt
from src.llm_client import call_llm
from src.evaluator import evaluate


def _run_single(task: dict) -> dict:
    """Run one LLM call and return result dict."""
    domain   = task["domain"]
    quality  = task["quality"]
    n_shots  = task["n_shots"]
    case_idx = task["case_idx"]
    tc       = task["tc"]
    examples = task["examples"]

    input_text = (
        tc.get("input") or
        tc.get("problem") or
        tc.get("request") or
        tc.get("text") or
        ""
    )

    prompt = build_prompt(domain, input_text, quality, examples)
    output = call_llm(prompt)
    score  = evaluate(domain, output, tc)

    return {
        "domain":        domain,
        "quality":       quality,
        "n_shots":       n_shots,
        "case_index":    case_idx,
        "score":         score,
        "prompt_length": len(prompt),
        "output_length": len(output),
    }


def run_experiment(max_workers: int = 40):
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # ── Build all 600 tasks ───────────────────────────────────────────────────
    tasks = []
    for domain in DOMAINS:
        test_cases = ALL_CASES[domain][:TEST_CASES_PER_CELL]
        for quality in QUALITY_LEVELS:
            for n_shots in SHOT_COUNTS:
                examples = get_examples(domain, quality, n_shots, seed=42)
                for i, tc in enumerate(test_cases):
                    tasks.append({
                        "domain":   domain,
                        "quality":  quality,
                        "n_shots":  n_shots,
                        "case_idx": i,
                        "tc":       tc,
                        "examples": examples,
                    })

    total = len(tasks)
    print(f"\n{'='*60}")
    print(f"  EXPERIMENT START — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Total LLM calls : {total}")
    print(f"  Workers         : {max_workers}")
    print(f"{'='*60}\n")

    # ── Run all in parallel ───────────────────────────────────────────────────
    raw_results = []
    done = 0
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_run_single, t): t for t in tasks}
        for future in as_completed(futures):
            result = future.result()
            raw_results.append(result)
            done += 1
            if done % 50 == 0 or done == total:
                elapsed = time.time() - start_time
                print(f"  [{done}/{total}] completed — {elapsed:.1f}s elapsed")

    print(f"\n  All {total} calls done in {time.time()-start_time:.1f}s\n")

    # ── Aggregate into summary rows ───────────────────────────────────────────
    from collections import defaultdict
    cell_scores = defaultdict(list)
    for r in raw_results:
        key = (r["domain"], r["quality"], r["n_shots"])
        cell_scores[key].append(r["score"])

    summary_rows = []
    for domain in DOMAINS:
        for quality in QUALITY_LEVELS:
            for n_shots in SHOT_COUNTS:
                scores = cell_scores[(domain, quality, n_shots)]
                mean   = round(sum(scores) / len(scores), 4) if scores else 0.0
                std    = round(_std(scores), 4)
                summary_rows.append({
                    "domain":     domain,
                    "quality":    quality,
                    "n_shots":    n_shots,
                    "mean_score": mean,
                    "std_score":  std,
                    "n_cases":    len(scores),
                })
                print(f"  {domain:25s} | {quality:6s} | {n_shots:2d} shots → mean={mean:.4f}  std={std:.4f}")

    # ── Save ──────────────────────────────────────────────────────────────────
    raw_path = os.path.join(RESULTS_DIR, "raw_results.json")
    with open(raw_path, "w") as f:
        json.dump(raw_results, f, indent=2)

    csv_path = os.path.join(RESULTS_DIR, "summary.csv")
    fieldnames = ["domain", "quality", "n_shots", "mean_score", "std_score", "n_cases"]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"\n[SAVED] {raw_path}")
    print(f"[SAVED] {csv_path}")
    print(f"\n{'='*60}")
    print(f"  EXPERIMENT COMPLETE — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    return raw_results, summary_rows


def _std(values: list) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    return variance ** 0.5
