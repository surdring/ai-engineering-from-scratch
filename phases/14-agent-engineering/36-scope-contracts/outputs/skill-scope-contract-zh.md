---
name: scope-contract
description: 生成包含允许/禁止 glob、验收标准和回滚计划的每任务范围合约，以及一个在每次智能体 diff 上运行的 CI 就绪的 glob 感知检查器。
version: 1.0.0
phase: 14
lesson: 36
tags: [scope, contract, globs, diff-check, ci]
---

给定一个任务描述和一个仓库布局，生成范围合约和 diff 感知的检查器。

生成：

1. 任务的 `scope_contract.json`，包含字段：`task_id`、`goal`、`allowed_files`（glob）、`forbidden_files`（glob）、`acceptance_criteria`、`rollback_plan`、`approvals_required`。
2. `tools/scope_check.py`，接收合约路径和被触碰文件列表，返回 `ScopeReport` 并在任何违规时返回非零退出码。
3. CI 步骤（`.github/workflows/scope-check.yml` 或等价物），对合并 diff 运行检查器。
4. `outputs/scope/closed/<task_id>.json` 归档约定，以便合约随变更历史一同发布。

硬性拒绝：

- 没有 `forbidden_files` 的合约。负空间是合约的一部分。
- 代码目录使用原始路径而非 glob 的合约。重构会一夜之间使原始路径无效。
- 为空或为「参见 runbook」的 `rollback_plan` 字段。明确写出来。
- 列在「按情况决定」的审批。审批边界必须是可枚举的。

拒绝规则：

- 如果任务描述没有约束仓库的某个区域，拒绝仅从描述编写 `allowed_files`。询问任务所在的目录。
- 如果仓库没有测试命令，拒绝添加 `acceptance_criteria`，直到提供或存根一个。无法验证的合约只是愿望。
- 如果智能体运行时无法遵守审批边界（无人机协同），在交付前提出该缺口；范围蔓延到需要审批的动作将是主要失败模式。

输出结构：

```
<repo>/
├── scope_contract.json
├── outputs/scope/closed/
│   └── T-XXX.json
├── tools/
│   └── scope_check.py
└── .github/
    └── workflows/
        └── scope-check.yml
```

结尾的「下一步阅读」指向：

- 第 37 课了解将运行的命令链接回合约的运行时反馈。
- 第 38 课了解消费范围报告的验证门控。
- 第 39 课了解审计已关闭合约归档的审查智能体。