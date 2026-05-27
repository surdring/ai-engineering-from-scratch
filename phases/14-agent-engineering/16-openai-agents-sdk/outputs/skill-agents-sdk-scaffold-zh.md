---
name: agents-sdk-scaffold
description: 搭建一个 OpenAI Agents SDK 应用，包含分流智能体、交接、输入/输出/工具护栏、会话存储和追踪处理器。
version: 1.0.0
phase: 14
lesson: 16
tags: [openai, agents-sdk, handoffs, guardrails, tracing, session]
---

给定一个产品领域和一个专家智能体列表，搭建一个 OpenAI Agents SDK 应用。

生成：

1. 每个专家一个 `Agent`，加上一个仅具有交接功能（无领域工具）的 `triage` 智能体。
2. 每个领域工具一个 `FunctionTool`，包含类型化输入模式、清晰的描述（告诉模型何时使用）和执行沙箱。
3. 从 triage 到每个专家的 `Handoff`。验证工具名称遵循 `transfer_to_<agent>` 约定。
4. 用于 PII、策略、范围的 `InputGuardrail`。默认使用并行模式，除非护栏 LLM 相对于主模型较大——则使用阻塞模式。
5. 用于长度、PII、策略的 `OutputGuardrail`。生产环境中对安全关键输出始终使用阻塞模式。
6. 涉及网络或文件系统的函数工具的逐工具护栏。
7. `Session` 存储（默认 SQLite；生产环境使用 Redis）。
8. `add_trace_processor` 将 span 接入你的后端，同时保留 OpenAI 的追踪 UI。

硬性拒绝：

- 具有领域工具的 Triage 智能体。Triage 仅交接；混合会稀释路由器的决策。
- 修改输入/输出的护栏。护栏审批或拒绝——它们不重写。
- 静默交接循环。要求跳数计数器（默认最多 3 跳）。

拒绝规则：

- 如果用户希望「不要护栏，快速推进」，对任何涉及付费用户或 PII 的产品拒绝。
- 如果产品只有 2 个专家，建议通过带直接分类器的 `Agents` 进行路由（第 12 课），而非 triage+交接——token 成本更低。
- 如果在生产环境中禁用了追踪，拒绝交付。多步失败在没有追踪的情况下是无法调试的。

输出：`agents.py`、`tools.py`、`guardrails.py`、`app.py`、`README.md`，包含 triage 智能体理由、护栏模式、追踪处理器和会话后端。结尾的「下一步阅读」指向第 23 课（OTel GenAI）、第 24 课（可观测性后端）或第 17 课关于 Claude Agent SDK 转换。