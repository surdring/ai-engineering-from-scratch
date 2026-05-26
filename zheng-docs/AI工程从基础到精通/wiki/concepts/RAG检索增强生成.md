# RAG 检索增强生成

## 知识库中的位置

RAG 是 LLM 连接外部知识的关键范式：

- [[../11-llm-engineering/04_rag-from-scratch]] — 从零实现 RAG
- [[../11-llm-engineering/05_embedding-models]] — 嵌入模型深度解析
- [[../11-llm-engineering/06_rag-evaluation]] — RAG 评估指标体系
- [[../11-llm-engineering/07_vector-databases]] — 向量数据库
- [[../11-llm-engineering/08_advanced-rag]] — 高级 RAG：Self-RAG、Corrective RAG、Agentic RAG、Graph RAG
- [[../05-nlp-foundations-to-advanced/23_chunking-strategies-rag]] — RAG 分块策略
- [[../05-nlp-foundations-to-advanced/14_information-retrieval-search]] — 信息检索基础
- [[../05-nlp-foundations-to-advanced/22_embedding-models-deep-dive]] — 嵌入模型深度解析
- [[../13-tools-and-protocols/05_vector-databases-comparison]] — 向量数据库对比
- [[../10-llms-from-scratch/19_long-context-and-retrieval-techniques]] — 长上下文与检索技术

## RAG 架构演进

### 1.0 朴素 RAG
Index → Retrieve → Generate。问题：检索不精准、上下文碎片化。

### 2.0 高级 RAG
- **Self-RAG**：LLM 自判断检索质量，决定是否需要检索
- **Corrective RAG**：检索后自纠偏
- **HyDE**：假设文档嵌入，先生成假设答案再检索
- **Re-ranking**：粗检索 + 精排序

### 3.0 Agentic RAG
- LLM 自主规划检索策略
- 多步推理 + 多源检索
- 与工具调用结合

### 4.0 Graph RAG
- 基于知识图谱的检索
- 实体关系推理
- 与向量检索互补

## 关键技术组件

| 组件 | 关键技术 |
|------|----------|
| 分块 | Fixed-size, Semantic, Recursive, Agentic |
| 嵌入 | text-embedding-3, bge, Jina, Cohere |
| 向量库 | Chroma, Pinecone, Milvus, Qdrant, Weaviate |
| 检索 | Dense, Sparse (BM25), Hybrid, Multi-vector |
| 重排序 | Cross-encoder, ColBERT, LLM-as-reranker |

## RAG vs 长上下文

一种观点的对比逻辑：

| 维度 | RAG | 长上下文 |
|------|-----|----------|
| 延迟 | 检索额外开销 | 无检索开销但 Prompt 更长 |
| 精度 | 检索质量决定 | 上下文窗口内精度高 |
| 成本 | 嵌入 + 向量库 | Token 数增加 |
| 更新 | 向量库可热更新 | 需重新 Prompt |
| 最佳场景 | 大规模外部知识 | 单文档深度分析 |

## 与 Karpathy LLM Wiki 的关系

本知识库本身就是一种「增强」——但用的是另一种范式：**编译时而非查询时**。RAG 是每次查询时检索，而 LLM Wiki 模式在录入时将知识编译进 Wiki。见 [[../wiki/guides/Karpathy-LLM-Wiki完全指南]]

## 跨阶段关联

- RAG 是 [[concepts/AI-Agent]] 的基础能力
- 依赖于 [[concepts/大语言模型LLM]] 的理解能力
- 与 MCP 协议（[[../13-tools-and-protocols/]]）互补