# Continual Learning — Catastrophic Forgetting Under Extreme Constraints

- **Year**: various
- **Venue**: PNAS / ICML / NeurIPS
- **Type**: concept-summary
- **Status**: reviewed

## Summary
Continual (incremental) learning studies how models can learn sequential tasks without forgetting previous ones. Core phenomenon: **catastrophic forgetting** — performance on earlier tasks degrades severely when training on new tasks.

## Key Methods Discussed
1. **Replay buffer**: Store a small subset of old task data and interleave during new task training.
2. **Regularization**: EWC (Elastic Weight Consolidation), SI (Synaptic Intelligence) — penalize changes to important weights.
3. **Progressive networks**: Add new capacity for each task (grows model size).

## Constraint Context for QA-009
- **Hardware**: CPU only (no GPU), max 2 hours training.
- **Data**: CIFAR-100 split into 10 sequential tasks.
- **Baseline**: Finetuning (PyTorch, serial task training).
- **Known failure**: After task 5, task 1 accuracy drops from 70% to 25%.
- **User preference**: Low-risk, Python only, lightweight regularization or replay buffer.

## Key Metrics
- Forgetting rate: (max accuracy - final accuracy) / max accuracy
- Average accuracy across all tasks after training
- Backward transfer: how much learning task T+1 hurts task T

## Key Limitation
The extreme CPU + 2h constraint rules out most SOTA methods (memory replay with large buffers, meta-learning, architecture search).
