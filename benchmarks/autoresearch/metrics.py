#!/usr/bin/env python3
"""benchmarks/autoresearch/metrics.py — main-only. QAs target `autoresearch`."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_common"))
from run_bench import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main("autoresearch", agent_id="main"))