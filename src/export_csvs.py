"""
Generates 5 clean CSVs from raw experiment results.
"""

import json
import csv
import os
from collections import defaultdict

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
EXPORT_DIR  = os.path.join(RESULTS_DIR, "export")

DOMAINS  = ["json_extraction", "code_debugging", "math_word_problems", "text_summarization", "sql_generation"]
QUALITIES = ["high", "medium", "low"]
SHOTS     = [1, 3, 5, 10]

DOMAIN_LABELS = {
    "json_extraction":    "JSON Extraction",
    "code_debugging":     "Code Debugging",
    "math_word_problems": "Math Word Problems",
    "text_summarization": "Text Summarization",
    "sql_generation":     "SQL Generation",
}


def load_raw():
    with open(os.path.join(RESULTS_DIR, "raw_results.json")) as f:
        return json.load(f)


def std(values):
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    return (sum((x - mean) ** 2 for x in values) / (len(values) - 1)) ** 0.5


def save_csv(filename, fieldnames, rows):
    path = os.path.join(EXPORT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[SAVED] {filename}  ({len(rows)} rows)")


def run():
    os.makedirs(EXPORT_DIR, exist_ok=True)
    raw = load_raw()

    # ── index raw by (domain, quality, n_shots, case_index) ──────────────────
    index = {}
    for r in raw:
        key = (r["domain"], r["quality"], r["n_shots"], r["case_index"])
        index[key] = r

    # ── also group scores by cell ─────────────────────────────────────────────
    cell_scores = defaultdict(list)
    for r in raw:
        cell_scores[(r["domain"], r["quality"], r["n_shots"])].append(r["score"])

    from src.test_cases import ALL_CASES

    # ──────────────────────────────────────────────────────────────────────────
    # CSV 1 — all_600_calls.csv
    # ──────────────────────────────────────────────────────────────────────────
    rows1 = []
    call_num = 0
    for domain in DOMAINS:
        for quality in QUALITIES:
            for n_shots in SHOTS:
                for i in range(10):
                    call_num += 1
                    key = (domain, quality, n_shots, i)
                    r = index.get(key, {})
                    tc = ALL_CASES[domain][i]
                    input_text = (
                        tc.get("input") or tc.get("problem") or
                        tc.get("request") or tc.get("text") or ""
                    )
                    score = r.get("score", "")
                    rows1.append({
                        "call_number":  call_num,
                        "domain":       DOMAIN_LABELS[domain],
                        "quality":      quality.capitalize(),
                        "n_shots":      n_shots,
                        "case_index":   i,
                        "test_input":   input_text,
                        "score":        round(score, 4) if score != "" else "",
                        "score_pct":    f"{round(score*100, 1)}%" if score != "" else "",
                    })

    save_csv("csv1_all_600_calls.csv",
             ["call_number","domain","quality","n_shots","case_index","test_input","score","score_pct"],
             rows1)

    # ──────────────────────────────────────────────────────────────────────────
    # CSV 2 — cell_summary.csv
    # ──────────────────────────────────────────────────────────────────────────
    rows2 = []
    cell_num = 0
    for domain in DOMAINS:
        for quality in QUALITIES:
            for n_shots in SHOTS:
                cell_num += 1
                scores = cell_scores[(domain, quality, n_shots)]
                mean   = sum(scores) / len(scores) if scores else 0
                sd     = std(scores)
                rows2.append({
                    "cell_number": cell_num,
                    "domain":      DOMAIN_LABELS[domain],
                    "quality":     quality.capitalize(),
                    "n_shots":     n_shots,
                    "n_calls":     len(scores),
                    "mean_score":  round(mean, 4),
                    "mean_pct":    f"{round(mean*100, 1)}%",
                    "std_dev":     round(sd, 4),
                    "min_score":   round(min(scores), 4) if scores else "",
                    "max_score":   round(max(scores), 4) if scores else "",
                })

    save_csv("csv2_cell_summary.csv",
             ["cell_number","domain","quality","n_shots","n_calls",
              "mean_score","mean_pct","std_dev","min_score","max_score"],
             rows2)

    # ──────────────────────────────────────────────────────────────────────────
    # CSV 3 — quality_comparison.csv
    # ──────────────────────────────────────────────────────────────────────────
    rows3 = []
    for domain in DOMAINS:
        low_scores = cell_scores[(domain, "low", 1)] + cell_scores[(domain, "low", 3)] + \
                     cell_scores[(domain, "low", 5)] + cell_scores[(domain, "low", 10)]
        low_mean   = sum(low_scores) / len(low_scores) if low_scores else 0

        for quality in QUALITIES:
            all_scores = []
            best_score = -1
            best_shots = None
            for n_shots in SHOTS:
                s = cell_scores[(domain, quality, n_shots)]
                all_scores.extend(s)
                m = sum(s)/len(s) if s else 0
                if m > best_score:
                    best_score = m
                    best_shots = n_shots

            mean = sum(all_scores)/len(all_scores) if all_scores else 0
            diff = mean - low_mean

            rows3.append({
                "domain":           DOMAIN_LABELS[domain],
                "quality":          quality.capitalize(),
                "mean_score":       round(mean, 4),
                "mean_pct":         f"{round(mean*100, 1)}%",
                "vs_low_quality_pp": f"{round(diff*100, 1):+.1f} pp",
                "best_shots":       best_shots,
                "best_score_pct":   f"{round(best_score*100, 1)}%",
            })

    save_csv("csv3_quality_comparison.csv",
             ["domain","quality","mean_score","mean_pct",
              "vs_low_quality_pp","best_shots","best_score_pct"],
             rows3)

    # ──────────────────────────────────────────────────────────────────────────
    # CSV 4 — shots_comparison.csv
    # ──────────────────────────────────────────────────────────────────────────
    rows4 = []
    for quality in QUALITIES:
        baseline_scores = []
        for domain in DOMAINS:
            baseline_scores.extend(cell_scores[(domain, quality, 1)])
        baseline_mean = sum(baseline_scores)/len(baseline_scores) if baseline_scores else 0

        for n_shots in SHOTS:
            all_scores = []
            for domain in DOMAINS:
                all_scores.extend(cell_scores[(domain, quality, n_shots)])
            mean = sum(all_scores)/len(all_scores) if all_scores else 0
            diff = mean - baseline_mean

            rows4.append({
                "quality":        quality.capitalize(),
                "n_shots":        n_shots,
                "mean_score":     round(mean, 4),
                "mean_pct":       f"{round(mean*100, 1)}%",
                "vs_1shot_pp":    f"{round(diff*100, 1):+.1f} pp",
            })

    save_csv("csv4_shots_comparison.csv",
             ["quality","n_shots","mean_score","mean_pct","vs_1shot_pp"],
             rows4)

    # ──────────────────────────────────────────────────────────────────────────
    # CSV 5 — headline_findings.csv
    # ──────────────────────────────────────────────────────────────────────────
    def domain_quality_mean(domain, quality):
        s = []
        for n in SHOTS:
            s.extend(cell_scores[(domain, quality, n)])
        return sum(s)/len(s) if s else 0

    def overall_quality_mean(quality):
        s = []
        for d in DOMAINS:
            for n in SHOTS:
                s.extend(cell_scores[(d, quality, n)])
        return sum(s)/len(s) if s else 0

    def shots_mean(quality, n_shots):
        s = []
        for d in DOMAINS:
            s.extend(cell_scores[(d, quality, n_shots)])
        return sum(s)/len(s) if s else 0

    high_overall  = overall_quality_mean("high")
    med_overall   = overall_quality_mean("medium")
    low_overall   = overall_quality_mean("low")
    three_high    = shots_mean("high", 3)
    ten_low       = shots_mean("low", 10)
    one_high      = shots_mean("high", 1)
    ten_high      = shots_mean("high", 10)

    rows5 = [
        {
            "finding":        "Overall Quality Effect",
            "value_a":        "High Quality",
            "score_a_pct":    f"{round(high_overall*100,1)}%",
            "value_b":        "Low Quality",
            "score_b_pct":    f"{round(low_overall*100,1)}%",
            "difference_pp":  f"{round((high_overall-low_overall)*100,1)} pp",
            "winner":         "High Quality",
        },
        {
            "finding":        "Overall Quality Effect",
            "value_a":        "Medium Quality",
            "score_a_pct":    f"{round(med_overall*100,1)}%",
            "value_b":        "Low Quality",
            "score_b_pct":    f"{round(low_overall*100,1)}%",
            "difference_pp":  f"{round((med_overall-low_overall)*100,1)} pp",
            "winner":         "Medium Quality",
        },
        {
            "finding":        "Core Claim: 3 High vs 10 Low",
            "value_a":        "3 High-Quality Examples",
            "score_a_pct":    f"{round(three_high*100,1)}%",
            "value_b":        "10 Low-Quality Examples",
            "score_b_pct":    f"{round(ten_low*100,1)}%",
            "difference_pp":  f"{round((three_high-ten_low)*100,1)} pp",
            "winner":         "3 High-Quality Examples",
        },
        {
            "finding":        "Shot Count Effect (High Quality only)",
            "value_a":        "1 Shot — High Quality",
            "score_a_pct":    f"{round(one_high*100,1)}%",
            "value_b":        "10 Shots — High Quality",
            "score_b_pct":    f"{round(ten_high*100,1)}%",
            "difference_pp":  f"{round((ten_high-one_high)*100,1)} pp",
            "winner":         "10 Shots — High Quality",
        },
    ]

    # Per domain best vs worst
    for domain in DOMAINS:
        h = domain_quality_mean(domain, "high")
        l = domain_quality_mean(domain, "low")
        rows5.append({
            "finding":       f"Domain Effect — {DOMAIN_LABELS[domain]}",
            "value_a":       "High Quality",
            "score_a_pct":   f"{round(h*100,1)}%",
            "value_b":       "Low Quality",
            "score_b_pct":   f"{round(l*100,1)}%",
            "difference_pp": f"{round((h-l)*100,1)} pp",
            "winner":        "High Quality" if h >= l else "Low Quality (anomaly)",
        })

    save_csv("csv5_headline_findings.csv",
             ["finding","value_a","score_a_pct","value_b","score_b_pct","difference_pp","winner"],
             rows5)

    print(f"\nAll CSVs saved to: {EXPORT_DIR}")


if __name__ == "__main__":
    run()
