---
pageType: source
id: source.knowledge-distillation-lineage
title: Knowledge Distillation Lineage
status: published
---

# Knowledge Distillation Lineage

This source summarizes a 2015-2023 knowledge distillation lineage and the uncovered gaps that should guide idea positioning.

Lineage:
- Hinton et al. introduced knowledge distillation as soft-target transfer from a teacher to a smaller student.
- FitNet extended KD by matching intermediate hints, making representation-level transfer explicit.
- CRD introduced contrastive representation distillation, improving feature relation transfer.
- ReviewKD revisited multilevel feature distillation and showed that reviewing hierarchical teacher features helps student learning.
- MaskedKD explored masked or selective distillation, reducing noisy transfer by distilling only informative regions or tokens.

What the lineage covers:
- Logit transfer from teacher to student.
- Intermediate feature matching.
- Contrastive relation transfer.
- Hierarchical feature review.
- Selective or masked distillation.

Uncovered gaps:
- Cross-architecture KD such as ViT to CNN remains underexplored.
- Cross-modal KD has limited systematic treatment.
- Imperfect teacher settings are rarely handled directly.
- OOD distillation and robustness effects are not well understood.

Positioning guidance:
- A Venn diagram can place ideas across three axes: architecture mismatch, teacher reliability, and distribution shift.
- An incremental idea changes one known component inside the lineage.
- A method improvement combines existing components with a clearer test.
- A paradigm-level idea reframes KD around imperfect teacher or OOD robustness rather than accuracy transfer alone.
- Every idea should state its delta and the specific gap it fills.
