---
name: vllm-scheduler-reader
description: 通过阅读调度器级配置项来诊断 vLLM 推理配置，识别 PagedAttention、连续批处理（continuous batching）和分块预填充（chunked prefill）中哪个是瓶颈。
version: 1.0.0
phase: 17
lesson: 04
tags: [vllm, paged-attention, continuous-batching, chunked-prefill, serving, scheduler]
---

给定 vLLM 推理配置（模型、dtype、硬件、`--gpu-memory-utilization`、`--max-num-batched-tokens`、`--enable-chunked-prefill`、`--speculative-model` 或 `--speculative-config`、最大并发和观测到的指标集：TTFT 均值/P99、ITL 均值/P99、吞吐 tok/s），生成调度器级诊断。

生成：

1. **配置解读。** 对每个标志，命名它控制的调度器行为和 2026 年默认值。标记任何设为非默认值的标志并说明原因。
2. **瓶颈识别。** 将瓶颈分类为以下之一：PagedAttention 供给不足（KV 块饥饿）、连续批处理停顿（WAITING 队列增长）、分块预填充尺寸错误（TTFT 尾延迟尖峰）、decode 计算瓶颈（ITL 下限）或 HBM 瓶颈（无法容纳批次）。用报告的指标论证。
3. **配置项建议。** 具体、有序的操作——翻转哪个标志、尝试什么值、观察哪个指标。在穷尽调度器级调优之前不要建议「尝试更多 GPU」。
4. **兼容性检查。** 针对 vLLM v0.18.0 特别说明：标记 `--enable-chunked-prefill` + `--speculative-model` 组合为硬不兼容。如果两者都需要，推荐 V1 中的 N-gram GPU 推测解码作为文档记录的例外。
5. **下一步阅读。** 根据诊断揭示的内容，指向 vLLM v0.18.0 发布说明、PagedAttention 论文或 Aleksa Gordic V1 调度器深入讲解之一。

硬性拒绝：
- 没有四个核心指标（TTFT、ITL、吞吐、并发）就进行诊断。拒绝并要求指标集。
- 不检查推测解码配置就推荐 `--enable-chunked-prefill`。
- 将 `DCGM_FI_DEV_GPU_UTIL` 视为扩缩容信号。vLLM 预分配 KV；占空比数字具有误导性。

拒绝规则：
- 如果报告的吞吐在 H100 上低于 100 tok/s，瓶颈可能不是 vLLM——检查客户端侧的 tokenizer、Python GIL 或请求级序列化。
- 如果 `--gpu-memory-utilization` 设置低于 0.7，拒绝进一步调优——运维人员选择将 HBM 留在桌面上，修复方法是先提高上限再翻转调度器标志。
- 如果运维人员要求基于 draft-model speculation 的推测解码 + 分块预填充方案，拒绝并指出 v0.18.0 不兼容。指向阶段 17 · 05 的 EAGLE-3。

输出：一页调度器诊断，列出标志、瓶颈、有序建议、兼容性说明和下一步阅读指引。以「下一步测量什么」段落结尾，根据识别的瓶颈指出 P99 ITL、块分配率或 WAITING 队列深度之一。