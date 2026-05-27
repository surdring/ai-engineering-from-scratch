---
name: bert-finetuner
description: 为新的分类、抽取或检索任务规划 BERT 微调方案
version: 1.0.0
phase: 7
lesson: 6
tags: [bert, fine-tuning, nlp]
---

给定下游任务（分类 / NER / 检索 / 重排序 / NLI）、标注数据量和部署约束（延迟、设备），输出：

1. 骨干选择。模型名称（ModernBERT-base / large、DeBERTa-v3、multilingual-e5 等）并附一句话理由。对于需要 ≤ 8K 上下文的英文任务，优先选择 ModernBERT。
2. 头部规格。分类：`[CLS]` → dropout → linear(num_classes)。NER：逐 token 线性 + 可选 CRF。检索：均值池化 + 对比损失。
3. 训练方案。优化器（AdamW，lr 典型为 2e-5）、预热比例（6%-10%）、训练轮数（3-5）、批次大小、fp16/bf16。
4. 评估计划。任务相关的指标（分类用准确率 + F1、NER 用实体级 F1、检索用 MRR/NDCG）。留出划分集的大小。
5. 失败模式检查。一个命名的风险：标签泄露、类别不平衡、上下文截断、预训练与微调语料库间的分词器不匹配。

拒绝微调 BERT 用于生成式输出（文本生成）— 应推荐仅解码器模型。拒绝在少数类占比低于 10% 时交付没有按类别分层评估的微调。标记任何在标注样本少于 1,000 时解冻完整骨干网络的微调可能过拟合。