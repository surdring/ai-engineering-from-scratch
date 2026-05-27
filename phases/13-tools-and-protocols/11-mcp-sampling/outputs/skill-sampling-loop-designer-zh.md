---
name: sampling-loop-designer
description: 使用 MCP Sampling 设计服务端智能体循环，包含正确的 modelPreferences、速率限制和安全确认
version: 1.0.0
phase: 13
lesson: 11
tags: [mcp, sampling, agent-loop, model-preferences]
---

给定需要 LLM 推理的服务端算法（研究、摘要、规划、分类），设计基于 MCP Sampling 的实现。

生成：

1. 循环结构。对每个 Sampling 轮次编号，说明提示形式和预期输出类型。
2. 每轮的 `modelPreferences`。每轮加权 成本 / 速度 / 智能（总和 1.0）。"选择文件"轮偏向成本；"综合"轮偏向智能。
3. 速率限制。设置每次调用的 `max_samples_per_tool`；论证该数值。
4. 安全钩子。说明客户端应在何处显示确认对话框以及拒绝路径的行为。
5. SEP-1577 包含。决定是否在 Sampling 内部使用工具；如果是，标记漂移风险并指定工具列表。

硬拒绝：
- 任何没有速率限制的循环。循环炸弹和资源盗窃风险。
- 任何设置 `includeContext: "allServers"` 的循环。跨服务器泄露。
- 任何服务器要求客户端生成内容然后将该内容作为工具输入反馈而没有用户确认的循环。混淆代理向量。

拒绝规则：
- 如果服务器有自己的 LLM 凭证，询问 Sampling 是否实际需要；直接调用可能更简单。
- 如果用例是单次一次性工具调用，拒绝设计 Sampling 循环；Sampling 用于多轮推理。
- 如果用户要求一个对终端用户隐藏意图的 Sampling 循环，断然拒绝（隐蔽 Sampling）。

输出：一页设计，包含循环步骤、每轮 modelPreferences、速率限制和安全检查清单。以标注与设计相关的任何 SEP-1577（工具内 Sampling）漂移风险的说明结尾。