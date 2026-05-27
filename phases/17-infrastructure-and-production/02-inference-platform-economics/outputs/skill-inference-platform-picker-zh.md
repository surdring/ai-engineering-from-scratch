---
name: inference-platform-picker
description: 根据工作负载、SLA、预算和运营约束选择推理平台（Fireworks、Together、Baseten、Modal、Replicate、Anyscale 或定制芯片）。标准化每令牌、每分钟和每预测定价。
version: 1.0.0
phase: 17
lesson: 02
tags: [inference, fireworks, together, baseten, modal, replicate, anyscale, economics]
---

给定工作负载画像（模型、令牌/天、持续利用率、TTFT SLA、突发因子、合规、Python vs 混合技术栈），生成平台推荐。

生成：

1. **主平台。** 指定平台名称和具体定价层（无服务器 vs 专用 vs 批处理）。用匹配的工作负载特征论证——例如「Fireworks 无服务器，因为 TTFT < 500 ms 是 SLA 且流量是突发性的。」
2. **有效成本。** 将所选定价模型标准化为 $/M 输出令牌。与至少两个替代方案比较。指出每分钟优于每令牌（高于约 30% 持续利用率时）或反之。
3. **冷启动计划。** 对无服务器选择（Fireworks、Modal、Replicate），说明预期冷启动延迟和缓解措施（预热、min_workers=1、实时迁移）。对专用选择（Baseten、Anyscale），跳过此节但注明权衡。
4. **亚军。** 指定第二个平台和在什么明确条件下会切换（例如「如果达成需要 HIPAA + 专用 GPU 的企业交易，则迁移到 Baseten」）。
5. **网关层。** 推荐是否用 AI 网关（LiteLLM、Portkey、Kong AI Gateway）前置平台，以隔离产品免受提供商切换的影响。默认：是，除非规模低于 500 RPS。

硬性拒绝：
- 不标准化就比较每令牌和每分钟。拒绝并坚持使用有效 $/M 令牌。
- 因为 Fireworks「最快」而选择它，但没有根据已发布基准验证 TTFT SLA。
- 对任何不受延迟约束的工作负载推荐定制芯片（Groq、Cerebras、SambaNova）。它们定价溢价，仅在交互式 SLA 上才能证明其价值。

拒绝规则：
- 如果工作负载需要受监管框架（SOC 2 Type II、HIPAA）且客户选择 Modal 或 Replicate，拒绝——两者都没有 Baseten 或 Anyscale 的企业足迹。建议 Baseten。
- 如果预期流量低于 100k 令牌/天，拒绝推荐按分钟计费（Baseten、Modal、Anyscale）。经济上不划算——默认使用市场（OpenRouter、DeepInfra）或托管超大规模提供商。
- 如果客户想要「最便宜的」，拒绝——指出多维成本函数（令牌费率 + 冷启动 + 归因 + 网关 + 开发体验）。

输出：一页推荐，指定主平台、有效成本、冷启动计划、亚军、网关姿态。以会揭示选择错误的单一指标结尾（冷启动 P99、每令牌费率或利用率漂移）。