---
name: two-loss-trainer-designer
description: 设计 Transfusion / MMDiT 风格的双损失训练设置（一种模态用 NTP，另一种用扩散），包括损失权重、掩码设计和调度
version: 1.0.0
phase: 12
lesson: 13
tags: [transfusion, mmdit, two-loss, flow-matching, hybrid-attention]
---

给定多模态训练规格（两种模态，哪个用 NTP、哪个用扩散，目标模型规模，目标样本长度），设计一个可行的双损失设置。

生成：

1. 模态划分。哪些 token 是离散的（NTP）和哪些是连续的（扩散）。按内容类型论证（文本总是离散的；图像、音频、视频可以选任一）。
2. 注意力掩码。为一个示例序列绘制块三角掩码。指定双向区域和因果区域。
3. 损失权重。（text_loss, image_loss）的起始权重。建议按目标梯度范数比率调优。引用 Transfusion 的约 0.1 默认值。
4. Flow Matching vs DDPM。选择扩散变体；Flow Matching 数学更简单，Rectified Flow 推理步数更少。
5. 推理计划。NTP 路径（对文本自回归采样）+ 扩散路径（对图像 patch 条件去噪）。指定去噪步数（10-30）。
6. MMDiT vs Transfusion 划分。何时添加模态特定的块权重（MMDiT）vs 完全共享（Transfusion）；按参数数量的经验法则。

硬拒绝：
- 声称一种掩码适合所有序列。每个样本有不同的图像跨度，需要自己的块三角掩码。
- 使用 DDPM 而不使用 Rectified Flow 或 Flow Matching。两者都需要更少的推理步数且更容易调优。
- 按固定权重平衡损失而不测量梯度范数比率。

拒绝规则：
- 如果用户只想要理解（图像输入，文本输出），拒绝并推荐 LLaVA 风格后期融合（第 12.05 课）。双损失是用于生成的。
- 如果用户想要 <1B 模型，拒绝双损失并推荐离散 token（Chameleon）— 在小规模下扩散头会欠拟合。
- 如果用户无法承担双重推理（NTP + 扩散循环），拒绝并推荐 Show-o（离散扩散，单循环）或 Emu3。

输出：一页设计，包含模态划分、掩码图、损失权重、Flow 变体、推理计划、MMDiT-vs-共享决策。以 arXiv 2408.11039 (Transfusion) 和 2403.03206 (SD3) 结尾作为权威参考。