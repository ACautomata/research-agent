# Read both source files
with open(r"D:\Code\= =\research-agent\research-agent-main\workspace\.openclaw\tmp\idea-generate-benchmark-design.md", encoding="utf-8") as f:
    design = f.read()

with open(r"D:\Code\= =\research-agent\research-agent-main\workspace\.openclaw\tmp\self-test-complete.md", encoding="utf-8") as f:
    test = f.read()

print(f"design: {len(design)} chars")
print(f"test: {len(test)} chars")
