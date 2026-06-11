#!/usr/bin/env python3
"""benchmarks/spec-generation/metrics.py — invokes `main`; main must delegate to
`judge` per QA for scoring. This benchmark scores spec agent's ability
to generate correct claude-code task prompts.
To regenerate qa.jsonl from the existing seed_qa.json:
  python3 benchmarks/spec-generation/build_qa.py
"""
import sys
from pathlib import Path

BENCH_NAME = "spec-generation"


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_common"))
    from run_bench import main  # noqa: E402

    sys.exit(main(BENCH_NAME, agent_id="main"))
