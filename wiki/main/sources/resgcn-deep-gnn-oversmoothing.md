# ResGCN — Residual GCN for Deep Graph Neural Networks

- **Year**: 2019
- **Venue**: ICML / NeurIPS
- **Type**: paper
- **Status**: reviewed

## Summary
Proposes residual connections in GCNs for deep architectures (>8 layers). Claims residual connections resolve oversmoothing.

## Key Claims
1. 16-layer ResGCN achieves SOTA on Cora, CiteSeer, PubMed.
2. Residual connections prevent oversmoothing via gradient flow and feature reuse.

## Key Limitations
1. **Split protocol controversy**: Later work found train/test split leakage inflating accuracy.
2. **Oversmoothing delayed, not eliminated**: Beyond 16 layers, representations still collapse.
3. Results may not generalize beyond specific split protocol.

## Experimental Setup
- **Datasets**: Cora, CiteSeer, PubMed
- **Model**: GCN + residual, 2–16 layers
- **Metrics**: Node classification accuracy
