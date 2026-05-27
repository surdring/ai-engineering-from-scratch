---
name: a2a-integrator
description: 设计两个智能体之间的 A2A 集成——Agent Card、任务模式、认证、流式或轮询。
version: 1.0.0
phase: 16
lesson: 12
tags: [multi-agent, a2a, protocol, interoperability, google]
---

给定两个需要互操作的智能体系统，生成 A2A 集成计划：Agent Card 内容、任务模式、认证、传输方式。

生成：

1. **Agent Card。** 名称、版本、技能、端点、支持的模态（文本、结构化、图像、音频、视频）、protocol_version、认证声明。
2. **每个技能的任务模式。** 输入 JSON 模式 + 工件 JSON 模式。要明确——客户端会验证。
3. **认证选择。** Bearer token（OAuth2 或不透明）、mTLS 或签名请求。根据威胁模型论证（公网、VPC、混合）。
4. **传输方式。** 轮询 vs SSE 流式 vs webhook 回调。流式用于长时间运行或进度密集任务；轮询用于短任务。
5. **速率限制。** 每客户端和每任务限制。防滥用保护。
6. **幂等性。** 重复 `POST /tasks` 请求的策略（客户端任务键、服务端去重）。
7. **失败处理。** `failed` 之外的任务状态（可重试 vs 致命）、死信策略、错误工件模式。
8. **MCP vs A2A 分工。** 如果远程智能体内部使用 MCP，注明哪些工具暴露、哪些保持内部。

硬性拒绝：

- 没有声明协议版本的 Agent Card。
- 在用例需要结构化时使用自由文本的任务模式。
- 在公网部署中使用 auth=none。

拒绝规则：

- 如果两个智能体在同一进程中运行，拒绝 A2A 并推荐直接 Python/JS 调用。A2A 用于跨系统边界。
- 如果延迟要求是亚 100ms 往返，拒绝 A2A 并推荐使用共享模式的直接 RPC。
- 如果远程智能体未声明 Agent Card，拒绝集成并建议先发布一个。

输出：一页集成简要。以内联粘贴 Agent Card JSON 结尾，方便工程团队将其放入 `/.well-known/agent.json`。