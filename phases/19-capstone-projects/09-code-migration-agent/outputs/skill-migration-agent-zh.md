---
name: migration-agent
description: 构建仓库级代码迁移智能体，结合确定性配方和智能体回退循环，通过 MigrationBench，并发布失败分类法。
version: 1.0.0
phase: 19
lesson: 09
tags: [capstone, code-migration, openrewrite, libcst, migrationbench, agent, sandbox]
---

给定 Java 8 或 Python 2 仓库，产出迁移分支（到 Java 17 或 Python 3.12），测试套件绿色且覆盖率退化最小。在 50 仓库 MigrationBench 子集上评估。

构建计划：

1. 确定性阶段：OpenRewrite（Java）或 libcst（Python）首先运行机械重写。作为「recipe」提交提交，diff 清晰。
2. Daytona 沙箱：预装目标运行时；逐分支构建；只读源挂载。
3. 智能体循环：LangGraph 或 OpenAI Agents SDK 基于 Claude Opus 4.7 + GPT-5.4-Codex。工具：`run_build`、`read_file`、`edit_file`、`run_test`、`git_diff`。分类失败（dep、syntax、test、build-tool），应用定向修复，重跑。
4. 预算上限：30 分钟、$8、20 回合。超任何一项则挂起并在 `budget_exhausted` 下存档当前 diff。
5. 测试 + 覆盖率门槛：构建绿色然后测试绿色；覆盖率不得下降超过 2%。
6. PR 打开附带 recipe-commit + 智能体提交 + 摘要评论。
7. 失败分类法：逐仓库标签从 `{dep_upgrade_required, build_tool_drift, custom_annotation, test_flake, syntax_edge_case, budget_exhausted, coverage_regression}`。
8. 50 仓库运行，跨 MigrationBench；发布逐类通过率、每仓库成本和覆盖率保留；对比仅确定性基线。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | MigrationBench 通过率 | 50 仓库子集 pass@1 |
| 20 | 测试覆盖率保留 | 相较基础分支的平均覆盖率 delta |
| 20 | 每迁移仓库成本 | 通过运行的平均 $/仓库 |
| 20 | 智能体 / 确定性工具集成 | OpenRewrite vs 智能体处理的修复比例 |
| 15 | 失败分析 write-up | 带有范例的分类法完整性 |

硬性拒绝：
- 跳过确定性阶段的流水线。OpenRewrite 比任何智能体更便宜、更可靠地处理 70-80% 的机械工作。
- 覆盖率退化超过 2% 仍视为通过。
- 将机械和智能体编写的更改打包到一个提交中的 PR。必须分离。
- 报告通过率而没有在同一 50 仓库上的匹配仅确定性基线。

拒绝规则：
- 拒绝在基础分支上强制推送迁移分支。始终新建分支 + PR。
- 拒绝打开沙箱中 CI 未变绿的 PR。
- 拒绝在没有显式修改许可的情况下在公司仓库上运行。

输出：包含双层迁移流水线、50 仓库 MigrationBench 运行日志、失败分类法仪表盘、匹配的仅确定性基线运行的仓库，以及指出三大最常见失败类别和能消除每个的配方更改的 write-up。