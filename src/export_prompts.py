"""
Rebuilds all 600 prompts and merges with saved scores into a single CSV.
No API calls needed — prompts are deterministic (seed=42, temp=0.0).
"""

import json
import csv
import os

from src.config import DOMAINS, SHOT_COUNTS, QUALITY_LEVELS, TEST_CASES_PER_CELL, RESULTS_DIR
from src.test_cases import ALL_CASES
from src.few_shot_examples import get_examples
from src.prompts import build_prompt


def export_prompts_csv():
    # ── Load saved scores ─────────────────────────────────────────────────────
    raw_path = os.path.join(RESULTS_DIR, "raw_results.json")
    with open(raw_path) as f:
        raw_results = json.load(f)

    # Index scores by (domain, quality, n_shots, case_index)
    score_index = {}
    output_index = {}
    for r in raw_results:
        key = (r["domain"], r["quality"], r["n_shots"], r["case_index"])
        score_index[key] = r["score"]
        output_index[key] = r.get("output_length", "")

    # ── Rebuild all 600 prompts ───────────────────────────────────────────────
    rows = []
    row_num = 0

    for domain in DOMAINS:
        test_cases = ALL_CASES[domain][:TEST_CASES_PER_CELL]
        for quality in QUALITY_LEVELS:
            for n_shots in SHOT_COUNTS:
                examples = get_examples(domain, quality, n_shots, seed=42)
                for i, tc in enumerate(test_cases):
                    row_num += 1

                    input_text = (
                        tc.get("input") or
                        tc.get("problem") or
                        tc.get("request") or
                        tc.get("text") or
                        ""
                    )

                    prompt = build_prompt(domain, input_text, quality, examples)
                    key = (domain, quality, n_shots, i)
                    score = score_index.get(key, "")

                    rows.append({
                        "call_number":  row_num,
                        "domain":       domain,
                        "quality":      quality,
                        "n_shots":      n_shots,
                        "case_index":   i,
                        "test_input":   input_text.replace("\n", " "),
                        "prompt":       prompt.replace("\n", "\\n"),
                        "score":        score,
                        "prompt_chars": len(prompt),
                    })

    # ── Save CSV ──────────────────────────────────────────────────────────────
    out_path = os.path.join(RESULTS_DIR, "all_prompts_and_results.csv")
    fieldnames = ["call_number", "domain", "quality", "n_shots", "case_index",
                  "test_input", "prompt", "score", "prompt_chars"]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[SAVED] {len(rows)} rows → {out_path}")
    return out_path


if __name__ == "__main__":
    export_prompts_csv()
