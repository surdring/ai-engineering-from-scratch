---
name: codec-picker
description: 为给定的生成或压缩任务选择神经音频编解码器（EnCodec / DAC / SNAC / Mimi）
version: 1.0.0
phase: 6
lesson: 13
tags: [codec, encodec, dac, snac, mimi, rvq, semantic-tokens]
---

给定任务（生成式语言模型、压缩、全双工对话、音乐编辑、保真度目标），输出：

1. 编解码器。EnCodec-24k · EnCodec-48k · DAC-44.1k · SNAC-24k · Mimi ·（回退方案：非神经压缩用 Opus）。一句话说明理由。
2. 帧率 + 码本。比特率预算、码本数量（通常 4-12）、目标音频时长的序列长度。
3. 分词方案。扁平式 vs 分层式（SNAC）vs 语义+声学（Mimi）。语言模型如何消费 token。
4. 解码器。编解码器内置解码器 · 外部声码器（HiFi-GAN）· 纯语言模型（不用声码器，直接预测编解码器 token）。解释原因。
5. 训练影响。需要训练编码器/解码器吗？在领域音频上微调（纯语音 → 领域特定音乐）？直接使用冻结的现成方案？

拒绝在延迟预算紧张时将 DAC 用于自回归语言模型工作负载 — 86 Hz 帧率 × 8 码本 = 每 10 秒 5,504 个 token，对快速生成来说过长。拒绝将 Mimi 用于音乐 — 它是针对语音调优的。拒绝将 EnCodec 用于语义条件生成 — 没有语义码本，从文本生成的语音会模糊。