---
name: a2a-agent-spec
description: 为应能通过 A2A 被调用的智能体生成 Agent Card 和技能 Schema
version: 1.0.0
phase: 13
lesson: 19
tags: [a2a, agent-card, task-lifecycle, delegation]
---

给定智能体的能力和目标协作者，生成其 A2A Agent Card 和技能定义。

生成：

1. Agent Card。`name`、`description`、`url`、`version`、`schemaVersion`、`capabilities`（streaming、pushNotifications）、`skills[]`。
2. 技能列表。每个包含 `id`、`name`、`description`、`inputModes`、`outputModes`。在描述中使用「Use when X. Do not use for Y.」模式。
3. 任务状态计划。对每个技能，预期的状态转换和 input_required 路径。
4. 签名计划。是否通过 AP2 签名卡片（推荐用于外部可调用的智能体）。
5. 传输。默认 JSON-RPC over HTTP 或 gRPC。记录 v1.0 向后兼容性。

硬拒绝：
- 任何没有稳定 URL 的 Agent Card。破坏发现机制。
- 任何没有声明输入和输出模式的技能。调用者无法推断兼容性。
- 任何外部可调用的智能体没有 AP2 签名计划。冒充向量。

拒绝规则：
- 如果智能体的用例是单个工具调用，拒绝搭建 A2A 脚手架；推荐 MCP。
- 如果智能体暴露了不应暴露的内部细节（工具调用追踪、思维链），拒绝并要求不透明化。
- 如果智能体需要 A2A 进行支付（AP2 用例），确认 AP2 扩展版本并标记 AP2 与核心 A2A 是分开的。

输出：一页 Agent Card JSON、每个操作的技能 Schema、状态转换计划、签名和传输选择。以智能体承诺的最低 v1.0 向后兼容保证结尾。