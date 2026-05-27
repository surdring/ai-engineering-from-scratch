---
name: gateway-picker
description: 根据规模、延迟预算、合规、运维姿态和定价容忍度选择 AI 网关（LiteLLM、Portkey、Kong AI、Cloudflare/Vercel）。
version: 1.0.0
phase: 17
lesson: 19
tags: [ai-gateway, litellm, portkey, kong, cloudflare, vercel, bifrost, fallback, rate-limit, guardrails]
---

给定 RPS（当前和 12 个月预测）、延迟预算、合规（需要自托管？）、护栏需求（PII 脱敏、越狱检测、审计）和定价容忍度，生成网关推荐。

生成：

1. **主网关。** 指定工具名称。用 RPS 上限、开销和功能匹配论证。
2. **后备链。** 三个提供商按顺序；OpenAI → Anthropic → 自托管是经典配置。计算预期可用性。
3. **速率限制策略。** >500 RPS 推荐滑动窗口；否则令牌桶可接受。每租户分层。
4. **护栏。** 如果需要 PII/越狱，使用 Portkey；如果需要规模 + 护栏，使用 Kong；如果仅开发层，使用 LiteLLM。
5. **可观测性交接。** 指向阶段 17 · 13 的选择；确认 OTel GenAI 约定流畅通过。
6. **迁移。** 如果从应用级集成迁移，分阶段上线（网关上 1% 金丝雀，成功后扩展）。

硬性拒绝：
- LiteLLM 在 >2000 RPS 下。拒绝——Kong 基准显示级联失败；先迁移。
- Portkey 在 TTFT P99 < 100 ms SLA 下。拒绝——30 ms 开销消耗太多预算。
- Cloudflare AI Gateway 用于受监管的本地客户。拒绝——仅托管；无自托管。

拒绝规则：
- 如果规模歧义很大（当前 100 RPS，6 个月内计划 2K+），在承诺 LiteLLM 之前需要迁移计划。
- 如果合规要求 SOC 2 Type II 且所选网关是仅 OSS 无托管 SLA，需要客户自己的 SOC 2 认证。
- 如果团队没有 Kubernetes 且选择 Kong 自托管，拒绝——推荐托管 Kong 或 Portkey 托管。

输出：一页决策，包含网关、后备链、速率限制策略、护栏姿态、可观测性流程、迁移计划。以一个指标结尾：过去一小时网关延迟 P99；突破时告警。