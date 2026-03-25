# Does Prompt Quality Actually Matter More Than Prompt Quantity?
### An Empirical Study on Few-Shot Example Quality vs. Count in Large Language Model Performance

**Author:** Aditya Prasad
**Institution:** Chitkara University Punjab
**Email:** aditya.1194.be22@chitkara.edu.in

---

## Overview

This repository contains the complete code, data, and paper for a research project investigating whether the **quality** of few-shot examples given to a large language model matters more than the **quantity**.

**Core finding:** 3 high-quality examples outperform 10 low-quality examples by **22.7 percentage points** on average across five task domains.

---

## Research Question

> Is a small number of high-quality examples more valuable than a larger number of low-quality ones in few-shot prompting?

---

## Experiment Design

A **3 × 4 × 5 factorial experiment** with:

| Variable | Values |
|---|---|
| Quality levels | High, Medium, Low |
| Shot counts | 1, 3, 5, 10 |
| Task domains | JSON Extraction, Math, SQL, Code Debugging, Summarization |

- **600 total LLM calls** to GPT-4o-mini at temperature 0.0
- 10 test cases per condition
- Domain-appropriate automatic evaluation metrics

---

## Key Results

| Comparison | Result |
|---|---|
| High quality vs Low quality | **+21.1 pp** (86.4% vs 65.2%) |
| 3 high-quality vs 10 low-quality | **+22.7 pp** (85.6% vs 63.0%) |
| Biggest domain gap (JSON) | **+65.8 pp** |
| Pearson r (quality vs accuracy) | **r = 0.31** |

---

## Repository Structure

```
├── main.py                        # Entry point — run experiment + analysis
├── requirements.txt               # Python dependencies
├── paper/
│   ├── research_paper.md          # Full research paper (Markdown)
│   └── research_paper.docx        # Full research paper (Word / Google Docs)
├── src/
│   ├── config.py                  # Model name, domains, shot counts, quality levels
│   ├── experiment.py              # Parallel experiment runner (ThreadPoolExecutor)
│   ├── prompts.py                 # Prompt templates for all 5 domains × 3 quality levels
│   ├── few_shot_examples.py       # Hand-crafted examples at high/medium/low quality
│   ├── test_cases.py              # Ground-truth test cases for all 5 domains
│   ├── evaluator.py               # Scoring functions per domain
│   ├── llm_client.py              # OpenAI API wrapper
│   ├── analyze.py                 # Statistical analysis — Pearson r, heatmaps, tables
│   ├── export_csvs.py             # Generates 5 structured result CSVs
│   ├── export_prompts.py          # Exports all 600 prompts + scores to CSV
│   └── export_docx.py             # Converts paper to .docx format
├── results/
│   ├── raw_results.json           # All 600 individual call scores
│   ├── summary.csv                # Mean + std per cell (60 rows)
│   ├── all_prompts_and_results.csv # Every prompt + score (600 rows)
│   └── export/
│       ├── csv1_all_600_calls.csv      # All 600 calls with scores
│       ├── csv2_cell_summary.csv       # 60 cells — mean, std, min, max
│       ├── csv3_quality_comparison.csv # Quality effect per domain
│       ├── csv4_shots_comparison.csv   # Shot count effect per quality
│       └── csv5_headline_findings.csv  # Key numbers for presentation
└── PRESENTATION_CRUX.md           # Presentation script and talking points
```

---

## How to Run

### 1. Clone the repo
```bash
git clone https://github.com/sudo-adi/llm-research-work.git
cd llm-research-work
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your OpenAI API key
```bash
export OPENAI_API_KEY=your_key_here
```

### 4. Run the full experiment (600 calls, ~60 seconds)
```bash
python main.py run
```

### 5. Run analysis and generate stats
```bash
python main.py analyze
```

### 6. Export all result CSVs
```bash
python -c "from src.export_csvs import run; run()"
```

---

## Evaluation Metrics

| Domain | Metric |
|---|---|
| JSON Extraction | Field-level F1 (exact match, partial, missing) |
| Math Word Problems | Exact numeric match with ±0.01 tolerance |
| SQL Generation | Keyword coverage (fraction of expected SQL keywords) |
| Code Debugging | Bug identification (0.5) + fix accuracy (0.5) |
| Text Summarization | Key-point coverage (partial phrase matching) |

---

## Notable Findings

1. **JSON extraction** — Low-quality prompts scored ~1%. Bad examples caused the model to stop returning JSON entirely.
2. **Math anomaly** — Medium quality (20%) scored worse than low quality (80%) due to a metric-format interaction. Medium prompts did not enforce the `Final Answer: X` pattern the evaluator requires.
3. **SQL immunity** — Smallest quality gap (+3.1 pp). GPT's strong SQL pretraining overrides bad examples.
4. **More bad examples hurt** — Medium and low quality accuracy declines as shot count increases from 1→10.

---

## Paper

The full paper is available in two formats:
- [`paper/research_paper.md`](paper/research_paper.md) — Markdown
- [`paper/research_paper.docx`](paper/research_paper.docx) — Word / Google Docs compatible

---

## Tech Stack

- **Model:** GPT-4o-mini (OpenAI)
- **Language:** Python 3.10+
- **Parallelism:** `concurrent.futures.ThreadPoolExecutor` (40 workers)
- **Libraries:** `openai`, `python-docx`
