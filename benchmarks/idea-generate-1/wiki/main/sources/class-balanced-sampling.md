---
pageType: source
id: source.class-balanced-sampling
title: Class-Balanced Sampling
status: published
---

# Class-Balanced Sampling

Class-balanced sampling is a long-tailed learning strategy that equalizes the probability of sampling each class during training. It improves exposure for minority classes but can over-sample rare examples and increase majority class overfitting or calibration errors.

Key facts for this benchmark:
- The method targets class imbalance by changing sampling probability rather than by changing the model architecture.
- It can improve tail or minority class accuracy when raw data are highly imbalanced.
- It can harm majority class quality by repeatedly showing a small number of minority examples and reducing natural distribution coverage.
- The trade-off is a static rebalancing rule, not an adaptive distillation budget.
- In dataset distillation, class-balanced sampling suggests allocating synthetic samples per class carefully rather than using one crude fixed budget.

Research ideas should compare class-balanced sampling against trajectory matching under the same CIFAR-LT split, report balanced accuracy and minority class accuracy, and watch for majority class overfitting.
