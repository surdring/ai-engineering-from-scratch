---
name: multi-agent-team
description: 构建多智能体软件团队，包含架构师、并行编码员、审阅者和测试者；对照 SWE-bench Pro 测量，并产出交接事后分析。
version: 1.0.0
phase: 19
lesson: 10
tags: [capstone, multi-agent, swe-bench, langgraph, a2a, worktree, roles]
---

给定 GitHub issue URL 和并行级别，部署一个产出可合并 PR 的多智能体软件团队。在 50 个 SWE-bench Pro 问题上评估并发布交接失败直方图。

构建计划：

1. 任务板：基于文件（或 Redis）的类型化消息 JSONL 存储。消息类型：plan_request、subtask、diff_ready、review_needed、review_feedback、approved、test_needed、test_passed、test_failed、replan_needed。
2. 架构师（Opus 4.7）：阅读 issue，编写计划，发出带显式接口（接触的文件、公共函数、测试影响）的子任务 DAG。
3. N 个编码员（Sonnet 4.7）：每个认领一个子任务，生成一个新的 `git worktree add` + Daytona 沙箱，独立实现。
4. 合并协调器：三路合并；LLM 介导的冲突解决仅在文件级重叠上。
5. 审阅者（GPT-5.4）：阅读合并 diff；不能批准自己编写或提议的 diff；输出 approved 或路由到相关编码员的 review_feedback。
6. 测试者（Gemini 2.5 Pro）：在干净沙箱中运行测试套件；输出 test_passed 或附带产物的 test_failed。
7. 交接核算：每条跨角色消息成为带 payload 大小和模型的 Langfuse span。计算 token amplification = total_tokens / single_agent_baseline_tokens。
8. 注入明显的 bug 探测（10% 运行）以测量审阅者假批准率。
9. 在 50 个 SWE-bench Pro 问题上运行；发布 pass@1、相较单智能体基线的实际耗时、逐角色令牌分解、交接失败直方图。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | SWE-bench Pro pass@1 | 50 问题子集 pass@1 |
| 20 | 并行加速比 | 相较单智能体基线的实际耗时 |
| 20 | 审查质量 | 注入 bug 探测上的假批准率 |
| 20 | 令牌效率 | 每解决问题相较单智能体的总令牌数 |
| 15 | 协调工程 | 合并冲突解决、交接失败直方图 |

硬性拒绝：
- 可以批准自己编写或提议的 diff 的审阅者。硬约束。
- 没有匹配单智能体基线运行的报告。多智能体必须在*每美元*上胜出，而非仅 pass@1。
- 消息是自由格式字符串而非类型化 A2A 消息的任务板。
- 悄悄丢弃冲突 diff 而非路由回重新规划的合并协调器。

拒绝规则：
- 拒绝在没有逐角色（令牌 + 美元）预算上限的情况下运行。
- 拒绝打开测试者未在干净沙箱中验证的 PR。
- 拒绝在单次运行中编码员超过 8 个。协调开销在此之上占主导。

输出：包含任务板 + 角色工作者、50 问题 SWE-bench Pro 运行日志、匹配单智能体基线运行、带角色标记 span 和逐角色令牌分解的 Langfuse 仪表盘、注入 bug 探测报告，以及指出最常出故障的三个交接和减少每个的消息模式或提示更改的事后分析的仓库。