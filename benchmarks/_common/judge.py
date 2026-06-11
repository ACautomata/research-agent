#!/usr/bin/env python3
"""Reusable scoring for benchmark metrics.py scripts.

Two judges:
  judge_with_rules(answer, qa)  -- rule-based, uses qa.gold_answer and must_contain-style hints.
  judge_with_agent(qa, answer, agent_id, model=None) -- LLM judge via direct `openclaw agent --agent reviewer`.

Both return a dict: {score: float (0-1), pass: bool, rationale: str, dimensions?: dict}.
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


def _extract_must_not_contain(gold: Any) -> list[str]:
    """Pull forbidden tokens/phrases from gold_answer.must_not_contain."""
    if not isinstance(gold, dict):
        return []
    out = gold.get("must_not_contain") or []
    return [str(t) for t in out if str(t).strip()]


def judge_with_rules(answer: str, qa: dict) -> dict:
    """Score an answer against qa.gold_answer with keyword coverage + forbidden-term check.

    Positive score = covered / len(required).
    Each forbidden term found (must_not_contain) reduces the effective covered count by 1.
    Final score = max(0, covered - violations) / len(required).
    Pass when score >= qa.pass_threshold.
    """
    gold = qa.get("gold_answer") or {}
    required = _extract_must_contain(gold)
    forbidden = _extract_must_not_contain(gold)
    violation_penalty = gold.get("violation_penalty", 1) if isinstance(gold, dict) else 1

    if not required:
        text = (answer or "").strip()
        if not text:
            return {"score": 0.0, "pass": False, "rationale": "empty answer, no gold to check against"}
        score = min(1.0, len(text) / 200.0)
        return {"score": score, "pass": score >= qa.get("pass_threshold", 0.5),
                "rationale": f"no gold_answer; scored on length={len(text)}"}

    text = (answer or "").lower()
    missing = [r for r in required if r.lower() not in text]
    violations = [f for f in forbidden if f.lower() in text]

    covered = len(required) - len(missing)
    effective_covered = max(0, covered - violation_penalty * len(violations))
    score = effective_covered / len(required)

    rationale_parts = [f"covered {covered}/{len(required)}"]
    if missing:
        rationale_parts.append(f"missing={missing[:5]}")
    if violations:
        rationale_parts.append(f"FORBIDDEN found={violations[:5]}")

    return {
        "score": round(score, 4),
        "pass": score >= qa.get("pass_threshold", 0.5),
        "rationale": "; ".join(rationale_parts),
        "missing": missing,
        "violations": violations,
    }


# --- LLM judge ---------------------------------------------------------------


def _extract_judge_text(stdout: str) -> str:
    """Extract the reviewer text from `openclaw agent --json` stdout."""
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


def _safe_int(value: object, default: int, *, minimum: int | None = None) -> int:
    """Parse integer config without crashing on malformed environment values."""
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    if minimum is not None:
        parsed = max(minimum, parsed)
    return parsed


def _extract_json_object(text: str, required_key: str) -> str | None:
    """Return the first JSON object containing required_key.

    The scanner tracks JSON string state so braces inside reviewer rationale
    strings do not prematurely close the object.
    """
    for match in re.finditer(r"\{", text or ""):
        start = match.start()
        depth = 0
        in_string = False
        escape = False
        for j in range(start, len(text)):
            ch = text[j]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    candidate = text[start:j + 1]
                    if f'"{required_key}"' in candidate:
                        return candidate
                    break
    return None


def _clip_text(text: str, limit: int) -> str:
    """Return a compact head/tail view, preserving both setup and conclusion."""
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    head = max(0, int(limit * 0.72))
    tail = max(0, limit - head)
    return (
        text[:head].rstrip()
        + f"\n\n...[truncated {len(text) - limit} chars]...\n\n"
        + text[-tail:].lstrip()
    )


def _compact_gold(gold: Any) -> dict | str:
    """Keep only reviewer-relevant reference fields in a bounded shape."""
    if not isinstance(gold, dict):
        return gold or "(none)"
    compact: dict[str, Any] = {}
    for key, limit in (
        ("must_contain", 40),
        ("must_not_contain", 30),
        ("fields", 30),
    ):
        values = gold.get(key)
        if isinstance(values, list) and values:
            compact[key] = [str(v) for v in values[:limit]]
    key_behavior = gold.get("key_behavior")
    if key_behavior:
        compact["key_behavior"] = _clip_text(str(key_behavior), 900)
    return compact or gold


def judge_with_agent(qa: dict, answer: str, agent_id: str = "reviewer",
                     model: str | None = None, timeout: int = 600,
                     container: str | None = None,
                     _retry_count: int = 0) -> dict:
    """Run a one-shot LLM judge by directly invoking the reviewer agent.

    The reviewer prompt asks for a JSON verdict:
    {"score": 0-1, "rationale": "...", "dimensions": {...}}.

    The judge call is bounded by `timeout` (default 600s) plus a 30s grace on
    the subprocess side; a hung judge therefore cannot stall the whole
    benchmark run. Judge failures fall back to rules so the report still has
    diagnostic score variance; the fallback is tagged with judge_error so it is
    not confused with a normal reviewer verdict.
    """
    agent_id = agent_id or "reviewer"
    rubric = qa.get("rubric") or "Score how well the answer matches the gold answer on a 0-1 scale."
    gold = qa.get("gold_answer")
    dimensions = qa.get("rubric_dimensions") or []
    compact_reference = _compact_gold(gold)
    compact_candidate = _clip_text(
        answer or "",
        _safe_int(os.environ.get("BENCH_JUDGE_CANDIDATE_CHARS", "4500"), 4500, minimum=500),
    )
    compact_rubric = _clip_text(
        str(rubric),
        _safe_int(os.environ.get("BENCH_JUDGE_RUBRIC_CHARS", "1200"), 1200, minimum=200),
    )
    compact_question = _clip_text(str(qa.get("question", "")), 700)
    prompt = (
        "You are the benchmark reviewer. Score the candidate strictly against "
        "REFERENCE and RUBRIC. Return JSON only, no markdown, no prose.\n"
        "Schema: {\"score\":0.0,\"rationale\":\"short\",\"dimensions\":{}}.\n"
        "For each listed dimension, include {\"score\":0..1,\"rationale\":\"short\"}. "
        "Keep all rationales under 25 words.\n"
        "Score anchors: 0.90-1.00 = all core requirements met with only minor gaps; "
        "0.75-0.89 = core requirements met but one secondary rubric item is weak; "
        "0.50-0.74 = partially correct with a meaningful missing requirement; "
        "<0.50 = core task failed or fabricated. Do not drop below 0.75 solely "
        "because evidence-strength labels are incomplete when the answer otherwise "
        "covers the main requested analysis.\n\n"
        f"QA: {compact_question}\n\n"
        f"REFERENCE: {json.dumps(compact_reference, ensure_ascii=False)}\n\n"
        f"RUBRIC: {compact_rubric}\n\n"
        f"DIMENSIONS: {json.dumps(dimensions, ensure_ascii=False)}\n\n"
        f"PASS_THRESHOLD: {qa.get('pass_threshold', 0.5)}\n\n"
        f"CANDIDATE:\n{compact_candidate}\n"
    )

    session_key = f"agent:{agent_id}:bench-judge-{os.getpid()}-{uuid.uuid4().hex}"
    cmd = ["openclaw", "agent", "--agent", agent_id, "--message", prompt, "--json", "--local",
           "--session-key", session_key, "--timeout", str(timeout)]
    container = container or os.environ.get("BENCH_CONTAINER")
    if container:
        cmd = [
            "docker", "exec", "-i",
            "-e", "DEEPSEEK_API_KEY", "-e", "DEEPSEEK_BASE_URL",
            "-e", "MINIMAX_API_KEY", "-e", "MINIMAX_BASE_URL",
            container,
        ] + cmd
    if model:
        cmd += ["--model", model]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
    except subprocess.TimeoutExpired as e:
        fallback = judge_with_rules(answer, qa)
        fallback["rationale"] = f"agent judge timed out after {timeout}s ({e}); " + fallback["rationale"]
        fallback["judge_error"] = "timeout"
        fallback["judge_fallback"] = "rules"
        return fallback
    except FileNotFoundError as e:
        fallback = judge_with_rules(answer, qa)
        fallback["rationale"] = f"agent judge unavailable ({e}); " + fallback["rationale"]
        fallback["judge_error"] = "unavailable"
        fallback["judge_fallback"] = "rules"
        return fallback

    # Only look at stdout for the JSON verdict; with --json, diagnostics
    # are routed to stderr (per docs.openclaw.ai/tools/agent-send).  OpenClaw
    # normally wraps replies in payloads[].text, so extract that before looking
    # for the reviewer's requested JSON verdict.
    text = _extract_judge_text(out.stdout or "")
    raw_json = _extract_json_object(text, "score")
    if not raw_json:
        fallback = judge_with_rules(answer, qa)
        fallback["rationale"] = "agent judge parse fail; " + fallback["rationale"]
        fallback["judge_error"] = "parse_fail"
        fallback["judge_stdout"] = (out.stdout or "")[:1000]
        fallback["judge_stderr"] = (out.stderr or "")[:1000]
        fallback["judge_fallback"] = "rules"
        return fallback

    def _repair_json(raw: str) -> str:
        """Best-effort repair of common LLM JSON formatting mistakes."""
        # 1. strip markdown code fences
        raw = re.sub(r'^```(?:json)?\s*\n?', '', raw.strip())
        raw = re.sub(r'\n?```\s*$', '', raw)
        # 2. Chinese punctuation → ASCII
        raw = raw.replace('“', '"').replace('”', '"')
        raw = raw.replace('：', ':').replace('，', ',')
        raw = raw.replace('‘', "'").replace('’', "'")
        # 3. missing commas: "val" "key" → "val", "key"
        raw = re.sub(r'"\s+"(?=[^:}])', '", "', raw)
        # 4. trailing comma before }
        raw = re.sub(r',\s*}', '}', raw)
        return raw

    verdict = None
    # Try direct parse first, then repair
    for attempt, candidate in enumerate([raw_json, _repair_json(raw_json)]):
        try:
            verdict = json.loads(candidate)
            break
        except (json.JSONDecodeError, ValueError, TypeError):
            if attempt == 0:
                continue
            # repair failed too → fallback
            fallback = judge_with_rules(answer, qa)
            fallback["rationale"] = f"agent judge JSON parse fail after repair; " + fallback["rationale"]
            fallback["judge_error"] = "json_parse_fail"
            fallback["judge_text"] = text[:1000]
            fallback["judge_fallback"] = "rules"
            return fallback

    try:
        score = float(verdict.get("score", 0.0))
    except (ValueError, TypeError):
        fallback = judge_with_rules(answer, qa)
        fallback["rationale"] = "agent judge invalid score schema; " + fallback["rationale"]
        fallback["judge_error"] = "invalid_schema"
        fallback["judge_text"] = text[:1000]
        fallback["judge_fallback"] = "rules"
        return fallback
    score = max(0.0, min(1.0, score))
    # Guard: when the reviewer returns a structurally valid but semantically
    # empty verdict (score=0, no rationale, no dimensions), it is almost
    # certainly a model glitch rather than a genuine assessment.  Retry once.
    rationale_str = str(verdict.get("rationale", "")).strip()
    dims = verdict.get("dimensions") if isinstance(verdict.get("dimensions"), dict) else {}
    if score == 0.0 and not rationale_str and not dims and _retry_count < 1:
        result = judge_with_agent(qa, answer, agent_id=agent_id, model=model,
                                  timeout=timeout, container=container,
                                  _retry_count=_retry_count + 1)
        result["judge_retry_attempted"] = True
        return result
    if score == 0.0 and not rationale_str and not dims:
        fallback = judge_with_rules(answer, qa)
        fallback["rationale"] = "agent judge returned empty verdict after retry; " + fallback["rationale"]
        fallback["judge_error"] = "empty_verdict"
        fallback["judge_fallback"] = "rules"
        fallback["judge_retry_attempted"] = True
        return fallback
    result = {
        "score": round(score, 4),
        "pass": score >= qa.get("pass_threshold", 0.5),
        "rationale": rationale_str[:500],
        "dimensions": dims,
    }
    if _retry_count > 0:
        result["judge_retry_attempted"] = True
    return result


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
