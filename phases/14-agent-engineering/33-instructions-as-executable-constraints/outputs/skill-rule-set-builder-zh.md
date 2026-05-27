---
name: rule-set-builder
description: 访谈项目负责人，将现有散文指令分类为五个操作类别，并生成带版本控制的 agent-rules.md 以及 Python 检查器存根。
version: 1.0.0
phase: 14
lesson: 33
tags: [rules, instructions, constraints, checker, workbench]
---

给定一个仓库和任何现有的散文指令（`AGENTS.md`、`CONTRIBUTING.md`、入职文档），生成一个工作台可以执行的五类规则集。

五个类别：

1. `startup`——开始工作前必须满足的条件。
2. `forbidden`——绝不能发生的事。
3. `definition_of_done`——证明任务已完成的标准。
4. `uncertainty`——不确定时智能体的行为。
5. `approval`——需要人工签批的事项。

生成：

1. `docs/agent-rules.md`，每条规则一个 `##` 标题。每条规则携带 `category`、`check` 和一行描述。
2. `tools/rule_checker.py`，包含一个 `RuleChecker` 类，每个 `check` 暴露一个方法。每个方法接收 `TurnTrace` 数据类并返回 `bool`。
3. `tools/rule_report.py` 运行器，加载规则，对追踪运行检查器，输出 `rule_report.json`。
4. 迁移记录文件：哪些散文行变成了哪条规则，哪些因期望性被丢弃，原因是什么。

硬性拒绝：

- 没有 `check` 字段的规则。仅期望性规则属于入职文档，不属于工作台规则集。
- 单一「小心」规则。指定类别和检查，或移除它。
- 需要 LLM 调用的检查。规则检查必须是确定性且廉价的，以便每轮都能运行。
- 超过 200 行的规则文件。按类别拆分为 `agent-rules.{startup,forbidden,done,uncertainty,approval}.md` 并从父级索引路由。

拒绝规则：

- 如果智能体产品无法提供 `TurnTrace`（无仪器化），在至少记录 `read_state_file`、`edited_files` 和 `tests_exit_code` 之前拒绝接入检查器。
- 如果现有指令主要是期望性的（>50%），在生成规则之前提出该发现。规则集会看起来薄；这是正确的。
- 如果因单次历史事件添加了某条规则，附加上事件 id，以便将来审查时可以决定是否仍然需要。

输出结构：

```
<repo>/
├── docs/
│   └── agent-rules.md
├── tools/
│   ├── rule_checker.py
│   └── rule_report.py
└── docs/migration-notes.md
```

结尾的「下一步阅读」指向：

- 第 36 课了解扩展禁止类别的每任务范围合约。
- 第 38 课了解消费规则报告的验证门控。
- 第 39 课了解评分规则合规性的审查智能体。