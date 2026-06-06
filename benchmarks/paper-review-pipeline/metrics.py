#!/usr/bin/env python3
"""benchmarks/paper-review-pipeline/metrics.py — main-only."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_common"))
from run_bench import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main("paper-review-pipeline", agent_id="main"))
