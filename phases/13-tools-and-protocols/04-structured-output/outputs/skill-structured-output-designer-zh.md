---
name: structured-output-designer
description: 为自由文本提取目标设计严格模式兼容的 JSON Schema 加 Pydantic 模型，包含类型化拒绝回答和重试处理框架
version: 1.0.0
phase: 13
lesson: 04
tags: [structured-output, json-schema, pydantic, strict-mode, extraction]
---

给定自由文本提取目标（发票、简历、支持工单、研究摘要），生成生产就绪的提取契约：JSON Schema 2020-12、Pydantic 模型、拒绝回答处理器和重试策略。

生成：

1. JSON Schema 2020-12。每个属性有类型。`required` 列出所有属性。每个对象上 `additionalProperties: false`。封闭值集使用枚举。无 `$ref`。无歧义的 `oneOf` / `anyOf`。已根据 OpenAI strict 模式要求验证。
2. Pydantic v2 BaseModel。Schema 的镜像，使用 Python 类型。`model_json_schema()` 必须产生与 (1) 等价的 Schema。
3. 拒绝回答处理器。类型化的 `Refusal(reason: str, category: str)` 结果。列出类别：`safety`、`input_mismatch`、`insufficient_info`。
4. 重试策略。三种重试形式：(a) 注入验证错误并重试一次（严格模式外）；(b) 接受拒绝为最终结果（严格模式）；(c) 重复拒绝时升级到更强的模型。
5. 测试向量。十个输入，涵盖正常路径、对抗性字段、部分输入和触发拒绝回答的案例。每个都有预期结果。

硬拒绝：
- 任何有未类型化字段的 Schema。同时无法通过严格模式和验证器。
- 任何缺少 `additionalProperties: false` 的 Schema。泄露幻觉内容。
- 任何使用 `oneOf` 但没有 discriminator 字段的 Schema。歧义解码。
- 任何没有检查其 JSON Schema 往返一致性的 Pydantic 模型。

拒绝规则：
- 如果目标领域包含个人身份数据但没有记录用途，拒绝并引导到 Phase 18（伦理）以获得合法依据论证。
- 如果用户要求一个无法用 JSON Schema 2020-12 表达的 Schema（如递归任意图），拒绝并提议最接近的可表达放宽。
- 如果提取目标是「从任何内容提取结构化数据」，拒绝并要求具体领域。

输出：一页契约，包含 Schema JSON、Pydantic 类、拒绝回答和重试策略以及十个测试向量。以关于首先面向哪个提供商及其原因的说明结尾。