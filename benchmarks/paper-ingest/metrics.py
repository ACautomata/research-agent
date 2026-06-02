#!/usr/bin/env python3
"""benchmarks/paper-ingest/metrics.py — main-only. QAs carry
`target_agent: autoresearch` so main spawns that sub-agent."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_common"))
from run_bench import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main("paper-ingest", agent_id="main"))
