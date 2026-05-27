---
name: music-designer
description: 为部署选择音乐生成模型、许可策略、长度方案和披露元数据
version: 1.0.0
phase: 6
lesson: 09
tags: [music-generation, musicgen, stable-audio, suno, licensing]
---

给定需求（纯器乐 vs 歌曲、长度、商业 vs 研究、风格、预算），输出：

1. 模型。MusicGen（尺寸）· Stable Audio Open · ACE-Step XL · YuE · Suno (v5) · Udio (v4) · ElevenLabs Music · Google Lyria 3 / RealTime · MiniMax Music 2.5。一句话说明理由。
2. 许可和权利。生成音频的商业许可 · 署名（CC）· 非商业限制 · 自有曲库微调。记录权利持有者和权利链。
3. 长度 + 结构。单次生成 · 分块 + 交叉淡入淡出 · 段落插值补全 · 如需编辑则使用音轨分离。明确处理 30 秒漂移墙。
4. Prompt 架构。调性 / BPM / 风格 / 乐器配置 +（声乐模型）歌词 + 情绪标签。限制名人姓名和商标风格标签。
5. 披露 + 元数据。水印（如适用 AudioSeal）、`isAIGenerated` 元数据标签、为遵守欧盟 AI 法案 / CA SB 942 的 AI 披露叠加层。

拒绝在开放模型上使用名人风格 Prompt（商业 API 会过滤；自托管不会）。拒绝将非商业许可的生成结果（Stable Audio Open）用于付费产品。拒绝在没有披露标签的情况下部署声乐生成。标记依赖 Udio 音轨分离的编辑流水线 — 这些带有商业条款，不可免费使用。