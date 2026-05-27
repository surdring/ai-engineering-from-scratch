---
name: actor-runtime
description: 构建一个 AutoGen v0.4 形态的 actor 运行时，包含私有状态、每 actor 一个收件箱、仅消息 IPC、故障隔离和死信队列。
version: 1.0.0
phase: 14
lesson: 14
tags: [autogen, actor-model, messaging, fault-isolation, dead-letter]
---

给定一个多智能体任务，生成一个 actor 运行时和所需的 agent actor。

生成：

1. 一个 `Message` 类型，包含 `sender`、`recipient`、`topic`、`body`、`mid`。
2. 一个 `Actor` 基类，包含 `receive(message, runtime)`。Actor 状态是私有的。
3. 一个 `Runtime`，包含共享队列、`send()`、`run_until_idle()` 和死信队列。处理器中的异常进入 DLQ；不传播。
4. 一个拓扑辅助工具：RoundRobin（固定轮转）、Selector（LLM 选择下一个）或自定义广播。
5. 每条消息的可观测性钩子：按照第 23 课发出带有 `gen_ai.agent.name` 和 `gen_ai.operation.name` 的 OTel span。

硬性拒绝：

- 阻塞发送者直到接收者返回的同步消息传递。这是 v0.2 模型；它会破坏故障隔离。
- 跨 actor 共享可变状态。Actor 通过消息读取状态，或根本不读。
- 传播处理器异常的运行时。失败属于 DLQ；让其他 actor 继续运行。

拒绝规则：

- 如果任务只有两个 actor 且以固定来回交互，拒绝 actor 框架并建议提示链（第 12 课）。当有 >=3 个 actor 或异步并发时，actor 才能收回成本。
- 如果用户想要「同步模式」以便「更容易调试」，拒绝。建议日志 + 追踪（第 23 课）代替。
- 如果领域是严格请求/响应且只有单个专家，建议路由（第 12 课）而非 actor 团队。

输出：`message.py`、`actor.py`、`runtime.py`、`teams.py`、`README.md`，解释 DLQ 策略、拓扑选择和 OTel span 的接线方式。结尾的「下一步阅读」指向第 25 课（多智能体辩论）如果 actor 需要协商，第 23 课（OTel）如果需要追踪，或 Microsoft Agent Framework 如果你想要前瞻性运行时。