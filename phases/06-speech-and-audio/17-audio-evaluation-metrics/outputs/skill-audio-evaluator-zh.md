---
name: audio-evaluator
description: 为任何音频模型的发布选择指标、基准测试、归一化规则和报告格式
version: 1.0.0
phase: 6
lesson: 17
tags: [evaluation, wer, mos, utmos, eer, der, fad, mmau, leaderboard]
---

给定任务（ASR / TTS / 克隆 / 说话人验证 / 日记化 / 分类 / 音乐 / LALM / 流式 S2S），输出：

1. 主要指标。WER · MOS · UTMOS · SECS · EER · DER · mAP · FAD · MMAU-Pro 准确率 · 延迟 P95。选其一。
2. 次要指标。1-3 个额外维度（速度、多样性、鲁棒性）及理由。
3. 归一化规则。小写化、标点去除、数字展开、空白符折叠。使用 Whisper 归一化器或自定义方案，文档化。
4. 公开基准测试。要对照报告的权威排行榜（Open ASR、TTS Arena、MMAU-Pro、VoxCeleb1-O、AudioSet、LongAudioBench 等）。
5. 内部测试集。含 N 个样本的留出领域数据；人口统计/声学切片分解。
6. 报告格式。分布（延迟报告 P50/P95/P99；分类报告每类召回率；MMAU 报告每类别）。发布说明模板。

拒绝延迟的单数字评估（应报告百分位数）。拒绝分类仅报告汇总指标（应报告每类指标）。拒绝 TTS 发布不同时给出 MOS/UTMOS 和 SECS（克隆场景）。拒绝 ASR 发布不包含 WER 归一化规范。拒绝音乐发布仅报告 FAD — 始终配合人工 MOS 评审组。