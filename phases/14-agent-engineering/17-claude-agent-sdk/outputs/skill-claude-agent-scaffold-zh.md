---
name: claude-agent-scaffold
description: 搭建一个 Claude Agent SDK 应用，包含子智能体、生命周期钩子、会话存储、MCP 服务器附件和 W3C 追踪传播。
version: 1.0.0
phase: 14
lesson: 17
tags: [claude-agent-sdk, subagents, hooks, session-store, mcp]
---

给定一个产品领域和一个 MCP 服务器列表，搭建一个 Claude Agent SDK 应用。

生成：

1. 一个主智能体定义，包含指令、内置工具访问（read_file、write_file、shell、grep、glob、web fetch）和自定义函数工具。
2. 用于并行化和上下文隔离的子智能体生成器。当编排器可能会超出其上下文预算时使用。
3. 注册生命周期钩子：PreToolUse + PostToolUse 用于审计，SessionStart 用于设置，SessionEnd 用于清理，UserPromptSubmit 用于规则执行（参见 pro-workflow 模式）。
4. 会话存储（默认 SQLite），通过 `list_subkeys` 渲染子智能体树。
5. 用于外部工具/资源表面的 MCP 服务器附件。
6. W3C 追踪上下文传播，使调用者的 OTel span 通过 CLI 持续传递。

硬性拒绝：

- 为单工具任务生成子智能体。子智能体用于并行化或上下文隔离；而非用于「一次 read_file 调用」。
- 钩子中包含同步的昂贵工作。钩子应在微秒到毫秒级别。长时间工作属于子智能体。
- 没有级联删除策略的会话存储。孤立的子智能体会话会膨胀存储。

拒绝规则：

- 如果产品需要长时间运行的异步工作（数小时到数天），拒绝自托管 SDK 并路由到 Claude Managed Agents。
- 如果用户要求 `--session-mirror` 到共享位置，拒绝。会话记录携带 PII；镜像到按用户加密的存储。
- 如果智能体依赖原始 LLM 流式传输用于 UX 而不使用工具，拒绝 Agent SDK 并直接推荐 Client SDK。

输出：`agent.py`、`tools.py`、`hooks.py`、`session.py`、`README.md`，解释子智能体策略、钩子注册表、会话后端、MCP 附件和 OTel 接线。结尾的「下一步阅读」指向第 22 课了解语音交接，第 23 课了解 OTel span 归属，或第 18 课如果产品需要生产运行时形态。