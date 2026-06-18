---
pageType: source
id: source.deepgc-oversmoothing-rethink
title: DeepGC Oversmoothing Rethink
status: published
---

# DeepGC Oversmoothing Rethink

DeepGC revisits deep GNN oversmoothing and argues that residual connection mostly delays oversmoothing rather than eliminating it. Beyond roughly 16 layers, node representations can still collapse, especially when evaluation uses strict split protocol controls.

Key claims:
- Residual connection reduces the speed of representation collapse but does not remove the cause of oversmoothing.
- On Cora, CiteSeer, and PubMed, deep models should be compared with consistent train/test split protocol.
- The paper warns that train/test leakage or split reuse can exaggerate depth gains.
- Representation similarity should be measured layer-wise to distinguish real performance from accidental split effects.

Research implication:
- The contradiction with ResGCN should be answered through a controlled re-evaluation.
- A good idea should vary depth, residual connection type, and split protocol while recording node classification accuracy and representation similarity.
