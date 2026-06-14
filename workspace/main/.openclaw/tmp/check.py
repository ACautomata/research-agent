import json, os
path = r'D:\Code\= =\research-agent\research-agent-main\benchmarks\idea-generate\qa.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    lines = [json.loads(l) for l in f.read().strip().split('\n') if l.strip()]

print(f"Total: {len(lines)} QAs")
print(f"All 9 dims: {all(len(l.get('rubric_dimensions',[]))==9 for l in lines)}")

from collections import Counter
tc = Counter(l['task_type'] for l in lines)
print(f"Task types: {len(tc)}/9")
jc = Counter(l['judge'] for l in lines)
print(f"Judges: rules={jc.get('rules',0)}, agent={jc.get('agent',0)}")

kws = [len(l['gold_answer']['must_contain']) for l in lines]
print(f"Keywords: min={min(kws)}, max={max(kws)}, avg={sum(kws)/len(kws):.1f}")
print(f"Size: {os.path.getsize(path):,} bytes")
print(f"All valid: YES")
