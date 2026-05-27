---
name: mcp-server-scaffolder
description: 为特定领域搭建 MCP 服务器脚手架，包含正确的工具/资源/提示划分和 SDK 渐进路径
version: 1.0.0
phase: 13
lesson: 07
tags: [mcp, server, fastmcp, scaffold]
---

给定一个领域（笔记、工单、文件、数据库等），生成 MCP 服务器计划：哪些能力暴露为工具、哪些为资源、哪些为提示，以及渐进到 Python 或 TypeScript SDK 的路径。

生成：

1. 工具列表。用户明确要求执行的原子操作。包含名称、描述（Use-when 模式）、输入 Schema 和标注提示。
2. 资源列表。用户想要读取的数据。URI 方案、mime 类型以及是否启用 `resources/subscribe`。
3. 提示列表。宿主应暴露为斜杠命令的可复用模板。参数列表。
4. 能力声明。服务器在 `initialize` 中返回的确切 `capabilities` 对象。
5. 渐进说明。每个部分的 FastMCP（Python）或 TypeScript SDK 等价物。指出一个替换脚手架中手写 stdlib 模式的 SDK 特性（如 `lifespan`、`context`）。

硬拒绝：
- 任何仅暴露为工具而不暴露为资源的「数据库查询」。正确划分是 `/list` 和 `/read` 用资源，`/query`（带参数）用工具。
- 任何在相同命名空间中混用用户输入工具和特权工具且不加标注的服务器。
- 任何声称具有 `resources/subscribe` 能力但没有持久通知机制的服务器脚手架。

拒绝规则：
- 如果领域没有只读界面，拒绝搭建资源脚手架；推荐仅工具服务器。
- 如果领域没有自然的斜杠命令模板，拒绝搭建提示脚手架。
- 如果用户要求认证方案，拒绝并引导到 Phase 13 · 16（OAuth 2.1）。

输出：一页服务器计划，包含三个原语列表、能力对象和一个 10 行的 `@app.tool()` 装饰器风格渐进代码片段。以服务器应设置的最重要标注标志结尾。