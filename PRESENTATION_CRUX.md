# What To Say — Presentation Crux
### One file. Everything you need to open your mouth confidently.

---

## ONE LINE SUMMARY
> "We proved that 3 good examples given to an AI beats 10 bad examples — by 22.7 percentage points."

---

## THE PROBLEM (say this first)
"Everyone assumes — more examples you give an AI, better it performs.
We asked — what if the quality of those examples matters more than the count?"

---

## WHAT WE DID (say this second)
"We ran a controlled experiment.
- 5 tasks: JSON, Math, SQL, Code, Summarization
- 3 quality levels: Good examples, Okay examples, Bad examples
- 4 shot counts: 1, 3, 5, 10 examples each time
- 600 total calls to GPT — all recorded, all scored"

---

## THE MAIN NUMBERS (memorize these 3)

| What | Number |
|---|---|
| High quality accuracy | 86.4% |
| Low quality accuracy | 65.2% |
| Gap | 21.1 percentage points |

**The killer number:**
> "3 good examples = 85.6% accuracy.
> 10 bad examples = 63.0% accuracy.
> Good quality wins by 22.7 points."

---

## 3 INTERESTING FINDINGS (say these for wow factor)

**Finding 1 — JSON**
"Low quality examples got nearly 0% on JSON.
Why? The bad examples didn't show JSON format.
So GPT forgot it was supposed to return JSON at all.
Format of your example directly controls format of GPT's answer."

**Finding 2 — Math anomaly**
"Medium quality scored 20%. Low quality scored 80%.
Medium was actually WORSE than bad.
Why? Our scorer needed 'Final Answer: X' format.
Medium prompts didn't enforce that format.
So even correct answers scored zero because they weren't readable.
Lesson: format matters as much as correctness."

**Finding 3 — More bad examples make it worse**
"With bad examples — going from 1 to 10 examples drops score from 65% to 63%.
More bad examples = more confusion for the AI.
But with good examples — going from 1 to 10 improves from 83% to 91%.
Quantity only helps if quality is already there."

---

## THE CONCLUSION (say this last)
"Don't collect more examples. Make better ones.
Medium quality is almost as bad as bad quality — only 0.7 points difference.
You either curate properly or you don't.
There is no reward for half effort."

---

## IF PROFESSOR ASKS TOUGH QUESTIONS

**"Why only 10 test cases per cell?"**
→ "600 API calls total — feasible for a college project. Acknowledged as a limitation in the paper."

**"Why only one AI model?"**
→ "Acknowledged in limitations. Future work would test GPT-4, Claude, Gemini."

**"Your medium scored worse than low in math — doesn't that break your thesis?"**
→ "Great observation. It's a metric artifact — the scorer needed a specific output format that medium prompts didn't enforce. We explain this in Section 4.3. It actually reinforces our finding — format compliance is part of quality."

**"How did you ensure fairness?"**
→ "Temperature set to 0.0 — same prompt always gives same answer. Equal 150 calls per shot count. Same test questions across all conditions."

**"What is a shot?"**
→ "One example shown to the AI before asking the real question. 3-shot means 3 examples were shown."

**"What does pp mean?"**
→ "Percentage points. If A scores 86% and B scores 65%, the gap is 21 pp — just simple subtraction."

---

## FILES TO SHOW IN ORDER
1. `csv5_headline_findings.csv` → show the main numbers
2. `csv4_shots_comparison.csv` → show quality × shots interaction
3. `csv3_quality_comparison.csv` → show per domain breakdown
4. `csv1_all_600_calls.csv` → show raw evidence
5. `paper/research_paper.md` → show the full paper

---

## OPENING LINE (memorize this)
"We ran 600 AI experiments to answer one question —
does the quality of examples you give an AI matter more than how many you give?
The answer is yes. And the gap is bigger than we expected."

## CLOSING LINE (memorize this)
"Invest in your examples. 3 good ones beat 10 bad ones every time."
