---
name: duplex-pipeline
description: 为语音智能体工作负载选择全双工（Moshi）还是流水线（VAD + STT + LLM + TTS）架构
version: 1.0.0
phase: 6
lesson: 15
tags: [moshi, hibiki, full-duplex, voice-agent, streaming]
---

给定工作负载（延迟目标、工具调用需求、语言覆盖范围、硬件预算、云端 vs 边缘），输出：

1. 架构。全双工（Moshi / GPT-4o Realtime / Gemini Live）vs 流水线（LiveKit + STT + LLM + TTS，第 12 课）。一句话说明理由。
2. 模型。Moshi · Hibiki · Hibiki-Zero · Sesame CSM · GPT-4o Realtime · Gemini 2.5 Live · 传统流水线。说明理由。
3. 规模。每会话 GPU 成本（Moshi 占用一个槽位）、最大并发会话数、冷启动影响。
4. 工具调用路径。如果需要 — 混合流水线（全双工 + 外部 LLM 做工具调用）或纯流水线。解释权衡。
5. 语言覆盖范围。全双工模型的语言支持较窄；流水线继承 LLM 的多语言能力。

拒绝将纯全双工架构用于需要工具调用/检索的企业级智能体 — Moshi 是对话模型，而非智能体框架。拒绝将纯流水线用于亚 250 ms 的对话式智能体 — 各阶段延迟会累积。拒绝将 Moshi 用于单 GPU 超过 4 个并发会话 — 会产生资源争用。