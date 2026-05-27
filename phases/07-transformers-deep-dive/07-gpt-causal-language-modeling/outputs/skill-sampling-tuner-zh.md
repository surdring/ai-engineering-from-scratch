---
name: sampling-tuner
description: 为给定的生成任务选择解码策略（贪心 / 温度 / top-k / top-p / min-p / 推测式）
version: 1.0.0
phase: 7
lesson: 7
tags: [gpt, sampling, decoding, inference]
---

给定生成任务（代码、创意写作、推理、对话、结构化输出）以及延迟/质量目标，输出：

1. 采样方法。以下之一：贪心解码、仅温度、top-k、top-p、min-p、束搜索-k、推测式解码。一句话理由。
2. 参数值。温度、top-k、top-p、min-p、重复惩罚 — 与任务类型相关的具体数值（例如代码用 temperature 0.2 + top-p 1.0；聊天用 min-p 0.1 + temperature 0.7）。
3. 停止条件。`max_new_tokens`、停止 token 列表、基于模式的停止（例如闭合 `</tool_call>`）。
4. 确定性开关。固定种子以可复现；标记用例（评估、法律）是否需要。
5. 质量检查。一句对照任务目标的测试（编译/通过单元测试、事实性、格式有效性等）。

拒绝为结构化输出或代码补全推荐 temperature > 1.0 — 幻觉风险急剧上升。拒绝为开放式对话推荐纯贪心解码 — 模型会陷入循环。拒绝在模型能生成模板/工具时不指定停止 token 列表的采样配置。