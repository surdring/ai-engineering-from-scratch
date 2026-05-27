---
name: eagle3-rollout
description: 生成分阶段 EAGLE-3 推测解码上线计划，在发布前测量真实流量上的接受率 alpha。
version: 1.0.0
phase: 17
lesson: 05
tags: [speculative-decoding, eagle-3, vllm, alpha, production-rollout]
---

给定目标模型、硬件（GPU 类型和数量）、流量描述（通用聊天/代码/专业）、并发目标和当前基线指标（TTFT、ITL、吞吐），生成分阶段 EAGLE-3 上线计划。

生成：

1. **基线测量计划。** 哪个基准（LLMPerf、GenAI-Perf 或生产影子）、哪个提示分布、哪个并发点、记录哪些指标（TTFT 均值/P99、ITL 均值/P99、吞吐、并发）。
2. **草稿头选择。** 通用聊天使用 ShareGPT 训练的 EAGLE-3。专业流量（代码、医疗、法律）使用领域训练的 EAGLE-3，或决定先训练一个再发布。
3. **配置。** 精确的 vLLM `speculative_config` 字段（method、model、num_speculative_tokens）。注意 v0.18.0 兼容性：draft-model speculation 不能与 `--enable-chunked-prefill` 组合；V1 中的 N-gram GPU 推测解码是例外。
4. **Alpha 门槛。** 在生产并发下目标 alpha >= 0.55。测量流程：影子流量 24 小时，记录 vLLM `spec_decode_metrics`，接受的令牌数除以请求的草稿长度。如果在任何 1 小时窗口内 alpha 低于 0.45，触发紧急开关。
5. **尾延迟监控。** 绘制 P99 ITL 增量（spec 开 - spec 关）。如果增量为正，被拒绝草稿的双遍模式有问题。降低 K 或在此工作负载上禁用。
6. **盈亏平衡检查。** 在报告的并发下，计算当前验证开销的盈亏平衡 alpha。仅当测量的 alpha 超过盈亏平衡至少 0.1 时才发布。

硬性拒绝：
- 不在生产流量上测量 alpha 就发布。拒绝并要求 24 小时影子测量。
- 声称 2-3x 加速而不说明测量的 alpha 值。
- 对延迟不是约束的离线批处理任务启用推测解码。
- 在 vLLM v0.18.0 上组合 draft-model speculation 和分块预填充。硬不兼容。

拒绝规则：
- 如果流量主要是非常短的输出（均值低于 50 个令牌），拒绝。草稿开销占主导；发布纯目标模型。
- 如果硬件是消费级（RTX 4090/5090）且批次大小保持在 8 以下，推荐纯目标模型——验证开销的批次摊销需要硬件无法提供的并发。
- 如果用户想在没有测量循环的情况下自动调优 K，拒绝。K 由测量的 alpha 加验证开销决定；没有自动调优能替代测量。

输出：一页分阶段上线计划，列出基线 → 配置 → alpha 门槛 → 尾延迟监控 → 盈亏平衡确认。以「下一步测量什么」段落结尾，根据诊断指出领域特定 EAGLE-3 训练、降低 K 或回退到纯目标模型之一。