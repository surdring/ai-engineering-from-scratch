---
name: topic-picker
description: 为语料库选择 LDA 或 BERTopic。指定库、配置参数和评估方式
version: 1.0.0
phase: 5
lesson: 15
tags: [nlp, topic-modeling]
---

给定语料库描述（文档数量、平均长度、领域、语言、计算预算），输出：

1. 算法。LDA / NMF / BERTopic / Top2Vec / FASTopic。一句话说明理由。
2. 配置。主题数量（从约 sqrt(n_docs) 开始），`min_df` / `max_df` 过滤参数，神经方法所用的嵌入模型。
3. 评估。通过 `gensim.models.CoherenceModel` 计算的主题一致性（c_v），主题多样性，外加 20 个样本的人工阅读。
4. 需探查的失败模式。对于 LDA，"垃圾主题"吸收了停用词和高频词。对于 BERTopic，-1 离群簇吞噬了模糊文档。

拒绝在文档长度超过嵌入模型上下文窗口的情况下不使用分块策略就推荐 BERTopic。拒绝在极短文本（推文、10 token 以下的评论）上使用 LDA，因为一致性会崩塌。标记任何 n_topics 选择在 5 以下或 200 以上时，对于真实数据很可能有问题。