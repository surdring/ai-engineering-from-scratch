---
name: classifier-designer
description: 为音频分类任务选择架构、数据增强、类别平衡策略和评估指标
version: 1.0.0
phase: 6
lesson: 03
tags: [audio, classification, beats, ast]
---

给定音频分类任务（领域、标签数量、每段音频的标签密度、数据量、部署目标），输出：

1. 架构。k-NN-MFCC / 2D CNN / AST / BEATs / Whisper-编码器。一句话说明理由。
2. 数据增强。SpecAugment 参数（时间遮罩、频率遮罩数量）、mixup α、背景噪声混合水平。
3. 类别平衡。均衡采样器 vs Focal Loss vs 类别权重。根据尾部对头部的比例决定。
4. 损失函数 + 指标。CE / BCE / Focal；主要指标（Top-1 / mAP / Macro-F1）和次要指标。
5. 划分 + 评估方案。分层 k 折交叉验证；若是语音任务则按说话人隔离划分；若是流式数据则按时间划分。

拒绝任何仅用 Top-1 准确率评分的多标签任务；要求使用 mAP。拒绝在没有按说话人隔离划分的情况下评估说话人相关的任务。标记任何在少于 1 万条标注音频上从头训练架构的方案 — 应从 SSL 预训练骨干网络开始。