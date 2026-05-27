---
name: structured-output-picker
description: 选择结构化输出方法、模式设计和验证计划
version: 1.0.0
phase: 5
lesson: 20
tags: [nlp, llm, structured-output]
---

给定用例（提供商、延迟预算、模式复杂度、失败容忍度），输出：

1. 机制。原生供应商结构化输出、Instructor 重试、Outlines FSM 或 XGrammar CFG。一句话说明理由。
2. 模式设计。字段顺序（推理字段在前，答案字段在后）、表示"未知"的可空字段、枚举 vs 正则表达式、必填字段。
3. 失败策略。最大重试次数、回退模型、优雅的 `null` 处理、分布外拒答。
4. 验证计划。模式合规率（目标 100%）、语义有效性（LLM 评判）、字段覆盖率、p50/p99 延迟。

拒绝任何将 `answer` 或 `decision` 放在推理字段之前的设计。拒绝在无模式的情况下使用裸 JSON 模式。标记仅支持 FSM 库背后的递归模式。