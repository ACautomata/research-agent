#!/usr/bin/env python3
"""benchmarks/idea-generate/metrics.py

CI policy: always invokes the `main` agent. Each QA's `target_agent` field
names the sub-agent main should spawn. For idea-generate the target is
`idea-generate` itself.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_common"))
from run_bench import main  # noqa: E402

BENCH_NAME = "idea-generate"


if __name__ == "__main__":
    sys.exit(main(BENCH_NAME, agent_id="main"))
