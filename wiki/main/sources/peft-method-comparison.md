# PEFT Method Comparison — Ranking Reversal Across Benchmarks

- **Type**: synthesis
- **Status**: reviewed

## The Ranking Reversal

Three PEFT methods perform similarly on GLUE (±1%), but rankings completely reverse on different benchmarks:

| Method | Core Hypothesis | LongRangeQA | CodeXGLUE | MMLU-Pro |
|--------|----------------|-------------|-----------|----------|
| LoRA | Low-rank adaptation | 3rd | **1st** | 2nd |
| Prefix Tuning | Input conditioning | **1st** | 3rd | 3rd |
| IA3 | Activation rescaling | 2nd | 2nd | **1st** |

## Interpretation
- **LongRangeQA** (long-document QA): Benefits from input-conditioning (prefix)—the model needs to attend to long-range context.
- **CodeXGLUE** (code generation): Benefits from weight modification (LoRA)—code syntax requires structural changes.
- **MMLU-Pro** (knowledge retrieval): Benefits from activation gating (IA3)—selectively amplifying relevant knowledge.

## Key Unanswered Question
"What task features determine which PEFT method works best?" No existing work systematically compares PEFT methods across a task taxonomy.

## Constraints for Benchmark
- Inference-only validation (cannot train new LLMs).
- Metric: task-type × method interaction effect.
