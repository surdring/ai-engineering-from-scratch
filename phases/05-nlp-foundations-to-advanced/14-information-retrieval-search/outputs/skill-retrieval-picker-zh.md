---
name: retrieval-picker
description: 为给定的语料库和查询模式选择检索技术栈
version: 1.0.0
phase: 5
lesson: 14
tags: [nlp, retrieval, rag, search]
---

给定需求（语料库大小、查询模式、延迟预算、质量要求、基础设施约束），输出：

1. 技术栈。仅 BM25、仅密集检索、混合检索（BM25 + 密集 + RRF）、混合 + 交叉编码器重排序，或三路检索（BM25 + 密集 + 学习型稀疏）。
2. 密集编码器。指定具体模型（`all-MiniLM-L6-v2`、`bge-large-en-v1.5`、`e5-large-v2`、`paraphrase-multilingual-MiniLM-L12-v2`）。与语言、领域、上下文长度匹配。
3. 重排序器。如果使用，指定交叉编码器模型（`cross-encoder/ms-marco-MiniLM-L-6-v2`、`BAAI/bge-reranker-large`）。标记在 Top-30 上增加约 30-100ms 延迟。
4. 评估计划。Recall@10 是主要的检索器指标。多答案场景用 MRR。先建立基线，再在其基础上衡量渐进改进。

拒绝为包含命名实体、错误代码或产品 SKU 的语料库推荐仅密集检索方案，除非用户有证据表明密集检索能处理精确匹配。拒绝在高风险检索（法律、医疗）场景中跳过重排序，其中最终 Top-5 决定了用户的答案。