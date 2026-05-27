---
name: multilingual-picker
description: 为多语言 NLP 任务选择源语言、目标模型和评估计划
version: 1.0.0
phase: 5
lesson: 18
tags: [nlp, multilingual, cross-lingual]
---

给定需求（目标语言、任务类型、每种语言可用的标注数据），输出：

1. 微调的源语言。默认用英语；如果目标语言有类型学上相近的高资源语言，查阅 LANGRANK 或 qWALS。
2. 基础模型。XLM-R（分类）、mT5（生成）、NLLB（翻译）、Aya-23（生成式 LLM）。
3. Few-shot 预算。如果可用，从 100-500 个目标语言样本开始。仅在标注不可行时使用零样本。
4. 评估计划。每种语言的准确率（而非汇总指标）、跨语言一致性、非拉丁文字上的实体级 F1。

拒绝不做逐语言评估就交付多语言模型 — 汇总指标会掩盖长尾失败。标记分词覆盖率低的文字（阿姆哈拉语、提格里尼亚语、许多非洲语言）需要具备字节回退的模型（SentencePiece 设置 byte_fallback=True，或 GPT-2 等字节级分词器）。