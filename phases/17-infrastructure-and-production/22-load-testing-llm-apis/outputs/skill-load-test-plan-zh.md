---
name: load-test-plan
description: 设计现实的 LLM 负载测试——选择工具（LLMPerf、k6、GenAI-Perf、guidellm），构建四种模式（稳态、斜坡、尖峰、浸泡），并在 CI 中把关。
version: 1.0.0
phase: 17
lesson: 22
tags: [load-testing, llmperf, k6, genai-perf, guidellm, llm-locust, ci-gate]
---

给定工作负载（端点、TTFT/TPOT/错误的 SLA）、目标规模（并发、RPS）和 CI 姿态（PR 把关或仅发布），生成负载测试计划。

生成：

1. **工具。** LLMPerf 用于基线运行；k6 + 流式扩展用于 CI 把关；GenAI-Perf 用于 NVIDIA 参考运行；guidellm 用于大规模合成。仅当已在 Locust 上时使用 LLM-Locust。
2. **提示分布。** 来自真实流量的输入令牌均值 + 标准差（如果可用）或已发布的分布（ShareGPT / HumanEval）。禁止循环使用一个提示。
3. **四种模式。** 稳态、斜坡、尖峰、浸泡。每种：目标 RPS、持续时间、预期失败模式。
4. **CI 把关。** 具体阈值：TTFT P95 < X，5xx < 5%，TPOT < Y。每 PR 运行时间：3-5 分钟。
5. **指标对齐。** 注意报告工具是 GenAI-Perf 风格（ITL 排除 TTFT）还是 LLMPerf 风格（ITL 包含 TTFT）。选择一种并保持一致。
6. **产出。** 一个提交到仓库的脚本文件（k6 JS、LLMPerf CLI）。

硬性拒绝：
- 使用均匀提示进行负载测试。拒绝——数字会说谎。
- 没有流式支持的负载测试。拒绝——LLM 端点默认是流式的。
- 在不承认指标定义差异的情况下跨工具比较数字。拒绝。

拒绝规则：
- 如果团队打算在普通 Locust 上运行而不使用 LLM-Locust 扩展，拒绝——GIL 陷阱。
- 如果 CI 把关预算每 PR < 60s，拒绝完整浸泡——提议快速稳态加单独的夜间浸泡。
- 如果提示分布数据不可用，需要文档记录的已发布分布（ShareGPT）并注明假设。

输出：一页计划，包含工具、提示分布、带目标的四种模式、CI 把关阈值、指标对齐。以单一 CI 输出结尾：仅当所有阈值满足、3 次运行稳定时 PR 变绿。