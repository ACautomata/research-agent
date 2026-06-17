---
pageType: source
id: source.pgexplainer
title: PGExplainer
status: published
---

# PGExplainer

PGExplainer trains a parameterized explainer to predict important edges for a GNN. It is designed to generalize explanations across graphs, avoiding per-graph optimization.

Default assumption:
- Explanation rules can generalize across graphs without retraining for each graph.
- A learned edge selector captures transferable structure rather than memorizing templates.

Challenge:
- Under distribution shift, the learned explainer can reuse spurious templates.
- Generalization may fail when graph motifs or labels change.
- A discriminating experiment should compare in-distribution fidelity with OOD fidelity on shifted graph families.

Research ideas should probe whether PGExplainer is learning causal signals, spurious correlation, or template memorization.
