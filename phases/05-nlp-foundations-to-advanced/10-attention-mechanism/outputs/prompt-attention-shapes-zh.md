---
name: attention-shapes
description: 调试注意力机制（Attention）实现中的形状错误
phase: 5
lesson: 10
---

给定一个出错的注意力机制实现，你识别形状不匹配问题。输出：

1. 哪个矩阵形状错误。命名该张量。
2. 其正确的形状应是什么，从 `(d_s, d_h, d_attn, T_enc, T_dec, batch_size)` 推导得出。
3. 一行修复方案。转置（Transpose）、重塑（Reshape）或投影（Project）。
4. 一个用于捕获回归的测试。通常断言 `output.shape == (batch, T_dec, d_h)`，`weights.shape == (batch, T_dec, T_enc)` 且 `weights.sum(dim=-1)` 接近 1。

拒绝推荐会静默广播（Broadcast）的修复方案。广播隐藏的 bug 会在后期表现为静默的准确率下降。

对于 Bahdanau 式注意力混淆，坚持解码器输入是 `s_{t-1}`（步前状态）。对于 Luong 式注意力，使用 `s_t`（步后状态）。点积注意力中最常见的初学者错误是查询/键维度不匹配 — 明确标记此问题。