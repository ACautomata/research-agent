#!/usr/bin/env python3
"""benchmarks/paper-review/metrics.py — always invokes `main`; main spawns
`paper-review` per QA. To regenerate qa.jsonl from the existing seed_qa.json:
  python3 benchmarks/paper-review/build_qa.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_common"))
from run_bench import main  # noqa: E402

BENCH_NAME = "paper-review"


if __name__ == "__main__":
    sys.exit(main(BENCH_NAME, agent_id="main"))
