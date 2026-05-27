---
name: mcp-client-harness
description: 给定 MCP 服务器的声明式列表（名称、命令、参数），搭建多服务器客户端，包含握手、命名空间合并和路由
version: 1.0.0
phase: 13
lesson: 08
tags: [mcp, client, multi-server, routing, namespace]
---

给定要运行的 MCP 服务器配置，生成客户端测试框架，该框架启动每个服务器、对每个服务器进行握手、将其工具列表合并到一个命名空间中，并将每个调用路由到所属服务器。

生成：

1. 服务器配置解析器。映射 `名称 -> {command, args, env}`。验证命令在路径上存在。
2. 启动计划。使用 subprocess.Popen 配合 stdin/stdout/stderr 管道、`bufsize=1`、文本模式。每个服务器一个后台读取线程。
3. 握手流水线。对每个会话：发送 `initialize`，等待响应，持久化能力，发送 `notifications/initialized`。
4. 命名空间合并。选择冲突策略：`prefix-on-collision`（默认）、`reject-on-collision` 或 `silent-overwrite`（禁止）。在启动时打印合并后的工具列表。
5. 路由函数。`client.call(canonical_name, arguments)` 查找所属会话并写入 `tools/call` 消息。通过待处理请求表中的 future 等待匹配 ID 的响应。

硬拒绝：
- 任何不在自己的进程中启动每个服务器的测试框架。进程内复用破坏了隔离模型。
- 任何以 `silent-overwrite` 作为默认冲突策略的测试框架。安全风险。
- 任何在 stdout 读取上阻塞主线程的测试框架。通知会被延迟。

拒绝规则：
- 如果服务器的命令不可信（不在固定允许列表中），拒绝启动并引导到 Phase 13 · 15 进行安全检查。
- 如果用户配置超过 10 个服务器且没有理由，警告并建议使用网关（Phase 13 · 17）。
- 如果被要求在此处处理 OAuth，拒绝并引导到 Phase 13 · 16。

输出：完整的客户端测试框架 Python 文件（约 150 行），包含 Session、合并逻辑、路由和测试每个配置服务器的主循环。以一句摘要说明冲突策略和合并工具数量的结尾。