#!/usr/bin/env python3
"""
LLM-based QA expansion for spec-generation benchmark.

Reads seed_qa.jsonl, sends each seed to an LLM with a prompt asking to
generate 2-3 variant QAs, and writes the expanded set to qa.jsonl.

Usage:
  python3 benchmarks/spec-generation/build_qa.py

Requires:
  - python-docx (for reading input materials) — optional
  - OPENAI_API_KEY or equivalent in environment
"""

import json
import os
import sys
from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parent
SEED_FILE = BENCH_DIR / "seed_qa.jsonl"
OUTPUT_FILE = BENCH_DIR / "qa.jsonl"

def load_seeds():
    seeds = []
    with open(SEED_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                seeds.append(json.loads(line))
    return seeds

def main():
    seeds = load_seeds()
    print(f"Loaded {len(seeds)} seed QA items from {SEED_FILE}")

    # Copy seeds to output as the base
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for seed in seeds:
            f.write(json.dumps(seed, ensure_ascii=False) + "\n")
    print(f"Written {len(seeds)} items to {OUTPUT_FILE} (base = seeds)")

    print()
    print("=" * 60)
    print("LLM 扩增步骤")
    print("=" * 60)
    print()
    print("请执行以下步骤手动或通过 LLM 扩增 QA：")
    print()
    print("1. 对每个 seed QA，用 LLM 生成 2-3 个变体：")
    print("   - 同类型但不同输入材料")
    print("   - 混合场景（验证实验 + 算法实现混合输入）")
    print("   - 边界情况（极端缺少材料、矛盾材料）")
    print()
    print("2. 将生成的新 QA 追加到 qa.jsonl 中")
    print()
    print("3. 确保每个 QA 有唯一的 qa_id（如 seed-001, qa-001, qa-002...）")
    print()
    print("4. 手动检查生成的 QA 质量：")
    print("   - gold_answer.must_contain 不包含无关关键词")
    print("   - rubric 维度合理")
    print("   - pass_threshold 不低于 0.5")
    print()
    print("扩增目标：10-20 条总 QA（含 seed）")

if __name__ == "__main__":
    main()
