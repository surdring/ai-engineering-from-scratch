---
name: mha-configurator
description: 为新 Transformer 推荐注意力头数、KV 头数以及投影策略（MHA / MQA / GQA / MLA）
version: 1.0.0
phase: 7
lesson: 3
tags: [transformers, attention, mha, gqa]
---

给定 Transformer 规格（参数量预算、隐藏维度 `d_model`、目标上下文长度、推理设备内存、训练 vs 推理的优先级），输出：

1. 投影变体。以下之一：MHA、GQA、MQA、MLA。一句话理由，与 KV 缓存约束相关联。
2. 头几何配置。`n_heads`、`n_kv_heads`、`d_head`。值必须满足 `d_model = n_heads * d_head` 且 `n_heads % n_kv_heads == 0`。
3. KV 缓存估算。所选变体在目标上下文长度下每层每 token 的字节数（fp16）。标记单个批次是否超出目标设备内存。
4. 初始化。Q、K、V、O 矩阵的 Xavier / Kaiming 缩放因子。说明是否包含偏置项（2026 年大多数模型已去除）。
5. 可测试性钩子。一个合成任务（如归纳头模式 `A B A ? → B`），该配置训练的两层版本应在此任务上达到 ≥ 95% 的解决率。

拒绝推荐 `d_head < 32` — 注意力动态会崩溃。拒绝为 32K 以上上下文长度且 `n_heads > 16` 推荐 MHA，除非明确估算 KV 缓存成本并建议改用 GQA 或 MLA。拒绝为 1B 以下参数的模型推荐 MLA，除非用户明确在对其进行基准测试。