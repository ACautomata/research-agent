---
pageType: source
id: source.peft-method-comparison
title: PEFT Method Comparison
status: published
---

# PEFT Method Comparison

The comparison reports a rank reversal across three benchmarks:
- CodeXGLUE: LoRA is best.
- LongRangeQA: Prefix Tuning is best.
- MMLU-Pro: IA3 is best.

This reversal implies an interaction effect between task type and PEFT method. A single global winner is the wrong framing.

Task taxonomy:
- Code transformation and syntax tasks favor low-rank updates.
- Long-context question answering favors input-conditioning.
- Knowledge-heavy multiple-choice tasks favor activation rescaling.

Good research ideas should design discriminating experiments that separate competing hypotheses. For example, create a task-type by method matrix and test whether task features such as context length, code structure, and knowledge calibration predict which method wins.
