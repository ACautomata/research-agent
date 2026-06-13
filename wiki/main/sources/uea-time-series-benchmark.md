# UEA Archive — Multivariate Time Series Classification Benchmark

- **Year**: 2018
- **Venue**: arXiv / UEA
- **Type**: benchmark
- **Status**: reviewed

## Summary
The UEA & UCR Time Series Classification Archive: a standardized benchmark collection of 30 multivariate time series classification datasets spanning diverse domains (human activity recognition, ECG, audio, gesture, etc.).

## Key Datasets Mentioned in QA-034
- **HumanActivityRecognition**: Smartphone accelerometer + gyroscope, 6 activity classes.
- **PenDigits**: Pen trajectory digit recognition from 2D spatial coordinates.

## Domain Characteristics
1. **Channel heterogeneity**: Different physical quantities (accel vs. gyro) with different units and scales.
2. **Temporal causality**: Time-axis transformations must respect causal order (no future information leakage).
3. **Cross-channel correlations**: Physical constraints (e.g., 3-axis accelerometer must maintain geometric consistency).

## Constraints for Transfer
- Offline batch training only.
- Inference latency <50ms.
- Must preserve temporal causality.
