---
pageType: source
id: source.clinical-text-classification-rare-disease
title: Clinical Text Classification for Rare Disease
status: published
---

# Clinical Text Classification for Rare Disease

Clinical rare disease detection is a long-document classification task. Notes can exceed 500 tokens, mention symptoms indirectly, and contain negated or historical findings. Positive labels are extremely rare, often below 1 percent.

Constraints for this benchmark:
- No fine-tune of a large model.
- API-only access.
- Total budget: 1000 calls.
- Target metric should reflect label imbalance, for example recall at fixed precision, macro-F1, or rare disease sensitivity.

Transfer challenges:
- Clinical notes are much longer than SST-2 or IMDB reviews.
- Label imbalance makes naive accuracy useless.
- Exemplar selection must represent rare positives, hard negatives, and negation patterns.
- A clinical prompt template should ask for evidence spans and uncertainty, not only a label.

Competitive alternative: zero-shot prompt plus rules for high-precision disease terms may beat few-shot transfer if exemplar cost consumes the 1000 calls budget.
