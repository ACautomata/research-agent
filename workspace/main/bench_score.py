#!/usr/bin/env python3
"""Step 3: Score the benchmark outputs.
Reads .bench-temp/output_*.jsonl files + index, produces bench-report.json.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(r"D:\Code\= =\research-agent")
BENCH_NAME = "idea-generate"
COMMON_DIR = REPO_ROOT / "benchmarks" / "_common"
RESULTS_DIR = REPO_ROOT / "bench-results"
REPORT_PATH = REPO_ROOT / "benchmarks" / BENCH_NAME / "bench-report.json"
TEMP_DIR = REPO_ROOT / "benchmarks" / BENCH_NAME / ".bench-temp"

sys.path.insert(0, str(COMMON_DIR))
from judge import judge_with_agent, judge_with_rules


def extract_answer_from_file(path: Path) -> str:
    """Read the openclaw JSON output and extract the agent reply text."""
    if not path.exists():
        return "(no output file)"
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return "(unreadable)"
    
    # Try to find the JSON payload
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                data = json.loads(line)
                payloads = data.get("payloads", [])
                if payloads:
                    texts = [p.get("text", "") for p in payloads if isinstance(p, dict)]
                    if texts:
                        return texts[0]
            except json.JSONDecodeError:
                continue
    
    # Fallback: try to find "finalAssistantVisibleText"
    import re
    m = re.search(r'"finalAssistantVisibleText"\s*:\s*"([^"]*)"', text)
    if m:
        return m.group(1)
    
    return "(parse failed)"


def main():
    index_file = TEMP_DIR / "bench_run_index.json"
    if not index_file.exists():
        print(f"ERROR: index file not found: {index_file}")
        return 1

    index = json.loads(index_file.read_text(encoding="utf-8"))
    run_id = index["run_id"]
    model = index["model"]
    qas_meta = index["qas"]

    results = []
    error_count = 0

    for qa_meta in qas_meta:
        qa_id = qa_meta["qa_id"]
        output_file = TEMP_DIR / f"output_{qa_id}.jsonl"

        answer = extract_answer_from_file(output_file)

        # Check for error indicators
        if answer in ("(no output file)", "(unreadable)", "(parse failed)"):
            print(f"  [{qa_id}] ERROR: {answer}")
            error_count += 1
            results.append({
                "qa_id": qa_id,
                "task_type": qa_meta.get("task_type"),
                "target_agent": qa_meta.get("target_agent"),
                "weight": qa_meta.get("weight", 1.0),
                "score": 0.0,
                "pass": False,
                "rationale": answer,
                "elapsed_seconds": 0,
                "session_key": "",
                "raw_output": answer,
            })
            continue

        qa_for_judge = {
            "qa_id": qa_id,
            "question": "",
            "gold_answer": qa_meta.get("gold_answer"),
            "rubric": qa_meta.get("rubric", ""),
            "pass_threshold": qa_meta.get("pass_threshold", 0.5),
            "judge": qa_meta.get("judge", "rules"),
            "weight": qa_meta.get("weight", 1.0),
        }

        judge_mode = qa_meta.get("judge", "rules")
        if judge_mode == "agent":
            verdict = judge_with_agent(
                qa_for_judge, answer,
                agent_id="reviewer",
                model=model,
            )
        else:
            verdict = judge_with_rules(answer, qa_for_judge)

        score = verdict.get("score", 0.0)
        passed = verdict.get("pass", False)

        print(f"  [{qa_id}] score={score:.3f} pass={passed}")

        results.append({
            "qa_id": qa_id,
            "task_type": qa_meta.get("task_type"),
            "target_agent": qa_meta.get("target_agent"),
            "weight": qa_meta.get("weight", 1.0),
            "score": round(score, 4),
            "pass": passed,
            "rationale": verdict.get("rationale", ""),
            "session_key": "",
            "raw_output": (answer or "")[:2000],
        })

    if results:
        weight_total = sum(r["weight"] for r in results) or 1.0
        weighted_score = sum(r["score"] * r["weight"] for r in results) / weight_total
        passed_count = sum(1 for r in results if r["pass"])
    else:
        weighted_score = 0.0
        passed_count = 0

    report = {
        "benchmark": BENCH_NAME,
        "agent": "main",
        "run_id": run_id,
        "model": model,
        "total": len(results),
        "passed": passed_count,
        "pass_rate": round(passed_count / len(results), 4) if results else 0.0,
        "avg_score": round(weighted_score, 4),
        "errors": error_count,
        "results": results,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / f"{BENCH_NAME}.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print()
    print("=" * 60)
    print(f"[score] {BENCH_NAME} RESULTS")
    print(f"  Total:     {len(results)}")
    if error_count:
        print(f"  Errors:    {error_count}")
    print(f"  Passed:    {passed_count}")
    print(f"  Pass rate: {passed_count/len(results):.1%}" if results else "  Pass rate: N/A")
    print(f"  Avg score: {weighted_score:.4f}")
    print(f"  Report:    {REPORT_PATH}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
