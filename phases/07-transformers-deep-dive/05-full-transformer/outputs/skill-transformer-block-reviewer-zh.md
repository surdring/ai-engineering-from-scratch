---
name: transformer-block-reviewer
description: 对照 2026 默认标准审查 Transformer 块实现并标记偏差
version: 1.0.0
phase: 7
lesson: 5
tags: [transformers, architecture, review]
---

给定 Transformer 块的源码（PyTorch / JAX / numpy / 伪代码）及其预期角色（编码器 / 解码器 / 编码器-解码器），输出：

1. 连接检查。Pre-norm 还是 Post-norm。每个子层周围的残差连接。标记 Post-norm 在 2026 年非默认，除非作者说明原因。
2. 归一化。LayerNorm vs RMSNorm。首选 RMSNorm。标记 Q/K/V/O 投影中是否存在偏置项 — 2026 年大多数模型已去除。
3. 注意力形状。MHA / GQA / MQA / MLA。对于解码器块：确认因果遮罩已应用。对于交叉注意力：确认 Q 来自解码器，K/V 来自编码器。
4. FFN。激活函数（ReLU / GELU / SwiGLU / GeGLU）。扩展比率。SwiGLU 配合约 2.67× 是现代默认值；4× ReLU/GELU 是经典配置。
5. 位置信号。确认 RoPE / ALiBi / 绝对位置编码在预期的位置应用（通常对 Q、K 投影应用 RoPE）。

拒绝签署一个超过 12 层且使用 Post-norm 且没有预热计划的块 — 训练会发散。拒绝没有因果遮罩的解码器块。标记任何 FFN 扩展比低于 2× 的块可能容量不足。警告如果块中硬编码了 `d_model` 而没有用于替换分块大小的配置字段。