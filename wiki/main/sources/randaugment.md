# RandAugment — Practical Automated Data Augmentation

- **Year**: 2019
- **Authors**: Cubuk et al. (Google Brain)
- **Venue**: NeurIPS 2019
- **Type**: paper
- **Status**: reviewed

## Summary
Simplifies automated augmentation search to a two-parameter method: (1) global magnitude M controls intensity of all transformations, (2) N transformations randomly selected per batch from a pool of 14 standard image transforms (rotation, translation, color, contrast, etc.).

## Key Design Components
1. **Global magnitude M**: Single parameter controlling all transformation intensities.
2. **Random selection per batch**: N out of 14 transforms randomly chosen each batch.
3. **Transform space**: 14 image-specific transforms (flip, rotate, shear, color, contrast, brightness, sharpness, etc.).

## Key Claims
1. RandAugment matches or exceeds learned augmentation policies (AutoAugment) with a fraction of the search cost.
2. CIFAR/ImageNet: +2-3% over baseline augmentation.
3. Universal: same M, N work across datasets with minimal tuning.

## Limitations for Time Series Transfer
1. Magnitude M assumes all transforms share a scale—time series channels have different physical units (acceleration m/s² vs gyroscope rad/s).
2. Time warping and pooling break temporal causality (cannot use future information).
3. Independent channel perturbation ignores physical correlations (e.g., 3-axis accelerometer).
4. Transform space is entirely image-specific—no native time series transforms.
