---
name: quantization-picker
description: 根据硬件、引擎、工作负载和质量容差选择 2026 年量化格式，并生成校准 + 验证计划。
version: 1.0.0
phase: 17
lesson: 09
tags: [quantization, awq, gptq, gguf, fp8, nvfp4, calibration]
---

给定硬件（CPU / H100 / H200 / B200 / GB200，及数量）、引擎（llama.cpp / vLLM / TRT-LLM / SGLang）、模型（大小 + 任务类型——常规聊天/推理/代码/多 LoRA）和质量容差（可承受 HumanEval / MATH / MMLU 上 N 分下降），选择量化格式并生成验证计划。

生成：

1. **格式推荐。** 以下之一：GGUF Q4_K_M、GGUF Q5_K_M、GPTQ-Int4 + Marlin、AWQ-Int4 + Marlin、FP8、NVFP4 + FP8 KV 或堆叠组合。通过决策树论证：CPU → GGUF；推理 → FP8；vLLM 上的多 LoRA → GPTQ；常规 GPU 聊天 → AWQ；Blackwell 验证 → NVFP4。
2. **内存预算。** 报告权重 + KV 缓存（在报告并发 × 上下文下）+ 激活。确认适配目标 GPU，或指出多 GPU 需求。
3. **校准计划。** 数据集来源（AWQ/GPTQ 用领域匹配；C4/WikiText 通用作为最后手段）。样本数（领域用 500-2000）。验证集（从校准池中保留 10%）。
4. **验证计划。** 与任务匹配的评估集：代码用 HumanEval，推理用 MATH/MMLU，聊天用 MT-Bench。基线 BF16 vs 量化。如果下降 ≤ 质量容差则发布。
5. **KV 缓存决策。** 与权重量化分离。推理推荐 FP8 KV；注意力准确性边缘时用 BF16 KV；仅验证后使用 INT8 KV。
6. **回滚路径。** 将 BF16/FP8 权重保留在磁盘上；标记若生产质量下降则切换回去。

硬性拒绝：
- 在没有评估集验证的情况下对推理密集型工作负载推荐 NVFP4 权重。
- 对领域模型使用通用网络数据校准。始终使用领域内数据。
- 忘记 HBM 预算中的 KV 缓存。始终逐项列出。
- 声称吞吐数字而不命名内核（Marlin-AWQ vs 普通 AWQ 差 10 倍）。

拒绝规则：
- 如果工作负载本质上是质量边缘化的（开放式创意生成、边界情况推理），拒绝激进 INT4。保持 FP8 或 BF16。
- 如果引擎是 llama.cpp，拒绝 GGUF 以外的任何格式。格式匹配引擎是基本要求。
- 如果用户无法运行 1000 样本评估，拒绝。不允许生产中盲目量化。

输出：一页量化选择，列出所选格式、HBM 预算、校准计划、验证计划、KV 缓存决策和回滚路径。以「下一步测量什么」段落结尾，根据关键风险指出评估集增量、峰值并发下的 KV 缓存压力或真实批次大小下的吞吐之一。