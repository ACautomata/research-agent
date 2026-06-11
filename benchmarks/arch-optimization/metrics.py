#!/usr/bin/env python3
"""benchmarks/arch-optimization/metrics.py — optimizer agent test."""
import sys
from pathlib import Path

BENCH_NAME = "arch-optimization"

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_common"))
    from run_bench import main
    sys.exit(main(BENCH_NAME, agent_id="main"))
