---
name: qa-architect
description: 选择问答架构、检索策略和评估计划
version: 1.0.0
phase: 5
lesson: 13
tags: [nlp, qa, rag]
---

给定需求（语料库大小、问题类型、事实性约束、延迟预算），输出：

1. 架构。抽取式（Extractive）、带抽取式阅读器的 RAG、带生成式阅读器的 RAG，或闭卷（Closed-book）LLM。一句话说明理由。
2. 检索器。无、BM25、密集检索（指定编码器如 `all-MiniLM-L6-v2`），或混合检索。
3. 阅读器。经 SQuAD 微调的模型（`deepset/roberta-base-squad2`）、指定名称的 LLM，或领域微调的 DistilBERT。
4. 评估。抽取式基准用 EM + F1；生产环境用答案准确率 + 引用准确率 + 拒答校准。说明你在测量什么以及如何测量。

拒绝为受监管或合规敏感的问题使用闭卷 LLM 答案。拒绝任何没有检索召回基线的问答系统（不知道检索器是否返回了正确的段落就无法评估阅读器）。标记需要多跳推理的问题为需要专用多跳检索器，如经 HotpotQA 训练的系统。