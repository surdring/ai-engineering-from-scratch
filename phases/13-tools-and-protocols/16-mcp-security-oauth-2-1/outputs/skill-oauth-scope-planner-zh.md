---
name: oauth-scope-planner
description: 为远程 MCP 服务器设计 OAuth 2.1 作用域集、固定规则和升级认证策略
version: 1.0.0
phase: 13
lesson: 16
tags: [oauth, pkce, resource-indicators, step-up, sep-835]
---

给定具有工具列表的远程 MCP 服务器，设计授权模型。

生成：

1. 作用域层次结构。渐进式作用域集（如 `read` -> `write` -> `delete` -> `admin`）。每个操作类一个作用域；不要膨胀作用域集。
2. 作用域到工具的映射。每个工具标注其所需作用域。标记任何需要多个作用域的工具。
3. 升级认证策略。哪些操作需要升级认证而非初始同意。通常：破坏性操作需要升级认证。
4. 资源指示器值。在 `resource` 参数中使用的规范 URL。确保 URL 匹配 `.well-known/oauth-protected-resource` 资源字段。
5. 受保护资源元数据。起草 `.well-known/oauth-protected-resource` JSON，包含 `authorization_servers`、`scopes_supported` 和 `resource`。

硬拒绝：
- 任何需要 admin 作用域但在没有显式确认对话框的情况下被调用的工具。需要升级认证。
- 任何覆盖多个操作类的作用域。权限膨胀。
- 任何跳过受众验证的服务器。混淆代理漏洞。

拒绝规则：
- 如果服务器是本地（stdio），拒绝 OAuth 并声明 stdio 继承父级信任。
- 如果服务器依赖旧版 OAuth 2.0 implicit 流程，拒绝并要求迁移到 2.1 + PKCE。
- 如果用户要求无密码「仅 API 密钥」认证，拒绝（远程服务器）；需要 OAuth 2.1 授权码 + PKCE 配合资源指示器进行用户授权访问。客户端凭证仅适用于没有用户委托的机器间场景。

输出：一页授权计划，包含作用域层次结构、作用域到工具的映射、升级认证策略、资源指示器和受保护资源元数据 JSON。以首次遇到时最可能让用户意外的升级认证操作结尾。