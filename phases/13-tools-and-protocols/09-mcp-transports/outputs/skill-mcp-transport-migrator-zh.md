---
name: mcp-transport-migrator
description: 制定从旧版 HTTP+SSE 到流式 HTTP 的迁移计划，包含会话 ID 连续性和 Origin 验证
version: 1.0.0
phase: 13
lesson: 09
tags: [mcp, streamable-http, sse-migration, session-id, origin]
---

给定现有 HTTP+SSE（旧版）MCP 服务器，生成到单端点流式 HTTP 的迁移计划。

生成：

1. 端点重写。将 `/messages` 和 `/sse` 合并为一个 `/mcp`。将 POST 映射到请求处理，GET 映射到 SSE 流，DELETE 映射到会话终止。
2. 会话连续性。在首次 POST 时生成新的 `Mcp-Session-Id`。拒绝客户端提供的 ID。如果客户端首先发送旧版会话 cookie，保留桥接逻辑。
3. Origin 验证。将显式生产域名加入允许列表（`https://app.company.com`、`https://claude.ai`、localhost 变体）。用 403 拒绝所有其他域名。
4. Last-Event-ID 重放。为每个会话保留最近事件的环形缓冲区，以便重连时恢复。
5. 弃用窗口。记录切换日期和 60 天宽限期，期间旧端点 301 重定向到新端点并附警告头。

硬拒绝：
- 任何无限期保留两个端点存活的计划。旧版 SSE 将在 2026 年移除。
- 任何会话 ID 由客户端生成的计划。违反密码学随机性要求。
- 任何没有 Origin 验证的计划。DNS 重绑定漏洞。

拒绝规则：
- 如果服务器是仅本地的（stdio），拒绝迁移到 HTTP；stdio 对本地是正确的。
- 如果服务器尚未部署 OAuth，在公开暴露之前先完成 Phase 13 · 16。
- 如果托管目标不支持长连接 HTTP（如 Vercel 免费层），拒绝并推荐 Cloudflare Workers。

输出：迁移手册，包含端点变更、Origin 允许列表、会话 ID 计划、弃用时间表和测试检查清单（覆盖 initialize、tools/list、流式通知、使用 last-event-id 重连和显式 DELETE）。