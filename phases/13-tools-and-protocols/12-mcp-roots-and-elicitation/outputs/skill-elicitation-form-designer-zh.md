---
name: elicitation-form-designer
description: 为需要调用中用户确认或消歧的工具设计启发表单 Schema 和消息模板
version: 1.0.0
phase: 13
lesson: 12
tags: [mcp, elicitation, user-input, forms]
---

给定一个行为可能需要调用中用户输入的工具，设计启发 Schema 和消息。

生成：

1. 触发条件。说明应导致工具调用 `elicitation/create` 的确切输入或歧义。
2. 消息模板。宿主向用户展示的一句话。简洁、具体、无术语。
3. Schema。扁平 JSON Schema，包含类型化属性和 `enum` 列表（消歧用）或 `boolean`（确认用）。不要嵌套。
4. 分支处理。将 `accept` / `decline` / `cancel` 映射到工具行为。
5. 速率限制规则。限制每次工具调用的启发请求数；永远不要在循环内触发启发。

硬拒绝：
- 任何嵌套对象的 Schema。Elicitation v1 是扁平的。
- 任何用于填补 LLM 本可以用自然语言询问的缺失参数的启发请求。
- 任何高频启发（每次工具调用超过一次）。

拒绝规则：
- 如果工具是只读且低风险的，拒绝启发并直接返回结果。
- 如果工具是破坏性的且宿主支持 `destructiveHint` 标注，建议使用标注并让客户端原生处理确认。
- 如果需要 OAuth 登录，推荐 URL 模式启发并标记 SEP-1036 漂移风险。

输出：一页设计，包含触发条件、消息模板、Schema、分支处理、速率限制规则，以及关于表单模式还是 URL 模式更适合的说明。