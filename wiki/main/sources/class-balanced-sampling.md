# Class-Balanced Sampling for Long-Tailed Recognition

- **Year**: 2019
- **Authors**: Cui et al. / Cao et al.
- **Venue**: CVPR / ICLR
- **Type**: paper
- **Status**: reviewed

## Summary
Proposes class-balanced resampling and reweighting strategies for long-tailed visual recognition. Gives minority-class samples higher effective frequency during training.

## Key Claims
1. Inverse-frequency weighting (w_c = 1/n_c) improves minority class accuracy.
2. Class-balanced sampling stabilizes long-tailed training.

## Key Limitations
1. **Majority class overfitting**: Static rebalancing reduces exposure to head-class samples, causing overfitting on majority classes and loss of useful features from head data.
2. No mechanism for progressive focus shift from majority to minority.

## Experimental Setup
- **Datasets**: CIFAR-LT (IR=100/50/10), ImageNet-LT, iNaturalist
- **Metrics**: Balanced accuracy, per-class accuracy
