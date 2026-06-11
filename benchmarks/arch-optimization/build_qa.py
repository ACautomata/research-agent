#!/usr/bin/env python3
"""LLM-based QA expansion for arch-optimization benchmark."""
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
    print("扩增建议：GAN/VAE 架构优化、激活函数替换、归一化策略选择等")
    print("目标总 QA：10-15 条")

if __name__ == "__main__":
    main()
