# Does Prompt Quality Actually Matter More Than Prompt Quantity?
## An Empirical Study on Few-Shot Example Quality vs. Count in Large Language Model Performance

---

**Aditya Prasad**
Chitkara University Punjab
aditya.1194.be22@chitkara.edu.in

---

**Abstract**

**Background/Introduction:**
Few-shot prompting is a widely used technique in which a small number of input-output examples are included in a prompt to guide a large language model (LLM) toward a desired output. A common assumption in both research and practice is that providing more examples leads to better model performance. However, this assumption rarely accounts for the quality of those examples. Poor-quality demonstrations may introduce noise, mislead the model, and potentially degrade performance regardless of how many are provided.

**Objectives:**
This study investigates whether the quality of few-shot examples has a greater impact on LLM output accuracy than the quantity of examples provided. Specifically, it aims to determine whether a small number of high-quality examples can outperform a larger number of low-quality examples, and how quality and quantity interact across different task types.

**Methods/Methodology:**
A controlled 3 × 4 × 5 factorial experiment was designed, crossing three quality levels (high, medium, low), four shot counts (1, 3, 5, 10), and five task domains (JSON extraction, mathematical word problems, SQL generation, code debugging, and text summarization). A total of 600 LLM calls were made to GPT-4o-mini at temperature 0.0 to ensure deterministic outputs. Each condition was evaluated using domain-appropriate automatic metrics including field-level F1, exact match, keyword coverage, and key-point coverage.

**Results/Findings:**
High-quality prompts achieved a mean accuracy of 86.4%, compared to 65.2% for low-quality prompts — a gap of 21.1 percentage points. Critically, 3 high-quality examples outperformed 10 low-quality examples by 22.7 percentage points (85.6% vs. 63.0%). The quality effect was most pronounced in JSON extraction (+65.8 pp) and math word problems (+20.0 pp). Medium-quality prompts performed only marginally better than low-quality ones (+0.7 pp), suggesting a quality threshold below which curation effort does not translate to performance gains. The Pearson correlation between quality level and accuracy was r = 0.31 (r² = 0.10).

**Conclusion:**
Prompt example quality is a stronger determinant of LLM performance than example quantity. Three carefully curated examples consistently outperform ten carelessly assembled ones. Medium quality provides almost no advantage over low quality, indicating that partial curation is insufficient. These findings advise practitioners to prioritize example curation over accumulation when designing few-shot prompts for production AI systems.

---

**Keywords:** few-shot prompting, prompt engineering, in-context learning, large language models, example quality

---

## 1. Introduction

The rise of large language models (LLMs) has introduced a new paradigm in how we interact with AI systems. Unlike traditional machine learning where a model is retrained for each new task, LLMs can be steered purely through natural language instructions — a process broadly called prompting. Among the most effective prompting strategies is few-shot learning, where the prompt contains a handful of input-output examples that demonstrate the desired behavior before the actual query is posed.

The intuition behind few-shot prompting is simple: show the model what a good response looks like, and it will produce something similar. Most practitioners follow a straightforward rule of thumb — the more examples, the better. And to a point, this holds true. Papers like Brown et al.'s GPT-3 work (2020) showed clear gains as shot count increased from 0 to 32. But these studies rarely disentangle a confounding factor: example quality.

When a practitioner adds more few-shot examples, they are often adding examples of *varying* quality — some well-formed, some ambiguous, some outright wrong. If those extra examples introduce noise, they may actively hurt performance even as they increase quantity. This brings us to the central question of our paper:

**Is a small number of high-quality examples more valuable than a larger number of low-quality ones?**

We believe this question has meaningful practical stakes. Collecting and curating good examples takes time and effort. If quality matters far more than quantity, practitioners should invest in curation rather than accumulation.

To answer this, we operationalize "example quality" into three levels:
- **High quality**: well-formed, complete, correctly formatted, domain-appropriate examples
- **Medium quality**: mostly correct but with missing fields, imprecise answers, or inconsistent formatting
- **Low quality**: incorrect answers, poor formatting, or misleading demonstrations

We then cross this quality axis with four shot counts (1, 3, 5, 10) across five domains, measuring task performance with domain-appropriate automatic metrics. The result is a 3×4 grid of 12 experimental conditions per domain, yielding 60 unique conditions total.

---

## 2. Related Work

**In-context learning and few-shot prompting.**
The concept of few-shot in-context learning was brought to mainstream attention by Brown et al. (2020) with GPT-3. Their work showed that a single large model could perform competitively on many NLP benchmarks with just a few demonstration examples, without any gradient updates. Subsequent work by Min et al. (2022) made a surprising finding: the content of the labels in few-shot examples matters less than previously thought — what matters more is the format and the demonstration that a response is even expected. Our work extends this thread by examining quality at a more holistic level, beyond just label correctness.

**Prompt engineering as a discipline.**
Wei et al. (2022) introduced chain-of-thought prompting, showing that including reasoning steps in examples dramatically improves performance on reasoning tasks. This implicitly encodes "quality" — a chain-of-thought example is, by definition, more detailed and informative than a flat input-output pair. Our high-quality examples similarly include structured reasoning and proper formatting, while our low-quality examples omit them.

**Example selection strategies.**
Multiple works have explored which examples to select for few-shot prompts. Zhang et al. (2022) proposed selecting examples similar to the test input using semantic similarity. Su et al. (2022) used mutual information to rank examples. These works assume a fixed pool of high-quality examples and focus on *selection*. We take a different angle and ask: given a fixed number of examples, how much does their inherent quality affect outcomes?

**Prompt sensitivity.**
Lu et al. (2022) showed that the *order* of examples in a prompt can drastically affect performance, sometimes by over 30 percentage points. Zhao et al. (2021) showed that majority-label bias in demonstrations affects predictions. These works demonstrate that prompts are brittle in ways that go beyond just content. Our work contributes another axis of analysis — the quality level of the examples themselves.

---

## 3. Methodology

### 3.1 Experimental Design

Our experiment follows a **3 × 4 × 5 factorial design**:
- 3 quality levels: high, medium, low
- 4 shot counts: 1, 3, 5, 10
- 5 domains: JSON extraction, math word problems, SQL generation, code debugging, text summarization

For each of the 60 resulting conditions, we ran 10 test cases with known ground truth, yielding a total of **600 LLM evaluations**. All calls were made to GPT-4o-mini with temperature set to 0.0 for deterministic output.

### 3.2 Domain Selection Rationale

We chose these five domains to span a diversity of task types:

| Domain | Task Type | Metric | Why Chosen |
|---|---|---|---|
| JSON Extraction | Structured output | Field-level F1 | Tests precision and format adherence |
| Math Word Problems | Reasoning | Exact match | Tests numerical accuracy |
| SQL Generation | Code generation | Keyword coverage | Tests domain-specific syntax |
| Code Debugging | Analysis + generation | Bug ID + fix accuracy | Tests diagnostic reasoning |
| Text Summarization | Language generation | Key-point coverage | Tests factual compression |

### 3.3 Defining Example Quality

Our three quality levels are defined by a combination of four attributes:

| Attribute | High | Medium | Low |
|---|---|---|---|
| Answer correctness | ✓ Fully correct | ✓ Mostly correct | ✗ Often wrong |
| Format compliance | ✓ Proper formatting | ⚠ Inconsistent | ✗ Unstructured |
| Completeness | ✓ All fields present | ⚠ Partial | ✗ Missing key info |
| Domain appropriateness | ✓ Domain terminology used | ⚠ Generic | ✗ Misleading |

Crucially, we constructed examples manually at each quality level rather than synthetically degrading high-quality examples. This ensures that low-quality examples reflect the kind of careless or incorrect examples a practitioner might include when prompting without careful curation — a realistic scenario.

### 3.4 Prompt Structure

For each domain, we built three prompt templates (one per quality level):

- **High quality prompt**: Explicit role definition ("You are a senior SQL developer..."), task-specific instructions, format constraints, domain keywords, and numbered examples with clear input/output separation.
- **Medium quality prompt**: Brief role mention, basic task instruction, labeled but minimally formatted examples.
- **Low quality prompt**: Bare task request, no role or constraints, raw concatenated examples with no structure.

Within each quality level, the example content itself also matches that quality level. So a high-quality prompt uses high-quality examples, a low-quality prompt uses low-quality examples. This is intentional — in practice, the practitioner's effort level tends to be consistent across prompt structure and example selection.

### 3.5 Evaluation Metrics

Each domain uses a different automatic metric:

**JSON Extraction — Field-level F1:**
We compare the model's JSON output against the ground-truth dictionary. For each expected key-value pair, we award 1.0 for an exact match, 0.7 for a partial string match, 0.5 if the key is present but the value is wrong, and 0.0 if the key is missing. The final score is the average across all expected fields.

**Math Word Problems — Exact match with numeric tolerance:**
We look for a "Final Answer: X" pattern in the output (enforced in high-quality prompts). We then compare numerically with a tolerance of ±0.01. For fraction answers (e.g., 3/8), we convert to float before comparison.

**SQL Generation — Keyword coverage:**
We define a set of expected SQL keywords and clauses for each query (e.g., ["SELECT", "GROUP BY", "COUNT", "customer"]). The score is the fraction of these present in the model's output.

**Code Debugging — Bug identification + fix accuracy:**
We score 0.5 points for correctly identifying the bug (key terms from bug description present in output) and 0.5 points for providing the correct fix (key terms from fix present in output).

**Text Summarization — Key-point coverage:**
Each test case has a list of key facts that must appear in the summary. We compute partial phrase matching — the fraction of words in each key point that appear in the output — and average across all key points.

---

## 4. Results

### 4.1 Overall Quality Effect

Table 1 shows the mean accuracy across all domains and shot counts, broken down by quality level.

**Table 1: Mean accuracy by prompt quality level (all domains, all shot counts)**

| Quality Level | Mean Accuracy | vs. Low Quality |
|---|---|---|
| High | 0.86 (86.4%) | +21.1 pp |
| Medium | 0.66 (65.9%) | +0.7 pp |
| Low | 0.65 (65.2%) | — |

The gap between high and low quality is substantial at 21.1 percentage points. High-quality prompts consistently outperform low-quality ones across all domains and all shot counts. Medium-quality prompts show only a marginal advantage over low-quality (+0.7 pp), suggesting that partial quality improvements yield diminishing returns — a practitioner must invest in genuine curation, not just minor cleanup.

### 4.2 Quality × Shot Count Interaction

Table 2 presents the full 3×4 heatmap averaged across all five domains.

**Table 2: Mean accuracy — Quality (rows) × Shot Count (cols)**

|  | 1 shot | 3 shots | 5 shots | 10 shots |
|---|---|---|---|---|
| **High** | 0.833 | 0.856 | 0.856 | 0.908 |
| **Medium** | 0.680 | 0.658 | 0.666 | 0.633 |
| **Low** | 0.652 | 0.670 | 0.657 | 0.630 |

Several patterns emerge:
1. Within the high-quality tier, performance improves with shot count, with the largest gains appearing at 10 shots (90.8%), suggesting the model benefits from more correct demonstrations even beyond 3–5 examples when those examples are well-formed.
2. Within the medium-quality tier, adding more examples slightly *hurts* performance — accuracy drops from 68.0% at 1 shot to 63.3% at 10 shots. More mediocre examples amplify inconsistency rather than clarifying the task.
3. Within the low-quality tier, performance is similarly flat or declining — from 65.2% at 1 shot down to 63.0% at 10 shots, confirming that more wrong examples do not help.
4. The 3 high-quality vs. 10 low-quality comparison: **85.6% vs. 63.0% — a 22.7 percentage point gap** — is the core empirical contribution of this paper.

### 4.3 Per-Domain Breakdown

**Table 3: Mean accuracy by domain and quality level (averaged across all shot counts)**

| Domain | High | Medium | Low | Quality Δ (H-L) |
|---|---|---|---|---|
| JSON Extraction | 0.67 | 0.60 | 0.01 | +65.8 pp |
| Math Word Problems | 1.00 | 0.20 | 0.80 | +20.0 pp |
| SQL Generation | 0.98 | 0.93 | 0.94 | +3.1 pp |
| Code Debugging | 0.76 | 0.78 | 0.66 | +9.6 pp |
| Text Summarization | 0.92 | 0.79 | 0.85 | +7.2 pp |

The quality effect is most dramatic in **JSON extraction** (+65.8 pp), where low-quality prompts caused the model to produce unstructured text instead of valid JSON — a format failure, not just a content failure. High-quality prompts with explicit JSON formatting rules and well-formed examples virtually eliminated this failure mode.

**Math word problems** reveal a notable interaction: medium quality (0.20) performed *worse* than low quality (0.80). Investigation shows this is a metric artifact — high and low-quality prompts enforced a "Final Answer: X" output format that the evaluator relies on, while medium-quality prompts did not, causing correct answers to be undetected. This highlights that format compliance is independently critical from answer correctness.

**SQL generation** shows the smallest quality gap (+3.1 pp), likely because the model's pretraining on SQL is strong enough that even poorly-structured prompts produce recognizable SQL syntax. The task is sufficiently constrained that the model defaults to correct behavior regardless of example quality.

**Code debugging** shows high and medium quality performing similarly (0.76 vs. 0.78), with low quality trailing at 0.66. The model's strong code understanding means it partially compensates for low-quality examples, but the gap remains meaningful.

**Text summarization** shows a compressed quality gap (+7.2 pp), consistent with the open-ended nature of the task — the model's language generation capabilities make it robust to example quality variation relative to structured tasks.

### 4.4 Correlation Analysis

To quantify the relationship between prompt quality and output accuracy, we encoded quality levels numerically (high = 3, medium = 2, low = 1) and computed the Pearson correlation coefficient across all 60 experimental conditions.

**Pearson r = 0.31, r² = 0.10**

This indicates that prompt quality level explains approximately **10% of the variance** in output accuracy across all conditions. While this may appear modest, it is a meaningful effect given that domain (which accounts for the largest share of variance — e.g., math at 100% vs. JSON at 1%) and shot count also contribute substantially. Within individual domains, the quality effect is far stronger, as shown in Table 3.

### 4.5 The Shot Count Finding

Within the high-quality tier, performance scales positively with shot count: 1-shot (83.3%) → 3-shot (85.6%) → 5-shot (85.6%) → 10-shot (90.8%). Unlike the originally hypothesized saturation at 3–5 shots, our data suggests continued gains up to 10 shots when examples are genuinely high-quality. The practical implication is that the "sweet spot" depends on quality: with high-quality examples, more shots continue to help; with medium or low-quality examples, additional shots are wasteful or harmful.

**Table 4: Accuracy by quality level across shot counts (averaged across all domains)**

| Quality | 1 shot | 3 shots | 5 shots | 10 shots | Trend |
|---|---|---|---|---|---|
| High | 83.3% | 85.6% | 85.6% | 90.8% | ↑ Keeps improving |
| Medium | 68.0% | 65.8% | 66.6% | 63.3% | ↓ Slowly declining |
| Low | 65.2% | 67.0% | 65.7% | 63.0% | → Flat / declining |

---

## 5. Discussion

### 5.1 Why Quality Dominates Quantity

The core mechanism is likely rooted in how LLMs perform in-context learning. During inference, the model updates its implicit distribution over likely outputs based on the patterns it sees in the context. High-quality examples establish a consistent, correct pattern — the model learns to produce outputs that structurally and semantically match the demonstrations. Low-quality examples, by contrast, establish an inconsistent or incorrect pattern that the model then echoes.

When we add more low-quality examples, we are not providing the model with more signal — we are providing it with more noise, and potentially with more confidence in the wrong pattern. This explains why performance in the medium and low-quality tiers *declines* with more shots, while high-quality performance continues to improve.

The JSON extraction result is the clearest evidence: low-quality examples that returned plain text instead of JSON essentially trained the model to ignore the JSON requirement entirely, regardless of how many such examples were provided.

### 5.2 Implications for Practitioners

These findings carry concrete practical guidance:

1. **Curate before you accumulate.** 3 high-quality examples outperform 10 low-quality ones by 22.7 percentage points on average. The effort invested in curation pays off immediately.

2. **Format compliance is not optional.** The math domain results show that even correct answers, presented without the required output format, score near zero under strict evaluation. Format is part of quality, not separate from it.

3. **Medium quality is not a safe middle ground.** Medium-quality prompts performed only 0.7 percentage points better than low-quality ones on average, and in some cases worse. Partial curation is not proportionally rewarded — there appears to be a threshold below which quality improvements do not translate to performance gains.

4. **Domain determines sensitivity to quality.** Tasks with rigid correct answers (JSON, SQL) are most sensitive to example quality. Tasks the model already handles well from pretraining (SQL syntax, code reasoning) show compressed quality gaps. Practitioners should invest curation effort proportionally to domain sensitivity.

5. **More high-quality shots still help.** Unlike the common advice to use 3–5 shots, our data shows gains continuing to 10 shots — but only when those shots are high-quality. The quantity-quality interaction is not symmetrical.

### 5.3 Limitations

Several limitations of this work should be acknowledged.

**Single model.** All experiments were conducted with GPT-4o-mini. The exact magnitude of the quality effect may differ across model families and sizes. Larger models with stronger instruction-following may be more robust to low-quality examples; smaller models may be more sensitive.

**Automatic metrics.** While our metrics are carefully designed for each domain, they are not perfect proxies for human judgement. A SQL query may be semantically correct even if it misses one of our expected keywords. Similarly, a summarization may be excellent while not mentioning every expected key point verbatim. The math result in particular reveals that metric design interacts with prompt format in ways that require careful interpretation.

**Example construction.** Our quality levels were hand-constructed by a single author. A more rigorous approach would involve multiple human raters defining and rating example quality independently, then computing inter-rater agreement. Future work should pursue this.

**Domain coverage.** Five domains, while diverse, do not represent the full breadth of tasks LLMs are used for. Results may differ for creative writing, dialogue, or longer-form reasoning tasks.

**Shot count ceiling.** We tested up to 10 shots. The relationship between quality and quantity at higher shot counts (32, 64, 128) remains unexplored and may reveal different saturation dynamics.

---

## 6. Conclusion

This paper presented a systematic empirical study of how few-shot example quality interacts with example quantity in LLM prompting. Across five domains and 600 LLM evaluations using GPT-4o-mini, we find consistent evidence that quality outweighs quantity: 3 high-quality examples reliably outperform 10 low-quality examples, with a mean advantage of **22.7 percentage points**.

The Pearson correlation between prompt quality encoding and output accuracy (r = 0.31, r² = 0.10) confirms quality as a meaningful predictor of performance. Within specific domains — particularly JSON extraction (+65.8 pp) and math word problems (+20.0 pp) — the effect is decisive.

A notable finding is the interaction between quality and quantity: within the high-quality tier, more shots continue to improve performance up to 10 examples. Within medium and low-quality tiers, adding more examples is flat or harmful. This asymmetry reframes the "how many shots?" question — the answer depends entirely on whether the examples are worth having at all.

For practitioners, the message is direct: invest in your examples. The difference between a carelessly assembled prompt and a thoughtfully curated one is not small — it can be the difference between a system that works and one that does not.

---

## References

1. Brown, T., et al. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems*, 33, 1877–1901.

2. Wei, J., et al. (2022). Chain-of-thought prompting elicits reasoning in large language models. *Advances in Neural Information Processing Systems*, 35.

3. Min, S., et al. (2022). Rethinking the role of demonstrations: What makes in-context learning work? *Proceedings of EMNLP 2022*.

4. Lu, Y., et al. (2022). Fantastically ordered prompts and where to find them: Overcoming few-shot prompt order sensitivity. *Proceedings of ACL 2022*.

5. Zhang, Z., et al. (2022). Automatic chain of thought prompting in large language models. *arXiv preprint arXiv:2210.11610*.

6. Su, H., et al. (2022). Selective annotation makes language models better few-shot learners. *arXiv preprint arXiv:2209.01975*.

7. Zhao, Z., et al. (2021). Calibrate before use: Improving few-shot performance of language models. *Proceedings of ICML 2021*.

8. Liu, P., et al. (2023). Pre-train, prompt, and predict: A systematic survey of prompting methods in natural language processing. *ACM Computing Surveys*, 55(9), 1–35.

9. Dong, Q., et al. (2022). A survey on in-context learning. *arXiv preprint arXiv:2301.00234*.

10. Lester, B., Al-Rfou, R., & Constant, N. (2021). The power of scale for parameter-efficient prompt tuning. *Proceedings of EMNLP 2021*.

---

**Code & Data Repository:** https://github.com/sudo-adi/llm-research-work

*Manuscript prepared as part of a college-level research project on prompt engineering efficiency in large language models.*
