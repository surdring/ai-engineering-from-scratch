---
name: mcp-server-platform
description: 部署生产 MCP 服务器，具有 StreamableHTTP、OAuth 2.1 范围、OPA 策略、破坏性工具的人工审批门槛和用于发现的注册中心。
version: 1.0.0
phase: 19
lesson: 13
tags: [capstone, mcp, fastmcp, streamablehttp, oauth, opa, registry, governance]
---

给定企业环境，交付一个包含 10 个内部工具的 MCP 服务器，一个用于发现的注册中心服务，以及一个通过 Slack 审批对破坏性工具进行把关的治理层。

构建计划：

1. FastMCP 服务器暴露 10 个只读工具（Postgres、S3、Jira、Linear、Datadog、PagerDuty、GitHub、Notion、Slack、Salesforce），每个都具有类型化 schema 和必需的范围。
2. StreamableHTTP 传输，无状态位于负载均衡器后。
3. OAuth 2.1 令牌内省中间件；通过 SPIFFE / SPIRE 的工作负载身份。
4. 每次工具调用上的 OPA / Rego 策略决策：范围强制执行、PII 脱敏、payload 大小上限。
5. 破坏性工具（Jira create、Linear create、Postgres write）在需要 `approved:by:human` 范围的单独 MCP 服务器上，在 15 分钟内通过 Slack 卡片提升。
6. 注册中心服务，轮询每个服务器的 `.well-known/mcp-capabilities`，用 JSON Schema 验证，暴露 list/search/validate/enable UI。
7. 逐租户 JSONL 审计日志，写入前通过 Presidio PII 脱敏。
8. 100 客户端负载测试演示水平扩展；通过 MCP 合规套件。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | 规范合规 | StreamableHTTP + capability manifest 通过 MCP 合规测试 |
| 20 | 安全性 | 范围强制执行、OPA 覆盖每个工具、密钥卫生 |
| 20 | 可观测性 | 逐工具调用审计日志，写入前 PII 脱敏 |
| 20 | 规模 | 100 客户端负载测试，演示水平扩展 |
| 15 | 注册中心 UX | 演练发现 / 验证 / 启用-禁用工作流 |

硬性拒绝：
- 需要有状态会话的服务器（违反 2026 StreamableHTTP 无状态合约）。
- 破坏性工具与只读共享同一认证面的单服务器拓扑。
- 持久化原始 PII 的审计日志。
- 忽略 capability manifest；注册中心集成是硬性要求。

拒绝规则：
- 拒绝在没有 OAuth 的情况下部署；匿名访问是不合格的。
- 拒绝在没有 Slack 审批流的情况下交付破坏性工具。
- 拒绝暴露范围或描述不在 capability manifest 中的工具。

输出：包含两个 MCP 服务器（只读 + 破坏性）、注册中心服务、Slack 审批集成、OPA 策略、100 客户端负载测试 harness、合规测试结果的仓库，以及描述哪些工具你考虑暴露但未暴露（以及原因）加上在 dry-run 期间捕获到接近触发的三大 OPA 规则的 write-up。