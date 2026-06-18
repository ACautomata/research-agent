---
pageType: source
id: source.prefix-tuning-peft
title: Prefix Tuning PEFT
status: published
---

# Prefix Tuning PEFT

Prefix Tuning uses learned continuous prefixes or prompts to condition the model input. Its central input-conditioning hypothesis is that task behavior can be steered through the context interface rather than by changing model weights.

Benchmark signal:
- Prefix Tuning ranks first on LongRangeQA in the provided comparison.
- It is strongest when the task depends on long context routing, retrieval-like cues, or instruction framing.

Competing hypothesis:
- Input-conditioning methods dominate when the decisive task feature is context organization rather than local parameter change.
