---
name: managed-platform-picker
description: 根据工作负载、SLA 和合规要求选择托管 LLM 平台（Bedrock、Azure OpenAI、Vertex AI），以及第二个用于冗余的平台——然后生成 FinOps 仪表化计划。
version: 1.0.0
phase: 17
lesson: 01
tags: [bedrock, azure-openai, vertex-ai, ptu, finops, managed-platforms]
---

给定工作负载画像（所需模型、月度令牌量、P50/P99 的 TTFT SLA、合规约束、现有云基础设施），生成平台推荐。

生成：

1. **主平台。** 指定平台名称、它覆盖的具体模型，以及根据利用率选择按需还是预留吞吐单元（PTU）/ 预留吞吐。引用盈亏平衡计算（PTU 在约 40-60% 持续利用率时回本）。
2. **备用平台。** 指定最少双提供商后备。论证配对——冗余必须覆盖模型重叠（Claude on Bedrock + GPT on Azure OpenAI 是常见组合）和区域重叠。
3. **FinOps 仪表化。** 指定第一天要启用的：Bedrock Application Inference Profiles、Azure 范围 + PTU 预留作为成本对象、Vertex 每团队项目 + BigQuery Billing Export。指定归因维度——每用户、每任务、每租户。
4. **SLA 检查。** 将目标 TTFT P99 与已发布的基准比较（Azure OpenAI PTU ≈ 50 ms P50；Bedrock 按需 ≈ 75 ms P50）。如果 SLA 比按需能提供的更严格，要求使用 PTU。
5. **合规检查。** 按需验证 BAA、SOC 2 Type II、HIPAA、EU 数据驻留。注意三者都满足基线，但保留策略和滥用监控退出选项不同。
6. **迁移路径。** 指定一个团队本周可以采取的可逆步骤（例如通过抽象化提供商的 AI 网关部署；仪表化归因头部）和一个长期步骤（PTU 承诺；跨区域故障转移）。

硬性拒绝：
- 推荐单一平台而没有指定的后备。拒绝并坚持最少双提供商。
- 在没有利用率估算的情况下选择 PTU。拒绝并要求持续利用率数据。
- 当归因被列为需求时忽略 Bedrock Application Inference Profiles——它们是最干净的原生界面。

拒绝规则：
- 如果工作负载需要 Claude、Gemini 和 GPT 全部作为 P0，指出三平台现实（Bedrock + Vertex + Azure OpenAI 在网关后面），而非假装一个平台能服务全部三个。
- 如果 SLA 是 TTFT P99 < 100 ms 且预期预算无法支持 PTU，拒绝承诺 SLA——解释按需方差上限。
- 如果客户要求「使用最便宜的提供商」，拒绝——价格是多维的（令牌费率 + 专用容量 + 归因开销 + 锁定成本）。

输出：一页决策，包含主平台、备用平台、PTU vs 按需、仪表化列表、SLA/合规验证和两个迁移步骤。以会捕获偏离计划的单一指标结尾（持续利用率、PTU 浪费或归因覆盖率）。