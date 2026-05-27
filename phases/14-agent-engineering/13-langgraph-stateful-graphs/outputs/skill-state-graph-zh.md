---
name: state-graph
description: 构建一个 LangGraph 形态的状态机，包含类型化状态、条件边、逐节点检查点和持久化恢复。
version: 1.0.0
phase: 14
lesson: 13
tags: [langgraph, state-machine, durable, checkpointing, human-in-the-loop]
---

给定一个目标运行时、一个状态形态、一组节点函数和一个检查点后端，生成一个有状态智能体图。

生成：

1. 一个类型化的 `State`（dict 或 Pydantic）。文档化每个字段。节点读取状态；返回更新。
2. 一个 `StateGraph`，包含 `add_node`、`add_edge`、`add_conditional_edges`、`set_entry`，以及 `START`/`END` 哨兵。
3. 一个 `Checkpointer` 接口，包含 `save(session_id, node, state)` 和 `load_latest(session_id)`。默认使用 SQLite；允许 Postgres/Redis/自定义。
4. 一个 `Runner`，逐步遍历图，每个节点后序列化状态，捕获 `PausedAtNode` 用于人机协同，并支持 `resume_from` 和可选的 `state_override`。
5. 三个拓扑辅助工具：supervisor（中心路由器）、swarm（共享工具交接）、hierarchical（子图）。

硬性拒绝：

- 没有显式随机种子或墙上时钟捕获的非确定性节点。恢复假设节点输出在给定输入状态时可复现。
- 只保存「摘要」状态的检查点器。序列化完整状态，否则恢复会失败。
- 每条边都是条件边的图。应优先选择线性链与偶尔的分支。

拒绝规则：

- 如果用户要求没有持久化的状态图，拒绝。全部意义就在于持久化恢复；如果不需要恢复，使用第 12 课的工作流模式。
- 如果用户要求「仅在成功时检查点」，拒绝。失败也需要状态——调试从这里开始。
- 如果图有超过约 30 个节点，拒绝平面布局并要求嵌套子图。平面 30 节点图是不可审查的。

输出：`state.py`、`graph.py`、`checkpointer.py`、`runner.py`、`README.md`，解释状态模式、检查点选择和恢复语义。结尾的「下一步阅读」指向第 14 课了解 actor 模型替代方案，第 16 课了解交接/护栏层，或第 23 课了解图步骤上的 OTel span。