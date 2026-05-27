---
name: transformer-review
description: 对照第 7 阶段的 13 节课审查从头实现的 Transformer 代码是否符合 2026 标准
version: 1.0.0
phase: 7
lesson: 14
tags: [transformers, review, capstone]
---

给定从头实现的 Transformer 代码库（PyTorch / JAX），对照 2026 默认标准审查并标记缺失或错误的部分：

1. 注意力机制。因果遮罩存在。按 `sqrt(d_head)` 缩放。多头分割正常工作。如可用则使用 Flash Attention。如果 d_model ≥ 1024，提及 GQA。
2. 位置编码。RoPE（2026 首选）或可学习绝对位置编码（小型模型可接受）。标记正弦编码为历史遗留。
3. 块连接。Pre-norm（非 Post-norm）。RMSNorm（非 LayerNorm）。SwiGLU FFN（非 ReLU/GELU）。每个子层周围的残差连接。线性层中去掉偏置项（现代默认）。
4. 训练。AdamW（或 2026+ 用 Muon）、带线性预热的余弦学习率调度、梯度裁剪 1.0、bf16 自动混合精度。token 嵌入和 lm_head 之间的权重绑定。
5. 损失函数。每个位置的移位交叉熵。如有填充则遮罩掉。以固定间隔记录训练和验证损失。

拒绝签署有以下任何一项的代码库：无明确原因的 Post-norm、2026 生产代码中无合理说明的 LayerNorm、解码器自注意力缺少因果遮罩、小型 LM 中未绑定的嵌入。标记：无验证集划分、无梯度裁剪、无预热的 LR > 1e-3，或块大小超出位置嵌入范围而无回退方案。推荐运行 `python code/main.py` 端到端，并检查在 nano 配置下 tinyshakespeare 上的最终验证损失是否低于 2.5。