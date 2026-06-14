#!/usr/bin/env python3
"""Local benchmark runner for idea-generate.

Mirrors the Docker CI pipeline but uses the local OpenClaw CLI.
Handles long prompts by writing temp script files.
"""
from __future__ import annotations

import json
import os
import re
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
TEMP_DIR = REPO_ROOT / "benchmarks" / BENCH_NAME / ".bench-temp"

sys.path.insert(0, str(COMMON_DIR))
from judge import judge_with_agent, judge_with_rules  # noqa: E402

MODEL_OVERRIDE = os.environ.get("BENCH_MODEL") or "deepseek/deepseek-v4-flash"

_NOISE_PREFIXES = (
    "[diagnostic]", "[context-engine]", "[gateway]", "[plugins]", "[secrets]",
    "[heartbeat]", "[ws]", "[memory-core]", "[memory-wiki]", "[memory-qmd]",
    "[qmd]", "[sandbox]", "[auth]", "[lanes]", "[tools]", "[model-fallback",
    "[model-errors]", "[secrets-ref]", "[secrets-store]", "[secrets-warning]",
    "[fallback]", "[init]", "[post-init]", "[config]", "[bridge]", "[obsidian]",
    "[vault]", "[wiki]", "[router]", "[worker]", "[spawn]", "[retry]", "[loop]",
    "Config health-state write failed", "=== ",
    "初始化", "配置", "启动", "挂载", "检测", "??",
    "已", "正在", "整体", "上下文", "最大", "API", "Base", "Gateway",
    "沙箱", "插件", "允许", "当前", "目标", "开放",
)
_BRACKET_TAG_RE = re.compile(r"^\s*\[(?P<tag>[a-zA-Z0-9_.-]+)\]\s*(?P<rest>.*)$")
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _strip_diagnostics(text: str) -> str:
    cleaned: list[str] = []
    for line in text.splitlines():
        stripped = _ANSI_RE.sub("", line).strip()
        if not stripped:
            continue
        if any(stripped.startswith(p) for p in _NOISE_PREFIXES):
            continue
        if _BRACKET_TAG_RE.match(stripped):
            continue
        cleaned.append(stripped)
    return "\n".join(cleaned)


def _extract_agent_text(stdout: str, stderr: str) -> str:
    if stdout.strip():
        try:
            data = json.loads(stdout)
        except json.JSONDecodeError:
            return _strip_diagnostics(stdout)
        if isinstance(data, dict):
            payloads = data.get("payloads")
            if isinstance(payloads, list) and payloads:
                texts = [p.get("text", "") for p in payloads if isinstance(p, dict)]
                joined = "\n".join(t for t in texts if t)
                if joined.strip():
                    return _strip_diagnostics(joined)
            result = data.get("result")
            if isinstance(result, dict):
                payloads = result.get("payloads")
                if isinstance(payloads, list) and payloads:
                    texts = [p.get("text", "") for p in payloads if isinstance(p, dict)]
                    joined = "\n".join(t for t in texts if t)
                    if joined.strip():
                        return _strip_diagnostics(joined)
    cleaned = _strip_diagnostics(stderr)
    if not cleaned.strip():
        return "(no agent response)"
    return cleaned


def load_qa(path: Path) -> list[dict]:
    qas: list[dict] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        qa = json.loads(line)
        qa.setdefault("qa_id", f"qa-{i:03d}")
        qa.setdefault("agent", "main")
        qa.setdefault("pass_threshold", 0.5)
        qa.setdefault("weight", 1.0)
        qa.setdefault("judge", "rules")
        qas.append(qa)
    return qas


def build_prompt(qa: dict) -> str:
    prompt = qa["question"]
    if qa.get("input_material"):
        material = qa["input_material"]
        if isinstance(material, dict):
            mc = material.get("content")
            if mc:
                material = mc
            else:
                material = Path(material["path"]).read_text(encoding="utf-8")
        prompt = f"{material}\n\n---\n\n{prompt}"

    target = qa.get("target_agent")
    if target and target != "main":
        prompt = (
            f"[BENCHMARK DIRECTIVE — read carefully]\n"
            f"This task must be executed by the `{target}` sub-agent.\n"
            f"Use the sessions_spawn tool to delegate:\n"
            f"  sessions_spawn(agentId=\"{target}\", task=<the full task below>, "
            f"mode=\"run\", context=\"isolated\", "
            f"runTimeoutSeconds={qa.get('timeout_seconds', 1800)})\n"
            f"sessions_spawn is non-blocking. After spawning, call "
            f"sessions_yield if it is available, and wait for the "
            f"sub-agent completion message before answering.\n"
            f"After the sub-agent completes, run the `reviewer` agent to audit "
            f"the sub-agent's final reply against this benchmark directive, the "
            f"full task, expected artifacts, gold_answer, and rubric below. "
            f"If reviewer returns FAIL, use sessions_send(sessionKey=<same sessionKey>, "
            f"message=<reviewer fix prompt>) to send its fix prompt back to the SAME "
            f"sub-agent session and wait for the repaired answer, then run "
            f"reviewer again. Do not start a new `{target}` session for fixes. "
            f"Skip this extra review loop only when the target sub-agent itself "
            f"is `reviewer`.\n"
            f"Then return the reviewer-passed sub-agent final reply as your only output.\n"
            f"Do NOT return a runId, pending status, or 'wait for completion' "
            f"message.\n"
            f"Do NOT solve the task yourself. Do NOT add commentary. Return the "
            f"sub-agent's reply verbatim after it has passed reviewer.\n\n"
            f"BENCHMARK GOLD_ANSWER: {json.dumps(qa.get('gold_answer'), ensure_ascii=False)}\n"
            f"BENCHMARK RUBRIC: {qa.get('rubric') or '(none)'}\n"
            f"BENCHMARK EXPECTED_ARTIFACTS: {json.dumps(qa.get('expected_artifacts'), ensure_ascii=False)}\n\n"
            f"---\n\n{prompt}"
        )
    return prompt


def run_agent(qa: dict, run_id: str) -> tuple[str, str]:
    prompt = build_prompt(qa)
    session_key = f"agent:main:bench-{run_id}-{qa['qa_id']}-{uuid.uuid4().hex}"
    timeout = qa.get("timeout_seconds", 1800)

    # Write prompt to temp file to avoid PowerShell quoting issues
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    prompt_file = TEMP_DIR / f"prompt_{qa['qa_id']}.txt"
    prompt_file.write_text(prompt, encoding="utf-8")

    # Write wrapper .ps1 script that reads prompt from file
    ps1_file = TEMP_DIR / f"run_{qa['qa_id']}.ps1"
    ps1_content = (
        "$prompt = Get-Content " + repr(str(prompt_file)) + " -Raw -Encoding UTF8\n"
        "openclaw agent --agent main --message $prompt "
        "--json --local "
        "--session-key " + session_key + " "
        "--timeout " + str(timeout) + " "
        + (("--model " + MODEL_OVERRIDE) if MODEL_OVERRIDE else "")
    )
    ps1_file.write_text(ps1_content, encoding="utf-8")

    cmd = [
        "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
        "-File", str(ps1_file)
    ]

    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, encoding='utf-8',
            timeout=timeout + 120,
            env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
        )
    except subprocess.TimeoutExpired:
        return ("(timeout)", session_key)
    except UnicodeDecodeError as e:
        return (f"(encoding error: {e})", session_key)

    return (_extract_agent_text(proc.stdout or "", proc.stderr or ""), session_key)


def judge_answer(answer: str, qa: dict) -> dict:
    mode = qa.get("judge", "rules")
    if mode == "agent":
        return judge_with_agent(
            qa, answer, agent_id="reviewer", model=MODEL_OVERRIDE,
        )
    else:
        return judge_with_rules(answer, qa)


def main():
    run_id = os.environ.get("BENCH_RUN_ID") or f"local-{int(time.time())}"
    max_qas_env = os.environ.get("MAX_QAS", "")
    max_qas = int(max_qas_env) if max_qas_env.strip() else None

    qas = load_qa(QA_PATH)
    total = len(qas)

    if max_qas:
        qas = qas[:max_qas]
        print(f"[{BENCH_NAME}] TEST MODE: first {max_qas} QAs only\n")

    print(f"[{BENCH_NAME}] Loading {total} QAs from {QA_PATH}")
    print(f"[{BENCH_NAME}] Model: {MODEL_OVERRIDE}")
    print()

    results: list[dict] = []

    for idx, qa in enumerate(qas, 1):
        qa_id = qa["qa_id"]
        task_type = qa.get("task_type", "?")
        judge_mode = qa.get("judge", "rules")
        print(f"[{idx}/{total}] {qa_id} ({task_type}, judge={judge_mode}) ...", end=" ", flush=True)

        t0 = time.time()
        answer, session_key = run_agent(qa, run_id)
        elapsed = time.time() - t0

        verdict = judge_answer(answer, qa)
        score = verdict.get("score", 0.0)
        passed = verdict.get("pass", False)
        rationale = verdict.get("rationale", "")

        head = (answer or "").replace("\n", "\\n")[:120]
        print(f"score={score:.3f} pass={passed} elapsed={elapsed:.0f}s head={head!r}")

        results.append({
            "qa_id": qa_id,
            "task_type": task_type,
            "target_agent": qa.get("target_agent"),
            "weight": qa.get("weight", 1.0),
            "score": round(score, 4),
            "pass": passed,
            "rationale": rationale,
            "elapsed_seconds": round(elapsed, 1),
            "session_key": session_key,
            "raw_output": (answer or "")[:2000],
        })

    weight_total = sum(r["weight"] for r in results) or 1.0
    weighted_score = sum(r["score"] * r["weight"] for r in results) / weight_total
    passed_count = sum(1 for r in results if r["pass"])

    report = {
        "benchmark": BENCH_NAME,
        "agent": "main",
        "run_id": run_id,
        "model": MODEL_OVERRIDE or "default",
        "total": total,
        "passed": passed_count,
        "pass_rate": round(passed_count / total, 4) if total else 0.0,
        "avg_score": round(weighted_score, 4),
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
    print(f"[{BENCH_NAME}] RESULTS")
    print(f"  Total ({'partial' if max_qas else 'full'}): {len(results)}")
    print(f"  Passed:    {passed_count}")
    print(f"  Pass rate: {passed_count/len(results):.1%}")
    print(f"  Avg score: {weighted_score:.4f}")
    print(f"  Report:    {REPORT_PATH}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
