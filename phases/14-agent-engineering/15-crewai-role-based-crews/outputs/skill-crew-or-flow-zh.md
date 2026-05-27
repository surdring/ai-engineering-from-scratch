---
name: crew-or-flow
description: 为给定任务选择 CrewAI Crew 或 Flow，并搭建最小实现。
version: 1.0.0
phase: 14
lesson: 15
tags: [crewai, crews, flows, multi-agent, role-based]
---

给定一个任务描述，选择 Crew（自主式）或 Flow（确定性），然后搭建。

决策：

1. 任务是否有 SLA、合规或确定性重放要求？-> Flow。
2. 任务是否是探索性的（研究、初稿、头脑风暴）？-> Crew。
3. 任务是否有 4+ 个专家且由 LLM 选择排序？-> 层级式 Crew。
4. 任务是否有 <=3 个专家且顺序固定？-> 顺序 Crew 或 Flow——优先 Flow。

对于 Crews，生成：

1. Agent 定义：role、goal、backstory（紧凑，<=200 字）、tools。
2. Task 定义：description、expected_output、agent。
3. 带有正确 Process（Sequential | Hierarchical）的 Crew。
4. 一个测试夹具，在样本输入上运行 Crew 并检查是否产生了 expected_outputs。

对于 Flows，生成：

1. `@start` 入口函数。
2. `@listen(topic)` 步骤组成 DAG。
3. 显式事件主题；无魔法广播。
4. 一个重放夹具：给定 kickoff 负载，确定性重新运行。

硬性拒绝：

- 没有 backstory 的 Crews。Backstory 是承重的。
- 没有显式主题名称的 Flows。「隐式链式调用」违背审计目的。
- 只有 2 个专家的层级式 Crews。管理者开销无法收回成本。

拒绝规则：

- 如果用户要求为仅生产的合规任务使用 Crew，拒绝并迁移到 Flow。
- 如果用户要求为开放式研究任务使用 Flow，拒绝并迁移到 Crew。
- 如果 backstory 超过 200 字，拒绝并要求精简。上下文预算是有限的。

输出：`agents.py`、`tasks.py`、`crew.py` 或 `flow.py`，加上带决策理由的 `README.md`。结尾的「下一步阅读」指向第 24 课（Langfuse/AgentOps）了解可观测性，或第 13 课如果 Flow 需要持久化恢复语义。