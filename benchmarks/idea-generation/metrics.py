#!/usr/bin/env python3
"""benchmarks/idea-generation/metrics.py — main-only. QAs target `idea-generate`."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_common"))
from run_bench import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main("idea-generation", agent_id="main"))