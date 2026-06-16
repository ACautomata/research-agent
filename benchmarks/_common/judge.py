#!/usr/bin/env python3
"""Reusable scoring for benchmark metrics.py scripts.

Two scoring entry points:
  judge_with_rules(answer, qa)            -- rule-based (qa.gold_answer / must_contain).
  judge_parse(judge_text, qa, candidate)  -- parse a 0..1 score produced by the
                                             dedicated `judge` agent (whose prompt
                                             is built by judge_prompt).

For LLM judging, run_bench.py builds the prompt with ``judge_prompt``, triggers
the ``judge`` agent, waits, reads the score out of the judge session log, and
hands the text to ``judge_parse``. ``judge_with_agent`` is kept only for the
manual ``judge.py agent ...`` CLI (a single-shot convenience).

Every function returns a dict: {score: float (0-1), pass: bool, rationale: str}.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import uuid
from typing import Any

# --- Rule-based judge --------------------------------------------------------

_KEYWORD_HINT = re.compile(r"必须[：:]\s*([^\n]+)|must_contain[：:]\s*([^\n]+)", re.I)


def _extract_must_contain(gold: Any) -> list[str]:
    """Pull a flat list of required tokens out of a gold_answer.

    Recognized shapes:
      - string: "Term1\nTerm2" (one per line) or "Term1, Term2"
      - object: {"must_contain": ["Term1", ...]} or {"fields": [...]}
    """
    if gold is None:
        return []
    if isinstance(gold, str):
        m = _KEYWORD_HINT.search(gold)
        if m:
            tail = m.group(1) or m.group(2) or ""
            return [t.strip() for t in re.split(r"[\n,，；;]", tail) if t.strip()]
        return [t.strip() for t in re.split(r"[\n,，；;]", gold) if t.strip() and len(t.strip()) > 1]
    if isinstance(gold, dict):
        out = list(gold.get("must_contain") or [])
        out += list(gold.get("fields") or [])
        return [str(t) for t in out if str(t).strip()]
    return []


def judge_with_rules(answer: str, qa: dict) -> dict:
    """Score an answer against qa.gold_answer with simple keyword coverage.

    Score = covered / required (0 if no requirements). Pass when score >= qa.pass_threshold.
    """
    required = _extract_must_contain(qa.get("gold_answer"))
    if not required:
        # No gold answer means we can only do a soft pass: not-empty + length sanity.
        text = (answer or "").strip()
        if not text:
            return {"score": 0.0, "pass": False, "rationale": "empty answer, no gold to check against"}
        score = min(1.0, len(text) / 200.0)
        return {"score": score, "pass": score >= qa.get("pass_threshold", 0.5),
                "rationale": f"no gold_answer; scored on length={len(text)}"}

    text = (answer or "").lower()
    missing = [r for r in required if r.lower() not in text]
    covered = len(required) - len(missing)
    score = covered / len(required)
    return {
        "score": round(score, 4),
        "pass": score >= qa.get("pass_threshold", 0.5),
        "rationale": f"covered {covered}/{len(required)}; missing={missing[:5]}",
        "missing": missing,
    }


# --- LLM judge: prompt + score parsing (pure) -------------------------------
#
# The benchmark flow triggers the dedicated `judge` agent, waits for it to
# finish, then reads its final assistant turn out of the judge session log.
# judge_prompt builds the (score-only) prompt; judge_parse turns the agent's
# text into a verdict. Both are pure -- no subprocess, no container -- so
# run_bench.py can reuse them without a circular import.


def judge_prompt(qa: dict, answer: str) -> str:
    """Build the score-only judge prompt for the dedicated judge agent.

    The judge agent's AGENTS.md already documents: "如 prompt 要求纯数字评分，
    输出只含 score (0 到 1 之间的数字)". We ask for exactly that so the score
    can be parsed trivially out of the session log.
    """
    rubric = qa.get("rubric") or "Score how well the answer matches the gold answer on a 0-1 scale."
    gold = qa.get("gold_answer")
    return (
        "You are the dedicated OpenClaw Judge agent: strict, fair, uncompromising. "
        "Read the QA, the reference answer, the rubric, and the candidate. "
        "Score strictly according to the rubric and required fields. "
        "Reply with ONLY a single number between 0 and 1 (the score). "
        "Do not output anything else -- no JSON, no rationale, no prose.\n\n"
        f"QA: {qa.get('question', '')}\n\n"
        f"REFERENCE: {json.dumps(gold, ensure_ascii=False) if gold else '(none)'}\n\n"
        f"RUBRIC: {rubric}\n\n"
        f"PASS_THRESHOLD: {qa.get('pass_threshold', 0.5)}\n\n"
        f"CANDIDATE:\n{(answer or '')[:8000]}\n"
    )


def _parse_judge_score(text: str) -> float | None:
    """Extract a 0..1 score from judge output.

    Handles (in order): a ``{"score": x}`` JSON fragment, a bare decimal in
    [0, 1], or any number (percent-style >1 is scaled by 0.01). Returns None if
    no number is found.
    """
    if not text:
        return None
    m = re.search(r"\{[^{}]*\"score\"[^{}]*\}", text, re.S)
    if m:
        try:
            return float(json.loads(m.group(0)).get("score"))
        except (ValueError, TypeError, json.JSONDecodeError):
            pass
    nums = re.findall(r"\d+(?:\.\d+)?", text)
    for n in nums:
        f = float(n)
        if 0.0 <= f <= 1.0:
            return f
    for n in nums:
        f = float(n)
        return f * 0.01 if f > 1 else f
    return None


def judge_parse(text: str, qa: dict, candidate: str = "") -> dict:
    """Turn the judge agent's output text into a verdict.

    Parses a 0..1 score with :func:`_parse_judge_score`; on failure, degrades to
    rule scoring against *candidate* and tags the rationale so the report can
    distinguish a real judge verdict from a degraded one.
    """
    score = _parse_judge_score(text or "")
    if score is None:
        fallback = judge_with_rules(candidate, qa)
        fallback["rationale"] = "agent judge score parse fail; " + fallback["rationale"]
        return fallback
    score = max(0.0, min(1.0, score))
    return {
        "score": round(score, 4),
        "pass": score >= qa.get("pass_threshold", 0.5),
        "rationale": f"judge score from log: {(text or '').strip()[:160]!r}",
    }


def _container_cli() -> str:
    """Return the container runtime CLI used for benchmark exec calls."""
    cli = os.environ.get("BENCH_CONTAINER_CLI") or os.environ.get("BENCH_CONTAINER_RUNTIME") or "docker"
    return "docker" if cli == "auto" else cli


# --- LLM judge ---------------------------------------------------------------


def _extract_judge_text(stdout: str) -> str:
    """Extract the judge agent text from `openclaw agent --json` stdout."""
    text = stdout or ""
    if not text.strip():
        return ""
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return text

    if isinstance(data, dict):
        if "score" in data:
            return json.dumps(data, ensure_ascii=False)
        payloads = data.get("payloads")
        if isinstance(payloads, list):
            joined = "\n".join(
                str(p.get("text", "")) for p in payloads
                if isinstance(p, dict) and p.get("text")
            )
            if joined.strip():
                return joined
        result = data.get("result")
        if isinstance(result, dict):
            payloads = result.get("payloads")
            if isinstance(payloads, list):
                joined = "\n".join(
                    str(p.get("text", "")) for p in payloads
                    if isinstance(p, dict) and p.get("text")
                )
                if joined.strip():
                    return joined
    return text


def judge_with_agent(qa: dict, answer: str, agent_id: str = "judge",
                     model: str | None = None, timeout: int = 600,
                     container: str | None = None) -> dict:
    """One-shot LLM judge for the manual ``judge.py agent`` CLI.

    Triggers the dedicated ``judge`` agent synchronously (no spawn -> no
    two-phase wait needed for this convenience path), extracts its reply, and
    parses the score. Falls back to rule scoring on timeout / CLI failure /
    parse failure, tagging the rationale so a degraded verdict is visible.

    The benchmark itself (run_bench.py) does NOT use this: it routes judging
    through the same trigger -> wait -> read-logs path as the answer QA via
    ``judge_prompt`` + ``judge_parse``.
    """
    agent_id = "judge"
    prompt = judge_prompt(qa, answer)
    session_key = f"agent:{agent_id}:bench-judge-{os.getpid()}-{uuid.uuid4().hex}"
    cmd = ["openclaw", "agent", "--agent", agent_id, "--message", prompt, "--json", "--local",
           "--session-key", session_key, "--timeout", str(timeout)]
    container = container or os.environ.get("BENCH_CONTAINER")
    if container:
        cmd = [
            _container_cli(), "exec", "-i",
            "-e", "LLM_API_KEY", "-e", "LLM_BASE_URL",
            container,
        ] + cmd
    if model:
        cmd += ["--model", model]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
    except subprocess.TimeoutExpired as e:
        fallback = judge_with_rules(answer, qa)
        fallback["rationale"] = f"agent judge timed out after {timeout}s ({e}); " + fallback["rationale"]
        return fallback
    except FileNotFoundError as e:
        fallback = judge_with_rules(answer, qa)
        fallback["rationale"] = f"agent judge unavailable ({e}); " + fallback["rationale"]
        return fallback

    # With --json, the structured payloads[].text is on stdout and diagnostics
    # on stderr. Extract the agent text, then parse the score out of it.
    text = _extract_judge_text(out.stdout or "")
    verdict = judge_parse(text, qa, answer)
    if verdict["rationale"].startswith("agent judge score parse fail"):
        # judge_parse already degraded to rules; nothing more to do.
        return verdict
    return verdict


# --- Entry point for direct CLI use -----------------------------------------


def main() -> int:
    """CLI: `python3 judge.py rules|agent <qa.json> <answer.txt>` prints JSON verdict."""
    if len(sys.argv) != 4:
        print("usage: judge.py {rules|agent} <qa.json> <answer.txt>", file=sys.stderr)
        return 2
    mode, qa_path, ans_path = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(qa_path, "r", encoding="utf-8") as f:
        qa = json.load(f)
    with open(ans_path, "r", encoding="utf-8") as f:
        answer = f.read()
    if mode == "rules":
        verdict = judge_with_rules(answer, qa)
    elif mode == "agent":
        verdict = judge_with_agent(qa, answer)
    else:
        print(f"unknown mode: {mode}", file=sys.stderr)
        return 2
    print(json.dumps(verdict, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
