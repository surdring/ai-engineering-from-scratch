---
name: mcp-handshake-tracer
description: 给定 MCP 客户端-服务器对话的 pcap 风格记录，为每条消息标注其原语、生命周期阶段和能力依赖
version: 1.0.0
phase: 13
lesson: 06
tags: [mcp, json-rpc, lifecycle, capabilities]
---

给定从 MCP 会话捕获的 JSON-RPC 2.0 信封序列，生成逐步讲解，为每条消息命名其原语、生命周期阶段和底层能力标志。

生成：

1. 每条消息的标注。对每条 `{request, response, notification}`，说明：方向（客户端到服务器或服务器到客户端）、原语（tools / resources / prompts / roots / sampling / elicitation / lifecycle）、生命周期阶段，以及使该消息合法所需的已协商能力标志。
2. 能力检查。从记录中重构 `initialize` 交换，列出所有已协商的能力。标记任何违反缺失能力的消息。
3. 错误诊断。对每个 JSON-RPC 错误，给出错误码和最可能的原因（基于周边上下文）。
4. 完整性审计。标记缺少以下之一的记录：`initialize`、`initialized` 通知、至少一个 `tools/list` 或等价物、优雅关闭。
5. 规范合规。根据 2025-11-25 规范的最小字段集检查每个请求的 params。标记遗漏。

硬拒绝：
- 任何使用规范允许集之外的方法但没有 `x-` 前缀的消息。
- 任何在客户端未声明 `sampling` 能力时的 `sampling/createMessage` 消息。
- 任何在 `notifications/initialized` 到达之前的调用。

拒绝规则：
- 如果被要求审计来自非 MCP 协议的记录，拒绝并指向 A2A 规范（Phase 13 · 19）作为替代。
- 如果被要求「修复」记录，拒绝。此技能只标注；不重写。通过实现 SDK 路由更正。

输出：每条消息在到达顺序中的一行标注：`[阶段/原语/能力] <方法或结果形态>`。以三行摘要说明任何能力违规和任何缺失的生命周期步骤结尾。