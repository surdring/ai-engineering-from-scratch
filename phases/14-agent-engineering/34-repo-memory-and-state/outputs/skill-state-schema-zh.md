---
name: state-schema
description: 为智能体状态和任务看板生成项目特定的 JSON Schema，一个带原子写入的 Python StateManager，以及一个迁移脚手架，确保模式版本升级不会损坏工作台。
version: 1.0.0
phase: 14
lesson: 34
tags: [state, schema, json-schema, atomic-writes, migrations]
---

给定一个仓库和在其中运行的智能体产品，为工作台生成模式优先的状态文件。

生成：

1. `schemas/agent_state.schema.json`，覆盖必需键、允许的状态值、数组与 null 的规范以及 `schema_version` 整数。
2. `schemas/task_board.schema.json`，覆盖任务 id 模式、允许的 owner、允许的 status 和 acceptance 数组。
3. `tools/state_manager.py`，暴露 `load`、`commit` 和 `update`，使用临时文件并重命名的原子写入。
4. `tools/migrate_state.py` 脚手架，用于下一次模式升级，如果是未知版本则大声失败。
5. `agent_state.json` 和 `task_board.json` 初始化为 `schema_version: 1` 和一个新的待办列表。

硬性拒绝：

- 没有 `schema_version` 字段的模式。迁移不是可选的。
- 在期望数组的地方允许 `null`。`null` 是伪装成数据的写入时 bug。
- 使用普通 `open(path, "w")` 的写入器。仅使用原子写入；部分文件会损坏真相源。
- 在状态中存储 token、原始聊天记录或 PII。状态用于仓库相关的事实。

拒绝规则：

- 如果仓库没有版本控制，拒绝交付状态文件。原子写入加 git diff 是持久性方案。
- 如果项目没有至少一个验收命令来验证 `done` 转换，拒绝 `status: done` 枚举值。在没有验收检查的情况下添加 `done` 是表演。
- 如果项目打算在没有锁策略的情况下跨进程共享状态，在交付前提出该发现；原子重命名是必要的但不足够。

输出结构：

```
<repo>/
├── agent_state.json
├── task_board.json
├── schemas/
│   ├── agent_state.schema.json
│   └── task_board.schema.json
└── tools/
    ├── state_manager.py
    └── migrate_state.py
```

结尾的「下一步阅读」指向：

- 第 35 课了解在启动时调用管理器的初始化脚本。
- 第 38 课了解读取状态来评分完成度的验证门控。
- 第 40 课了解消费相同模式的交接生成器。