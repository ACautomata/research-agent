---
pageType: source
id: source.prompt-based-few-shot-classification
title: Prompt-Based Few-Shot Classification
status: published
---

# Prompt-Based Few-Shot Classification

Prompt-based few-shot classification maps an input text plus a prompt template to a label verbalizer. In sentiment datasets such as SST-2 or IMDB, examples are short, labels are balanced, and exemplar selection can be done with low token cost.

Reusable components:
- Prompt template: can be reused only after rewriting the label descriptions and evidence instructions.
- Exemplar selection: useful, but long documents make each exemplar expensive.
- Verbalizers: simple sentiment words do not transfer directly to rare disease classification.

Transfer risks:
- Domain gap from movie reviews to clinical notes.
- Clinical notes often exceed 500 tokens and include abbreviations, negation, temporal status, and domain-specific terminology.
- A 1000 calls budget must be split between prompt design, exemplar screening, validation, and final evaluation.
- No fine-tune means the method must rely on API-only prompting and retrieval of compact evidence snippets.

Feasibility signal: prompt-based adaptation is plausible only if exemplars are compressed and selected by clinical relevance rather than generic semantic similarity.
