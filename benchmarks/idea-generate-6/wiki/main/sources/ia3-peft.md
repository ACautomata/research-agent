---
pageType: source
id: source.ia3-peft
title: IA3 PEFT
status: published
---

# IA3 PEFT

IA3 is a parameter-efficient method that rescales internal activations. Its activation rescaling hypothesis is that task adaptation can be achieved by modulating existing feature channels rather than adding low-rank updates or long prefixes.

Benchmark signal:
- IA3 ranks first on MMLU-Pro in the provided comparison.
- It is strongest when the task depends on broad knowledge calibration and selecting among already represented concepts.

Competing hypothesis:
- Activation rescaling is best when the task feature is knowledge selection or calibration rather than new skill acquisition.
