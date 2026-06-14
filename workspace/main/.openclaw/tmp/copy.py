with open(r"D:\Code\= =\research-agent\research-agent-main\workspace\.openclaw\tmp\idea-generate-benchmark-design.md", encoding="utf-8") as f:
    content = f.read()
with open(r"D:\Code\= =\research-agent\research-agent-main\workspace\.openclaw\tmp\design_raw.txt", "w", encoding="utf-8") as f:
    f.write(content)
print(f"Copied: {len(content)} chars")
