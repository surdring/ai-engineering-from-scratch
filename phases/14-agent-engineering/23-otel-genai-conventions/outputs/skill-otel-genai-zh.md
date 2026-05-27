---
name: otel-genai
description: 使用 OpenTelemetry GenAI 语义约定（invoke_agent、chat、tool_call span，具有正确的属性和可选内容捕获）对智能体进行仪器化。
version: 1.0.0
phase: 14
lesson: 23
tags: [opentelemetry, genai, observability, tracing, semantic-conventions]
---

给定一个智能体运行时，接入 OTel GenAI 语义约定。

生成：

1. 每次智能体运行一个 `invoke_agent` span。远程智能体服务使用 Kind CLIENT，进程内使用 INTERNAL。名称：`invoke_agent {gen_ai.agent.name}`。
2. 每次 LLM 调用一个 `chat` span，包含 `gen_ai.operation.name=chat`、`gen_ai.provider.name`、`gen_ai.request.model`、`gen_ai.response.model`。
3. 每次工具调用一个 `tool_call` span，包含 `gen_ai.tool.name`，以及适用时的 `gen_ai.data_source.id`（RAG 语料库 / 记忆存储）。
4. 可选内容捕获：默认关闭；开启时，将输入/输出存储到外部并在 span 上记录 `*.reference_id`。
5. 上下文传播：使用 W3C 追踪上下文头，使多进程运行（Claude Agent SDK CLI 子进程）拼接为一个追踪。

硬性拒绝：

- 默认内联捕获完整提示/输出。PII 和密钥泄露风险；也违反规范。
- 缺少 `gen_ai.provider.name`。多服务商仪表板会崩溃。
- 孤立的工具 span。始终通过活动上下文设置父子关系。

拒绝规则：

- 如果运行时无法跨进程边界传播上下文，拒绝。多进程追踪拼接对 Claude Agent SDK + CLI 用户是必需的。
- 如果产品有监管约束（HIPAA、GDPR），拒绝内联内容捕获。仅使用带访问控制的外部存储。
- 如果后端未设置 `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`，警告：属性名称可能在收集器升级时更改。

输出：`tracer.py`、`attributes.py`、`content_store.py`、`README.md`，解释 span 结构、稳定性选择加入和内容捕获策略。结尾的「下一步阅读」指向第 24 课（后端：Langfuse、Phoenix、Opik）或第 17 课了解 Claude Agent SDK 追踪上下文传播。