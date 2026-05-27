---
name: vllm-stack-decider
description: 根据工作负载和设备群规模决定 vLLM 部署布局——生产栈 Helm 图表、KV 卸载（原生 CPU 或 LMCache）、路由器/可观测性集成。
version: 1.0.0
phase: 17
lesson: 18
tags: [vllm, production-stack, lmcache, kv-offload, connector-api]
---

给定工作负载（提示形态、并发、前缀复用模式）、设备群（引擎、GPU 类型）和运维上下文（Kubernetes 原生、多租户、预算），生成 vLLM 技术栈计划。

生成：

1. **技术栈。** 使用 vLLM production-stack Helm 图表（推荐用于新部署）或自己搭建。说明适用于哪些 operator/CRD。
2. **KV 卸载。** 选择：
   - 无（短提示、低并发——开销超过收益）。
   - 原生 vLLM CPU 卸载（单引擎 HBM 压力，简单）。
   - LMCache 连接器（多引擎前缀复用、抢占严重或多租户共享提示）。
3. **HBM 利用率监控。** 设置带余量的 `--gpu-memory-utilization`；持续 92%+ 时告警作为预抢占信号。
4. **路由器集成。** 缓存感知路由器（阶段 17 · 11）。确认 KV 事件通道已配置。
5. **可观测性。** 每引擎 Prometheus 抓取，OTel GenAI 属性（阶段 17 · 13），来自 production-stack 的 Grafana 仪表盘模板。
6. **预期影响。** 量化相对于当前的预期吞吐增益——引用 16x H100 基准形态（当 KV 占用超过 HBM 时 LMCache 有帮助）。

硬性拒绝：
- 在没有共享前缀或抢占的情况下部署 LMCache。拒绝——开销，无收益。
- 在没有 HBM 压力监控的情况下运行 vLLM。拒绝——首次抢占将是意外。
- 当 Helm 图表覆盖用例时手工搭建 production-stack。拒绝——重复发明成本。

拒绝规则：
- 如果设备群引擎 <2，拒绝 LMCache——跨引擎复用是重点；单引擎使用原生。
- 如果工作负载提示 < 1K 令牌且并发 < 100，拒绝任何类型的卸载——HBM 余量足够。
- 如果团队没有 K8s 能力，拒绝 production-stack——从单引擎 vLLM + 简单代理开始。

输出：一页计划，指定技术栈、KV 卸载选择、HBM 监控、路由器集成、可观测性、预期影响。以单一门槛结尾：过去 24h HBM 利用率 P99。