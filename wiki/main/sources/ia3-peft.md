# IA3 — Infused Adapter by Inhibiting and Amplifying Inner Activations

- **Year**: 2022
- **Authors**: Liu et al.
- **Venue**: NeurIPS 2022
- **Type**: paper
- **Status**: reviewed

## Summary
Introduces three scaling vectors (key, value, FFN) that rescale activations. <0.01% parameters—the most parameter-efficient PEFT method.

## Core Hypothesis
**"Task adaptation requires only rescaling activations, not re-weighting"** — magnitude modulation suffices.

## Key Claims
1. IA3 achieves competitive performance with only 3 learned vectors per layer.
2. Strong on knowledge-intensive tasks (MMLU-Pro) where activation gating is critical.

## Limitations
1. Very limited expressivity—may underfit on tasks requiring complex weight interactions.
2. Performance varies dramatically by task type.
3. Excels on MMLU-Pro but weaker on LongRangeQA.
