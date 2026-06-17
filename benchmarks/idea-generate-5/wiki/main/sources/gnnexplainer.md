---
pageType: source
id: source.gnnexplainer
title: GNNExplainer
status: published
---

# GNNExplainer

GNNExplainer explains a trained graph neural network by selecting a compact subgraph and feature mask that maximizes mutual information with the model prediction.

Default assumption:
- The important subgraph is the subgraph with the largest prediction influence.
- High explanation fidelity is treated as evidence that the explanation captures the true reason for the prediction.

Challenge:
- A high-fidelity subgraph can encode spurious correlation rather than a causal mechanism.
- The selected subgraph may match dataset templates instead of robust decision evidence.
- Counterfactual and intervention tests are needed to distinguish causal evidence from correlation.

For this benchmark, ideas must fit graphs with at most 500 nodes on CPU and should measure explanation fidelity plus OOD generalization gap.
