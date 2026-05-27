---
name: summary-picker
description: 选择抽取式或生成式摘要方法，指定库，添加事实性检查
version: 1.0.0
phase: 5
lesson: 12
tags: [nlp, summarization]
---

给定任务（文档类型、合规要求、长度、计算预算），输出：

1. 方法。抽取式或生成式。一句话解释原因。
2. 起始模型 / 库。明确名称。`sumy.TextRankSummarizer`、`facebook/bart-large-cnn`、`google/pegasus-pubmed`，或 LLM 提示。
3. 评估计划。ROUGE-1、ROUGE-2、ROUGE-L（使用 `rouge-score` 并启用词干提取）。如果是生成式摘要，再加事实性检查。
4. 一个需探查的失败模式。命名实体替换是生成式新闻摘要中最常见的问题；标记源实体未出现在摘要中的样本。

拒绝为医疗、法律、金融或受监管内容使用生成式摘要，除非具备事实性把关。标记超出模型上下文窗口的输入需要分块 Map-Reduce 式摘要，而非简单的截断。