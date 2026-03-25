"""
Prompt templates at three quality levels for each domain.
HIGH: role + context + domain keywords + format + constraints
MEDIUM: role + task, no format or keywords
LOW: bare task only, no structure
"""

# ─── JSON EXTRACTION ──────────────────────────────────────────────────────────

def json_extraction_prompt(text: str, quality: str, examples: list) -> str:
    example_block = _build_example_block(examples, quality, "json_extraction")

    if quality == "high":
        return f"""You are a precise information extraction system. Your task is to parse unstructured natural language text and extract structured data as valid JSON.

Rules:
- Output ONLY a valid JSON object. No explanation, no markdown, no extra text.
- Use lowercase keys with underscores (snake_case).
- Infer numeric types where applicable (e.g., age should be an integer, not a string).
- If a field is not present in the text, omit it from the JSON.

{example_block}

Now extract structured JSON from the following text:
\"{text}\""""

    elif quality == "medium":
        return f"""You are a helpful assistant. Extract information from the text below and return it as JSON.

{example_block}

Text: \"{text}\"
JSON:"""

    else:  # low
        return f"""Extract info from this text as JSON.

{example_block}

{text}"""


# ─── MATH WORD PROBLEMS ───────────────────────────────────────────────────────

def math_problem_prompt(problem: str, quality: str, examples: list) -> str:
    example_block = _build_example_block(examples, quality, "math_word_problems")

    if quality == "high":
        return f"""You are a mathematics tutor with expertise in arithmetic, algebra, and word problems. Solve the following math problem step by step, then provide the final numerical answer.

Instructions:
- Show each calculation step clearly.
- Label each step (Step 1, Step 2, etc.).
- End with: "Final Answer: <number>" on its own line.
- Do not include units in the final answer unless the problem explicitly requires them.

{example_block}

Problem: {problem}"""

    elif quality == "medium":
        return f"""Solve this math problem. Show your work and give the final answer.

{example_block}

Problem: {problem}
Answer:"""

    else:  # low
        return f"""Solve this:

{example_block}

{problem}"""


# ─── SQL GENERATION ───────────────────────────────────────────────────────────

def sql_generation_prompt(request: str, quality: str, examples: list) -> str:
    example_block = _build_example_block(examples, quality, "sql_generation")

    if quality == "high":
        return f"""You are a senior SQL developer with deep knowledge of relational databases. Convert the natural language request below into a correct and efficient SQL query.

Requirements:
- Use standard SQL syntax (compatible with MySQL/PostgreSQL).
- Write the query using proper capitalization for SQL keywords (SELECT, FROM, WHERE, etc.).
- Use aliases where helpful for readability.
- Output ONLY the SQL query. No explanation, no markdown code blocks.
- If a JOIN is needed, use explicit JOIN syntax (not implicit comma joins).

{example_block}

Request: {request}
SQL:"""

    elif quality == "medium":
        return f"""Convert this to SQL. Return only the query.

{example_block}

Request: {request}
SQL:"""

    else:  # low
        return f"""Write SQL for this:

{example_block}

{request}"""


# ─── CODE DEBUGGING ───────────────────────────────────────────────────────────

def code_debug_prompt(code: str, quality: str, examples: list) -> str:
    example_block = _build_example_block(examples, quality, "code_debugging")

    if quality == "high":
        return f"""You are an expert Python developer and code reviewer. Analyze the following Python code for bugs, logical errors, edge case failures, and performance issues.

Instructions:
- Identify every bug present in the code.
- Explain why each bug is a problem.
- Provide the corrected version of the code.
- Format your response as:
  BUG: <description of the bug>
  FIX: <corrected code or line>

{example_block}

Code to debug:
```python
{code}
```"""

    elif quality == "medium":
        return f"""Find bugs in this Python code and fix them.

{example_block}

Code:
{code}

Bugs and fixes:"""

    else:  # low
        return f"""Fix this code:

{example_block}

{code}"""


# ─── TEXT SUMMARIZATION ───────────────────────────────────────────────────────

def summarization_prompt(text: str, quality: str, examples: list) -> str:
    example_block = _build_example_block(examples, quality, "text_summarization")

    if quality == "high":
        return f"""You are a professional editor skilled at distilling complex information into clear, concise summaries. Summarize the passage below.

Requirements:
- Write exactly 2-3 sentences.
- Retain all key facts, figures, and named entities.
- Use neutral, factual language. Avoid subjective terms.
- Do not add information not present in the original text.

{example_block}

Passage:
\"{text}\"

Summary:"""

    elif quality == "medium":
        return f"""Summarize the following text in 2-3 sentences.

{example_block}

Text: \"{text}\"
Summary:"""

    else:  # low
        return f"""Summarize this:

{example_block}

{text}"""


# ─── EXAMPLE BLOCK BUILDER ────────────────────────────────────────────────────

def _build_example_block(examples: list, quality: str, domain: str) -> str:
    """
    Build the few-shot example block.
    HIGH quality: well-formatted, labeled, clear separation.
    MEDIUM quality: labeled but minimal formatting.
    LOW quality: raw, no labels, no separation.
    """
    if not examples:
        return ""

    lines = []

    if quality == "high":
        lines.append("Examples:")
        for i, ex in enumerate(examples, 1):
            lines.append(f"\nExample {i}:")
            lines.append(f"  Input: {ex['input']}")
            lines.append(f"  Output: {ex['output']}")
        lines.append("")

    elif quality == "medium":
        lines.append("Examples:")
        for ex in examples:
            lines.append(f"Input: {ex['input']}")
            lines.append(f"Output: {ex['output']}")
        lines.append("")

    else:  # low — noisy, random order, no clear labels
        for ex in examples:
            lines.append(ex['input'])
            lines.append(str(ex['output']))

    return "\n".join(lines)


# ─── MASTER DISPATCHER ────────────────────────────────────────────────────────

PROMPT_BUILDERS = {
    "json_extraction": json_extraction_prompt,
    "math_word_problems": math_problem_prompt,
    "sql_generation": sql_generation_prompt,
    "code_debugging": code_debug_prompt,
    "text_summarization": summarization_prompt,
}

def build_prompt(domain: str, input_text: str, quality: str, examples: list) -> str:
    builder = PROMPT_BUILDERS[domain]
    return builder(input_text, quality, examples)
