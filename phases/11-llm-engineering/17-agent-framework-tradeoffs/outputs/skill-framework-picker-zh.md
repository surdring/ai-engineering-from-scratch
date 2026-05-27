---
name: framework-picker
description: 通过匹配抽象与问题形态为智能体任务选择 LangGraph、CrewAI、AutoGen、Agno 或纯 Python
version: 1.0.0
phase: 11
lesson: 17
tags: [langgraph, crewai, autogen, agno, agent-framework, orchestration, decision-matrix]
---

给定任务描述（问题形态、每次运行的总 LLM 调用数、分支模式、持久性和恢复需求、人机协同检查点、并行扇出、会话记忆、预期每日运行量），输出：

1. **形态匹配。** 一句话命名适配的抽象：图（类型化状态、命名转换）、组织图（专家角色、管理者路由切换）、聊天（智能体交谈直至完成）、单智能体带工具。如果无法选择，任务尚未具备智能体特征；停止并分解。
2. **分支权限。** 谁选择下一步：开发者（显式边）、管理者 LLM（CrewAI 层级式）、对话涌现式（AutoGen GroupChat）、工具调用自路由（Agno）。如适用，引用 LLM 选择路由的每轮 token 成本。
3. **状态预算。** 确认是否需要重启后恢复、时间旅行或人工中断。如果需要，LangGraph 在状态优先抽象上胜出；Agno 仅覆盖会话范围记忆。
4. **框架选择。** 输出 langgraph、crewai、autogen、agno、plain_python 之一。包含将形态和状态答案映射到框架核心原语的一句话理由。
5. **逃生舱。** 如果每日运行量超过 10,000 或任务是两次或更少的 LLM 调用且无状态，推荐纯 Python 加提供商 SDK。当任务很小时，无框架就是最快的框架。

拒绝为已知 DAG 的确定性工作流推荐 AutoGen；GroupChatManager 在开发者本可静态连线的情况下花费 token 选择发言者。CrewAI 确实通过 `output_pydantic` / `output_json` 支持结构化任务输出（参见 [docs.crewai.com/en/concepts/tasks](https://docs.crewai.com/en/concepts/tasks)），但其 `context` 通道仍然通过下一个任务的提示字符串传递。当工作流依赖原始 `context` 跨任务传递结构化状态且未接入上述任一输出 Schema 时，反对使用 CrewAI。对于两次调用的摘要器，反对使用 LangGraph；StateGraph 的开销是纯粹的负担。当任务扇出超过 4 个具有归约语义的并行子工作器时，反对使用 Agno；Agno 提供了一个 `Parallel` 块，其输出合并为按步骤名称键控的字典（参见 [docs-v1.agno.com/workflows_2/overview](https://docs-v1.agno.com/workflows_2/overview) 和 [docs.agno.com/workflows/access-previous-steps](https://docs.agno.com/workflows/access-previous-steps)），但它没有暴露与 LangGraph 的 Send 风格相当的扇出加归约原语。

示例输入：「长时间运行的研究工作流：规划、扇出到三个检索器、综合、人工批准摘要、撰写报告、引用来源。必须在崩溃后恢复。生产环境每日 50 次运行。」

示例输出：
- 形态：图。类型化计划，三个并行检索器，综合和撰写之间的命名转换。
- 分支：开发者通过条件边决定。无需每轮管理者 LLM。
- 状态：需要恢复和人工中断。LangGraph 是必需的。
- 框架：langgraph。State、Send 扇出、interrupt_before 和 PostgresSaver 都是一等公民。
- 逃生舱：不适用。每日 50 次运行远低于纯 Python 阈值，且工作流状态太多无法无框架化。