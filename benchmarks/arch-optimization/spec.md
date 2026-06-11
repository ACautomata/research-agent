# arch-optimization Benchmark

评估 optimizer agent 的模型架构优化方案生成质量。

## 测试维度

| 维度 | QA 覆盖 |
|------|---------|
| 架构瓶颈诊断 | seed-001 |
| 模型压缩/加速 | seed-002 |
| 过拟合分析 | seed-003 |
| 注意力机制选择 | seed-004 |
| 迁移路径设计 | seed-005 |

## 使用

```bash
bash benchmarks/_common/env_setup.sh
bash benchmarks/arch-optimization/env.sh
python3 benchmarks/arch-optimization/metrics.py
```
