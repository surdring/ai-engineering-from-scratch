---
name: llm-observability
description: 构建自托管 LLM 可观测性仪表盘，摄取 OpenTelemetry GenAI span、运行评估，并在五分钟内捕获注入的退化。
version: 1.0.0
phase: 19
lesson: 11
tags: [capstone, observability, otel, langfuse, phoenix, evals, drift, clickhouse]
---

给定至少六个 SDK 系列（OpenAI、Anthropic、Google GenAI、LangChain、LlamaIndex、vLLM）的生产 LLM 流量，部署摄取 OTLP GenAI-semconv span、运行评估、检测漂移和告警的自托管可观测平面。

构建计划：

1. OpenTelemetry Collector，带 OTLP HTTP 接收器、尾部采样处理器（保留 100% 错误、10% 成功、100% 高毒性/PII），导出器到 ClickHouse + S3。
2. 反映 GenAI semconv 的 ClickHouse span 模式：gen_ai.system、gen_ai.request.model、usage.input/output_tokens、latency_ms、user_id、app_id，加用于 prompts/completions 的 JSON 包。
3. Postgres 元数据存储用于 apps、users、sessions、annotation queue。
4. 在每个 SDK 系列的客户端应用上使用 OpenLLMetry 自动仪表化；验证规范 span 到达。
5. 在采样 track 上调度的 DeepEval + RAGAS + Phoenix evaluator pack；自定义 LLM-judge 用于 PII 和离策略。
6. 在池化的提示嵌入上的每周 PSI / KL 漂移检测器；告警阈值 0.2。
7. Prometheus 导出器用于评估分数聚合和延迟百分位；Alertmanager 到 Slack（warning）+ PagerDuty（critical）。
8. Next.js 15 App Router 仪表盘：概览、trace 搜索 + waterfall、评估趋势、漂移图表、告警。
9. 退化探测：注入 1% 时间泄露假 SSN 的响应模式；测量 MTTR（告警触发时间）。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | Trace-模式覆盖 | 产生规范 GenAI span 的 SDK 系列数量（目标 6+） |
| 20 | 评估正确性 | DeepEval / RAGAS 分数 vs 手动标记集 |
| 20 | 仪表盘 UX | 注入退化上的 MTTR（目标低于 5 分钟） |
| 20 | 成本 / 规模 | 持续 1k spans/sec 摄取无积压 |
| 15 | 告警 + 漂移检测 | 端到端锻炼 Prometheus/Alertmanager 链 |

硬性拒绝：
- 发明不在 OpenTelemetry GenAI semconv 中的属性名的 span 模式。
- 丢弃错误的尾部采样策略（众所周知的坏实践）。
- 以摄取速率运行评估而不采样（不可接受的成本）。
- 显示「延迟」而不区分 p50/p95/p99 的仪表盘。

拒绝规则：
- 拒绝在没有 PII 脱敏策略的情况下持久化提示或补全。
- 拒绝在没有逐 SDK 规范 span 退化测试的情况下声称「多 SDK 支持」。
- 拒绝在没有基线窗口的情况下交付漂移检测；零样本漂移是无用的。

输出：包含 collector 配置、ClickHouse schema、Next.js 15 仪表盘、评估作业、漂移检测器、告警链、带有注释退化的 10k trace 演示数据集的仓库，以及记录用于注入 PII 退化的 MTTR 加上在迭代中降低 MTTR 的三大仪表盘 UX 改进的 write-up。