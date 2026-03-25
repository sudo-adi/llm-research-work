import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
MODEL_NAME = "gpt-4o-mini"

# Domains we test across
DOMAINS = ["json_extraction", "code_debugging", "math_word_problems", "text_summarization", "sql_generation"]

# Few-shot counts to test
SHOT_COUNTS = [1, 3, 5, 10]

# Example quality levels
QUALITY_LEVELS = ["high", "medium", "low"]

# How many test cases per cell in the grid
TEST_CASES_PER_CELL = 10

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
