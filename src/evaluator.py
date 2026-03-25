"""
Evaluates LLM outputs against ground truth for each domain.
Returns a score 0.0 – 1.0 per test case.
"""

import json
import re
import string


# ─── JSON EXTRACTION EVALUATOR ────────────────────────────────────────────────

def evaluate_json(output: str, expected: dict) -> float:
    """
    Score = fraction of expected key-value pairs correctly extracted.
    Partial credit: key present but wrong value = 0.5 * (1/n).
    """
    try:
        # Strip markdown code fences if present
        clean = re.sub(r"```[a-z]*\n?", "", output).strip()
        parsed = json.loads(clean)
    except Exception:
        # Try to extract JSON object from text
        match = re.search(r"\{.*\}", output, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
            except Exception:
                return 0.0
        else:
            return 0.0

    if not expected:
        return 1.0

    total = len(expected)
    score = 0.0

    for key, exp_val in expected.items():
        # Normalize key matching (handle minor name variations)
        found_val = None
        for k in parsed:
            if not isinstance(k, str):
                continue
            if k.lower().replace(" ", "_") == key.lower().replace(" ", "_"):
                found_val = parsed[k]
                break

        if found_val is None:
            continue  # key missing → 0

        # Normalize values for comparison
        exp_str = str(exp_val).lower().strip()
        got_str = str(found_val).lower().strip()

        if exp_str == got_str:
            score += 1.0
        elif isinstance(exp_val, (int, float)):
            # Try numeric comparison with tolerance
            try:
                if abs(float(found_val) - float(exp_val)) < 0.01:
                    score += 1.0
                else:
                    score += 0.5  # partial — key found but value wrong
            except Exception:
                score += 0.5
        elif isinstance(exp_val, list):
            # Lists: Jaccard similarity
            exp_set = set(str(x).lower() for x in exp_val)
            got_set = set(str(x).lower() for x in (found_val if isinstance(found_val, list) else [found_val]))
            if exp_set:
                score += len(exp_set & got_set) / len(exp_set | got_set)
        else:
            # String: partial match check
            if exp_str in got_str or got_str in exp_str:
                score += 0.7
            else:
                score += 0.0

    return round(score / total, 4)


# ─── MATH EVALUATOR ───────────────────────────────────────────────────────────

def evaluate_math(output: str, expected: str) -> float:
    """
    Looks for 'Final Answer: X' pattern first.
    Falls back to last number in output.
    Checks string match, then numeric match.
    """
    output_clean = output.strip().lower()
    expected_clean = expected.strip().lower()

    # Extract "Final Answer: X" pattern
    final_match = re.search(r"final answer[:\s]+([^\n]+)", output_clean)
    if final_match:
        candidate = final_match.group(1).strip()
    else:
        # Get last number-like token
        numbers = re.findall(r"-?\d+(?:[./]\d+)?", output_clean)
        candidate = numbers[-1] if numbers else ""

    if not candidate:
        return 0.0

    # Exact string match (handles fractions like 3/8)
    if candidate.strip() == expected_clean.strip():
        return 1.0

    # Numeric match
    try:
        def parse_num(s):
            if "/" in s:
                parts = s.split("/")
                return float(parts[0]) / float(parts[1])
            return float(s)

        got = parse_num(candidate)
        exp = parse_num(expected_clean)
        return 1.0 if abs(got - exp) < 0.01 else 0.0
    except Exception:
        return 0.0


# ─── SQL EVALUATOR ────────────────────────────────────────────────────────────

def evaluate_sql(output: str, expected_keywords: list) -> float:
    """
    Score = fraction of expected SQL keywords/phrases present in output.
    Case-insensitive.
    """
    output_upper = output.upper()
    hits = sum(1 for kw in expected_keywords if kw.upper() in output_upper)
    return round(hits / len(expected_keywords), 4) if expected_keywords else 0.0


# ─── CODE DEBUG EVALUATOR ─────────────────────────────────────────────────────

def evaluate_code_debug(output: str, bug_description: str, fix: str) -> float:
    """
    Score based on:
    - 0.5 points: mentions the bug (key terms from bug description appear in output)
    - 0.5 points: provides the fix (key terms from fix appear in output)
    """
    output_lower = output.lower()
    score = 0.0

    # Extract key terms from bug description and fix
    bug_terms = _key_terms(bug_description)
    fix_terms = _key_terms(fix)

    if bug_terms:
        bug_hits = sum(1 for t in bug_terms if t in output_lower)
        score += 0.5 * (bug_hits / len(bug_terms))

    if fix_terms:
        fix_hits = sum(1 for t in fix_terms if t in output_lower)
        score += 0.5 * (fix_hits / len(fix_terms))

    return round(score, 4)


def _key_terms(text: str) -> list:
    """Extract meaningful words from a description (ignore stop words)."""
    stop = {"the", "a", "an", "is", "in", "of", "to", "and", "or", "for",
            "be", "use", "used", "not", "with", "by", "on", "at", "it"}
    words = re.findall(r"[a-z_][a-z_0-9]+", text.lower())
    return [w for w in words if w not in stop and len(w) > 2]


# ─── TEXT SUMMARIZATION EVALUATOR ─────────────────────────────────────────────

def evaluate_summary(output: str, key_points: list) -> float:
    """
    Score = fraction of key_points present in the summary.
    Each key_point is a string or short phrase.
    Partial phrase matching allowed.
    """
    output_lower = output.lower()
    score = 0.0

    for point in key_points:
        terms = point.lower().split()
        hits = sum(1 for t in terms if t in output_lower)
        score += hits / len(terms)

    return round(score / len(key_points), 4) if key_points else 0.0


# ─── MASTER EVALUATOR ─────────────────────────────────────────────────────────

def evaluate(domain: str, output: str, test_case: dict) -> float:
    if domain == "json_extraction":
        return evaluate_json(output, test_case["expected"])
    elif domain == "math_word_problems":
        return evaluate_math(output, test_case["expected"])
    elif domain == "sql_generation":
        return evaluate_sql(output, test_case["expected_keywords"])
    elif domain == "code_debugging":
        return evaluate_code_debug(output, test_case["bug"], test_case["fix"])
    elif domain == "text_summarization":
        return evaluate_summary(output, test_case["key_points"])
    else:
        raise ValueError(f"Unknown domain: {domain}")
