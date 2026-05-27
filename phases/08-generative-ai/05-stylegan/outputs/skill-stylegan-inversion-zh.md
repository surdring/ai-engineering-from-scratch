---
name: stylegan-inversion
description: 为预训练 StyleGAN 在真实照片上选择反演和编辑流水线
version: 1.0.0
phase: 8
lesson: 05
tags: [stylegan, inversion, editing]
---

给定真实照片 + 预训练 StyleGAN 检查点（FFHQ-1024、StyleGAN-XL、自定义微调）和目标编辑（年龄、微笑、姿态、头发、身份保持），输出：

1. 反演方法。e4e（快速，低保真）、ReStyle（迭代编码器）、HyperStyle（超网络）、PTI（关键调优），或直接 W 空间优化。一句话理由，与保真度 vs 速度相关。
2. 目标空间。W、W+ 或 StyleSpace。权衡：W = 最解纠缠但保真度最低，W+ = 每层独立 w，StyleSpace = 通道级别。
3. 编辑方向。命名的方向来源：InterFaceGAN（基于 SVM）、StyleSpace 通道、GANSpace PCA，或学习型分类器。
4. 保真度预算。身份漂移前的 LPIPS 阈值；回滚启发式规则。
5. 评估。身份相似度（ArcFace 余弦相似度）、与原始图像的 LPIPS、编辑强度（目标属性分类器分数）。

拒绝任何直接在 Z 空间中编辑的流水线（未解纠缠）。拒绝做大范围编辑（W 空间中 > 1.5 sigma）而无身份检查。标记需要开放领域编辑的需求（如"把他变成卡通人物"）— 这些需要扩散模型 + IP-Adapter，而非 StyleGAN。