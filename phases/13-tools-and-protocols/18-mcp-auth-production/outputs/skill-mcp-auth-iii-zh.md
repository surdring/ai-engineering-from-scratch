---
name: mcp-auth-iii-wiring
description: 将生产级 MCP 授权（RFC 8414、7591、8707、7636 PKCE、9728）接入 iii 原语 — HTTP/cron 用 registerTrigger，验证用 registerFunction，JWKS 缓存用 state::*
version: 1.0.0
phase: 13
lesson: 18
tags: [mcp, oauth, dcr, jwks, iii, rfc8414, rfc7591, rfc8707, rfc7636, rfc9728]
---

给定 MCP 服务器配置和 IdP 能力集，输出构成生产认证层的 iii 原语和拒绝规则。

输入：

- `mcp_resource_url` — 规范资源 URL（无路径），用作 `aud` 和受保护资源元数据的 `resource` 值。
- `idp_metadata_url` — IdP 的 `/.well-known/oauth-authorization-server` URL。
- `idp_capabilities` — 观察到的 `code_challenge_methods_supported`、`grant_types_supported`、`registration_endpoint`、`response_types_supported` 的值。
- `tools` — MCP 工具列表，包含每个工具所需的作用域。

生成：

1. **拒绝门控。** 如果以下四个条件中任一个失败，拒绝接入并停止：
   - `code_challenge_methods_supported` 中缺少 `S256`。
   - `grant_types_supported` 中缺少 `authorization_code`。
   - `registration_endpoint` 不存在（没有 RFC 7591 DCR）。
   - `response_types_supported` 不是精确的 `["code"]`。

2. **受保护资源元数据文档**（RFC 9728），供 MCP 服务器在 `/.well-known/oauth-protected-resource` 发布。包含 `resource`、`authorization_servers`（发行方允许列表）、`scopes_supported`、`bearer_methods_supported: ["header"]`。

3. **iii 触发器注册。** 逐字发出每次调用：
   - `iii.registerTrigger("http", {"path": "/.well-known/oauth-protected-resource", "method": "GET"}, "auth::serve-protected-resource")`
   - `iii.registerTrigger("http", {"path": "/mcp", "method": "POST"}, "mcp::dispatch")` — 调度器在任何工具运行之前调用 `iii.trigger("auth::validate-jwt", ...)`。
   - `iii.registerTrigger("cron", {"schedule": "<rotation_schedule>"}, "auth::rotate-jwks")` — 默认调度为 `0 */6 * * *`；高轮换频率 IdP 收紧为 `*/15 * * * *`。

4. **iii 函数注册。** 逐字发出每次调用：
   - `iii.registerFunction("auth::validate-jwt", handler)` — 检查 `iss` 允许列表、根据缓存 JWKS 验证签名、`aud == mcp_resource_url`、`exp`、所需作用域。
   - `iii.registerFunction("auth::rotate-jwks", handler)` — 获取 `jwks_uri`，写入 `state::set("auth/jwks/<iss>", {keys, fetched_at})`。
   - `iii.registerFunction("auth::serve-protected-resource", handler)` — 返回 (2) 中的文档。
   - `iii.registerFunction("auth::issue-step-up", handler)` — 仅当工具列表包含用户最初未授权作用域门控的操作时。

5. **状态键计划。** 每个接受的发行方一个键：`auth/jwks/<issuer>` 持有 `{keys, fetched_at}`。记录读取模式：验证器从 `state::get` 读取，在 `kid` 未命中时回退到同步 `iii.trigger("auth::rotate-jwks", ...)`。

6. **作用域映射。** 将每个工具映射到其所需作用域。输出表格：
   `| tool | required_scope | rationale |`。将破坏性工具分组到自己的作用域下；永远不要复用读取作用域给写入工具。

7. **运行时的拒绝规则**（验证器必须编码这些 — 在处理程序体中发出）：
   - 当 `aud != mcp_resource_url` 时拒绝。
   - 当 `iss not in authorization_servers` 时拒绝。
   - 当 `kid` 在单次轮换回退后不在缓存的 JWKS 中时拒绝。
   - 当所需作用域缺失时拒绝 → 403 `Bearer error="insufficient_scope", scope="<required>", resource="<mcp_resource_url>"`。
   - 拒绝任何没有 `code_verifier` 或 `resource` 参数的令牌请求。

硬拒绝（永远不要接入以下任何一项 — 拒绝请求并记录原因）：

- 在 iii 状态存储中以明文存储 `client_secret`。公共客户端使用 `token_endpoint_auth_method: none`；机密客户端使用 `private_key_jwt`。`state::*` 或注册响应日志中不能有明文共享密钥。
- 验证器跳过 `aud` 检查。RFC 8707 + RFC 9728 的全部原因就是混淆代理问题。
- 允许无 PKCE 的授权码请求。OAuth 2.1 禁止；验证器必须拒绝任何存储的授权码记录缺少 `code_challenge` 的 `/token` 交换。
- 缓存 JWKS 而没有刷新任务。要么部署 cron 触发器，要么不部署认证层。
- 信任 `iss` 声明而没有允许列表。任何接受来自任何 `iss` 的令牌的验证器都让攻击者可以搭建自己的 IdP 并伪造令牌。
- 以明文存储 `registration_access_token`。存储时哈希；每次更新需要明文。