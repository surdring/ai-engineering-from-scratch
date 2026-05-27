---
name: inference-server
description: 交付推测解码推理服务器，具有 EAGLE-3 或 P-EAGLE 草稿、K8s 自动扩缩容和完整的吞吐/延迟/成本报告。
version: 1.0.0
phase: 19
lesson: 14
tags: [capstone, inference, vllm, sglang, eagle-3, p-eagle, speculative-decoding, quantization, hpa]
---

给定两个开源目标模型（Llama 3.3 70B 和 Qwen3-Coder-30B MoE 或 GPT-OSS-120B），交付具有推测解码、量化和 Kubernetes 自动扩缩容的生产部署栈。发布测量加速比和尾部延迟数字。

构建计划：

1. 在 vLLM 0.7（或 SGLang 0.4）下部署目标模型，使用 FP8 Marlin 量化。
2. 加载 Red Hat Speculators 的对齐 EAGLE-3 草稿（或通过 SpecForge 训练一个）。
3. 基线数字：无推测下 batch 1/8/32 的 tokens/s 和 p50/p99 延迟。
4. 启用 EAGLE-3。重跑同一基准测试。报告加速比、接受率、p99 尾部延迟增量。
5. 启用 P-EAGLE 并行推测；报告更深的树有帮助 vs 有害的拐点。
6. 跨分布运行基准：ShareGPT、HumanEval、领域数据。发布接受率漂移。
7. 在第二个目标模型（MoE）上重复；识别草稿接受中的路由噪声敏感度。
8. 使用跟踪 `queue_wait_ms` 的 HPA 部署在 Kubernetes 上。演示负载三倍时的扩容。
9. 在匹配评估上比较 anthropological Claude Sonnet 4.7 和 OpenAI GPT-5.4 的 $/1M tokens。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | 相较基线的测量加速比 | 两个模型上在匹配质量下 2.5x+ 吞吐 |
| 20 | 现实流量上的接受率 | 逐分布接受率报告 |
| 20 | P99 尾部延迟纪律 | batch 1/8/32 下有/无推测的 p99 |
| 20 | 运维 | K8s 部署、HPA 监控 queue-wait、平滑上线、drain-first upgrade |
| 15 | Write-up 和方法论 | 指标推导清晰、基线匹配 |

硬性拒绝：
- 报告稳态吞吐而不报告尾部延迟。
- HPA 监控 CPU 而非 queue-wait。会在 GPU 饱和下颠簸。
- 忽略草稿-目标版本对齐。漂移的草稿比没有推测成本更高。
- 忽略托管 API 提示缓存折扣的成本比较。

拒绝规则：
- 拒绝在没有上线 drain 的情况下部署。在请求进行中热升级是不合格的。
- 拒绝报告跨分布聚合的接受率。逐分布是强制性的。
- 拒绝在 bs=32 下声称推测解码获胜而没有匹配的非推测数字。

输出：包含 vLLM / SGLang 配置、EAGLE-3 草稿下载脚本、K8s 部署清单、监控 queue-wait 的 HPA 配置、ShareGPT / HumanEval / 领域数据的基准 harness、$/1M tokens 比较表的仓库，以及指出推测解码引入的三大尾部延迟退化和修复每个的缓解措施（batch gating、ngram fallback、quantization tweak）的 write-up。