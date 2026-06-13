# Prompt-Based Few-Shot Text Classification

- **Year**: 2020–2022
- **Authors**: Gao et al. / Schick et al. / Brown et al. (GPT-3)
- **Venue**: ACL / NeurIPS
- **Type**: paper
- **Status**: reviewed

## Summary
Uses GPT-style API with 5-shot exemplar selection + prompt template engineering for text classification. Demonstrates strong performance on sentiment analysis benchmarks (SST-2, IMDB).

## Key Claims
1. Prompt-based few-shot learning matches or exceeds fine-tuned small models on sentiment tasks.
2. Only 5 exemplars + template engineering needed.
3. No fine-tuning required—API-only access.

## Key Limitations
1. Evaluated only on short, balanced, common-domain text (movie reviews, sentiment).
2. Domain gap to specialized text (clinical, legal, technical) is unstudied.
3. Exemplar selection and prompt template quality are critical but fragile.

## Experimental Setup
- **Source benchmarks**: SST-2, IMDB (sentiment, short text, balanced labels)
- **Method**: GPT-style API, 5-shot, prompt template engineering
- **Metrics**: Accuracy, F1
