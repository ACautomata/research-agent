# Synthetic-XG Benchmark — OOD Explanation Fidelity

- **Year**: 2023
- **Type**: benchmark
- **Status**: reviewed

## Summary
A benchmark for evaluating GNN explanation methods under distribution shift. Tests whether explanation methods maintain fidelity when test graphs come from a different distribution than training graphs.

## Key Finding
Both GNNExplainer and PGExplainer show >40% fidelity drop on OOD graphs, revealing that:
- Maximum-impact subgraphs ≠ causal subgraphs.
- Parametric explanations degrade to memorized templates under distribution shift.

## Constraints
- Graph size ≤ 500 nodes (CPU-feasible).
- Metrics: explanation fidelity, OOD generalization gap.
