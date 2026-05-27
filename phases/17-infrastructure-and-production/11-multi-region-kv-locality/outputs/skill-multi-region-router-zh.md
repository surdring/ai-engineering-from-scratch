---
name: multi-region-router
description: 设计一个具有 KV 缓存局部性、驻留边界、灾备（DR）清单和季度故障转移演练的多区域 LLM 路由计划。
version: 1.0.0
phase: 17
lesson: 11
tags: [multi-region, kv-cache, routing, dr, bedrock-cri, vllm-router, llm-d, gorgo]
---

给定范围内的区域、驻留边界、预期前缀缓存多样性和 TTFT SLA，生成多区域路由和 DR 计划。

生成：

1. **路由器选择。** 选择缓存感知路由器（vLLM Router、llm-d router）并描述 KV 事件通道。说明前缀哈希算法（例如 512 令牌滚动）和打破平局规则（最低队列深度）。
2. **路由策略。** 区域优先还是全局（GORGO 风格）最小化 prefill + RTT？用提示长度分布论证——长提示（>8K 令牌）受益于跨区域路由；短提示不会。
3. **驻留分区。** 在任何优化之前：哪些请求因法律原因（GDPR、HIPAA）绑定到哪些区域。禁止跨驻留路由，即使 TTFT 会改善。
4. **商业 CRI 层。** 推荐是否启用 Bedrock Cross-Region Inference 或 GKE Multi-Cluster Gateway 作为可用性层。明确说明此层不是 TTFT 优化。
5. **灾备清单。** 最少三个文件（HF 仓库 + 引擎配置 + 部署清单）。验证 tokenizer、量化配置、RoPE、聊天模板、LoRA 适配器都包含在内。说明存储方式（S3 跨区域复制、多区域 GCS）。
6. **故障转移演练。** 季度频率。谁执行、测量什么（RTO、RPO、缓存预热时间）。目标：30 分钟 RTO，与 2024 年 JPMorgan 真实演练匹配。

硬性拒绝：
- 为路由优化忽略驻留。拒绝——GDPR 违规胜过 TTFT 收益。
- 声称 Bedrock CRI「解决」跨区域路由。拒绝——CRI 是可用性，不是 TTFT。
- 仅备份权重。拒绝——指明 32% DR 失败统计并要求三文件清单。

拒绝规则：
- 如果只有一个区域在范围内，拒绝该计划——单区域有不同的失败模式（阶段 17 · 03 涵盖）。
- 如果驻留和 TTFT SLA 不兼容（例如欧盟驻留强制每次请求在冷前缀上进行 prefill，且 8K 提示的 P99 TTFT < 100 ms），拒绝承诺 SLA 并升级产品需求。

输出：一页计划，指定路由器、路由策略、驻留分区、CRI 层姿态、DR 清单、季度演练负责人。以要告警的单一指标结尾：跨区域前缀缓存命中率低于计划指定阈值。