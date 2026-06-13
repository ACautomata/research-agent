# LoRA — Low-Rank Adaptation of Large Language Models

- **Year**: 2021
- **Authors**: Hu et al. (Microsoft)
- **Venue**: ICLR 2022
- **Type**: paper
- **Status**: reviewed

## Summary
Proposes low-rank decomposition for efficient LLM fine-tuning. Freezes pretrained weights and injects trainable rank-decomposition matrices into attention layers. <1% trainable parameters, zero inference overhead.

## Core Hypothesis
**"Task adaptation lives in a low-rank subspace"** — the weight update during fine-tuning has low intrinsic rank.

## Key Claims
1. LoRA matches full fine-tuning performance on GLUE with <1% parameters.
2. Zero inference latency overhead (weights can be merged).
3. Works across model scales (RoBERTa to GPT-3).

## Limitations
1. Optimal rank selection lacks theoretical foundation.
2. Multi-task/continual LoRA is underexplored.
3. Performance varies by task type—excels on CodeXGLUE but weaker on LongRangeQA.
