---
name: voice-pipeline
description: 搭建一个 Pipecat 形态的语音流水线（VAD + STT + LLM + TTS + 传输），包含打断、置信度门控和延迟预算执行。
version: 1.0.0
phase: 14
lesson: 22
tags: [voice, pipecat, livekit, webrtc, latency]
---

给定一个语音产品规格（语言、传输、服务商），搭建一个基于帧的流水线。

生成：

1. `Frame` 类型，包含 `kind`、`payload`、`direction`（下行 / 上行）。
2. 处理器：`VAD`、`STT`、`LLM`、`TTS`、`Transport`。每个都有 `process(frame)`。
3. `link()` 辅助函数，将处理器正向和反向链式连接。
4. 取消帧处理：从 transport 到 TTS 到 LLM 到 STT 的 UPSTREAM 路径，在每个阶段丢弃待处理工作。
5. 观察器：每阶段延迟指标；为每个跨越处理器的帧发出 OTel span（第 23 课）。
6. STT 上的置信度门控：低于阈值时，发出「请重复」文本帧而非转录文本。

硬性拒绝：

- 没有 UPSTREAM 处理的流水线。打断对语音而言不是可选的。
- 没有流式传输的 LLM 调用。首 token 延迟占主导；必须流式传输。
- 无视置信度的 STT。将错误的转录输入 LLM 会产生错误的回复。

拒绝规则：

- 如果冷启动时端到端延迟超过 1500ms，拒绝交付。优化链路或使用 MultimodalAgent（LiveKit 直接音频）。
- 如果产品以电话为主且流水线没有 SIP 适配器，拒绝。通过 LiveKit SIP 或平台（Vapi/Retell）路由。
- 如果产品承载 PII 音频但在传输中未加密，拒绝。

输出：`frames.py`、`processors.py`、`pipeline.py`、`observers.py`、`README.md`，解释延迟预算、打断设计和传输选择。结尾的「下一步阅读」指向第 23 课（OTel）、第 24 课（可观测性后端）或 LiveKit 文档了解 WebRTC 细节。