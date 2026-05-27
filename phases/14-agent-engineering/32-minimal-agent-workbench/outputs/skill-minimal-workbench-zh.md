---
name: minimal-workbench
description: 为任意仓库铺设三文件的最小可行智能体工作台——简短的 AGENTS.md 路由器、持久的 agent_state.json 和与项目当前待办事项匹配的 JSON task_board.json。
version: 1.0.0
phase: 14
lesson: 32
tags: [workbench, agents-md, state, task-board, scaffold]
---

给定一个仓库路径和一个简短的待办事项列表，搭建最小可行智能体工作台。

生成：

1. `AGENTS.md` 不超过 80 行。它必须路由到：状态文件、任务看板、更深层的规则文档（即使为空）和验证命令。此文件中不包含散文教程。
2. `agent_state.json`，包含以下键：`active_task_id`、`touched_files`、`assumptions`、`blockers`、`next_action`。所有可选字段默认为空数组或空字符串，数组绝不为 `null`。
3. `task_board.json` 作为 JSON 任务数组。每个任务包含 `id`、`goal`、`owner`（`builder` | `reviewer` | `human`）、`acceptance`（字符串列表）和 `status`（`todo` | `in_progress` | `done` | `blocked`）。
4. `docs/agent-rules.md` 占位文件，每个表面一个 H2，以便后续课程填充。

硬性拒绝：

- `AGENTS.md` 超过 80 行或少于 10 行。太长智能体会跳过；太短则没有路由功能。
- 引用聊天历史而非仓库的状态文件。仓库是记录系统。
- 没有 `acceptance` 的任务看板。没有验收标准的任务会变成「看起来不错」的橡皮图章。
- `owner` 为 `agent` 或 `model` 的任务。Owner 是角色，不是实体。

拒绝规则：

- 如果仓库没有验证命令，拒绝写入 `AGENTS.md`，直到提供或存根一个。指向缺失门控的路由器比没有路由器更糟。
- 如果待办事项有超过 12 个开放任务，拒绝并要求用户拆分。超过一屏的看板会沦为规划表演。
- 如果项目在追踪文件中附带密钥，拒绝写入状态文件，并首先将密钥泄露作为阻塞性发现提出。

输出结构：

```
<repo>/
├── AGENTS.md
├── agent_state.json
├── task_board.json
└── docs/
    └── agent-rules.md
```

结尾的「下一步阅读」指向：

- 第 33 课将规则占位符转化为可执行约束。
- 第 34 课了解持久状态模式。
- 第 36 课了解每任务的范围合约。