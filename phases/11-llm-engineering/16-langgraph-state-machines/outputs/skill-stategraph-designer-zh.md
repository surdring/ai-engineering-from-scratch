---
name: stategraph-designer
description: 将智能体任务转化为带有命名节点、类型化状态、归约器、检查点和人工中断的 LangGraph StateGraph
version: 1.0.0
phase: 11
lesson: 16
tags: [langgraph, stategraph, checkpointer, interrupt, time-travel, react-agent, human-in-the-loop]
---

给定智能体任务（面向用户的目标、可用工具、预期轮次数、带安全影响范围的副作用、持久性要求、目标延迟预算），输出：

1. **节点列表。** 命名每个离散步骤：LLM 思考器、每个工具执行器、每个人工审查步骤、任何摘要器或评论器、任何检索器。如果任何节点涉及多个关注点，拒绝该设计；将其拆分。
2. **状态 Schema。** TypedDict（或 Pydantic）字段，每个列表使用归约器。消息日志始终使用 Annotated[list, add_messages]。将任何任务特定的列表从消息中提升出来（计划、预算计数器、检索文档列表），以便归约器在并行更新下保持正确。
3. **边映射。** 静态边：下一步是确定性的。条件边带命名路由函数：仅在模型选择下一步时使用。拒绝任何其路由函数依赖于尚未在先前节点中完成的新 LLM 调用的图。
4. **中断放置。** interrupt_before 放在每个具有不可逆副作用的节点上（写入、删除、支付、带成本的外部 API 调用）。interrupt_after 放在模型节点上，当输出验证在单独进程中运行时。拒绝在任何产生副作用的节点上使用 interrupt_after；那时副作用已经发生了。
5. **检查点器。** MemorySaver 仅用于测试。在必须能够存活重启的任何环境中从 PostgresSaver、SQLiteSaver、RedisSaver 中选择。确认 thread_id 策略（按用户、按会话、按对话）和检查点 TTL。

拒绝交付没有检查点器的 LangGraph。没有检查点器意味着无法恢复、无法时间旅行、无法人机协同回放。拒绝交付没有 add_messages 的 messages 字段；第二次写入会静默覆盖第一次，一半对话消失。拒绝每个转换都是由规划器 LLM 路由的条件边的图；那是带额外步骤的 AutoGen，每轮都会消耗 token。

示例输入：「基于 Anthropic Claude 的退款处理智能体，使用三个工具（lookup_order、issue_refund、send_email），超过 100 美元的退款前必须暂停等待人工审批，必须在服务器重启后恢复，p95 延迟预算 8 秒。」

示例输出：
- 节点：agent（LLM 调用）、lookup_tool、refund_tool、email_tool、human_review。
- 状态：messages 带 add_messages、order_context（覆盖）、refund_amount（覆盖）、reviewer_decision（覆盖）。
- 边：agent 到 should_continue 路由器，分支包括 lookup_tool、refund_tool、email_tool、human_review、END。工具节点返回 agent。
- 中断：refund_amount > 100 时 interrupt_before 放在 refund_tool 上。lookup_tool 或 email_tool 不做中断。
- 检查点器：PostgresSaver，thread_id 为 "user:{user_id}:case:{case_id}"，30 天 TTL。