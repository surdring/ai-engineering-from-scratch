---
name: any-to-any-pipeline-auditor
description: 审计对话式任意到任意（any-to-any）设计，并计算 MIO / AnyGPT / Moshi 系列技术栈的延迟预算
version: 1.0.0
phase: 12
lesson: 16
tags: [mio, anygpt, moshi, any-to-any, streaming, ttfab]
---

给定对话式产品（语音输入 / 语音输出，可选的视觉，可选的音乐）、模型大小和目标延迟，审计任意到任意设计并生成可行的配置。

生成：

1. 模态组合。哪些模态输入，哪些输出。选择系列：MIO / AnyGPT（离散 token，4 模态）、Moshi（聚焦语音+文本，内心独白）、Unified-IO 2（视觉丰富）。
2. 共享词汇表计划。文本 + 图像 + 语音 + 音乐 + 分隔符的 ID 范围。总大小通常 40-50k。
3. 分词器技术栈。BPE + SEED + SpeechTokenizer-RVQ + Encodec。高亮哪些仍然是瓶颈（通常是语音质量）。
4. 训练课程。四阶段 MIO 配方，或语音聚焦的 Moshi 的两阶段。
5. TTFAB 延迟预算。麦克风编码器 + 预填充 + 首 token + 残差解码 + 语音解码器。与约 500ms 对话标准对比。
6. 质量-vs-延迟帕累托。更小模型带来低延迟，更大模型更高质量；每个 A100/H100 的大致数字。

硬拒绝：
- 当需求是对话流畅性时提议每模态独立模型。流水线延迟叠加且体验更差。
- 使用只有 1 个码本层的语音分词器。对任何生产级语音，质量会很机械。
- 声称 MIO 的 TTFAB 匹配 GPT-4o。目前还不匹配；Moshi 160ms 是最接近的开放数字。

拒绝规则：
- 如果目标 TTFAB <200ms，拒绝 MIO 规模（8B+）并推荐 Moshi 级别（7B，为语音优化）或更小的语音专用模型。
- 如果用户想要录音室级质量的语音输出，拒绝开放 residual-VQ 并推荐 ElevenLabs / 链式 TTS，直到开放质量赶上（Qwen3-Omni / Moshi2）。
- 如果用户想要在语音通话中生成图像，拒绝流式语音优先方案并提议带模式切换的分离流水线。

输出：一页审计，包含模态组合、词汇表计划、分词器技术栈、课程、TTFAB 延迟、质量-延迟帕累托。以 arXiv 2409.17692 (MIO)、2410.00037 (Moshi)、2402.12226 (AnyGPT) 结尾。