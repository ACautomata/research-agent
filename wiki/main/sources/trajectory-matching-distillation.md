# Trajectory Matching for Dataset Distillation

- **Year**: 2022
- **Authors**: Cazenavette et al.
- **Venue**: ECCV / arXiv
- **Type**: paper
- **Status**: reviewed

## Abstract / Summary

Proposes a dataset distillation method that matches model-training trajectories between the full dataset and a small synthetic set. Instead of matching final gradients or features, the method aligns the entire optimization trajectory of models trained on real vs. synthetic data.

## Key Claims

1. Trajectory matching produces higher-quality synthetic samples than gradient-matching approaches.
2. The synthetic set can be as small as 1 image per class (IPC=1) while retaining reasonable downstream accuracy.
3. Works well on balanced datasets like CIFAR-10/100.

## Key Limitations

1. **Class imbalance amplification**: In long-tailed settings, minority classes have fewer real training steps, so their synthetic samples receive weaker optimization signals. Minority class accuracy is substantially lower than majority class accuracy.
2. Synthetic set quality is proportional to original class frequency.
3. The matching objective has no mechanism to counteract original data imbalance.

## Experimental Setup

- **Datasets**: CIFAR-10, CIFAR-100, CIFAR-LT
- **IPC range**: 1, 10, 50
- **Downstream classifier**: ConvNet
- **Metrics**: Accuracy, per-class accuracy

## Relevance to Benchmark

This paper is the anchor source for QA-001 (dataset distillation for long-tailed image classification). The core pain point: trajectory matching inherits or amplifies class imbalance, producing weak synthetic samples for minority/tail classes.
