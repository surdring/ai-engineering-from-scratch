---
name: inference-optimizer
description: 为新的推理部署选择注意力实现、KV 缓存策略、量化和推测式解码
version: 1.0.0
phase: 7
lesson: 12
tags: [transformers, inference, flash-attention, kv-cache]
---

给定推理部署（模型名称 + 参数量、目标硬件、并发、最大上下文长度、延迟 SLO、吞吐量目标），输出：

1. 推理服务栈。vLLM（默认生产选择）、SGLang（每 token 最低延迟）、TensorRT-LLM（NVIDIA 最优）、llama.cpp（边缘/CPU）、MLX（Apple 芯片）。一句话理由。
2. 注意力实现。Flash Attention 2（Ampere/Ada 默认）、Flash Attention 3（Hopper）、Flash Attention 4（Blackwell，仅前向）。指定回退方案。
3. KV 缓存。数据类型（fp16 默认，如支持则 fp8）、分页 vs 连续、前缀缓存开启/关闭、并行采样共享 KV。
4. 量化。fp16 / bf16（默认）、int8（仅权重）、AWQ / GPTQ / GGUF 用于权重。仅在基准测试后使用激活量化。
5. 额外加速。推测式解码（EAGLE 2 / Medusa / 草稿模型）、连续批处理（始终开启）、分块预填充（长 Prompt 工作负载）、如有重复 Prompt 则开启前缀缓存。

拒绝为训练部署 Flash Attention 4 — 发布时仅支持前向。拒绝在未对目标任务进行质量影响基准测试的情况下推荐 fp8 KV 缓存。标记任何 70B+ 且没有 GQA 的模型在 32K+ 上下文下 KV 缓存不可管理。要求任何重复系统 Prompt 的智能体/工具调用部署开启前缀缓存。