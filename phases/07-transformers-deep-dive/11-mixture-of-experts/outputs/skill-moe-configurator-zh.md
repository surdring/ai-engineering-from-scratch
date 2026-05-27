---
name: moe-configurator
description: 为新的 MoE Transformer 选择专家数量、top-k、负载均衡策略和共享专家布局
version: 1.0.0
phase: 7
lesson: 11
tags: [transformers, moe, mixture-of-experts, scaling]
---

给定 Transformer 规格（总参数量预算、每 token 期望的活跃参数量、可用训练 token、推理硬件），输出：

1. MoE 布局。`n_experts`、`top_k`、`n_shared`。前沿规模选细粒度（256+ 专家，top-8）；较小规模选经典（8 专家，top-2）。一句话理由。
2. 负载均衡策略。无辅助损失（DeepSeek-V3，默认）、Switch 式辅助损失，或专家容量 + token 丢弃。如果无辅助损失，指定 `γ` 值。
3. 专家并行方案。给定 VRAM，如何在多 GPU 间分片专家。说明每专家 VRAM 成本和总机器规模。
4. 路由精度。fp32 路由器分数 vs fp16。路由器精度在大规模时至关重要。
5. 失败模式检查。明确风险：路由器崩溃、专家饿死、全对全网络瓶颈、路由开销导致的推理延迟、检查点内存占用。

拒绝为活跃参数量低于 4B 的场景推荐 MoE — 在同等计算量下密集模型胜出。拒绝在 2026 年新项目中使用纯辅助损失均衡（无辅助损失是默认选择）。拒绝在总参数量超过 80 GB 时交付没有专家并行方案的 MoE。标记 MoE 在延迟敏感的单用户路径上可能比同等密集模型更慢。