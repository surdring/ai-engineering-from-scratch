---
name: positional-encoding-picker
description: 根据上下文长度和训练预算选择位置编码（RoPE、ALiBi、正弦编码）+ 缩放策略
version: 1.0.0
phase: 7
lesson: 4
tags: [transformers, positional-encoding, rope, alibi]
---

给定 Transformer 规格（推理目标上下文长度、训练上下文长度、外推需求、按 token 计的微调预算），输出：

1. 基础编码。以下之一：RoPE、ALiBi、正弦编码、可学习绝对位置编码。一句话理由。
2. 超参数。如果是 RoPE：`base` 值、`d_head` 需为偶数。如果是 ALiBi：斜率公式。如果是正弦编码：`max_len`。
3. 扩展策略。如果目标长度 > 训练长度：NTK-aware 缩放因子、YaRN 配置、LongRoPE 规格，或位置插值比率。声明微调 token 预算。
4. 测试计划。最大上下文下的 NIAH（大海捞针）通过率目标、与训练长度基线的困惑度差距在 X 以内。
5. 回退方案。如果长上下文评估失败：用更大的 `base` 重新训练、切换到 ALiBi，或限制部署的上下文长度。

拒绝在 2026 年为新模型推荐正弦编码或可学习绝对位置编码 — 它们不可外推，且所有现代技术栈都假定使用 RoPE 或 ALiBi。拒绝在没有微调阶段的情况下将 RoPE 扩展到训练长度的 8 倍以上。拒绝在没有在全部署长度上运行 NIAH 的情况下交付长上下文配置。