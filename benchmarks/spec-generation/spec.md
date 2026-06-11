# spec-generation Benchmark

评估 spec agent（pipeline S5）生成 claude-code 任务提示词的质量。

## 测试维度

| 维度 | 描述 | QA 覆盖 |
|------|------|---------|
| 验证实验提示词 | 基于问题分析和实验设计生成完整提示词 | seed-001 |
| 算法实现提示词 | 面向「从零实现算法」场景的提示词生成 | seed-002 |
| 缺失信息处理 | 输入材料不完整时正确使用占位符 | seed-003 |
| 边界约束 | 输出不包含论文总结、分析正文 | seed-004 |
| 汇报格式 | 提示词中包含完整的 claude-code 汇报要求 | seed-005 |

## QA 格式

每条 QA 使用 `judge: "rules"` 进行基于关键词的评分。评分维度：
- 关键词覆盖（must_contain）
- 关键词排除（must_not_contain）
- 评分细则（rubric）

## 使用

```bash
# 运行完整评测
bash benchmarks/_common/env_setup.sh
bash benchmarks/spec-generation/env.sh
python3 benchmarks/spec-generation/metrics.py

# LLM 扩增 QA
python3 benchmarks/spec-generation/build_qa.py
```
