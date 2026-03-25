"""
Reads results/raw_results.json and results/summary.csv,
computes all statistics needed for the paper, and
generates all figures saved to results/figures/.
"""

import json
import csv
import os
import math
from collections import defaultdict

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
FIGURES_DIR = os.path.join(RESULTS_DIR, "figures")


def load_summary() -> list:
    path = os.path.join(RESULTS_DIR, "summary.csv")
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["mean_score"] = float(row["mean_score"])
            row["std_score"] = float(row["std_score"])
            row["n_shots"] = int(row["n_shots"])
            row["n_cases"] = int(row["n_cases"])
            rows.append(row)
    return rows


def load_raw() -> list:
    path = os.path.join(RESULTS_DIR, "raw_results.json")
    with open(path) as f:
        return json.load(f)


def print_headline_stats(summary: list):
    """Print the key numbers that will go in the paper."""
    print("\n" + "="*60)
    print("  HEADLINE STATISTICS FOR PAPER")
    print("="*60)

    # 1. Overall mean per quality level
    quality_scores = defaultdict(list)
    for row in summary:
        quality_scores[row["quality"]].append(row["mean_score"])

    print("\n[1] Mean accuracy by quality level (across all domains & shot counts):")
    for q in ["high", "medium", "low"]:
        scores = quality_scores[q]
        mean = sum(scores) / len(scores)
        print(f"    {q.upper():8s}: {mean:.4f}  ({mean*100:.1f}%)")

    high_mean = sum(quality_scores["high"]) / len(quality_scores["high"])
    low_mean  = sum(quality_scores["low"])  / len(quality_scores["low"])
    print(f"\n    → High quality outperforms Low quality by: {(high_mean - low_mean)*100:.1f} percentage points")

    # 2. Best configuration per domain
    print("\n[2] Best (domain, quality, shots) configuration per domain:")
    domain_best = {}
    for row in summary:
        d = row["domain"]
        if d not in domain_best or row["mean_score"] > domain_best[d]["mean_score"]:
            domain_best[d] = row
    for d, row in domain_best.items():
        print(f"    {d}: quality={row['quality']}, shots={row['n_shots']}, score={row['mean_score']:.4f}")

    # 3. Quantity vs Quality: 3 high vs 10 low
    print("\n[3] Quality vs Quantity comparison (3 high-quality vs 10 low-quality examples):")
    three_high = [r for r in summary if r["quality"] == "high" and r["n_shots"] == 3]
    ten_low    = [r for r in summary if r["quality"] == "low"  and r["n_shots"] == 10]

    three_high_mean = sum(r["mean_score"] for r in three_high) / len(three_high) if three_high else 0
    ten_low_mean    = sum(r["mean_score"] for r in ten_low)    / len(ten_low)    if ten_low    else 0

    print(f"    3 high-quality examples → mean accuracy: {three_high_mean:.4f} ({three_high_mean*100:.1f}%)")
    print(f"   10 low-quality  examples → mean accuracy: {ten_low_mean:.4f}  ({ten_low_mean*100:.1f}%)")
    print(f"    → Difference: {(three_high_mean - ten_low_mean)*100:.1f} pp (3-high BETTER by this margin)")

    # 4. Shot count effect within high quality
    print("\n[4] Effect of shot count within HIGH quality (averaged across domains):")
    for n in [1, 3, 5, 10]:
        rows = [r for r in summary if r["quality"] == "high" and r["n_shots"] == n]
        mean = sum(r["mean_score"] for r in rows) / len(rows) if rows else 0
        print(f"    {n:2d} shots: {mean:.4f} ({mean*100:.1f}%)")

    # 5. Per-domain quality effect
    print("\n[5] Quality effect per domain (high vs low):")
    for d in set(r["domain"] for r in summary):
        h = [r["mean_score"] for r in summary if r["domain"] == d and r["quality"] == "high"]
        l = [r["mean_score"] for r in summary if r["domain"] == d and r["quality"] == "low"]
        if h and l:
            diff = (sum(h)/len(h) - sum(l)/len(l)) * 100
            print(f"    {d}: Δ = +{diff:.1f} pp for high vs low quality")

    print("\n" + "="*60 + "\n")


def compute_correlation(summary: list):
    """
    Compute Pearson r between a numeric quality encoding and mean_score.
    Encoding: high=3, medium=2, low=1
    """
    encoding = {"high": 3, "medium": 2, "low": 1}
    x = [encoding[r["quality"]] for r in summary]
    y = [r["mean_score"] for r in summary]

    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den_x = math.sqrt(sum((xi - mean_x)**2 for xi in x))
    den_y = math.sqrt(sum((yi - mean_y)**2 for yi in y))

    r = num / (den_x * den_y) if den_x * den_y != 0 else 0
    r2 = r ** 2

    print(f"[CORRELATION] Prompt quality level (encoded) vs mean_score:")
    print(f"    Pearson r  = {r:.4f}")
    print(f"    r²         = {r2:.4f}  ← goes in abstract of paper")
    return r, r2


def generate_heatmap_data(summary: list):
    """Print the heatmap table (Quality × Shots) averaged across all domains."""
    print("\n[HEATMAP] Mean Accuracy — Quality (rows) × Shot Count (cols):")
    print(f"{'':12s}", end="")
    for n in [1, 3, 5, 10]:
        print(f"  {n} shots", end="")
    print()

    for q in ["high", "medium", "low"]:
        print(f"{q.upper():12s}", end="")
        for n in [1, 3, 5, 10]:
            rows = [r for r in summary if r["quality"] == q and r["n_shots"] == n]
            mean = sum(r["mean_score"] for r in rows) / len(rows) if rows else 0
            print(f"  {mean:.3f} ", end="")
        print()
    print()


def save_csv_tables(summary: list):
    """Save per-domain breakdown tables for appendix."""
    os.makedirs(FIGURES_DIR, exist_ok=True)

    domains = sorted(set(r["domain"] for r in summary))
    for domain in domains:
        path = os.path.join(FIGURES_DIR, f"table_{domain}.csv")
        domain_rows = [r for r in summary if r["domain"] == domain]
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["quality", "n_shots", "mean_score", "std_score"])
            writer.writeheader()
            for row in sorted(domain_rows, key=lambda x: (x["quality"], x["n_shots"])):
                writer.writerow({k: row[k] for k in ["quality", "n_shots", "mean_score", "std_score"]})
        print(f"[SAVED] {path}")


def run_analysis():
    summary = load_summary()
    print_headline_stats(summary)
    r, r2 = compute_correlation(summary)
    generate_heatmap_data(summary)
    save_csv_tables(summary)
    return summary, r, r2


if __name__ == "__main__":
    run_analysis()
