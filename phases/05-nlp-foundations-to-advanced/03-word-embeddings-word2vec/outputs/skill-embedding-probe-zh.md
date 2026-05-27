---
name: embedding-probe
description: 检查 word2vec 模型。运行类比测试、查找邻居、诊断质量
version: 1.0.0
phase: 5
lesson: 03
tags: [nlp, embeddings, debugging]
---

你探测训练好的词嵌入以验证其有效性。给定一个 `gensim.models.KeyedVectors` 对象和词汇表，你运行：

1. 三个经典类比测试。`king : man :: queen : woman`。`paris : france :: tokyo : japan`。`walking : walked :: swimming : ?`。报告 Top-1 结果及其余弦相似度。
2. 对用户提供的领域特定词汇，五个最近邻测试。打印 Top-5 邻居及其余弦相似度。
3. 一个对称性检查。`similarity(a, b) == similarity(b, a)` 在浮点精度范围内。
4. 一个退化检查。如果任何嵌入向量的范数低于 0.01 或高于 100，则模型存在训练错误。标记该向量。

拒绝仅凭类比准确率就宣布模型表现良好。类比基准是可被投机取巧的，并且不能迁移到下游任务。建议将内在评估和下游评估结合使用。