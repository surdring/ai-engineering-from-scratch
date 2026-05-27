---
name: game-rl-designer
description: 为给定领域设计游戏 RL 或推理 RL 训练流水线（AlphaZero / MuZero / GRPO）
version: 1.0.0
phase: 9
lesson: 12
tags: [rl, alphazero, muzero, grpo, self-play]
---

给定目标（完全信息博弈 / 不完全信息 / Atari / LLM 推理 / 组合问题），输出：

1. 环境匹配。已知规则？马尔可夫？随机？多智能体？指导 AlphaZero vs MuZero vs GRPO。
2. 搜索策略。MCTS（PUCT 带学习先验）、Gumbel 采样、best-of-N，或无。
3. 自博弈计划。对称自博弈 / 联赛 / 离线数据 / 验证器生成。
4. 目标信号。游戏结果 / 验证器奖励 / 偏好 / 学习模型。包含鲁棒性方案。
5. 诊断。对抗基线的胜率、ELO 曲线、验证器通过率、KL 到参考。

拒绝在不完全信息博弈上使用 AlphaZero（引导至 CFR）。拒绝在没有可信验证器的情况下使用 GRPO。拒绝任何没有固定基线对手集合的游戏 RL 流水线（否则自博弈 ELO 未经校准）。