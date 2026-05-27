---
name: td-agent
description: 为表格型或小特征强化学习任务在 Q-learning、SARSA、期望 SARSA 之间选择
version: 1.0.0
phase: 9
lesson: 4
tags: [rl, td-learning, q-learning, sarsa]
---

给定表格型或小特征环境，输出：

1. 算法。Q-learning / SARSA / 期望 SARSA / n 步变体。一句话理由，与同策略 vs 异策略和方差相关。
2. 超参数。α、γ、ε、衰减调度。
3. 初始化。Q_0 值（乐观 vs 零）及理由。
4. 收敛诊断。目标学习曲线、如果可以 DP 则检查 `|Q - Q*|`。
5. 部署注意事项。推理时探索如何表现？SARSA 的保守性是否必要？

拒绝在状态空间 > 10⁶ 上应用表格 TD。拒绝交付未说明最大偏差（max-bias）问题的 Q-learning 智能体。标记任何训练全程 ε 保持 1.0 的智能体（无利用阶段）。