---
pageType: source
id: source.synthetic-xg-benchmark
title: Synthetic-XG Benchmark
status: published
---

# Synthetic-XG Benchmark

Synthetic-XG is a benchmark designed to stress-test graph explanations under distribution shift. It creates graph families where the training distribution contains shortcuts and the OOD distribution changes motif frequency or label rules.

Key observation:
- Explanation fidelity can drop by more than 40 percent OOD.
- The drop reveals a generalization gap between in-distribution explanation quality and OOD explanation quality.
- Some explainers preserve high apparent fidelity by relying on template memorization.

Useful tests:
- Counterfactual deletion or insertion of candidate motifs.
- Intervention on graph edges that should be causally irrelevant.
- Separate metrics for fidelity, OOD fidelity, and generalization gap.

Problematization direction: challenge the assumption that faithful explanations are automatically causal explanations.
