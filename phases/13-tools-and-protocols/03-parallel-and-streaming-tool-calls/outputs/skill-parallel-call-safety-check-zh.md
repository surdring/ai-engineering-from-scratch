---
name: parallel-call-safety-check
description: 审计工具注册表的并行安全性。标记每个工具的 parallel_safe、记录排序依赖并标记下游速率限制风险
version: 1.0.0
phase: 13
lesson: 03
tags: [parallel-tool-calls, streaming, correlation, rate-limits]
---

给定一个工具注册表（包含名称、描述和执行器的工具列表），返回带注释的副本，添加 `parallel_safe: bool`、`ordering_deps: [tool_name]` 和 `rate_limit_group: name` 字段。

生成：

1. 每工具分类。对每个工具决定：在同一回合内并行运行是否安全（纯读取、不同资源）；不安全（变更操作、共享资源、外部速率限制）。
2. 依赖图。识别一个工具的输出应馈入另一个工具输入的配对。不能在回合内并行化。用 `ordering_deps` 标记。
3. 速率限制分组。访问相同下游 API 的工具共享一个组。宿主应按组而非按工具限制并发。
4. 安全建议。对每个不安全工具，说明是否该回合禁用并行、排队还是按资源分片。
5. 提供商特定标志。当集合中有任何不安全工具时，推荐在 OpenAI 上使用 `parallel_tool_calls=false` 或 Anthropic 上使用 `disable_parallel_tool_use=true`。

硬拒绝：
- 任何审计后没有分类的注册表。默认拒绝；未知意味着不安全。
- 任何在共享资源上标记 `parallel_safe: true` 的写路径工具。竞态条件。
- 任何访问有速率限制的外部 API 但没有 `rate_limit_group` 的工具。

拒绝规则：
- 如果被要求未经检查就标记所有工具为并行安全，拒绝。
- 如果注册表包含在相同资源上的后果性工具（如同一路径上的 `delete_file` 和 `write_file`），拒绝并行化并指向 Phase 14 · 09 了解沙箱级串行化。
- 如果用户声称其工具不会发生竞态，拒绝并要求证据（测试、日志或形式化论证）。竞态在生产中默默发生。

输出：修订后的注册表，以 JSON blob 形式每个工具附带三个新字段，随后是简短摘要，指出最高风险的并行化选择和建议的缓解措施。以建议的当前回合 `tool_choice` 覆盖结尾。