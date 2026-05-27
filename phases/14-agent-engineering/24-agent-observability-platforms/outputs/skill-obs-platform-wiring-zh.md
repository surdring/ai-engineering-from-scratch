---
name: obs-platform-wiring
description: 选择可观测性平台（Langfuse、Phoenix、Opik、Datadog）并将追踪 + 评估 + 提示版本接入现有智能体。
version: 1.0.0
phase: 14
lesson: 24
tags: [observability, langfuse, phoenix, opik, datadog, tracing]
---

给定一个智能体运行时和产品需求，选择一个可观测性平台并搭建接线。

决策：

1. 需要在同一位置管理提示 + 会话回放 -> **Langfuse**。
2. 需要深度 RAG 相关性 + 漂移/异常检测 -> **Phoenix**。
3. 需要自动化提示优化 + PII 护栏 -> **Opik**。
4. 已在运行 Datadog -> **Datadog LLM Observability**（从 v1.37+ 原生映射 GenAI）。
5. 需要 ELv2 兼容许可 -> **Langfuse**（MIT）或 **Opik**（Apache 2.0）；纯 OSS 分发避免 Phoenix。

生成：

1. OTel GenAI 仪器化（第 23 课）——这是通用基础。
2. 平台特定的 SDK 或 OTel 导出器配置。
3. 针对你领域的 LLM 评判器评分标准（事实正确性、范围、语气、拒绝质量）。
4. 接入追踪的提示版本管理（Langfuse）或追踪聚类配置（Phoenix）或实验定义（Opik）。
5. 对记录内容的护栏：PII 脱敏、密钥擦除。
6. 仪表板：会话健康、失败分类、延迟分布、每会话成本。

硬性拒绝：

- 没有评估就交付。仅有追踪是昂贵的日志记录。
- 使用自写的 LLM 评判器而没有外部验证。CRITIC 模式（第 05 课）：评判器需要外部工具进行事实支撑。
- 在 span 体中存储 PII。始终使用外部存储 + 引用 ID。

拒绝规则：

- 如果用户要求「一个平台满足一切」，拒绝并给出上述决策。没有单一平台在所有三个轴上都占主导。
- 如果产品对每个智能体任务没有验收标准，拒绝交付评估。LLM 评判器需要评分标准；评分标准需要产品决策。
- 如果用户想要「不采样，捕获一切」，拒绝。追踪量随流量线性增长；大规模下采样（头采样或尾采样）是必需的。

输出：`instrumentation.py`、`judge.py`、`dashboards.md`、`README.md`，解释平台选择、评分标准、采样策略和事件响应。结尾的「下一步阅读」指向第 30 课（评估驱动开发）或第 26 课（失败模式分类）。