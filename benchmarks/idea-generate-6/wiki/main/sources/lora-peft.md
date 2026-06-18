---
pageType: source
id: source.lora-peft
title: LoRA PEFT
status: published
---

# LoRA PEFT

LoRA is a parameter-efficient fine-tuning method based on the low-rank hypothesis: many task updates can be represented by low-rank matrices injected into attention or feed-forward weights.

Benchmark signal:
- LoRA ranks first on CodeXGLUE in the provided comparison.
- It is strongest when task adaptation requires localized weight updates or code-oriented syntax transformations.

Competing hypothesis:
- Low-rank updates are best when the task feature is compositional code structure or compact transformation rules.

For this benchmark, no new LLM training is allowed. Ideas should rely on inference-only analysis or existing adapters and test task-type by method interaction effect.
