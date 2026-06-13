# Prefix Tuning — Optimizing Continuous Prompts for Generation

- **Year**: 2021
- **Authors**: Li & Liang (Stanford)
- **Venue**: ACL 2021
- **Type**: paper
- **Status**: reviewed

## Summary
Prepends trainable continuous token embeddings to the input. Only <0.1% parameters. No weight modification to the base model.

## Core Hypothesis
**"Task adaptation is primarily input-conditioning, not weight modification"** — changing what the model attends to is sufficient.

## Key Claims
1. Prefix tuning matches fine-tuning on generation tasks with 0.1% parameters.
2. Works by steering attention patterns through prepended tokens.

## Limitations
1. Inference overhead (prefix tokens consume context window).
2. Performance drops on tasks requiring deep structural changes (e.g., CodeXGLUE).
3. Excels on LongRangeQA but underperforms on code tasks.
