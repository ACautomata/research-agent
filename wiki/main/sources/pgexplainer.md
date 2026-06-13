# PGExplainer — Parameterized Explainer for Graph Neural Networks

- **Year**: 2020
- **Authors**: Luo et al.
- **Venue**: NeurIPS
- **Type**: paper
- **Status**: reviewed

## Summary
Parameterizes explanation generation as a learned neural network, eliminating per-instance retraining. Generates explanations in a single forward pass.

## Default Assumption
**"Explanations generalize to new graphs without per-instance retraining"** — learned explanation patterns transfer across instances.

## Key Claims
1. Parameterized explanations are faster than GNNExplainer (no per-instance optimization).
2. Explanations can generalize to unseen graph structures.

## Key Limitations
1. In OOD/distribution shift settings (Synthetic-XG), explanation fidelity drops 40%+.
2. Under distribution shift, generalized explanations degrade to "memorized templates."
3. The parametric explainer inherits biases from training distribution.

## Experimental Setup
- **Datasets**: Synthetic benchmarks, MUTAG, BA-2Motifs
- **Metrics**: Explanation fidelity, OOD generalization gap
