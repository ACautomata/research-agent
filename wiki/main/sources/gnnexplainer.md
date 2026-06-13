# GNNExplainer — Generating Explanations for Graph Neural Networks

- **Year**: 2019
- **Authors**: Ying et al.
- **Venue**: NeurIPS
- **Type**: paper
- **Status**: reviewed

## Summary
Learns subgraph explanations via edge mask optimization. Identifies the minimal subgraph that maximizes mutual information with the GNN's prediction.

## Default Assumption
**"Important subgraph = subgraph with maximum impact on prediction"** — i.e., predictive importance equals causal importance.

## Key Claims
1. Edge masks can identify the subgraph that drives a GNN's prediction.
2. Explanations are instance-specific and model-agnostic.

## Key Limitations
1. In OOD settings (Synthetic-XG benchmark), explanation fidelity drops 40%+.
2. The "maximum impact" subgraph may capture spurious correlations, not causal relationships.
3. Explanations are not guaranteed to be causally faithful.

## Experimental Setup
- **Datasets**: Synthetic benchmarks, MUTAG, BA-2Motifs
- **Metrics**: Explanation fidelity, accuracy
