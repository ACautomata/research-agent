---
pageType: source
id: source.continual-learning-cpu-constraint
title: Continual Learning CPU Constraint
status: published
---

# Continual Learning CPU Constraint

This benchmark concerns continual learning for image classification on CIFAR-100 split into 10 sequential tasks. The available baseline is Python/PyTorch finetuning that trains each task serially.

Hard constraints:
- CPU-only.
- Maximum training time budget: 2 hours.
- 10 sequential tasks.
- Low-risk, Python-only changes.
- Prefer lightweight regularization or a replay buffer.

Observed failure:
- The finetuning baseline shows catastrophic forgetting.
- After task 5, task 1 accuracy drops from 70 percent to 25 percent.
- A useful metric is forgetting rate: max historical task accuracy minus final task accuracy.

Feasible idea space:
- Small replay buffer with class-balanced sampling.
- Lightweight regularization such as L2, EWC-style diagonal penalty, or logit consistency.
- Prototype replay or feature-statistics replay instead of full-image replay.
- Training-time accounting must show why the method fits CPU-only 2 hours.

Evaluation should report average accuracy, forgetting rate, task 1 retention, memory size, and wall-clock training time.
