---
pageType: source
id: source.uea-time-series-benchmark
title: UEA Time Series Benchmark
status: published
---

# UEA Time Series Benchmark

The UEA archive is a public benchmark collection for time series classification. It includes univariate and multivariate datasets with diverse sampling rates, sensor channels, and domain-specific invariances.

Benchmark constraints:
- Training can be offline.
- Inference latency must stay below 50ms.
- Augmentation must preserve time causality when the task assumes causal order.
- Physical constraint matters in multichannel sensor data: cross-channel relationships should not be independently corrupted.

Useful evaluation:
- Compare baseline, image-style RandAugment transfer, and time-series-specific augmentation.
- Report accuracy, latency, and failure by channel-wise transformation type.
- Use ablations for warping, magnitude adaptation, and cross-channel coupling.

The domain gap is not only input shape. It includes temporal order, physical sensor semantics, and causal validity.
