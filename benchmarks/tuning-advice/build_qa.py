#!/usr/bin/env python3
"""
LLM-based QA expansion for tuning-advice benchmark.

Reads seed_qa.jsonl, prints instructions for LLM expansion.
Copy seeds to qa.jsonl as base, then expand using LLM.

Usage:
  python3 benchmarks/tuning-advice/build_qa.py
"""

import json
from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parent
SEED_FILE = BENCH_DIR / "seed_qa.jsonl"
OUTPUT_FILE = BENCH_DIR / "qa.jsonl"

def main():
    seeds = []
    with open(SEED_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                seeds.append(json.loads(line))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for seed in seeds:
            f.write(json.dumps(seed, ensure_ascii=False) + "\n")

    print(f"Written {len(seeds)} seeds to {OUTPUT_FILE}")
    print()
    print("扩增建议：对每个 seed 生成 2 个变体")
    print("- 参数分析场景：不同模型（GAN/Transformer/CNN/LSTM）")
    print("- 预算约束场景：不同预算等级")
    print("- 策略推荐场景：NAS/RL/主动学习等特殊场景")
    print("- 评估方案场景：不同统计方法")
    print("目标总 QA：10-15 条")

if __name__ == "__main__":
    main()
