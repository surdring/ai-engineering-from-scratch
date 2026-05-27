---
name: workbench-pack
description: 生成一个项目调优的即插即用智能体工作台包——规则根据团队历史优化，范围 glob 匹配仓库，评分标准维度扩展一个领域特定条目。
version: 1.0.0
phase: 14
lesson: 42
tags: [capstone, workbench-pack, installer, schemas, drop-in]
---

给定一个仓库、团队的事件历史以及在其中运行的智能体产品，生成一个调优的 agent-workbench-pack 和安装器。

生成：

1. `agent-workbench-pack/` 目录，匹配规范布局：AGENTS.md、docs/、schemas/、scripts/、bin/、README.md、VERSION。
2. 一个 `bin/install.sh`，拒绝在没有 `--force` 的情况下覆盖现有包，并在目标仓库中写入 `.workbench-version`。
3. 项目调优版本的 `agent-rules.md`（每个类别至少一条规则，来源于团队最近六次事件）、`reviewer-rubric.md`（包含第六个领域维度）和 `scope_contract.schema.json`（包含项目特定的 glob）。
4. 一个 `lint_pack.py` 脚本，在脚本与模式之间或 VERSION 与模式的 `schema_version` 之间不一致时失败。
5. 可选的 CI 集成，在演示分支上安装包，并对已知良好任务运行验证门控。

硬性拒绝：

- 包含项目特定任务的包。任务存在于目标仓库的看板上。
- 绑定到单一供应商 SDK 的包。仅框架无关；SDK 接线是目标仓库的工作。
- 变更状态文件的安装器。安装器是幂等的表面操作；状态属于智能体和人类。
- 没有对应检查函数的规则。期望性规则属于入职文档，不属于包。

拒绝规则：

- 如果事件历史为空，拒绝交付调优的 `agent-rules.md`。使用规范默认值并提出该缺口。
- 如果目标仓库的 CI 与安装不兼容（没有 `.github/workflows/`，无等价物），拒绝可选 CI 步骤并记录手动路径。
- 如果团队使用包的私有分支，拒绝编写公共安装器。私有安装器携带私有不变量。

输出结构：

```
agent-workbench-pack/
├── AGENTS.md
├── docs/
├── schemas/
├── scripts/
├── bin/install.sh
├── lint_pack.py
├── VERSION
└── README.md
```

结尾的「下一步阅读」指向：

- 第 41 课了解此包改进的前后对比基准。
- 第 30 课（评估驱动智能体开发）了解消费包裁决的评估循环。
- [SkillKit](https://github.com/rohitg00/skillkit) 了解将包分发给 32 个 AI 智能体。