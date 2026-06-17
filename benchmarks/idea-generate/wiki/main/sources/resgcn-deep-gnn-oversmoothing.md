---
pageType: source
id: source.resgcn-deep-gnn-oversmoothing
title: ResGCN Deep GNN Oversmoothing
status: published
---

# ResGCN Deep GNN Oversmoothing

ResGCN studies deep graph neural networks for citation-network node classification. It argues that residual connection design lets a GNN train at much greater depth and reports gains through 16 layers on Cora, CiteSeer, and PubMed.

Key claims:
- Residual connection and normalization are presented as remedies for oversmoothing.
- Performance is reported on node classification benchmarks such as Cora.
- Layer-wise results suggest that depth can keep helping up to 16 layers.
- The claim is strong: residual connections appear to solve or nearly solve oversmoothing in the reported setting.

Benchmark risk:
- The result depends on split protocol, hyperparameter selection, and data leakage controls.
- A controlled re-evaluation should use fixed train/validation/test splits, repeated seeds, and identical preprocessing.

Useful diagnostics:
- Layer-wise accuracy.
- Representation similarity across nodes.
- Pairwise cosine similarity or Dirichlet energy by depth.
- Train/test leakage checks.
