"""
Entry point.
Usage:
  python main.py run              # runs all 600 calls
  python main.py run 1 5          # runs cells 1-5 (50 calls)
  python main.py analyze          # analyzes saved results
  python main.py all              # run all then analyze
"""

import sys
import os


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"

    if cmd in ("run", "all"):
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            print("[ERROR] Set OPENAI_API_KEY environment variable before running.")
            print("  export OPENAI_API_KEY=your_key_here")
            sys.exit(1)

        import src.config as cfg
        cfg.OPENAI_API_KEY = api_key

        from src.experiment import run_experiment
        run_experiment()

    if cmd in ("analyze", "all"):
        from src.analyze import run_analysis
        run_analysis()


if __name__ == "__main__":
    main()
