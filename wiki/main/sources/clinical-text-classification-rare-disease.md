# Clinical Text Classification — Rare Disease Mention Detection

- **Year**: various
- **Venue**: JAMIA / ACL BioNLP
- **Type**: domain-summary
- **Status**: reviewed

## Summary
Medical text classification from clinical notes (MIMIC-III, i2b2). Task: identify rare disease mentions in 500+ token clinical documents.

## Domain Characteristics
1. **Long text**: Clinical notes average 500+ tokens (vs. SST-2 ~20 tokens).
2. **Extreme label imbalance**: Rare diseases <<1% prevalence.
3. **Dense domain terminology**: Medical jargon, abbreviations, negated mentions.
4. **Privacy constraints**: No fine-tuning of large models on clinical data without IRB.

## Key Challenges for Few-Shot Transfer
1. Token length 25x longer than SST-2 → exemplar selection cost and context window constraints.
2. Label imbalance → 5-shot may contain 0 positive examples for rare diseases.
3. Domain terminology → GPT-style models may hallucinate or misinterpret medical terms.
4. API call budget constraints → 1000 calls max.

## Relevant Benchmarks
- MIMIC-III clinical notes
- i2b2/VA challenge tasks
- BioCreative / BioNLP shared tasks
