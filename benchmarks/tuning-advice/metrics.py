#!/usr/bin/env python3
"""benchmarks/tuning-advice/metrics.py — invokes `main`; main delegates to
tuning agent via orchestrate for scoring.
"""
import sys
from pathlib import Path

BENCH_NAME = "tuning-advice"

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_common"))
    from run_bench import main  # noqa: E402
    sys.exit(main(BENCH_NAME, agent_id="main"))
