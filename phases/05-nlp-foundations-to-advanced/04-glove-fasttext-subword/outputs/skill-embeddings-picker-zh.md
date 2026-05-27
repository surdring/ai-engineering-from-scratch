---
name: skill-embeddings-picker
description: 为新的语言模型或文本流水线选择分词方法
version: 1.0.0
phase: 5
lesson: 04
tags: [nlp, tokenization, embeddings]
---

给定任务和数据集描述，你输出：

1. 分词策略（词级、BPE、WordPiece、SentencePiece、字节级 BPE）。一句话说明理由。
2. 词表大小目标。仅英文 LM：32k。多语言：64k-100k。代码：50k-100k。
3. 库调用及确切的训练命令。命名库（Hugging Face `tokenizers`、`sentencepiece`）。引用参数。
4. 一个可复现性陷阱。分词器与模型不匹配是最常见的静默生产故障。指明哪个分词器对应哪个预训练检查点，警告不要混用。

当用户微调预训练 LLM 时，拒绝推荐训练自定义分词器（微调必须使用预训练分词器）。拒绝推荐任何生产推理路径使用词级分词。标记非英语或多文字语料需要 SentencePiece 加字节回退。