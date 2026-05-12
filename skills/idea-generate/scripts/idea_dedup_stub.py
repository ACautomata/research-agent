#!/usr/bin/env python3
"""First-pass deduplication for draft idea lists.

Input: JSON array of idea objects with optional keys such as:
  - title
  - mechanism
  - target_problem

Output: JSON array with simple duplicate collapse by normalized title+mechanism.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def normalize(text: str) -> str:
    return " ".join((text or "").lower().split())


def dedup_key(idea: dict) -> tuple[str, str]:
    title = normalize(idea.get("title", ""))
    mechanism = normalize(idea.get("mechanism", ""))
    return title, mechanism


def dedup_ideas(ideas: list[dict]) -> list[dict]:
    seen: set[tuple[str, str]] = set()
    result: list[dict] = []
    for idea in ideas:
        key = dedup_key(idea)
        if key in seen:
            continue
        seen.add(key)
        result.append(idea)
    return result


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: idea_dedup_stub.py <input.json> <output.json>", file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    ideas = json.loads(input_path.read_text(encoding="utf-8-sig"))
    if not isinstance(ideas, list):
        print("Input must be a JSON array.", file=sys.stderr)
        return 2

    deduped = dedup_ideas([idea for idea in ideas if isinstance(idea, dict)])
    output_path.write_text(
        json.dumps(deduped, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {len(deduped)} ideas to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
