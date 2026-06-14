#!/usr/bin/env python3
"""Generate all 38 new QA items and append to qa.jsonl."""
import json
from pathlib import Path

QA_PATH = Path(r"D:\Code\= =\research-agent\research-agent-main\benchmarks\idea-generate\qa.jsonl")

BASE_DIMS = [
    "evidence_grounding", "constraint_following", "idea_completeness",
    "testability", "falsifiability", "importance", "rival_awareness",
    "contribution_positioning", "risk_honesty"
]

def qa(qa_id, task_type, input_material, question, must_contain, rubric, judge="rules", weight=1.0):
    return {
        "qa_id": qa_id, "agent": "main", "target_agent": "idea-generate",
        "skill": "idea-generate", "task_type": task_type,
        "input_material": input_material, "question": question,
        "gold_answer": {"must_contain": must_contain},
        "rubric": rubric, "rubric_dimensions": BASE_DIMS,
        "pass_threshold": 0.5, "judge": judge, "weight": weight
    }

new_qas = []

# ==== PAPER-ONLY (QA-013~015) ====
new_qas.append(qa("QA-013", "paper-only",
    "研究主题：out-of-distribution generalization for vision transformers。\n论文 A 摘要：ViT 在 ImageNet 上通过 patch-based attention 优于 CNN，但在 ImageNet-C（corruption）上精度下降 30%，远超 ResNet 的 15%。可能原因：patch embedding 对高频噪声更敏感。\n论文 B 摘要：CNN 的 inductive bias（平移等变性、局部感受野）天然提供 OOD 鲁棒性，ViT 缺乏这些偏置，需要更多数据或更强的 augmentation。\n约束：CIFAR-10-C/CIFAR-100-C 小规模验证，指标为 corruption error (CE) 和 relative robustness gap。",
    "请基于两篇论文的 limitation 生成 3 个 research idea cards，目标是在不增加训练数据的前提下缩小 ViT 与 CNN 的 OOD robustness gap。",
    ["patch embedding","high-frequency","inductive bias","corruption error","robustness gap","ViT","CNN","augmentation","OOD","Fourier","regularization","attention"],
    "12 keywords。命中>=6 通过。"))

new_qas.append(qa("QA-014", "paper-only",
    "研究主题：Neural ODE 在 irregular time series 上的应用。\n论文 A 摘要：Neural ODE 将时间序列建模为连续动态系统，相比 RNN 能自然处理不规则采样，但在 PhysioNet（48h ICU 数据）上仅比 GRU-D 高 1.2% AUROC。\n论文 B 摘要：引入 attention-based time encoding 到 ODE solver，让模型感知采样间隔，在 MIMIC-III 上提升 3.5% 但计算量增加 4x。\n约束：公开 benchmark（PhysioNet/MIMIC-III），指标为 AUROC + solver steps（效率）。",
    "请基于两篇论文各自未解决的问题生成 3 个 research idea cards。",
    ["Neural ODE","irregular sampling","solver steps","AUROC","PhysioNet","time encoding","attention","continuous dynamics","GRU","efficiency","adjoint","stiffness"],
    "12 keywords。命中>=6 通过。"))

new_qas.append(qa("QA-015", "paper-only",
    "研究主题：causal representation learning for disentanglement。\n论文 A 摘要：beta-VAE 通过加大 KL 散度权重实现 disentanglement，但 reconstruction quality 显著下降，且两者的 trade-off 未被定量分析。\n论文 B 摘要：将因果图结构注入 latent space 的正则化，在 dSprites 上 disentanglement score 提升 15%，但方法要求预知 causal graph，实际场景不可用。\n约束：dSprites/Cars3D/Shapes3D 验证，指标为 MIG（Mutual Information Gap）和 FactorVAE score。",
    "请基于两篇论文的 limitation 生成 3 个 research idea cards，重点解决 disentanglement 与 reconstruction 的 trade-off 和因果先验不可用时的替代方案。",
    ["disentanglement","reconstruction trade-off","causal graph","beta-VAE","MIG","dSprites","latent space","regularization","causal prior","identifiability","spurious","intervention"],
    "12 keywords。命中>=6 通过。"))

# ==== PAPER-PLUS-CODE (QA-016~019) ====
new_qas.append(qa("QA-016", "paper-plus-code",
    "研究主题：code generation evaluation metrics。\n论文材料：CodeBERTScore 使用 BERT 嵌入计算生成代码与参考代码的语义相似度，但忽略了代码的执行正确性——语义相似但功能不同的代码仍得高分。\n代码约束：已有 HumanEval + MBPP test harness（包括 test case runner），只能改 scoring function 和 test case sampling 策略，不能改模型。\n指标：pass@k、functional correctness rate、与人工评分的 Spearman 相关系数。",
    "请生成 2-4 个低成本 idea，目标是在不改模型的前提下让 code generation 评估更贴近 functional correctness。",
    ["functional correctness","test execution","pass@k","CodeBERTScore","HumanEval","semantic similarity","scoring function","test case","execution feedback","Spearman","coverage","oracle"],
    "12 keywords。命中>=6 通过。额外：提出重训 backbone 直接 0 分。"))

new_qas.append(qa("QA-017", "paper-plus-code",
    "研究主题：adversarial attack transferability。\n论文材料：MI-FGSM 通过动量迭代提高对抗样本跨模型迁移性，但在防御模型（adversarial training/randomized smoothing）上成功率骤降至 <30%。\n代码约束：已有 5 个预训练分类器（ResNet50/ViT/ConvNeXt/Swin/MobileNet），只能改 attack generation pipeline（PGD/优化器/surrogate ensemble），不能改目标模型。\n指标：attack success rate、transfer rate、Lp perturbation budget。",
    "请生成 2-4 个低成本 idea，在不访问目标模型内部的前提下提高黑盒攻击迁移性。",
    ["transferability","black-box","surrogate ensemble","MI-FGSM","PGD","attack success rate","Lp norm","defense","gradient","momentum","decision boundary","query"],
    "12 keywords。命中>=6 通过。提出重训目标模型的 0 分。"))

new_qas.append(qa("QA-018", "paper-plus-code",
    "研究主题：multi-modal alignment for vision-language models。\n论文材料：CLIP 通过对比学习对齐图像和文本，但 fine-grained 对齐（如'红色条纹衬衫'与图像区域的对应）很差，因为全局对比损失无法建模细粒度对应。\n代码约束：已有 frozen CLIP encoders（ViT-B/32 + GPT text encoder），只能改 alignment head 和对比损失函数，不能重训 backbone。\n指标：grid-to-text retrieval recall、fine-grained alignment accuracy、zero-shot classification 不能下降。",
    "请生成 2-4 个低成本 idea，在 frozen backbone 下改善 VLM 的 fine-grained 对齐。",
    ["fine-grained","alignment","CLIP","frozen backbone","contrastive loss","local-global","patch","grid","retrieval","attention","grounding","region"],
    "12 keywords。命中>=6 通过。重训 backbone 直接 0 分。"))

new_qas.append(qa("QA-019", "paper-plus-code",
    "研究主题：knowledge distillation for object detection。\n论文材料：传统 KD 用 KL 散度对齐 teacher-student logits，但对 detection head 不适用——分类和回归分支需要不同蒸馏策略。已有方法将 classification KD 和 localization KD 分开设计，但两个损失的权重需手工调参。\n代码约束：已有 Faster R-CNN teacher（ResNet101）和 student（MobileNetV3），只能改蒸馏损失函数和权重调度，不能改 backbone 和 head 结构。\n指标：mAP@0.5:0.95、KD gain（student+KD vs student 的提升量）。",
    "请生成 2-4 个低成本 idea，改善 detection 蒸馏中分类和回归分支的自动平衡。",
    ["object detection","KD","classification head","regression head","loss balancing","teacher-student","mAP","Faster R-CNN","logit","bounding box","weight schedule","task weight"],
    "12 keywords。命中>=6 通过。"))

# ==== FAILED-EXPERIMENT-DRIVEN (QA-020~023) ====
new_qas.append(qa("QA-020", "failed-experiment-driven",
    "研究主题：RLHF reward model overoptimization。\n已失败实验：使用 PPO 微调 LLM 时，随着训练步数增加，reward model 打分持续上升（+0.8），但人工评估的 helpfulness 在第 2000 步达到峰值后开始下降（peak 3.8/5，最终 3.1/5）。即 reward model 被 overoptimized——模型学会了利用 reward model 的漏洞而非真正提升质量。\n论文 insight：reward model 只在训练分布内准确，OOD response 的 reward 不可靠。\n约束：不能重新训练 reward model，只能改 RL 训练策略（早停/正则化/reward shaping/多 reward ensemble）。",
    "请基于 reward overoptimization 失败现象生成 research ideas。每个 idea 必须引用失败实验的具体数据点。",
    ["reward hacking","PPO","helpfulness","peak-then-decline","overoptimization","OOD reward","KL penalty","reward ensemble","early stopping","reward shaping","distribution shift","ground truth"],
    "Score 0-1。加分(+0.2 each): 引用峰值时间点(2000步)和下降幅度(3.8→3.1); 提出检测 reward hacking 的监控指标; 区分 reward model 不确定性与真实质量; 给出 falsifiability 条件。扣分: 提出重训 reward model(0分); 仅建议更多人工标注(-0.2); 未讨论 OOD reward(-0.2)",
    judge="agent", weight=1.5))

new_qas.append(qa("QA-021", "failed-experiment-driven",
    "研究主题：Neural Architecture Search (NAS) 搜索成本。\n已失败实验：使用 DARTS 在 NAS-Bench-201 上搜索 cell 结构，search phase 耗费 12 GPU-hours，但最终发现的 architecture 的 test accuracy (94.1%) 与随机采样的 top-5 平均值 (93.8%) 无显著差异（p=0.34，Welch t-test）。zero-cost proxy（如 NASWOT、Synflow）虽然搜索仅需 5 秒，但与真实 accuracy 的 Spearman 相关系数在 NAS-Bench-301 上仅 0.45-0.55。\n论文 insight：search space 设计可能比 search algorithm 更重要——如果 search space 中大部分 architecture 性能接近，NAS 的收益有限。\n约束：只能用公开 NAS benchmark（NAS-Bench-201/301），不能设计新 search space。",
    "请基于 NAS 搜索成本与收益不成比例的失败现象生成 research ideas。",
    ["DARTS","zero-cost proxy","search cost","NAS-Bench","Spearman","random baseline","p-value","architecture ranking","search space","proxy quality","correlation collapse","efficiency"],
    "Score 0-1。加分(+0.2 each): 引用 p=0.34 和 Spearman 0.45-0.55 具体数字; 提出 detect search space saturated 的早期信号; 区分 search cost 与 proxy quality 的 joint optimization。扣分: 提出新 search space(0分); 声称 NAS 无用(-0.3); 未讨论 random baseline 的重要性(-0.2)",
    judge="agent", weight=1.5))

new_qas.append(qa("QA-022", "failed-experiment-driven",
    "研究主题：self-supervised pretraining 的 representation collapse。\n已失败实验：直接增加 SimSiam 的 predictor 深度（2 层→4 层）后，linear probing accuracy 反而下降（CIFAR-100: 62.3% → 58.1%），t-SNE 可视化显示 representations 退化到低维流形——即 model collapse 而非改进。减少 predictor 深度到 1 层则 accuracy 恢复到 63.5%。\n论文 insight：predictor 的架构选择对 collapse 非常敏感，stop-gradient 操作不是万能的崩溃防护。\n约束：只能改 projector/predictor 架构和损失函数，不能用负样本（保持 SimSiam 的 negative-free 特性）。",
    "请基于 predictor 深度与 representation collapse 的失败现象生成 research ideas。",
    ["SimSiam","predictor depth","collapse","t-SNE","dimensional collapse","stop-gradient","negative-free","projector","linear probing","rank","degeneration","regularization"],
    "Score 0-1。加分(+0.2 each): 引用准确率下降数据(62.3%→58.1%); 提出监测 collapse 的 online metric（如特征矩阵秩）; 区分 dimensional collapse 与 complete collapse; 给出 falsifiability 条件。扣分: 改用负样本方法(0分); 仅建议调 predictor 深度(-0.3); 未讨论负样本方法的对比(-0.1)",
    judge="agent", weight=1.5))

new_qas.append(qa("QA-023", "failed-experiment-driven",
    "研究主题：data augmentation for chest X-ray classification。\n已失败实验：将 ImageNet 标准的强 augmentation（RandAugment、CutMix）直接应用到 CheXpert 胸部 X 光片分类上，AUC 反而下降（从 0.842 降到 0.831，p=0.03）。根本原因：CutMix 产生的混合图像（例如将气胸区域粘贴到正常肺上）创建了医学上不可能的特征组合，混淆了模型。\n论文 insight：医学图像的 augmentation 必须保持解剖学/病理学合理性，domain-agnostic augmentation 可能引入虚假特征。\n约束：只能设计 augmentation 策略，不能用更大模型或更多标注数据。已有 CheXpert/Chest X-ray14 benchmark。",
    "请基于强 augmentation 在医学图像上失败的现象生成 research ideas。",
    ["CheXpert","AUC drop","CutMix","anatomical","pathological validity","RandAugment","domain-agnostic","spurious feature","medical imaging","augmentation","plausibility","segmentation mask"],
    "Score 0-1。加分(+0.2 each): 引用 AUC 下降数据(0.842→0.831, p=0.03); 提出 augmentation anatomical validity score; 利用已有 segmentation mask 做 constrained augmentation。扣分: 提出更大模型或更多标注(0分); 建议回退到弱 augmentation(-0.3); 未讨论其他医学模态的适用性(-0.1)",
    judge="agent", weight=1.5))

# ==== WEAK-EVIDENCE (QA-024~027) ====
new_qas.append(qa("QA-024", "weak-evidence",
    "研究主题：quantum neural networks for image classification。\n只有一段会议摘要：提出一种 quantum circuit encoding 方案将 MNIST 图像映射到 8-qubit 系统上，声称在 binary classification（3 vs 6）上达到 91% accuracy。缺信息：没有对比经典 baseline（线性分类器即可在这对数字上达到 99%+）；没说用了多少 training samples；没说 circuit depth 和 noise model；没在 n-qubit 与 accuracy 之间给出 scaling 趋势。\n用户要求：给出可能的 idea，但证据极弱。",
    "请生成 idea cards，标注 evidence strength，在 Open Questions 中列出所有缺失的关键信息。不得做任何 SOTA 声明。",
    ["low-confidence","classical baseline","MNIST 3vs6","binary trivial","circuit depth","noise model","scaling","quantum advantage","no evidence","reproducibility","8-qubit","missing metrics"],
    "Score 0-1。加分(+0.2 each): 声明无法生成 evidence-medium 以上 idea; 指出 3 vs 6 binary classification 在 MNIST 上过于简单; Open Questions>=5 条且逐条映射到受影响 idea; 最小实验优先做经典 baseline 复现。扣分: 声称量子优势(0分); 未标记低置信度(-0.3); risk 像 certainty(-0.2)",
    judge="agent", weight=1.5))

new_qas.append(qa("QA-025", "weak-evidence",
    "研究主题：AI-driven drug candidate screening。\n一篇 industry blog post 声称其内部模型在 kinase inhibitor 虚拟筛选中将 hit rate 从 0.1% 提升到 2%，但未提供：训练集大小/来源/分布、测试集的 temporal split 信息（是否存在 data leakage）、与 docking simulation baseline 的对比、false positive rate、外部湿实验验证的样本量和 blinding 协议。\n用户要求：给出可验证的 research idea，但证据严重不足。",
    "请生成 idea cards，标注 evidence strength，明确说明哪些 idea 依赖'假设 blog post 数据可信'这一未验证前提。",
    ["hit rate","virtual screening","data leakage","temporal split","docking baseline","blinding","false positive","proprietary","unverifiable","wet lab","kinase","assay"],
    "Score 0-1。加分(+0.2 each): 指出 blog post 数据不可审计; 区分'假设 blog 可信'的 idea 与'不依赖 blog'的 benchmark 复现 idea; 最小实验从公开 benchmark（如 DUD-E/LIT-PCBA）开始。扣分: 引用 blog 数据作为确定性事实(0分); 未区分两类 idea(-0.3); 无湿实验验证计划(-0.1)",
    judge="agent", weight=1.5))

new_qas.append(qa("QA-026", "weak-evidence",
    "研究主题：EEG-based emotion recognition with deep learning。\n一篇硕士论文的前两章（只有 intro + related work），声称使用 32 通道 EEG 和 LSTM 在 DEAP 数据集上达到 87% valence classification accuracy。缺信息：没有说明训练/测试 split 策略（subject-independent 还是 subject-dependent？后者会导致 inflated accuracy 因为同一 subject 的 EEG 高度相关）；没有报告 subject-wise standard deviation；没有与 DEAP benchmark 上的 published SOTA（典型为 60-70% subject-independent）对齐比较。\n用户要求：生成 idea cards 但标注证据不足。",
    "请生成 idea cards，特别关注 EEG-based emotion recognition 的 subject-independent vs subject-dependent evaluation protocol 这个关键 confound。",
    ["subject-independent","data leakage","DEAP","EEG","emotion recognition","evaluation protocol","subject-wise","inflated accuracy","valance","LSTM","cross-subject","confound"],
    "Score 0-1。加分(+0.2 each): 指出 subject-dependent evaluation 的 inflated accuracy 问题; 明确区分 subject-independent protocol 作为 baseline 要求; 提出复现前先确认 split protocol。扣分: 接受 87% 作为可信结果(-0.3); 未讨论 evaluation protocol(-0.3); 声称优于 DEAP SOTA(0分)",
    judge="agent", weight=1.5))

new_qas.append(qa("QA-027", "weak-evidence",
    "研究主题：LLM-based automated essay scoring for non-native English。\n一篇预印本声称其 prompt-engineered GPT 模型在 TOEFL essay scoring 上与 human rater 的相关性达到 r=0.82。缺信息：未提供 prompt template 原文（无法复现）；未比较 fine-tuned BERT baseline（如 Automated Essay Scoring shared task 的 SOTA）；未按 L1 language background 分层报告（不同母语背景的评分偏差可能完全被平均掩盖）；未说明 human rater 是单评还是双评+仲裁。\n用户要求：生成 idea cards 但严格标注证据缺口。",
    "请生成 idea cards，诚实评估当前证据下能做什么、不能做什么。",
    ["prompt template","non-native","TOEFL","rater bias","language background","fairness","BERT baseline","inter-rater","reproducibility","essay scoring","confound","stratification"],
    "Score 0-1。加分(+0.2 each): 指出 prompt template 不可复现; 按 L1 background 分层分析的必要性; 区分单评与双评+仲裁的 rater reliability 差异。扣分: 声称 GPT 优于人类评分(0分); 未讨论 fairness 和母语偏差(-0.3); 忽略 BERT baseline(-0.2)",
    judge="agent", weight=1.5))

# ==== CONSTRAINT-HEAVY (QA-028~030) ====
new_qas.append(qa("QA-028", "constraint-heavy",
    "研究主题：time series anomaly detection on edge devices。\n硬约束：部署在 Raspberry Pi 4（4GB RAM, ARM Cortex-A72），模型必须 <50MB（含权重+推理代码），推理延迟 <100ms per sample，每天最多 1 小时训练时间。\n已有 baseline：简单的 moving average + 3-sigma 规则（CPU 5ms/sample，F1=0.62 on NAB benchmark）。\n已知问题：深度学习模型（如 LSTM-AE、TranAD）在 NAB 上 F1 可达 0.80+，但模型大小为 200MB+。\n用户偏好：Python only、轻量级特征工程可接受、不需要 stream processing。",
    "请基于极强边缘计算约束（50MB/100ms/1h training）生成 2-3 个 research ideas。每个 idea 必须给出内存/延迟/训练时间的估算分解。",
    ["Raspberry Pi","50MB","100ms latency","1 hour training","anomaly detection","NAB","F1 score","LSTM-AE","model compression","feature engineering","memory budget","inference time"],
    "12 keywords。命中>=6 通过。"))

new_qas.append(qa("QA-029", "constraint-heavy",
    "研究主题：on-device keyword spotting (KWS)。\n硬约束：部署在 MCU（ARM Cortex-M4, 256KB SRAM, 1MB Flash），模型必须 <200KB（int8 量化后），推理延迟 <10ms，功耗 <5mW。\n已有 baseline：传统 MFCC + DNN classifier（80KB, F1=0.85 on Google Speech Commands v2 10-class 子集）。\n已知问题：SOTA KWS 模型（如 BC-ResNet、TC-ResNet）F1 可达 0.94，但 <200KB 约束下量化后精度衰减严重（从 0.94 降到 0.88）。\n用户偏好：TFLite Micro 兼容、PyTorch 训练 OK、不接受 cloud offloading。",
    "请基于 MCU 极强约束（200KB/10ms/5mW）生成 2-3 个 research ideas。每个 idea 必须给出参数量/存储/延迟估算。",
    ["MCU","ARM Cortex-M4","200KB","keyword spotting","MFCC","Speech Commands v2","int8 quantization","BC-ResNet","TFLite Micro","power budget","accuracy decay","feature extraction"],
    "12 keywords。命中>=6 通过。"))

new_qas.append(qa("QA-030", "constraint-heavy",
    "研究主题：real-time video action recognition on consumer GPU。\n硬约束：单张 GTX 1660（6GB VRAM），必须处理 30fps 视频流（即每帧 <33ms），batch size=1（在线推理），功耗无限制但不可用云端。\n已有 baseline：MobileNetV3-Small + TSM（Temporal Shift Module），在 UCF-101 上 top-1=78.3%，推理 22ms/frame。\n已知问题：VideoMAE/VideoSwin 等 SOTA 在 UCF-101 上 top-1=95%+，但需要 100ms+/frame，无法实时。\n约束：不能在训练时用更多 GPU，但推理时可以使用 temporal batching 如果设计得当。",
    "请基于实时视频约束（30fps/33ms/batch=1 on GTX 1660）生成 2-3 个 research ideas。",
    ["30fps","33ms latency","GTX 1660","UCF-101","TSM","MobileNet","VideoMAE","temporal","batch=1","action recognition","real-time","temporal redundancy"],
    "12 keywords。命中>=6 通过。"))

# ==== CROSS-PAPER-CONTRADICTION (QA-031~033) ====
new_qas.append(qa("QA-031", "cross-paper-contradiction",
    "研究主题：attention interpretability——attention weights 是否等于 feature importance？\n论文 A（Attention is not Explanation, 2019）：通过在 attention weights 上施加对抗扰动（不改变预测），发现完全不同的 attention 分布可产生相同预测——即 attention weights 不可靠作为解释。\n论文 B（Attention is not not Explanation, 2020）：反驳 A，声称只要正确选择'对抗扰动'的约束集——只扰动而不改变模型决策边界的先验——attention 就仍是可解释的。进一步声称 A 的扰动超出了合理范围。\n张力：A 和 B 使用同一组实验（binary text classification on SNLI/MIMIC），但 B 的实验设置不同（adversarial objective 的 constraint 不同）。核心分歧：'什么算 fair perturbation'——这本身是一个方法论争议而非技术事实。\n约束：只能做 controlled re-evaluation（不改模型），使用公开 text classification benchmark（SNLI/MIMIC/SST-2）。",
    "请识别两篇论文的核心方法论争议，并生成 2-3 个 research ideas 来澄清'什么条件下 attention 可作为解释'。",
    ["attention","interpretability","adversarial perturbation","fair perturbation","constraint set","SNLI","decision boundary","feature importance","explanation fidelity","methodology disagreement","controlled evaluation","counterfactual"],
    "12 keywords。命中>=6 通过。"))

new_qas.append(qa("QA-032", "cross-paper-contradiction",
    "研究主题：data augmentation vs architecture for small datasets。\n论文 A（CutMix, 2019）：声称对于 CIFAR-100 with limited data（只用 20% 训练集），强 augmentation（CutMix+AutoAugment）比专门设计的小数据架构（如 PyramidNet+ShakeDrop）更有效——CutMix 提升 4.2%，而架构改进仅提升 2.1%。\n论文 B（Rethinking Data Augmentation, 2021）：在相同设置下复现，发现当 training budget 从 300 epochs 增加到 1200 epochs 时，结论反转——架构改进（PyramidNet+ShakeDrop+EMA）提升 6.8%，而 CutMix 的边际收益降至 1.3%。即 augmentation 的优势来自 implicit regularization via longer effective training。\n张力：A 和 B 对'什么更有效'给出相反结论，根本原因是 training budget 不同。\n约束：只能在 CIFAR-100/Stanford Cars/FGVC-Aircraft 上验证，使用公开代码。",
    "请识别两个结论反转的根因，并生成 2-3 个 research ideas 来系统回答'小数据场景下 augmentation 和 architecture 什么时候各自更有效'。",
    ["CutMix","small dataset","training budget","epochs","architecture vs augmentation","CIFAR-100","implicit regularization","ShakeDrop","conclusion reversal","interaction effect","compute tradeoff","data regime"],
    "12 keywords。命中>=6 通过。"))

new_qas.append(qa("QA-033", "cross-paper-contradiction",
    "研究主题：early stopping vs explicit regularization for deep learning generalization。\n论文 A（2019）：在 387 个 CIFAR-10 训练配置的元分析中，发现 early stopping 与 weight decay/L2 的效果几乎完全重叠（rank correlation 0.91）——即 early stopping 和显式正则化在功能上等价，选其一即可。\n论文 B（2022）：在更大规模（ImageNet-level）和更现代架构（ViT/Swin）上重复分析，发现 early stopping 和 weight decay 的 rank correlation 降至 0.62——在过参数化模型中，early stopping 主要影响优化轨迹而非泛化边界；weight decay 的作用机制完全不同（控制 effective learning rate × weight norm）。\n张力：小规模实验结论在大规模/现代架构上不成立；两个方法的等价性取决于模型过参数化程度。\n约束：不能从头训练大型模型，但可以使用公开 pretrained checkpoint 做 fine-tuning 分析。",
    "请识别矛盾根因，生成 2-3 个 research ideas 来澄清'early stopping 和显式正则化在什么时候等价、什么时候互补'。",
    ["early stopping","weight decay","rank correlation","overparameterization","ViT","equivalence breakdown","ImageNet","optimization trajectory","generalization bound","effective learning rate","model scale","complementary"],
    "12 keywords。命中>=6 通过。"))

# ==== TRANSFER-DRIVEN (QA-034~037) ====
new_qas.append(qa("QA-034", "transfer-driven",
    "研究主题：图像 data augmentation 方法迁移到时序数据。\n源域方法：RandAugment 在图像分类上通过随机组合 14 种基础变换（旋转/翻转/色彩等），在 CIFAR/ImageNet 上稳定提升 2-3%。关键设计：(1) 全局幅度参数 M 控制所有变换强度，(2) 每 batch 随机选择 N 种变换。\n目标域：multivariate time series classification（如 UEA archive: HumanActivityRecognition, PenDigits）。特征：(1) 每个 channel 有不同的物理量纲（加速度 vs 陀螺仪），不可统一缩放；(2) 时间轴的变换（warping/pooling）会破坏因果性（不能用未来信息）；(3) channel 之间的相关性（如三轴加速度）有物理意义，不可独立扰动。\n迁移约束：只能做离线训练（batch processing），推理延迟 <50ms，必须保持时间因果性。",
    "请评估 RandAugment 从图像迁移到时序分类的可行性，逐组件分析（全局幅度、随机变换选择、变换空间定义）的可复用性，生成 2-3 个 research ideas。",
    ["RandAugment","time series","channel-wise","warping","causality","physical constraint","UEA archive","magnitude","magnitude adaptation","cross-channel","time causal","domain gap"],
    "Score 0-1。加分(+0.2 each): 定量对比图像与时序的变换空间差异; 逐组件评估(幅度可适配/变换集需重定义/随机选择可复用); 给出时序适配的变换示例。扣分: 简单套用 RandAugment 不做适配(-0.3); 违反时间因果性(-0.3); 未讨论 channel 间的物理约束(-0.2)",
    judge="agent", weight=1.5))

new_qas.append(qa("QA-035", "transfer-driven",
    "研究主题：text style transfer 方法迁移到 code refactoring。\n源域方法：Styleformer 使用 Transformer + adversarial style classifier，将非正式文本转正式（如 gonna→going to），在 GYAFC 数据集上 BLEU=38.5 + style accuracy=92%。关键组件：(1) style classifier 提供对抗信号；(2) content preservation loss 保证语义不变。\n目标域：自动 code refactoring（如 for-loop → list comprehension，mutable → immutable）。特征：(1) 代码的'语义'是执行的输入输出行为——content preservation 变成了 functional equivalence（需测试验证，而非 BLEU）；(2) 代码的'风格'有精确的 AST 约束——for→list comprehension 必须保证相同作用域和异常语义；(3) 对抗训练需要可微分编译器（不存在）。\n迁移约束：不能引入可微分编译器，只能用 Python AST + test cases 做约束。",
    "请评估 Styleformer 的 style transfer 范式迁移到 code refactoring 的可行性，逐组件分析差距，生成 2-3 个 research ideas。",
    ["code refactoring","style transfer","AST","functional equivalence","BLEU","content preservation","test case","adversarial style","differentiable compiler","syntax constraint","Styleformer","Python"],
    "Score 0-1。加分(+0.2 each): 逐组件分析可复用性; 指出 BLEU vs functional equivalence 的根本差异; 提出 AST-level constraint 方案。扣分: 简单套用 text style transfer(-0.3); 忽略 functional equivalence 验证(-0.3); 未讨论 AST 约束(-0.2)",
    judge="agent", weight=1.5))

new_qas.append(qa("QA-036", "transfer-driven",
    "研究主题：graph pooling 方法迁移到 point cloud downsampling。\n源域方法：DiffPool 在图分类中通过可微分软分配矩阵，将 N 个节点层次化聚合为 K 个 cluster（N→K 粗化），在 PROTEINS/NCI1 上提升 GNN 分类精度。关键：(1) 分配矩阵 S 由 GNN 生成，(2) 粗化后的图保留邻接结构。\n目标域：3D point cloud downsampling for classification（如 ModelNet40 keypoint selection）。特征：(1) 点云没有显式邻接矩阵——需基于 k-NN/radius 动态构图；(2) 3D 空间有刚体变换不变性要求（SE(3) invariance）——graph pooling 的分配矩阵不是 SE(3)-invariant；(3) 点云密度不均匀——近处点密、远处点稀，固定 K 的粗化会偏向近处。(4) 局部几何特征（法向量/曲率）可能需要额外的编码。\n迁移约束：已有 PointNet++ baseline，只能改 downsampling 策略。",
    "请评估 DiffPool 从图池化迁移到点云下采样的可行性，重点关注 SE(3)-invariance 和密度不均的挑战，生成 2-3 个 research ideas。",
    ["DiffPool","point cloud","downsampling","SE(3)","k-NN graph","density","assignment matrix","invariance","ModelNet40","PointNet++","farthest point","geometric"],
    "Score 0-1。加分(+0.2 each): 指出 SE(3)-invariance 是核心迁移障碍; 讨论密度自适应的粗化策略; 逐组件评估（分配矩阵需重设计/邻接构建可适配/GNN encoder 可复用）。扣分: 直接套用 DiffPool(-0.3); 未讨论 invariance(-0.3); 忽略密度问题(-0.2)",
    judge="agent", weight=1.5))

new_qas.append(qa("QA-037", "transfer-driven",
    "研究主题：tabular imputation 方法迁移到 missing modality imputation。\n源域方法：MIWAE（Deep Generative Missingness Model）使用 VAE + importance weighting 在 UCI 数据集上做缺失值补全，关键优势：在 MAR（Missing At Random）和 MNAR（Missing Not At Random）下均有效。\n目标域：多模态学习的 missing modality——例如 audio-visual speech recognition 中 video stream 间歇性缺失（camera occlusion），或 medical diagnosis 中某些 lab test 未做。特征：(1) 模态缺失通常是模态级（整个 modality missing）而非特征级（个别特征 missing）；(2) 模态间有 shared semantics——video+audio 共同表达说话内容，可以用可用模态推断缺失模态；(3) 缺失机制通常是 MNAR——lab test 不做是因为医生认为不需要（informative missingness）；(4) 补全的目标不是重建原始模态，而是提取对下游任务有用的特征。\n迁移约束：只能用公开多模态数据集（AVSpeech/CMU-MOSEI/MIMIC-IV），不能访问缺失模态的真实值用于验证。",
    "请评估 MIWAE 的 VAE+importance weighting 范式从表格缺失值补全迁移到多模态缺失补全的可行性，生成 2-3 个 research ideas。",
    ["missing modality","MIWAE","VAE","importance weighting","MNAR","MAR","multimodal","task-relevant imputation","shared semantics","audio-visual","informative missingness","cross-modal"],
    "Score 0-1。加分(+0.2 each): 区分模态级缺失 vs 特征级缺失; 讨论 MNAR in medical setting 的挑战; 提出下游任务导向而非重建质量导向的补全评估。扣分: 直接套用 MIWAE(-0.3); 忽略 MNAR(-0.3); 未讨论无法验证真实模态值的问题(-0.2)",
    judge="agent", weight=1.5))

# ==== ASSUMPTION-CHALLENGE (QA-038~042) ====
new_qas.append(qa("QA-038", "assumption-challenge",
    "研究主题：低资源语言的 NLP——挑战'more data always helps'的默认假设。\n默认假设：更多训练数据（即使是 noisy/synthetic）总是提升低资源语言模型性能。\n反例证据：(1) 在 Quechua→Spanish 机器翻译中，加入 50K 从西班牙语反向翻译的 synthetic parallel data 后，BLEU 反而从 18.2 降到 16.7——synthetic data 将西班牙语的词序偏好强加于 Quechua (SOV vs SVO 差异)；(2) 在 Swahili NER 中，用 GPT-4 生成的标注数据替代 20% 人工标注后，F1 下降 4.3 点——LLM 的标注偏好偏向 high-resource language patterns。\n约束：只能做公开低资源语言 benchmark（FLORES-200/UD 2.13/MasakhaNER），不能收集新人工标注。",
    "请识别自然语言处理中'more data always helps'这个默认假设，用反例证据挑战它，生成 2-3 个超越这个假设的 research ideas。不要只做 gap-spotting。",
    ["more data assumption","low-resource","synthetic data harm","language typology","SOV vs SVO","data quality vs quantity","MasakhaNER","FLORES","annotation bias","problematization","language-specific","data curation"],
    "Score 0-1。加分(+0.2 each): 显式命名'data quantity = data quality'假设并用反例挑战; 引用具体 BLEU/F1 下降数字; 提出超越该假设的 paradigm-level idea。扣分: 只做 gap-spotting 不提假设(-0.4); 声称数据总是好(-0.3); 无 falsifiability 条件(-0.15)",
    judge="agent", weight=1.5))

new_qas.append(qa("QA-039", "assumption-challenge",
    "研究主题：heterophilic graphs 上的 GNN——挑战'deeper GNNs capture better representations'的默认假设。\n默认假设：更深的 GNN（更多层）能捕获更长程的依赖，从而提升节点分类性能。\n反例证据：(1) 在 heterophilic graph benchmark（Roman-Empire/Amazon-Ratings/Questions）上，2 层 GCN 的 accuracy 为 63.2%，加深到 8 层后反而降至 51.1%——heterophily 导致邻居信息与中心节点标签负相关，加深会放大错误信号；(2) LINKX（仅用 MLP on raw features + adjacency features）在 Questions 数据集上 2 层就达到 74.1%，超过 8 层 GCN 的 51.1% 超过 23 个点——说明 heterophilic 图上的有效信息主要在节点特征本身，而非邻居聚合。\n约束：只能在公开 heterophilic benchmark（Roman-Empire/Amazon-Ratings/Questions/Chameleon）上验证。",
    "请识别并挑战 GNN 领域'deeper is always better'的默认假设，生成 2-3 个范式级 research ideas。",
    ["heterophily","depth degradation","neighbor aggregation","negative signal","LINKX","GCN","Roman-Empire","MPNN assumption","feature vs topology","homophily assumption","adaptive depth","message passing"],
    "Score 0-1。加分(+0.2 each): 命名'homophily assumption of message passing'为被挑战的默认假设; 引用具体 accuracy 下降和 LINKX 对比数据; 提出挑战 MPNN 范式本身的 idea。扣分: 只做改进 GCN 不做范式挑战(-0.4); 未讨论 heterophily 的本质(-0.2)",
    judge="agent", weight=1.5))

new_qas.append(qa("QA-040", "assumption-challenge",
    "研究主题：长序列处理——挑战'attention captures all dependencies'的默认假设。\n默认假设：Transformer 的 self-attention 可以捕获任意距离的依赖关系，注意力图反映了 token 间的真实语义关联。\n反例证据：(1) 在 Long Range Arena (LRA) benchmark 的 Pathfinder 任务（判断两点是否由路径连接）上，标准 Transformer 的 accuracy 仅 50.3%（≈随机猜测），而状态空间模型 S4 达到 92.3%——self-attention 在需要精确空间推理的长程任务上完全失败；(2) 注意力图可视化显示，在后层中大多数 token 的注意力集中在 [CLS] 和前几个 token（所谓的 attention sink），而非语义相关的 token——即注意力机制退化为固定的静态模式，失去动态选择能力。\n约束：只能在 LRA benchmark 上验证，不设计新的长序列任务。",
    "请识别并挑战'attention captures all dependencies'的默认假设，特别注意 attention sink 现象，生成 2-3 个范式级 research ideas。",
    ["attention sink","Long Range Arena","Pathfinder","S4","SSM","static pattern","spatial reasoning","self-attention failure","diluted attention","long-range dependency","attention collapse","selective mechanism"],
    "Score 0-1。加分(+0.2 each): 命名'attention as universal dependency capture'为默认假设; 引用 Pathfinder 50.3% vs S4 92.3% 具体数据; 提出超越 attention 的 alternative mechanism。扣分: 只做 attention 变体改进不做范式挑战(-0.4); 忽视 attention sink 现象(-0.2)",
    judge="agent", weight=1.5))

new_qas.append(qa("QA-041", "assumption-challenge",
    "研究主题：对比学习中的 batch size——挑战'larger batch = better representations'的默认假设。\n默认假设：更大的 batch size 提供更多负样本，从而学到更好的表征。SimCLR 在 batch=8192 时 ImageNet linear eval 达到 70.0%，batch=256 时仅 62.4%。\n反例证据：(1) MoCo v3 发现当 batch 从 4096 提升到 6144 时，ViT 的 training 变得不稳定，出现 spike——不是因为 memory，而是大 batch 下梯度统计性质改变；(2) BYOL 完全不需要负样本（batch=4096 时 74.3% vs SimCLR batch=8192 时 70.0%），说明'负样本数量 = 表征质量'的假设可能从根本上错误；(3) 在 long-tailed 数据（iNaturalist 2018）上，大 batch 对比学习导致 tail class 的表征 collapse 到少数方向——即大 batch 在类别不均衡时放大 bias。\n约束：只能在 ImageNet-100 / iNaturalist 2018 子集上验证，batch size 受 8×A100 80GB 限制。",
    "请识别并挑战对比学习中'larger batch always better'的默认假设，特别关注 BYOL negative-free 范式和不均衡数据下的退化，生成 2-3 个范式级 research ideas。",
    ["batch size","contrastive learning","negative samples","BYOL","SimCLR","negative-free","long-tailed","representation collapse","gradient statistics","MoCo","tail class","positive-only"],
    "Score 0-1。加分(+0.2 each): 命名'negative sample count = representation quality'为默认假设; 引用 BYOL 的 negative-free 成功作为关键反例; 讨论 long-tailed 下的退化机制。扣分: 只做 batch size tuning 不做范式挑战(-0.4); 忽略 BYOL 的 implication(-0.3)",
    judge="agent", weight=1.5))

new_qas.append(qa("QA-042", "assumption-challenge",
    "研究主题：医学图像分析的迁移学习——挑战'ImageNet pretraining helps all vision tasks'的默认假设。\n默认假设：在 ImageNet 上预训练的模型为所有下游视觉任务提供有用的特征，包括医学图像。\n反例证据：(1) 在 CheXpert（胸部 X 光）上，随机初始化的 DenseNet-121 经过充分训练后 AUC=0.842，ImageNet 预训练版本 AUC=0.841——无差异（p=0.78）；(2) 在 MIMIC-CXR 上随机初始化 vs ImageNet pretrained 的差距仅 0.5%，但用相同的 compute budget 训练 2x epochs（随机初始化）反而超过 pretrained 版本 1.2%；(3) ImageNet 的纹理偏置（texture bias）可能在医学图像中引入虚假相关性——X 光片中的诊断信息主要在形状/边界/密度，而非纹理；(4) 对于 3D 医学图像（CT/MRI），ImageNet pretraining 只能初始化 2D slice encoder，丢失了关键的 volumetric context。\n约束：只能在公开医学图像数据集（CheXpert/MIMIC-CXR/RadImageNet）上验证。",
    "请识别并挑战'ImageNet pretraining universally helps'的默认假设，用医学图像的反例证据分析 ImageNet 的 texture bias 与医学诊断 shape-based nature 的根本冲突，生成 2-3 个范式级 research ideas。",
    ["ImageNet","medical imaging","texture bias","shape-based","CheXpert","pretraining","random init","volumetric","2D vs 3D","domain gap","RadImageNet","task-specific pretraining"],
    "Score 0-1。加分(+0.2 each): 命名'natural image features transfer to medical domain'为默认假设; 引用 CheXpert p=0.78 无差异和 MIMIC-CXR 反超数据; 分析 texture bias vs shape-based diagnosis 的根本冲突; 提出医学专用预训练范式。扣分: 只建议换 backbone 不做范式挑战(-0.4); 忽视 3D 语境(-0.2)",
    judge="agent", weight=1.5))

# ==== LINEAGE-CONTEXTUALIZED (QA-043~050) ====
new_qas.append(qa("QA-043", "lineage-contextualized",
    "研究谱系：knowledge distillation。\n[2015] Hinton et al. — 提出 KD 基础范式：teacher soft label + temperature scaling。CIFAR-100 提升 3-5%。\n[2017] FitNet — 加入中间层 feature map 匹配（hint-based）。\n[2019] CRD — 用对比学习取代直接 feature matching。ImageNet 上 KD gain 从 2.1% 扩大到 3.8%。\n[2021] ReviewKD — 跨层连接（student shallow→teacher deep）。\n[2023] MaskedKD — 随机 mask teacher features for student prediction。\n当前 uncovered gaps: (1) 所有 KD 方法都在同架构验证，跨架构（ViT→CNN）和跨模态几乎无研究；(2) teacher 本身不完美时（biased/partially wrong）的蒸馏策略；(3) 蒸馏对 OOD robustness 的影响未知。",
    "请基于这个知识蒸馏的 5 篇论文谱系（2015-2023），在谱系中定位 2 个 research ideas。每个 idea 必须：(1) 画出它在这个谱系中的位置；(2) 说明已有工作覆盖了什么、留下了什么 gap；(3) 诚实标注增量大小（范式级/方法改进/微调变体）。",
    ["Hinton","FitNet","CRD","ReviewKD","MaskedKD","cross-architecture","imperfect teacher","OOD distillation","lineage","incremental","paradigm","gap","Venn diagram","uncovered","delta"],
    "15 keywords。命中>=7 通过。额外：必须给出谱系定位描述。"))

new_qas.append(qa("QA-044", "lineage-contextualized",
    "研究谱系：graph attention mechanisms。\n[2018] GAT — 首个将 attention 引入 GNN。Cora/CiteSeer/PubMed 上超越 GCN 1-3%。\n[2019] GATv2 — 修复静态 attention 问题，改用动态 attention。\n[2020] SuperGAT — 用 self-supervised edge prediction 增强 attention 学习。\n[2021] Graph Transformer (GT) — 加入 positional encoding、edge features，使 GNN attention 接近 standard Transformer。\n[2022] NodeFormer — kernelized attention 将 O(N^2) 降到 O(N)。\n[2023] SGFormer — 单层 attention propagation 质疑'deep attention for graphs'的必要性。\n当前 uncovered gaps: (1) heterophilic graphs 上 attention 的 benefit 不明确；(2) attention 可解释性在 GNN 中从未被严格验证；(3) 动态图上的 attention 几乎未被探索。",
    "请基于这个 graph attention 的 6 篇论文谱系（2018-2023），在谱系中定位 2 个 research ideas。",
    ["GAT","GATv2","SuperGAT","Graph Transformer","NodeFormer","SGFormer","heterophilic","temporal graphs","scalability","interpretability","dynamic attention","positional encoding","lineage","O(N)"],
    "14 keywords。命中>=7 通过。"))

new_qas.append(qa("QA-045", "lineage-contextualized",
    "研究谱系：diffusion model fast sampling。\n[2020] DDPM — 1000 步采样，FID=3.17，推理需数分钟。\n[2021] DDIM — 确定性采样，100 步，推理加速 10x。\n[2022] DPM-Solver — ODE solver 数值方法，10-20 步达 SOTA。\n[2022] Progressive Distillation — teacher(1024 steps)→student(8 steps)。\n[2023] Consistency Models — 单步映射，无需迭代。CIFAR-10 单步 FID=6.2。\n[2024] LCM-LoRA — consistency distillation 适配 Stable Diffusion，4-step 高质量生成。\n当前 uncovered gaps: (1) Consistency Models 单步质量在复杂场景仍落后；(2) 条件生成下的 trade-off 曲线 vs 无条件生成完全不同；(3) 加速方法对 safety/fairness 的影响未知。",
    "请基于 diffusion 加速采样的 6 篇论文谱系（2020-2024），在谱系中定位 2 个 research ideas。",
    ["DDPM","DDIM","DPM-Solver","Progressive Distillation","Consistency Models","LCM","sampling steps","FID","single-step","ODE solver","distillation","conditioned tradeoff","safety","lineage"],
    "14 keywords。命中>=7 通过。"))

new_qas.append(qa("QA-046", "lineage-contextualized",
    "研究谱系：parameter-efficient fine-tuning (PEFT)。\n[2019] Adapter — bottleneck 模块，~3% 参数。GLUE 接近 full fine-tuning。\n[2021] Prefix Tuning — 输入前加可学习 token，<0.1% 参数。\n[2021] LoRA — 低秩分解，<1% 参数，zero inference overhead。\n[2022] (IA)^3 — 三组缩放向量，<0.01% 参数。\n[2023] QLoRA — LoRA + 4-bit 量化，65B 模型单卡 fine-tune。\n[2024] DoRA — magnitude + direction 分解。\n当前 uncovered gaps: (1) multi-task/continual PEFT 几乎未探索；(2) LoRA rank 选择缺乏理论基础；(3) 不同 PEFT 方法的组合效果与交互未知。",
    "请基于 PEFT 的 6 篇论文谱系（2019-2024），在谱系中定位 2 个 research ideas。",
    ["Adapter","Prefix Tuning","LoRA","IA3","QLoRA","DoRA","multi-task PEFT","rank theory","method combination","continual PEFT","reparameterization","parameter efficiency","lineage","composability"],
    "14 keywords。命中>=7 通过。"))

new_qas.append(qa("QA-047", "lineage-contextualized",
    "研究谱系：self-supervised contrastive learning for vision。\n[2020] SimCLR — 对比学习+大batch(8192)，ImageNet linear eval 70.0%。projection head 很重要。\n[2020] MoCo v2 — momentum encoder + memory bank 解耦 batch dependency。\n[2020] BYOL — 完全不需要负样本！positive-only 学习，74.3%。\n[2021] SimSiam — 连 momentum encoder 都不需要，stop-gradient 防 collapse。质疑 BYOL 的 momentum 是否必要。\n[2021] DINO — 自监督 ViT attention map 自动产生语义分割——无需 pixel-level 监督。\n[2022] MAE — 转向 mask-and-reconstruct 范式(generative)，证明对比学习不是唯一路径。\n当前 uncovered gaps: (1) 简化路径在细粒度/长尾/医疗图像上是否同样有效？(2) 不同 SSL 方法在哪种下游任务上各自最优？(3) SSL 预训练的计算最优分配没有系统回答。",
    "请基于 SSL 对比学习的 6 篇论文谱系（2020-2022），在谱系中定位 2 个 research ideas。",
    ["SimCLR","MoCo","BYOL","SimSiam","DINO","MAE","negative-free","projection head","stop-gradient","momentum encoder","generative vs contrastive","compute allocation","downstream specificity","lineage"],
    "14 keywords。命中>=7 通过。"))

new_qas.append(qa("QA-048", "lineage-contextualized",
    "研究谱系：adversarial training for robustness。\n[2015] FGSM — 单步攻击+对抗训练，快速但防御有限。\n[2018] PGD — 多步迭代攻击，CIFAR-10 robust accuracy 45-50%，但 clean accuracy 95%→87%。核心 insight：robustness-accuracy trade-off。\n[2019] TRADES — 公式化 trade-off：clean loss + beta * robust boundary loss。\n[2020] AWP — Adversarial Weight Perturbation，寻找更平坦 loss landscape。\n[2021] Perceptual Adversarial Training — Lp-bounded attacks 不反映人类感知，语义级攻击 Lp-robust 模型几乎无防御。\n[2023] Denoised Smoothing — 扩散去噪+随机平滑认证。ImageNet 首次 L2 radius=1.0 下 certified accuracy>40%。\n当前 uncovered gaps: (1) ImageNet-scale 收敛性质完全不同；(2) adversarial training 对 fairness 的影响——不同 subgroup 的 robust accuracy 是否均匀？(3) 针对对抗训练的 meta-attack。",
    "请基于对抗训练的 6 篇论文谱系（2015-2023），在谱系中定位 2 个 research ideas。",
    ["FGSM","PGD","TRADES","AWP","perceptual attack","Denoised Smoothing","clean-robust tradeoff","fairness","certified radius","meta-attack","LPIPS","loss landscape","ImageNet-scale","lineage"],
    "14 keywords。命中>=7 通过。"))

new_qas.append(qa("QA-049", "lineage-contextualized",
    "研究谱系：federated learning personalization。\n[2017] FedAvg — 联邦学习基础。IID 效果好，non-IID 下降 10-20%。\n[2020] FedProx — proximal term 约束本地更新不偏离全局。\n[2020] Per-FedAvg — 重新定义为 meta-learning：学习好全局初始化。\n[2021] Ditto — 同时训练全局+个性化本地模型，极端 non-IID 下显著优于 FedAvg+fine-tuning。\n[2022] FedRep — shared representation + personalized head。representation 全局共享，classifier 本地个性化。\n[2023] pFedBayes — Bayesian 框架统一 FL personalization，提供不确定性估计。\n当前 uncovered gaps: (1) 真实 FL 的 non-IID 有更复杂结构（temporal shift/concept drift/adversarial clients）；(2) personalization 和 privacy 的联合优化——DP 约束可能与个性化冲突；(3) multi-modal FL（clients 不同 data modality）完全没有被现有方法覆盖。",
    "请基于联邦学习个性化的 6 篇论文谱系（2017-2023），在谱系中定位 2 个 research ideas。",
    ["FedAvg","FedProx","Per-FedAvg","Ditto","FedRep","pFedBayes","non-IID","personalization","meta-learning","privacy-personalization tradeoff","multi-modal FL","concept drift","representation sharing","lineage"],
    "14 keywords。命中>=7 通过。"))

new_qas.append(qa("QA-050", "lineage-contextualized",
    "研究谱系：LLM reasoning enhancement。\n[2022] Chain-of-Thought (Wei et al.) — GSM8K accuracy 从 18% 跃升至 58%。reasoning 仅从 prompting 涌现。\n[2022] Self-Consistency (Wang et al.) — 多条 CoT + 投票，GSM8K 提升到 74%。\n[2023] Tree-of-Thought (Yao et al.) — 线性链→搜索树，允许回溯。Game of 24 从 CoT 4%→74%。\n[2023] ReAct (Yao et al.) — reasoning 与 tool use 交错：思考→调用工具→反思→再思考。\n[2024] Quiet-STaR (Zelikman et al.) — 每个 token 位置并行生成内部思考，REINFORCE 优化。模型自己学会'何时该思考'。\n[2025] DeepSeek-R1 (DeepSeek-AI) — pure RL 训练 LLM 产生 long chain-of-thought。reasoning 从 RL reward 自发涌现。\n当前 uncovered gaps: (1) CoT→Tree-of-Thought→ReAct 增加了搜索成本(O(L)→O(B^D))，效率 vs accuracy 的 Pareto frontier 未系统研究；(2) Quiet-STaR 和 R1 证明'reasoning 可以不需要 human CoT 数据'，但自发涌现 reasoning 的可控性和安全性完全未探索；(3) multi-agent debate reasoning 在数学之外的领域效果未知。",
    "请基于 LLM reasoning 的 6 篇论文谱系（2022-2025），在谱系中定位 2 个 research ideas。",
    ["Chain-of-Thought","Self-Consistency","Tree-of-Thought","ReAct","Quiet-STaR","DeepSeek-R1","reasoning cost","Pareto frontier","emergent reasoning","safety","multi-agent debate","search efficiency","no-human-demonstration","lineage"],
    "14 keywords。命中>=7 通过。"))

# Write all to file
lines = []
for q in new_qas:
    lines.append(json.dumps(q, ensure_ascii=False))

# Append to existing qa.jsonl
existing = QA_PATH.read_text(encoding="utf-8").rstrip()
QA_PATH.write_text(existing + "\n" + "\n".join(lines) + "\n", encoding="utf-8")

print(f"Generated {len(new_qas)} new QAs")
print(f"QA range: QA-013 ~ QA-050")
print(f"Total in file: {len(QA_PATH.read_text(encoding='utf-8').splitlines())}")

# Validate
all_ok = True
for i, line in enumerate(QA_PATH.read_text(encoding="utf-8").strip().split("\n")):
    if not line.strip():
        continue
    try:
        obj = json.loads(line)
        dims = len(obj.get("rubric_dimensions", []))
        if dims != 9:
            print(f"WARN: Line {i+1} ({obj.get('qa_id')}) has {dims} dims")
            all_ok = False
    except json.JSONDecodeError as e:
        print(f"ERROR: Line {i+1}: {e}")
        all_ok = False

if all_ok:
    print("All lines valid JSON with 9 dimensions")
