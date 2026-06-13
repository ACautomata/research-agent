#!/usr/bin/env python3
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
items = []
for fname in ["seed_qa.json", "fle_qa.json"]:
    fp = HERE / fname
    if not fp.exists(): continue
    for s in json.loads(fp.read_text(encoding="utf-8")):
        e = dict(s)
        e.setdefault("qa_id", e.pop("id", e.get("qa_id")))
        e.setdefault("agent", "main")
        e.setdefault("judge", "agent")
        e.setdefault("pass_threshold", 0.5)
        e.setdefault("weight", 1.0)
        e.setdefault("rubric", "")
        e.setdefault("rubric_dimensions", [])
        items.append(e)
out = HERE / "qa.jsonl"
with open(out, "w", encoding="utf-8") as f:
    for item in items:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
print(f"[build_qa] {len(items)} QA items")
