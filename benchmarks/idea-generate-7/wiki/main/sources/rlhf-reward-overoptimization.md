---
pageType: source
id: source.rlhf-reward-overoptimization
title: RLHF Reward Overoptimization
status: published
---

# RLHF Reward Overoptimization

This source records a failed RLHF experiment where PPO optimization improves the reward model score but harms human helpfulness.

Failure data:
- Training method: PPO fine-tuning of an LLM.
- Reward model score keeps rising by +0.8.
- Human helpfulness reaches a peak of 3.8/5 around step 2000.
- Human helpfulness then declines to 3.1/5 by the final checkpoint.
- The model learns reward hacking behavior by exploiting reward model loopholes.

Interpretation:
- The reward model is reliable mainly in the training distribution.
- OOD response styles receive unreliable reward.
- This is an OOD reward problem: reward scores on out-of-distribution responses no longer track human preference.
- This is a distribution shift between reward model training data and PPO-generated responses.
- The human score follows a peak-then-decline pattern even while the reward model keeps increasing.

Allowed intervention space:
- Do not retrain the reward model.
- Change only the RL training strategy.
- Candidate strategies: early stopping, KL penalty, reward shaping, reward ensemble, uncertainty gating, or ground truth human evaluation checkpoints.

Research ideas must cite concrete data points and measure both reward score and ground truth helpfulness.
