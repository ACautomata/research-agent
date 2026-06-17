---
pageType: source
id: source.low-resource-nlp-data-harm
title: Low-Resource NLP Data Harm
status: published
---

# Low-Resource NLP Data Harm

This source challenges the default assumption that more data always helps in low-resource NLP. The evidence shows that noisy or synthetic data can reduce performance when it imports typological bias or annotation bias.

Counterexamples:
- Quechua to Spanish machine translation adds 50K synthetic examples and BLEU falls from 18.2 to 16.7.
- The suspected mechanism is language typology mismatch: Spanish SVO word order contaminates Quechua SOV patterns.
- The core typology failure is SOV vs SVO transfer: Quechua is treated as if Spanish-like word order were harmless.
- Swahili NER replaces 20 percent human annotation with GPT-4 labels and F1 drops by 4.3 points.
- The suspected mechanism is annotation bias and entity boundary drift.

Allowed benchmarks:
- FLORES-200 for machine translation.
- UD 2.13 for syntax and typology-aware diagnostics.
- MasakhaNER for African-language named entity recognition.

Research implication:
- The right problem is data quality vs quantity, not only scaling.
- Ideas should use problematization to challenge the more data assumption.
- Promising directions include language-specific data curation, typology filters, synthetic data harm detectors, and quality-weighted training sets.
