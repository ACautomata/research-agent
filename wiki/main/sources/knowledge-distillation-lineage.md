# Knowledge Distillation Lineage (2015–2023)

- **Type**: lineage-overview
- **Status**: reviewed

## Paper Lineage

| Year | Method | Core Contribution | Key Metric |
|------|--------|-------------------|------------|
| 2015 | **Hinton KD** | Teacher soft label + temperature scaling; foundational KD paradigm | CIFAR-100: +3-5% |
| 2017 | **FitNet** | Intermediate layer feature map matching (hint-based distillation) | Extends KD to intermediate layers |
| 2019 | **CRD** | Contrastive representation distillation replaces direct feature matching | ImageNet KD gain: 2.1% → 3.8% |
| 2021 | **ReviewKD** | Cross-layer connection (student shallow → teacher deep features) | Multi-scale feature distillation |
| 2023 | **MaskedKD** | Randomly mask teacher features for student prediction; self-supervised distillation | Improved robustness |

## Uncovered Gaps
1. **Cross-architecture distillation**: All methods validated on same architecture (CNN→CNN, ResNet→ResNet). Cross-architecture (ViT→CNN) and cross-modal almost unstudied.
2. **Imperfect teacher**: All assume a near-perfect teacher. Distillation from biased/partially wrong teachers is unexplored.
3. **OOD robustness**: Impact of distillation on out-of-distribution robustness is unknown.
4. **Compute-optimal distillation**: No systematic study of compute budget allocation between teacher training vs. distillation.
