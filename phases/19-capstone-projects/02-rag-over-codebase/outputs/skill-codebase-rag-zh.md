---
name: codebase-rag
description: 构建跨仓库语义搜索系统，具有 AST 感知分块、混合检索、增量重索引和带引用的答案。
version: 1.0.0
phase: 19
lesson: 02
tags: [capstone, rag, code-search, tree-sitter, qdrant, bm25, hybrid-retrieval]
---

给定总计至少 200 万行代码的 10+ 个仓库，构建摄取流水线、混合索引和引用强制查询智能体，以可验证的 file:line 锚点回答跨仓库问题。

构建计划：

1. 用 tree-sitter 解析每个文件。在函数和类节点边界处分块。存储 `{repo, path, start_line, end_line, symbol, body}`。
2. 使用提示缓存的系统提示通过 Claude Haiku 4.5 或 Gemini 2.5 Flash 总结每个块。在块旁边存储一句话摘要。
3. 索引到三种结构：Qdrant（密集，Voyage-code-3 或 nomic-embed-code）、Tantivy（带字段权重的 BM25）和 kuzu（导入、调用、继承的符号图边）。
4. 构建具有三个节点的 LangGraph 查询智能体：检索（密集并行 BM25）、重排序（Cohere rerank-3 或 bge-reranker-v2-gemma-2b）、综合（Claude Sonnet 4.7，带提示缓存和 file:line 引用要求）。
5. 后过滤：拒绝任何没有可验证 `(repo/path:start-end)` 锚点的声明；重新查询或丢弃。
6. 连接 git push webhook，计算符号级别差异并仅重新嵌入更改的块。目标：在 2M LOC 舰队上 60s 内可搜索 50 文件提交。
7. 使用 100 问题保留集评估。报告 MRR@10、nDCG@10、引用忠实度和延迟百分位数。
8. 运行每周漂移作业，重新执行评估并在 MRR@10 下降 > 5% 时告警。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | 检索质量 | 在 100 问题保留集上的 MRR@10 和 nDCG@10 |
| 20 | 引用忠实度 | 具有可验证 file:line 锚点的答案声明比例 |
| 20 | 延迟和规模 | 在索引语料库规模上 10k QPS 的 p95 查询延迟 |
| 20 | 增量索引正确性 | 从 git push 到 50 文件提交可搜索的时间 |
| 15 | UX 和答案格式 | 引用可点击性、片段预览、后续查询能力 |

硬性拒绝：
- 固定大小令牌分块而非 AST 感知分块。会毒害代码生成密集的语料库。
- 仅余弦检索而没有 BM25 或重排序。已知在精确符号名称查询上失败。
- 没有强制 file:line 引用的答案。
- 每次 git push 重新嵌入整个语料库；必须是增量的。

拒绝规则：
- 拒绝在不阅读许可证的情况下索引仓库。有些禁止在第三方向量存储中嵌入。
- 拒绝回答声称引用索引从未见过的文件的问题；返回前始终验证锚点。
- 拒绝提供 p95 超过 4s 的答案；改为返回带有后续处理句柄的部分结果。

输出：包含摄取流水线、LangGraph 查询智能体、100 问题标记评估集、Langfuse 仪表盘链接的仓库，以及一份指出你修复的三大检索失败模式（生成代码毒害、长尾符号召回、跨仓库符号解析）和修复每个的具体更改的 write-up。