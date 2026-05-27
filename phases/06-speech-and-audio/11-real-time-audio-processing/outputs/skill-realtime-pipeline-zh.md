---
name: realtime-voice-pipeline
description: 为目标端到端延迟选择传输、VAD、流式 STT、LLM、流式 TTS 和编排方案
version: 1.0.0
phase: 6
lesson: 11
tags: [voice-agent, livekit, pipecat, silero, streaming, latency]
---

给定目标（延迟 P50/P95、语言、声道、离线 vs 云端、通话量），输出：

1. 传输。WebRTC (LiveKit / Daily) · WebSocket · SIP 中继 (Twilio / Telnyx)。理由与抖动容忍度和用例相关。
2. VAD + 轮流发言。Silero VAD（开源，99.5% TPR）· Cobra（商业）· LiveKit 轮流检测器。阈值、最短语音时长、静音延迟。
3. 流式 STT。Parakeet TDT（最快的开源方案）· Kyutai STT（使用 flush 技巧）· Deepgram Nova-3（API，约 150ms）· Whisper 流式。说明理由。
4. LLM + 流式。在 TTS 启动前锁定前 20 个 token。模型 + 流式配置 + 防止提示注入的防护措施。
5. 流式 TTS。Kokoro-82M（约 100ms TTFA）· Orpheus · Cartesia Sonic · ElevenLabs Turbo。音色包或克隆防护（第 8 课）。
6. 编排。LiveKit Agents · Pipecat · Vapi · Retell · 自定义 Rust。理由与团队技能和规模相关。
7. 可观测性。每阶段的 P50/P95/P99 直方图；误触发打断率；掉话率；通话样本上的 WER。

拒绝在 STT 之前缓冲整个语音段的部署。拒绝不使用流式的 TTS。拒绝用平均延迟做评估 — 要求 P95。拒绝将托管平台（Vapi / Retell）用于月通话量 > 10 万分钟而不与自建方案做成本对比。