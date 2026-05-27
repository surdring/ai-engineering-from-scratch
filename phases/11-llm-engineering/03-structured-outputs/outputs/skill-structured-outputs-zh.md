---
name: skill-structured-outputs
description: 根据提供商、可靠性和复杂性选择结构化输出策略的决策框架
version: 1.0.0
phase: 11
lesson: 03
tags: [structured-output, json, schema, constrained-decoding, pydantic, function-calling]
---

# 结构化输出策略

在构建需要结构化数据的 LLM 应用时，应用此决策框架。

## 何时使用每种方法

**基于提示（"Return JSON"）：** 仅用于原型开发。对偶尔解析失败可容忍的内部工具可以接受。添加带重试的 try/except。绝不要在生产流水线中使用。

**JSON 模式（API 标志）：** 你需要保证有效的 JSON，但 Schema 简单或灵活。当你在应用侧验证形态时使用。可用：OpenAI、Anthropic（通过工具使用）、Google。

**Schema 模式（受限解码）：** 每个输出必须匹配特定 Schema 的生产系统。零解析失败。零 Schema 违规。默认用于任何生产级抽取或分类任务。可用：OpenAI 结构化输出、Outlines、Guidance。

**函数调用 / 工具使用：** 模型需要选择调用哪个函数，而不仅仅是填充参数。你有多个 Schema，模型选择合适的一个。在与现有工具/函数基础设施集成时也使用此方法。

**Instructor 库：** 你想要跨任何提供商的 Pydantic 验证和自动重试。Python 项目的最佳开发者体验。封装 OpenAI、Anthropic、Google 以及开源模型。

## 提供商特定指南

**OpenAI：** 使用 `response_format` 的 `json_schema` 类型。受限解码内置。Pydantic 模型可直接使用。最可靠的结构化输出实现。

**Anthropic：** 使用工具使用来实现结构化输出。定义一个带有目标 Schema 的单一工具。模型返回与 Schema 匹配的工具调用参数。可靠但需要工具使用 API 模式。

**开源模型（vLLM、Ollama）：** 使用 Outlines 或 Guidance 进行受限解码。这些库将 JSON Schema 编译为有限状态机，在生成过程中屏蔽无效 token。需要在本地运行推理。

## Schema 设计指南

1. 尽可能保持 Schema 扁平。超过 2 层的嵌套对象会增加抽取错误。
2. 对分类字段使用枚举。不要依赖模型自己发明正确的字符串。
3. 将模糊字段设为必填并显式支持 null，而不是设为可选。强制模型做出决定。
4. 为 Schema 属性添加描述。模型将这些描述作为指令读取。
5. 除非必要，避免联合类型（oneOf/anyOf）。它们增加解码复杂性。
6. 对数字设置最小/最大值。捕捉幻觉的极端值。
7. 对数组使用 minItems/maxItems 以防止空输出或无界输出。

## 常见失败模式与修复

- **模型将 JSON 包裹在 Markdown 围栏代码块中**：从基于提示切换到 JSON 模式或 Schema 模式
- **Schema 有效但事实错误**：抽取后添加 LLM 作为裁判的验证步骤
- **不一致的枚举值**：切换到受限解码或添加后处理标准化
- **缺失可选字段**：将其改为必填或在应用代码中添加默认值
- **抽取非常慢**：受限解码增加 5-15% 延迟，对延迟敏感的场景减少 Schema 复杂性
- **包含不同项目的大数组**：分块输入并逐块抽取，然后合并结果

## 可靠性阶梯

| 方法 | 解析成功率 | Schema 匹配 | 设置工作量 |
|----------|-------------|-------------|-------------|
| 基于提示 | ~90% | ~80% | 1 分钟 |
| JSON 模式 | 100% | ~90% | 5 分钟 |
| Schema 模式 | 100% | ~99% | 15 分钟 |
| 受限解码 | 100% | 100% | 30 分钟 |
| Instructor + 重试 | 100% | ~99.5% | 10 分钟 |