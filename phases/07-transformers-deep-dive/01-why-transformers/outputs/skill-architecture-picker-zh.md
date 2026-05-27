---
name: sequence-architecture-picker
description: 根据长度、吞吐量和训练预算选择序列架构（RNN、Transformer、SSM、混合）
version: 1.0.0
phase: 7
lesson: 1
tags: [transformers, architecture, rnn, ssm]
---

给定序列问题（最大长度、批次形状、训练 token 预算、推理延迟目标、设备类别），输出：

1. 主要架构。以下之一：Transformer、状态空间模型（SSM，如 Mamba/RWKV）、混合 SSM+注意力、RNN。一句话理由，与主导约束相关联。
2. 上下文长度策略。如果是 Transformer：全注意力截断、滑动窗口大小、RoPE 缩放因子。如果是 SSM：扫描块大小。如果是 RNN：隐藏宽度。
3. 训练 FLOP 概况。来自架构 + 上下文的每个 token 的近似 FLOPs；说明该规格是否符合计算预算。
4. 推理内存概况。Transformer 的 KV 缓存、SSM 的状态大小、RNN 的每 token 内存。标记目标设备是否能容纳单批量大小为 1。
5. 风险提示。一个该选择在该规格规模下已知的具体失败模式（例如，在没有 Flash Attention 的情况下，24GB GPU 上 64K 上下文的 Transformer 会 OOM）。

拒绝在没有明确说明梯度流和并行化代价的情况下，为任何超过 10 亿 token 的训练推荐纯 RNN。拒绝在没有说明 `O(N²)` 内存成本的情况下，为 > 64K 上下文推荐全注意力 Transformer。拒绝在没有指定回退方案的情况下，为生产环境推荐全新架构（发表不到 12 个月）。