---
pageType: source
id: source.randaugment
title: RandAugment
status: published
---

# RandAugment

RandAugment is an image data augmentation method that removes expensive policy search. It samples N transformations from a fixed augmentation space and applies a shared global magnitude M.

Reusable components:
- Random transformation selection.
- A compact search space controlled by N and magnitude M.
- Offline augmentation during training, so inference latency is unchanged.

Transfer risks for time series:
- A single magnitude may not scale across accelerometer, gyroscope, ECG, or other sensor channels.
- Image operations such as rotation or translation do not map directly to time series.
- Time warping can break time causal assumptions.
- Channel-wise independent noise may violate physical constraint and cross-channel correlations.

Adaptation direction: replace global image magnitude with channel-aware magnitude adaptation and restrict transformations to time causal operations.
