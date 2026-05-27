---
name: orchestration-picker
description: 为给定问题选择一个编排拓扑（supervisor、swarm、hierarchical、debate 或无），并最小化实现它。
version: 1.0.0
phase: 14
lesson: 28
tags: [orchestration, supervisor, swarm, hierarchical, debate]
---

给定一个产品领域和一个任务类别，选择最小拓扑。

决策：

1. 1 个智能体 + 工作流模式（第 12 课）够用？-> 根本不用拓扑。
2. 2-4 个专家且职责不同？-> **supervisor-worker**。
3. 延迟关键且专家可以干净交接？-> **swarm**。
4. 10+ 个专家，supervisor 上下文预算不够？-> **hierarchical**。
5. 准确率比成本更重要，多提案 + 评判有帮助？-> **debate**（第 25 课）。

生成：

1. 所选拓扑脚手架。
2. swarm 上的跳数计数器；hierarchical 上的嵌套深度限制；debate 上的轮次上限。
3. 每次交接或每步的可观测性钩子（OTel GenAI span，第 23 课）。
4. 一个「为什么选这个，不选那个」的 README 部分。

硬性拒绝：

- 将 3 次 LLM 顺序调用称为「多智能体」。那是提示链。
- 没有跳数计数器的 swarm。弹跳是必然的。
- 每个分支底部只有 1 个专家的 hierarchical。扁平化。

拒绝规则：

- 如果用户想为单个 ReAct 循环就能处理的任务使用多智能体，拒绝并建议第 01 课。
- 如果用户想为 2 步任务使用 supervisor，拒绝并建议提示链（第 12 课）。
- 如果领域有合规/审计要求，拒绝 swarm 并建议 supervisor 或 hierarchical。

输出：拓扑脚手架 + 带决策理由的 README。结尾的「下一步阅读」指向第 13 课（LangGraph）了解 supervisor 实现，第 16 课（OpenAI Agents SDK）了解交接即工具，或第 25 课了解辩论细节。