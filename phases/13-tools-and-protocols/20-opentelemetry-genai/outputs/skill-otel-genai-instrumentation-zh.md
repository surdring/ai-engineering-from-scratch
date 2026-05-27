---
name: otel-genai-instrumentation
description: 为智能体代码库制定监控计划，端到端发送 OTel GenAI Span
version: 1.0.0
phase: 13
lesson: 20
tags: [otel, observability, gen-ai, tracing]
---

给定智能体代码库（LLM 调用、工具分发、MCP 客户端、子智能体），制定 OTel GenAI 监控计划。

生成：

1. Span 层次结构。根 `agent.invoke_agent`（INTERNAL）和子级：`llm.chat`（CLIENT）、`tool.execute`（INTERNAL）、`mcp.call`（CLIENT）、`subagent.invoke`（INTERNAL）。
2. 每个 Span 的属性检查清单。`gen_ai.operation.name`、`gen_ai.provider.name`、`gen_ai.request.model`、`gen_ai.response.model`、`gen_ai.usage.*`、`gen_ai.tool.name`、`gen_ai.agent.name`。
3. 传播规则。在每个远程调用上注入 W3C traceparent；对于 MCP stdio 使用 `_meta.traceparent` 作为临时字段。
4. 内容捕获策略。默认关闭；记录哪个环境变量启用；指出 PII 风险。
5. 导出器选择。Jaeger / Tempo / Langfuse / Phoenix / Datadog / Honeycomb；使用 OTLP 作为传输层。

硬拒绝：
- 任何缺少跨 MCP 或子智能体边界的追踪传播的计划。
- 任何默认开启内容捕获的计划。泄露提示和 PII。
- 任何发送没有 `gen_ai.` 或明确供应商前缀的任意自定义属性的计划。

拒绝规则：
- 如果代码库使用具有内置 OTel 自动检测的框架（Pydantic AI、LangGraph、AgentOps），优先推荐框架钩子。
- 如果导出器后端是本地部署且团队没有 SRE 支持，推荐托管后端。
- 如果用户要求在生产调试中捕获内容，在没有类型化同意策略和 PII 脱敏流水线的情况下拒绝。

输出：一页计划，包含 Span 层次结构、每个 Span 的属性检查清单、传播规则、内容捕获策略和导出器选择。以需要告警的首要指标（通常是 p95 `gen_ai.client.operation.duration`）结尾。