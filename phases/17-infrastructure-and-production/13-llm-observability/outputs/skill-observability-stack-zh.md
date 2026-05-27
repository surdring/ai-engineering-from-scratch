---
name: observability-stack
description: 根据技术栈、规模、预算和许可证姿态选择 LLM 可观测性技术栈（开发平台 + 网关 + 可选规模层），并定义 OpenTelemetry GenAI 属性集。
version: 1.0.0
phase: 17
lesson: 13
tags: [observability, langfuse, langsmith, phoenix, arize, helicone, opik, opentelemetry, genai-conventions]
---

给定技术栈（LangChain / DSPy / 原生 SDK）、规模（追踪数/天）、预算、许可证姿态（仅 MIT vs 商业 OK）和自托管需求，生成可观测性计划。

生成：

1. **开发平台选择。** Langfuse（OSS）、LangSmith（LangChain 优先商业）、Opik（Comet OSS）或不使用。用技术栈和许可证论证。
2. **网关/遥测选择。** Helicone（代理 + 网关）、SigNoz（全 APM）、OpenLLMetry（纯 OTel）。如果已使用 AI 网关（阶段 17 · 19），指定集成方式。
3. **规模/湖层。** 可选的；长期分析使用 Arize AX 或原始 Iceberg，RAG 漂移使用 Phoenix。
4. **OTel GenAI 约定。** 指定最小属性集：`gen_ai.system`、`gen_ai.request.model`、`gen_ai.usage.input_tokens`、`gen_ai.usage.output_tokens`、`gen_ai.request.temperature`、`gen_ai.response.finish_reasons`，加上组织特定的（tenant_id、user_id、task）。
5. **采样策略。** 100% 错误、100% 高成本（>$0.10/调用）、N% 成功采样率。原始保留窗口（14d/30d/90d）。聚合保留更长时间。
6. **告警。** 必须有告警的五个指标：错误率、P99 TTFT、成本/请求、提示缓存命中率、拒绝率。

硬性拒绝：
- 在框架特定 SDK 内部仪表化而没有 OTel 后备。拒绝——框架锁定。
- 对非监管工作负载在 Datadog 级定价 >$500/月下保留 100% 追踪。拒绝——推荐采样。
- 忽略 OpenTelemetry GenAI 约定。拒绝——2026 年互操作性需要它们。

拒绝规则：
- 如果追踪数/天 > 5M 且团队坚持全面 Datadog 保留，在没有成本预测的情况下拒绝。
- 如果团队仅接受 MIT 却选择 LangSmith，拒绝——Langfuse 是 MIT 等价物。
- 如果团队没有 AI 网关且选择 Helicone 同时作为网关和可观测性，接受——代理兼作网关可达约 500 RPS（阶段 17 · 19 涵盖网关规模）。

输出：一页计划，指定开发平台、网关、规模层（如有）、OTel 属性集、采样规则、五个告警。以标志技术栈漂移的单一指标结尾：过去 7 天内具有完整 OTel GenAI 属性的 LLM 调用百分比。