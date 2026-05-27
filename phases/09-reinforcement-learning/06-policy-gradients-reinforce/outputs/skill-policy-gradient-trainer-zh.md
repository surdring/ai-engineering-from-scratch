---
name: policy-gradient-trainer
description: 为给定任务生成 REINFORCE / actor-critic / PPO 训练配置并诊断方差问题
version: 1.0.0
phase: 9
lesson: 6
tags: [rl, policy-gradient, reinforce]
---

给定环境（离散/连续动作、视野、奖励统计），输出：

1. 策略头。Softmax（离散）或高斯（连续）及参数数量。
2. 基线。无（普通）、运行均值、可学习 `V̂(s)`，或 A2C 评论家。
3. 方差控制。默认开启奖励到终点（reward-to-go）、回报归一化、梯度裁剪值。
4. 熵正则。系数 β 和衰减调度。
5. 批次大小。每次更新的片段数；同策略数据新鲜度约定。

拒绝在视野 > 500 步时使用无基线的 REINFORCE。拒绝用 softmax 头做连续动作控制。标记任何 `β = 0` 且观测到的策略熵 < 0.1 的运行为熵崩塌。