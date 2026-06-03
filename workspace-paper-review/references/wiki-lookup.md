# Wiki 查找流程

在执行任何 pipeline 阶段前，必须先找到论文对应的 wiki 条目。Wiki 是所有后续工作的基础输入。

## 查找顺序

依次尝试，找到即停止。

### 1. 检查 outputs 目录

查看 `outputs/{论文简称}/{论文简称}-wiki.md` 是否存在。

如果 main agent 在委托时已传递 wiki 路径，直接使用，跳过后续查找。

### 2. 搜索 autoresearch 知识库

位置：`/workspace/shared/autoresearch-wiki/`（非沙箱环境可用 `../workspace-autoresearch/wiki/`）

查找方法（按推荐顺序）：

- **读索引**：读 `/workspace/shared/autoresearch-wiki/index.md`，搜索论文标题关键词，根据链接定位到具体文件
- **按标题搜文件**：在 `domains/` 下递归搜索 .md 文件，用方法名、缩写、第一作者等匹配文件名或文件内容
- **按领域推断**：如已知论文所属领域（如 federated-learning），直接进入 `domains/{domain}/papers/` 查找

### 3. 未找到时

- **有 PDF/URL**：直接读论文原文作为替代输入，在产出中标注"Wiki 缺失，基于论文原文直接提取"
- **只有标题**：告知需要补充 PDF 或先由 autoresearch 入库
- **不要自行整理 wiki**——那不是你的职责

## 格式兼容

autoresearch 的 wiki 模板（Citation / Problem Setting / Method / Experiments / Results / Limitations 等）与本 agent 下游阶段所需信息高度兼容。使用时注意：

- wiki 中的 Experiments 和 Results 对应 S2 所需的基础实验信息
- 缺少的细节（消融实验完整数据、参数敏感性曲线等）在 S2 阶段从论文原文补充
- wiki 的 evidence_level 为 skimmed 或 abstract-only 时，S2 阶段需更多依赖论文原文

## 阶段依赖

| 目标阶段 | 必需前置 |
|---------|---------|
| S2 | Wiki + 论文原文 |
| S3 | Wiki + S2 产出（*-experiment.md） |
| S4 | Wiki + S3 产出（*-problem.md） |
| S5 | Wiki + S3 + S4 产出（*-problem.md + *-validation.md） |
| S6 | S2–S5 全部产出 + Wiki |

前置缺失时自动按序补齐（S2→S3→S4→S5），不询问。补齐过程中某阶段因信息不足无法完成时，在产出中标注缺失并继续。
