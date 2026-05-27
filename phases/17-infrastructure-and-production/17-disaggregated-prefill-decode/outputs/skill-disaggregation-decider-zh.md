---
name: disaggregation-decider
description: 决定是否为给定工作负载和集群采用分离式 prefill/decode（Dynamo 或 llm-d）。量化 prefill:decode 比率、KV 传输成本和预期节省。
version: 1.0.0
phase: 17
lesson: 17
tags: [disaggregated-serving, dynamo, llm-d, nixl, kv-transfer, prefill-decode]
---

给定工作负载画像（提示/输出长度分布、模型、并发）、集群拓扑（GPU、网络结构、RDMA 可用性）和当前推理成本，生成分离决策。

生成：

1. **分离？** 是/否，附带编号论证。基线：提示 > 512 且输出 > 200。网络结构：RDMA 可用有帮助；仅 TCP 会拉长盈亏平衡。
2. **技术栈选择。** NVIDIA Dynamo（在 vLLM/SGLang/TRT-LLM 之上的托管编排器）或 llm-d（Kubernetes 原生 Services）。匹配运维上下文。
3. **Prefill:decode 比率。** 使用 Dynamo Planner Profiler 读数，或从工作负载形态计算（prefill TFLOPS vs decode bytes/sec）。示例：RAG 密集型 2 prefill : 1 decode；输出密集型 1:2。
4. **KV 传输计划。** 指定传输方式（NIXL over InfiniBand / RDMA / TCP 后备）。为提示 P99 计算每次请求的传输税。
5. **路由器集成。** 前面必须有缓存感知路由器（阶段 17 · 11）——没有前缀匹配的分离会失去缓存收益。
6. **预期节省。** 计算 vs 共存基线；引用已发布案例（相同 SLA 下 30-40%）。

硬性拒绝：
- 对短提示工作负载（<512 令牌）进行分离。拒绝——传输税占主导。
- 在没有缓存感知路由器的情况下部署。拒绝——盲目路由否定 KV 局部性。
- 忽略拓扑（机架打包）。拒绝——多机架跳转的 KV 传输比同机架 RDMA 成本更高。

拒绝规则：
- 如果集群 GPU < 4，拒绝——池多样性不足以让分离带来回报。
- 如果没有 RDMA/InfiniBand 且没有计划，注意 TCP 将盈亏平衡提高到提示 >2K；重新评估。
- 如果团队无法运营具有每角色扩缩容的两个 GPU 池，拒绝 llm-d 并要求 Dynamo 作为托管替代。

输出：一页决策，包含分离是/否、技术栈选择、比率、传输、路由器、预期节省。以要验证的单一指标结尾：KV 传输 P99 延迟；以超过计划指定阈值为门槛。