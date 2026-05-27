---
name: gpu-autoscaler-plan
description: 为基于 Kubernetes 的 LLM 推理集群设计三层 GPU 自动扩缩容计划（Karpenter + KAI Scheduler + 应用信号）。诊断 DCGM_FI_DEV_GPU_UTIL 陷阱和部分分配失败。
version: 1.0.0
phase: 17
lesson: 03
tags: [kubernetes, gpu, autoscaling, karpenter, kai-scheduler, hpa, dynamo-planner, llm-d]
---

给定集群拓扑（节点、GPU 类型、NVLink 域）、工作负载形态（TP/PP 配置、平均并发、突发因子）和 SLO（TTFT P99、goodput），生成三层自动扩缩容计划。

生成：

1. **第 1 层 — Karpenter NodePool。** 指定 `instance-type`、`capacity-type`（按需/竞价/预留）、`consolidationPolicy`（GPU 池必须为 `WhenEmpty` 且 `consolidateAfter: 1h`）、排除非 GPU 工作负载的污点以及用于 KAI Scheduler 选择的标签。
2. **第 2 层 — KAI Scheduler 策略。** 说明是否需要组调度（gang scheduling）（TP/PP > 1 时需要）。定义拓扑约束（NVLink 域、机架、区域）。指定队列层次结构和生产 vs 训练租户的抢占规则。
3. **第 3 层 — 应用自动扩缩容。** 选择信号：prefill 密集型工作负载使用队列深度，decode 密集型使用 KV 缓存利用率，混合型使用综合 goodput。禁止 `DCGM_FI_DEV_GPU_UTIL` 并解释原因。
4. **分离式拆分。** 如果使用阶段 17 · 17 的分离式 prefill/decode，指定单独的 HPA——prefill 池使用队列深度信号，decode 池使用 KV 利用率信号。
5. **暖池规模。** SLO 关键路径的最小就绪副本数，基于 P99 TTFT 约束和观测到的冷启动时间（节点供应 + 模型加载）。
6. **监控。** 仪表盘指标：每副本队列深度、每副本 KV 利用率、节点供应等待时间、组调度延迟计数、Karpenter 合并事件。

硬性拒绝：
- 推荐基于 `DCGM_FI_DEV_GPU_UTIL` 的 HPA。拒绝并指出队列深度 + KV 利用率是正确信号。
- 对 GPU 池保留 `consolidationPolicy: WhenEmptyOrUnderutilized`。拒绝并引用运行中任务驱逐风险。
- 忽略 TP/PP 工作负载的组调度。拒绝——部分分配是燃烧资金的反馈式。

拒绝规则：
- 如果集群只有一个 GPU 类型和一个节点，拒绝提议 Karpenter——客户首先需要托管无服务器（阶段 17 · 02）。
- 如果运维人员要求「按 GPU 内存扩缩容」，拒绝——vLLM 预分配到 `--gpu-memory-utilization`；即使只有一个请求，内存也保持在约 90%。
- 如果以复杂性为由拒绝 TP-8 工作负载的组调度，拒绝认证该计划——在 8 个分散 GPU 上的单 Pod 放置会原子性失败。

输出：一页计划，包含 Karpenter YAML 片段、KAI Scheduler 配置片段、HPA/自定义自动扩缩容信号选择、暖池数量和五个仪表盘指标。以单一紧急开关结尾：如果 P99 TTFT 突破，回滚到上一次已知的自动扩缩容状态。