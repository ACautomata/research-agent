# DeepGC — Rethinking Deep GCNs and Oversmoothing

- **Year**: 2020
- **Venue**: ICLR / NeurIPS
- **Type**: paper
- **Status**: reviewed

## Summary
Systematically investigates oversmoothing in deep GNNs. Shows residual connections only delay oversmoothing; identifies split leakage in prior deep GNN results including ResGCN.

## Key Claims
1. Residual connections delay but do not eliminate oversmoothing—16+ layers → collapse.
2. Train/test split leakage can inflate accuracy for deep models.
3. In controlled experiments, deep GCNs degrade beyond ~8 layers.

## Key Limitations
1. Analysis limited to homophilic graphs (Cora/CiteSeer/PubMed).
2. Does not propose a complete solution—only diagnoses.
3. Controlled re-evaluation needed but code may be unavailable.

## Experimental Setup
- **Datasets**: Cora, CiteSeer, PubMed (same as ResGCN)
- **Models**: GCN ± residual, 2–64 layers
- **Key finding**: representation similarity collapse at 16+ layers
