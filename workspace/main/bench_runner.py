#!/usr/bin/env python3
"""
Local benchmark runner for idea-generate.

Directly calls idea-generate agent, then runs reviewer for scoring.
Bypasses main agent orchestration (sessions_yield CLI issue).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

REPO_ROOT = Path(r"D:\Code\= =\research-agent")
BENCH_NAME = "idea-generate"
QA_PATH = REPO_ROOT / "benchmarks" / BENCH_NAME / "qa.jsonl"
COMMON_DIR = REPO_ROOT / "benchmarks" / "_common"
RESULTS_DIR = REPO_ROOT / "bench-results"
REPORT_PATH = REPO_ROOT / "benchmarks" / BENCH_NAME / "bench-report.json"

sys.path.insert(0, str(COMMON_DIR))
from judge import judge_with_agent, judge_with_rules

MODEL = os.environ.get("BENCH_MODEL") or "deepseek/deepseek-v4-flash"
NODE_EXE = r"C:\Program Files\nodejs\node.exe"
APPDATA = os.environ.get("APPDATA", "")
OPENCLAW_MJS = os.path.join(APPDATA, "npm", "node_modules", "openclaw", "openclaw.mjs")


def call_agent(agent_id: str, prompt: str, timeout_seconds: int) -> str:
    """Call an OpenClaw agent via direct node and return the text response."""
    session_key = f"agent:{agent_id}:bench-{time.time()}-{uuid.uuid4().hex[:8]}"
    args = [
        NODE_EXE, OPENCLAW_MJS,
        "agent",
        "--agent", agent_id,
        "--message", prompt,
        "--json", "--local",
        "--session-key", session_key,
        "--timeout", str(timeout_seconds),
        "--model", MODEL,
    ]
    try:
        proc = subprocess.run(args, capture_output=True, timeout=timeout_seconds + 60)
    except subprocess.TimeoutExpired:
        return "(timeout)"

    # Parse stdout JSON
    stdout = proc.stdout.decode("utf-8", errors="replace")
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        payloads = data.get("payloads", [])
        if payloads:
            texts = [p.get("text", "") for p in payloads if isinstance(p, dict)]
            if texts:
                return texts[0]

    # Fallback: finalAssistantVisibleText
    import re
    m = re.search(r'"finalAssistantVisibleText"\s*:\s*"((?:[^"\\]|\\.)*)"', stdout)
    if m:
        return m.group(1)
    return f"(parse failed: {stdout[:200]})"


def main():
    run_id = f"local-{int(time.time())}"
    max_qas_env = os.environ.get("MAX_QAS", "")
    max_qas = int(max_qas_env) if max_qas_env.strip() else None
    skip_env = os.environ.get("SKIP_QAS", "")
    skip_set = set(skip_env.split(",")) if skip_env.strip() else set()

    lines = QA_PATH.read_text(encoding="utf-8").splitlines()
    qas = []
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        qa = json.loads(line)
        qa.setdefault("qa_id", f"qa-{i:03d}")
        qa.setdefault("timeout_seconds", 600)
        qa.setdefault("weight", 1.0)
        qa.setdefault("pass_threshold", 0.5)
        qa.setdefault("judge", "rules")
        qas.append(qa)

    if max_qas:
        qas = qas[:max_qas]

    print(f"[{BENCH_NAME}] Model: {MODEL}, QAs: {len(qas)}")
    print()

    results = []
    for idx, qa in enumerate(qas, 1):
        qa_id = qa["qa_id"]
        if qa_id in skip_set:
            continue

        task_type = qa.get("task_type", "?")
        jmode = qa.get("judge", "rules")
        timeout = qa.get("timeout_seconds", 600)

        # Build prompt for idea-generate (omit BENCHMARK DIRECTIVE)
        prompt = qa["question"]
        if qa.get("input_material"):
            material = qa["input_material"]
            if isinstance(material, dict):
                mc = material.get("content")
                if mc: material = mc
                else: material = Path(material["path"]).read_text(encoding="utf-8")
            prompt = f"{material}\n\n---\n\n{prompt}"

        print(f"[{idx}/{len(qas)}] {qa_id} ({task_type}) ...", end=" ", flush=True)
        t0 = time.time()

        # Step 1: Call idea-generate
        answer = call_agent("idea-generate", prompt, timeout)
        elapsed = time.time() - t0

        # Step 2: Score
        if answer.startswith("(timeout") or answer.startswith("(parse failed"):
            score = 0.0
            passed = False
            rationale = answer
        else:
            qa_for_judge = {
                "qa_id": qa_id, "question": prompt,
                "gold_answer": qa.get("gold_answer"),
                "rubric": qa.get("rubric", ""),
                "pass_threshold": qa.get("pass_threshold", 0.5),
                "judge": jmode, "weight": qa.get("weight", 1.0),
            }
            if jmode == "agent":
                verdict = judge_with_agent(qa_for_judge, answer, agent_id="reviewer", model=MODEL)
            else:
                verdict = judge_with_rules(answer, qa_for_judge)
            score = verdict.get("score", 0.0)
            passed = verdict.get("pass", False)
            rationale = verdict.get("rationale", "")

        print(f"score={score:.3f} pass={passed} {elapsed:.0f}s")

        results.append({
            "qa_id": qa_id, "task_type": task_type,
            "target_agent": "idea-generate",
            "weight": qa.get("weight", 1.0),
            "score": round(score, 4), "pass": passed,
            "rationale": rationale,
            "elapsed_seconds": round(elapsed, 1),
            "raw_output": (answer or "")[:3000],
        })

    weight_total = sum(r["weight"] for r in results) or 1.0
    weighted_score = sum(r["score"] * r["weight"] for r in results) / weight_total
    passed_count = sum(1 for r in results if r["pass"])

    report = {
        "benchmark": BENCH_NAME, "agent": "idea-generate",
        "run_id": run_id, "model": MODEL,
        "total": len(results), "passed": passed_count,
        "pass_rate": round(passed_count / len(results), 4) if results else 0.0,
        "avg_score": round(weighted_score, 4),
        "results": results,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / f"{BENCH_NAME}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print()
    print("=" * 60)
    print(f"[{BENCH_NAME}] RESULTS")
    print(f"  Total:     {len(results)}")
    print(f"  Passed:    {passed_count}")
    print(f"  Pass rate: {passed_count/len(results):.1%}" if results else "  N/A")
    print(f"  Avg score: {weighted_score:.4f}")
    print(f"  Report:    {REPORT_PATH}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
