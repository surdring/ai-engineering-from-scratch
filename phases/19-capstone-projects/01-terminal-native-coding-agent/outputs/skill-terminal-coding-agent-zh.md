---
name: terminal-coding-agent
description: 构建并评估一个终端原生编码智能体，对照 SWE-bench Pro，具有受限成本、沙箱化工具和完整的 2026 hook 表面。
version: 1.0.0
phase: 19
lesson: 01
tags: [capstone, coding-agent, claude-code, swe-bench, mcp, hooks, sandbox]
---

给定目标仓库和自然语言任务，构建一个在沙箱中规划、执行并提交 Pull Request 的 harness。在 30 任务 SWE-bench Pro 子集上匹配或超越 mini-swe-agent 基线，同时保持在每任务 $5 预算内。

构建计划：

1. 搭建 Bun + Ink TUI harness，具有规划面板、工具调用流和实时令牌/美元预算。
2. 通过 Model Context Protocol StreamableHTTP 定义六个工具（read_file、edit_file、ripgrep、tree_sitter_symbols、run_shell、git）。每次调用最多返回 4k 令牌。
3. 在 E2B 或 Daytona 沙箱中，在全新的 `git worktree add` 分支上运行每个工具调用。绝不触碰主机文件系统。
4. 连接全部八个 2026 钩子事件：SessionStart、SessionEnd、PreToolUse、PostToolUse、UserPromptSubmit、Notification、Stop、PreCompact。至少提供四个用户编写的钩子（破坏性命令守卫、令牌核算、OTel span 发射器、trace bundle 写入器）。
5. 强制三个预算：50 回合、200k 令牌、$5 美元。PreCompact 在 150k 时触发并总结较早的回合。
6. 向自托管 Langfuse 发射具有 GenAI 语义约定的 OpenTelemetry span。
7. 成功后，推送分支并打开包含计划和 trace bundle 正文的 PR。
8. 在 30 个问题的 SWE-bench Pro Python 子集上对比 mini-swe-agent 评估，记录 pass@1、回合、令牌和每任务美元。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | SWE-bench Pro pass@1 | 在 30 任务子集上对比 mini-swe-agent 基线 |
| 20 | 架构清晰度 | 规划/行动/观察分离、钩子表面、工具模式可读性 |
| 20 | 安全性 | 沙箱逃逸红队 + 破坏性命令守卫审计 |
| 20 | 可观测性 | 100% 工具调用被追踪，每回合令牌核算 |
| 15 | 开发者 UX | 2s 内冷启动、崩溃恢复、Ctrl-C 取消语义 |

硬性拒绝：
- 在主机文件系统上通过 shell 调用 git 而非在沙箱内。
- 任何可以在 worktree 外写入或未经显式允许列表钩子 curl 外部 URL 的智能体。
- 在没有同一 30 个问题的匹配基线运行的情况下报告的评估数字。
- 依赖于重试之间 `git reset --hard` 的「通过率」声明；SWE-bench Pro 是 pass@1。

拒绝规则：
- 在任何配置下拒绝直接推送到 main。仅 PR 分支。
- 拒绝禁用破坏性命令守卫。这是评分标准的硬性要求。
- 拒绝在没有预算上限的情况下运行。开放式运行污染评估比较。

输出：包含 harness 的仓库、固定的 30 任务 SWE-bench Pro 评估 harness（带匹配的 mini-swe-agent 基线运行）、至少 5 次完整运行的 OpenTelemetry trace 存档，以及一份说明 harness 解决了哪些基线未解决的任务（反之亦然）的 write-up。以你观察到的三大失败模式以及修复每个模式的钩子更改结尾。