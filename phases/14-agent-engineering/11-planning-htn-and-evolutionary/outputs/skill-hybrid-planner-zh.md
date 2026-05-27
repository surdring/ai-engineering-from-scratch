---
name: hybrid-planner
description: 构建一个混合规划器——ChatHTN 用于可证明正确的计划，AlphaEvolve 用于带机器可检查评估器的代码搜索——并为问题选择正确的规划器。
version: 1.0.0
phase: 14
lesson: 11
tags: [planning, htn, chathtn, alphaevolve, evolutionary-search]
---

给定一个问题类别（策略绑定的工作流 vs 代码优化 vs 开放式任务），选择一个规划器并生成正确的脚手架。

决策：

1. 问题是否有硬性前置条件 / 策略 / 调度约束？-> HTN（ChatHTN）。
2. 问题是否有确定性的、机器可检查的适应度函数？-> 进化搜索（AlphaEvolve）。
3. 两者都不是？-> 转向 ReAct（第 01 课）或 ReWOO（第 02 课）。

对于 HTN，生成：

1. `Operator` 类型，包含 `preconditions`、`effects_add`、`effects_remove`。
2. `Method` 类型，包含 `task`、`preconditions`、`subtasks`。
3. 一个规划器，优先尝试方法，回退到 LLM 分解，并缓存成功的 LLM 分解。
4. 一个验证步骤，拒绝引用未知算子或方法的 LLM 分解。

对于进化搜索，生成：

1. 一个候选程序的种子种群。
2. 一个返回标量适应度的确定性评估器。
3. 一个变异算子（LLM 驱动或基于规则）。
4. 一个选择循环（保留 top-k，变异，重复），包含早停。

硬性拒绝：

- ChatHTN 中 LLM 输出未经算子模式验证而直接应用。正确性声明会失效。
- AlphaEvolve 中评估器调用 LLM 评判器。适应度必须是确定性的；LLM 评判器引入的随机噪声是循环无法恢复的。
- 任一模式用于开放式任务（「写一篇博客」）。没有评估器，没有前置条件 -> 使用 ReAct。

拒绝规则：

- 如果领域没有明确的算子模式，拒绝 ChatHTN。建议 ReWOO 或纯 ReAct。
- 如果领域没有机器可检查的适应度，拒绝 AlphaEvolve。建议 Self-Refine（第 05 课）。
- 如果用户希望「规划器 + LLM 做最终决定」，拒绝。符号正确性和 LLM 探索之间的分离是承重的。

输出：`operators.py`、`methods.py`、`planner.py`（HTN）或 `evaluator.py`、`mutator.py`、`loop.py`（进化搜索），加上带决策理由的 `README.md`。结尾的「下一步阅读」指向第 25 课如果辩论式验证适合该问题，或第 02 课如果任务实际上是 ReWOO 形态。