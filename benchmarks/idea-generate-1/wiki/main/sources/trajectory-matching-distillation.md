---
pageType: source
id: source.trajectory-matching-distillation
title: Trajectory Matching Distillation
status: published
---

# Trajectory Matching Distillation

Trajectory matching is a dataset distillation method that optimizes a small synthetic training set so that a student network trained on the synthetic data follows parameter trajectories close to a teacher trained on the full real dataset.

For long-tailed image classification, the method is evaluated on CIFAR-LT. A small distillation budget such as 1 to 10 synthetic samples per class is attractive for fast pilot studies, but the same fixed samples per class budget can underrepresent minority classes.

Key facts for this benchmark:
- Task: dataset distillation for long-tailed image classification.
- Dataset: CIFAR-LT / CIFAR-10-LT style class imbalance.
- Metrics: balanced accuracy and minority class accuracy.
- Failure mode: trajectory matching tends to follow majority class optimization dynamics because the teacher trajectory is dominated by head classes.
- Observable risk: synthetic examples can preserve majority class decision boundaries while minority class accuracy remains low.
- Useful idea direction: reweight trajectory segments, allocate distillation budget by class difficulty, or use minority-aware matching losses.

Implication: an idea should not only improve overall balanced accuracy. It should explicitly track minority class accuracy and explain how many synthetic samples per class are assigned to head and tail classes.
