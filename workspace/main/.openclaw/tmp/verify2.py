import json

path = r"D:\Code\= =\research-agent\research-agent-main\benchmarks\idea-generate\qa.jsonl"
with open(path, encoding="utf-8") as f:
    lines = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]

print(f"Total QAs: {len(lines)}")
for l in lines:
    qa = json.loads(l)
    kc = len(qa["gold_answer"]["must_contain"])
    judge = qa["judge"]
    wt = qa["weight"]
    print(f"  {qa['qa_id']}: {qa['task_type']:30s} judge={judge:5s} kw={kc} wt={wt}")
print("All valid JSON")
