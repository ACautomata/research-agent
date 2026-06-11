# tuning-advice Benchmark

评估 tuning agent 的调参优化方案生成质量。

## 测试维度

| 维度 | 描述 | QA 覆盖 |
|------|------|---------|
| 参数分析 | 基于代码仓库和配置文件的完整调参方案 | seed-001, qa-001, qa-002 |
| 预算约束 | 有限预算下的调参策略 | seed-002, qa-003 |
| 策略推荐 | 为不同场景推荐搜索策略 | seed-003, qa-004 |
| 评估方案设计 | 调参结果的可靠性验证 | seed-004 |
| 参数范围推荐 | 经验搜索范围参考 | seed-005 |
| 多目标优化 | 同时优化多个指标的方案 | qa-005 |

## QA 格式

每条 QA 使用 `judge: "rules"` 进行基于关键词的评分。

## 使用

```bash
bash benchmarks/_common/env_setup.sh
bash benchmarks/tuning-advice/env.sh
python3 benchmarks/tuning-advice/metrics.py
```
