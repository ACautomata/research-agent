#!/usr/bin/env python3
"""
Step 1: Prepare benchmark prompts and generate the master runner script.
Step 2: PowerShell runs the master script to collect raw agent outputs.
Step 3: Python scores and generates report.

Usage:
  python bench_prepare.py                    # Step 1
  powershell -File .bench-temp\run_all.ps1   # Step 2
  python bench_score.py                      # Step 3
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(r"D:\Code\= =\research-agent")
BENCH_NAME = "idea-generate"
QA_PATH = REPO_ROOT / "benchmarks" / BENCH_NAME / "qa.jsonl"
TEMP_DIR = REPO_ROOT / "benchmarks" / BENCH_NAME / ".bench-temp"
MODEL = os.environ.get("BENCH_MODEL") or "deepseek/deepseek-v4-flash"


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
            f"[BENCHMARK DIRECTIVE]\n"
            f"This task must be executed by the `{target}` sub-agent.\n"
            f"Use sessions_spawn(agentId=\"{target}\", task=<the full task below>, "
            f"mode=\"run\", context=\"isolated\", "
            f"runTimeoutSeconds={qa.get('timeout_seconds', 1800)}). "
            f"After spawning, call sessions_yield and wait. "
            f"Then run the reviewer agent. "
            f"If reviewer returns FAIL, sessions_send the fix prompt back to the SAME session and rerun reviewer. "
            f"Return the reviewer-passed final reply.\n"
            f"Do NOT solve the task yourself.\n\n"
            f"GOLD_ANSWER: {json.dumps(qa.get('gold_answer'), ensure_ascii=False)}\n"
            f"RUBRIC: {qa.get('rubric') or '(none)'}\n"
            f"EXPECTED_ARTIFACTS: {json.dumps(qa.get('expected_artifacts'), ensure_ascii=False)}\n\n"
            f"---\n\n{prompt}"
        )
    return prompt


def main():
    max_qas_env = os.environ.get("MAX_QAS", "")
    max_qas = int(max_qas_env) if max_qas_env.strip() else None

    lines = QA_PATH.read_text(encoding="utf-8").splitlines()
    qas = []
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        qa = json.loads(line)
        qa.setdefault("qa_id", f"qa-{i:03d}")
        qa.setdefault("timeout_seconds", 1800)
        qas.append(qa)

    if max_qas:
        qas = qas[:max_qas]

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    run_id = f"local-{int(time.time())}"

    # Write prompt files + build runner script lines
    runner_lines = []
    meta_list = []

    for qa in qas:
        qa_id = qa["qa_id"]
        prompt = build_prompt(qa)
        prompt_file = TEMP_DIR / f"prompt_{qa_id}.txt"
        prompt_file.write_text(prompt, encoding="utf-8")

        meta = {
            "qa_id": qa_id,
            "task_type": qa.get("task_type", ""),
            "judge": qa.get("judge", "rules"),
            "weight": qa.get("weight", 1.0),
            "pass_threshold": qa.get("pass_threshold", 0.5),
            "timeout": qa.get("timeout_seconds", 1800),
            "target_agent": qa.get("target_agent"),
            "gold_answer": qa.get("gold_answer"),
            "rubric": qa.get("rubric", ""),
        }
        meta_list.append(meta)

        # Each runner line: call openclaw and save stdout to a file
        prompt_file_ps = str(prompt_file).replace("'", "''")
        out_file = str(TEMP_DIR / f"output_{qa_id}.jsonl").replace("'", "''")
        session_key = f"agent:main:bench-{run_id}-{qa_id}"

        runner_lines.append(
            f'Write-Progress -Activity "Benchmark $qa_id" -Status "$qa_id" -PercentComplete -1\n'
            f'$t0 = Get-Date\n'
            f'openclaw agent --agent main --message (Get-Content \'{prompt_file_ps}\' -Raw -Encoding UTF8) '
            f'--json --local --session-key \'{session_key}\' --timeout {meta["timeout"]} --model {MODEL} '
            f'2>$null | Out-File -FilePath \'{out_file}\' -Encoding UTF8\n'
            f'$t1 = Get-Date\n'
            f'$elapsed = ($t1 - $t0).TotalSeconds\n'
            f'$size = (Get-Item \'{out_file}\').Length\n'
            f'Write-Output "[$qa_id] took $elapsed s, $size bytes written to output"'
        )

    # Write the master runner script
    ps1_content = '\n'.join([
        'param()',
        '$base = "' + str(TEMP_DIR).replace("'", "''") + '"',
        '',
        '# Run each QA sequentially',
        *[f"$qa_id = '{m['qa_id']}'; " + line for m, line in zip(meta_list, runner_lines)],
        '',
        'Write-Output "=== ALL DONE ==="',
    ])

    ps1_path = TEMP_DIR / "run_all.ps1"
    ps1_path.write_text(ps1_content, encoding="utf-8")

    # Write index
    index = {
        "run_id": run_id,
        "model": MODEL,
        "base": str(TEMP_DIR),
        "total_qas": len(meta_list),
        "qas": meta_list,
    }
    index_file = TEMP_DIR / "bench_run_index.json"
    index_file.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"=== Benchmark Prep: {BENCH_NAME} ===")
    print(f"  Run ID:    {run_id}")
    print(f"  Model:     {MODEL}")
    print(f"  QAs:       {len(meta_list)}")
    print(f"  Temp dir:  {TEMP_DIR}")
    print(f"  Runner:    {ps1_path}")
    print()
    print("  To run:")
    print(f'    powershell -ExecutionPolicy Bypass -File "{ps1_path}"')
    print()
    print("  Then score:")
    print("    python bench_score.py")

    # Also tell the user what to do next
    print()
    print(f"BENCH_INDEX={index_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
