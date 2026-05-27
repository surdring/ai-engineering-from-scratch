---
name: provider-portability-audit
description: 审计针对一个提供商的函数调用集成，识别移植到另外两个提供商会出现的所有破坏性问题
version: 1.0.0
phase: 13
lesson: 02
tags: [function-calling, openai, anthropic, gemini, portability]
---

给定一个针对单个提供商（OpenAI、Anthropic 或 Gemini）的函数调用集成，生成可移植性审计，列出当相同逻辑部署到另外两个提供商时出现的每个字段重命名、行为差异和硬限制冲突。

生成：

1. 声明差异。对集成中的每个工具，展示迁移到其他两个提供商所需的信封/字段重命名/Schema 翻译。标记目标提供商不支持的任何 JSON Schema 构造（Gemini：OpenAPI 3.0 子集；OpenAI strict：不支持 `$ref`、歧义的 `oneOf`）。
2. 响应差异。记录工具调用在每个提供商响应结构中的位置（`tool_calls[]` vs `content[]` 块 vs `parts[]` 条目）以及谁负责解析 `arguments`（OpenAI 上是字符串，Anthropic 和 Gemini 上是对象）。
3. `tool_choice` 差异。将集成当前的选择设置（auto / forbid / force / required）映射到目标提供商的格式；标记缺失模式。
4. 限制冲突。报告工具数量（128 / 64 / 64）、Schema 深度（5 / 10 / 实际上无上限）和每个参数的长度上限。对任何超出目标提供商限制的集成提出阻止级严重性。
5. 严格模式映射。说明严格模式语义在目标上是否保留。OpenAI `strict: true` 在 Anthropic 上没有精确等价物；Gemini `responseSchema` 近似但是在请求级别。

硬拒绝：
- 任何在非 OpenAI 目标上假设 `arguments` 是字符串的集成。会默默产生错误结果。
- 任何工具数量在移植到 Anthropic 或 Gemini 时超过 64 但没有路由器的集成。
- 任何在目标为 OpenAI strict 模式时在 Schema 中使用 `$ref` 的集成。

拒绝规则：
- 如果被要求移植一个依赖无类比功能的提供商特定特性（如 OpenAI Responses API 有状态回合、Anthropic 计算机操作块），拒绝并解释哪个特性没有目标等价物。
- 如果被要求选胜者，拒绝。选择取决于宿主的严格模式需求、成本概况和并行调用需求。

输出：一页审计，包含每工具差异表、限制表和每个目标提供商的最终「移植裁决」（部署 / 需要路由器 / 被特性阻止）。以一句指出最高杠杆的迁移变更结尾。