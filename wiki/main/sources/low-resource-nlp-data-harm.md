# Low-Resource NLP — Challenging "More Data Always Helps"

- **Year**: various
- **Venue**: ACL / EMNLP
- **Type**: concept-summary
- **Status**: reviewed

## Default Assumption Being Challenged
**"More training data (even noisy/synthetic) always improves low-resource language model performance."**

## Counter-Evidence
1. **Quechua→Spanish MT**: Adding 50K back-translated synthetic data dropped BLEU from 18.2 to 16.7. Spanish SOV→SVO word order bias was imposed on Quechua (SOV), degrading output.
2. **Swahili NER**: Replacing 20% human annotations with GPT-4-generated labels dropped F1 by 4.3 points. LLM annotation bias favors high-resource language patterns.

## Key Insight
Data quality and typological appropriateness matter more than data quantity. Synthetic data from high-resource languages can actively harm low-resource language models by imposing foreign linguistic structures.

## Benchmarks
- **FLORES-200**: 200-language parallel text for MT evaluation.
- **UD 2.13** (Universal Dependencies): Cross-lingual syntactic annotation, includes low-resource languages.
- **MasakhaNER**: Named entity recognition benchmark for African languages.

## Constraint
Cannot collect new human annotations—must work with existing public benchmarks.
