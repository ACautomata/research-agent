#!/usr/bin/env python3
"""benchmarks/paper-review/metrics.py — always invokes `main`; main spawns
`paper-review` per QA. If the wiki import failed during env.sh setup, the
benchmark scores 0 without running any QA.
To regenerate qa.jsonl from the existing seed_qa.json:
  python3 benchmarks/paper-review/build_qa.py
"""
import json
import os
import sys
from pathlib import Path

BENCH_NAME = "paper-review"


def _emit_zero_report(reason: str) -> int:
    """Emit a 0-score bench-report.json and return 0."""
    report_path = Path(os.environ.get("BENCH_REPORT_PATH",
                           Path(__file__).resolve().parent / "bench-report.json"))
    report = {
        "benchmark": BENCH_NAME,
        "agent": "main",
        "run_id": os.environ.get("BENCH_RUN_ID", "unknown"),
        "model": os.environ.get("BENCH_MODEL", "default"),
        "total": 0, "passed": 0, "pass_rate": 0.0, "avg_score": 0.0,
        "results": [],
        "skipped": reason,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    # Also write to bench-results so the PR comment picks it up.
    results_dir = Path(os.environ.get("BENCH_RESULTS_DIR",
                          Path(__file__).resolve().parent.parent.parent / "bench-results"))
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / f"{BENCH_NAME}.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[{BENCH_NAME}] SKIPPED: {reason}, scoring 0")
    return 0


if __name__ == "__main__":
    # If the wiki import failed during env.sh, short-circuit to 0.
    marker = Path(__file__).resolve().parent / ".wiki-import-failed"
    if marker.exists():
        sys.exit(_emit_zero_report("wiki import failed during env.sh setup"))

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_common"))
    from run_bench import main  # noqa: E402

    sys.exit(main(BENCH_NAME, agent_id="main"))
