---
name: prompt-caching-planner
description: 设计缓存友好的提示布局并选择正确的提供商缓存模式
version: 1.0.0
phase: 11
lesson: 15
tags: [llm-engineering, caching, cost]
---

给定一个提示（系统 + 工具 + few-shot + 检索 + 历史 + 用户）和一个使用画像（每小时请求数、所需 TTL、提供商），输出：

1. **布局。** 重新排序的段，标记单个缓存断点；解释哪些段是稳定的，哪些是变化的。
2. **提供商模式。** Anthropic cache_control、OpenAI 自动或 Gemini CachedContent。根据 TTL 和复用模式给出理由。
3. **盈亏平衡。** TTL 内每次写入的预期读取数；带数学计算的净成本 vs 无缓存。
4. **验证计划。** CI 断言第二次相同请求上 cache_read_input_tokens > 0；面板按缓存 vs 非缓存 token 拆分。
5. **失败模式。** 列出此设置中缓存最可能未命中的三个原因（动态时间戳、工具重新排序、近似重复文本）以及你将如何防止每个原因。

拒绝交付将动态字段放在断点之上的缓存计划。拒绝在没有使 2 倍写入溢价回本的复用次数的情况下启用 1 小时 TTL。