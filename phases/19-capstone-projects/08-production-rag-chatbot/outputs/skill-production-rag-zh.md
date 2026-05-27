---
name: production-rag
description: 部署一个受监管领域的 RAG 聊天机器人，具有角色 + 管辖区过滤、提示缓存、护栏和实时漂移监控。
version: 1.0.0
phase: 19
lesson: 08
tags: [capstone, rag, chatbot, regulated, llama-guard, nemo-guardrails, ragas, langfuse]
---

给定受监管领域语料库（法律合同、临床试验方案、保险政策或类似），部署一个使用可验证引用回答问题、尊重角色和管辖区访问策略的聊天机器人，并进行漂移监控。

构建计划：

1. 用 docling 或 Unstructured 解析语料库；通过 ColPali 路由视觉丰富文档。产出带角色和管辖区标签的块。
2. 索引密集到 pgvector + pgvectorscale（Voyage-3 或 Nomic-embed-v2）；通过 Tantivy 索引稀疏 BM25。
3. 连接 LangGraph 对话智能体：检索（按角色 + 管辖区过滤，混合 dense+BM25，reciprocal rank fusion）、重排序（bge-reranker-v2-gemma-2b 或 Voyage rerank-2）、综合（Claude Sonnet 4.7 带提示缓存）。
4. 使用稳定前缀组装提示：系统前言 -> 策略块 -> 重排序上下文 -> 用户查询。目标 60-80% 提示缓存命中率。
5. 护栏：Llama Guard 4 在输入和输出上、NeMo Guardrails v0.12 用于离域和策略禁止问题、Presidio PII 脱敏输出、引用强制执行后置过滤。
6. 构建 200 问题专家标记黄金集，包含（答案、引用）。评分精确引用匹配、答案正确性、RAGAS 忠实度。
7. 构建 50 提示红队（PAIR、TAP、PII 提取、离域、跨管辖区探测）。
8. Arize Phoenix 漂移仪表盘跟踪检索 nDCG 和引用忠实度每周；5% 下降则告警。
9. Langfuse 成本报告：提示缓存命中率、每查询令牌数、按阶段的 $/查询。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | RAGAS 忠实度 + 答案相关性 | 在 200 问题黄金集上的在线评分 |
| 20 | 引用正确性 | 具有可验证源锚点的答案比例 |
| 20 | 护栏覆盖 | Llama Guard 4 通过率 + 越狱套件结果 |
| 20 | 成本 / 延迟工程 | 提示缓存命中率、p95 延迟、$/查询 |
| 15 | 漂移监控仪表盘 | 具有每周检索质量趋势的实时 Phoenix 仪表盘 |

硬性拒绝：
- 任何泄露跨管辖区数据的聊天机器人。角色+管辖区过滤必须在检索前强制执行，而非之后。
- 破坏缓存前缀的综合提示（在系统和上下文之间重排策略）。会破坏缓存经济。
- 没有记录红队运行的护栏配置。
- 没有引用的答案；没有可验证锚点的引用。

拒绝规则：
- 拒绝在没有每个块的管辖区标签的情况下在受监管领域部署。
- 拒绝在专家标记黄金集问题上训练检索。污染破坏评估可信度。
- 拒绝在没有 README 中包含显式 SOC2/HIPAA/GDPR 适用性矩阵的情况下声称「合规」。

输出：包含摄取流水线、LangGraph 对话智能体、200 问题黄金集、50 提示红队、Phoenix 漂移仪表盘、Langfuse 成本仪表盘的仓库，以及指出你观察到的三大引用断裂模式以及每个模式的检索或提示修复的 write-up。