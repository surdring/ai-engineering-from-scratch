---
name: actor-critic-trainer
description: 为给定环境生成 A2C / A3C / GAE 配置，指定优势估计和损失权重
version: 1.0.0
phase: 9
lesson: 7
tags: [rl, actor-critic, gae]
---

给定环境和计算预算，输出：

1. 并行方式。A2C（GPU 批量）vs A3C（CPU 异步）和工作器数量。
2. 推演长度 T。每个环境每次更新的步数。
3. 优势估计器。n 步或 GAE(λ)；指定 λ。
4. 损失权重。`c_v`（值）、`c_e`（熵）、梯度裁剪。
5. 学习率。Actor 和 Critic（如果分开使用则分别设置）。

拒绝在视野 > 1000 的环境上使用单工作器 A2C（太同策略，太慢）。拒绝交付没有优势归一化的方案。标记任何 `c_e = 0` 且观测熵 < 0.1 的运行为熵崩塌。