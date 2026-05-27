---
name: skill-bpe-vs-wordpiece
description: 为给定的语料库和部署目标选择分词算法、词表大小和库
version: 1.0.0
phase: 5
lesson: 19
tags: [nlp, tokenization]
---

给定语料库（规模、语言、领域）和部署目标（从头训练 / 微调 / API 兼容推理），输出：

1. 算法。BPE、Unigram 或 WordPiece。一句话说明理由。
2. 库。SentencePiece、HF Tokenizers 或 tiktoken。说明理由。
3. 词表大小。四舍五入到最接近的 1k。理由与模型大小和语言覆盖范围相关。
4. 覆盖率设置。`character_coverage`、`byte_fallback`、特殊 token 列表。
5. 验证计划。留出集上的平均每词 token 数、OOV 率、压缩率、往返解码一致性。

拒绝在包含稀有文字内容的语料库上训练字符覆盖率 < 0.995 的分词器。拒绝在 CI 中没有冻结 `tokenizer.json` 哈希校验的情况下交付词表。标记任何 16k 以下词表的单语分词器可能能力不足。