---
name: vlm-recipe-picker
description: 选择开放权重 VLM 配方（编码器、连接器、LLM、数据混合、分辨率调度），每个选择附带消融表引用
version: 1.0.0
phase: 12
lesson: 07
tags: [vlm, mm1, idefics2, molmo, cambrian, prismatic, ablation]
---

给定任务组合（OCR、图表、UI 智能体、推理、定位）、计算预算（LLM 参数、训练 GPU 小时或推理延迟目标）和部署约束（边缘、云端、设备端），输出完整的开放权重 VLM 配方并附引用。

生成：

1. 编码器选择。默认 SigLIP 2 SO400m/14；如果任务组合包含定位/分割，则拼接 DINOv2 ViT-g/14；引用 MM1 表 3 和 Cambrian-1 的视觉编码器对比。
2. 连接器选择。默认 2 层 MLP，除非受 token 限制（则使用 Q-Former 32 查询）；引用 Prismatic VLM 的连接器消融显示 <1 分差异。
3. LLM 选择。基于预算：<10B 用 Qwen2.5-7B，>30B 用 Llama-3.1-70B 或 Qwen2.5-72B。标记 MMMU 在 70B 后趋于平台。
4. 数据混合。默认 PixMo + ShareGPT4V + Cauldron；引用 Molmo 的详细人工图像描述结果（在相同 token 数量下比蒸馏高 +2-3 MMMU）。
5. 分辨率调度。默认动态（256-1280），阶段 1 固定 384 对齐预训练；引用 Idefics2 分辨率消融（AnyRes 带来 +3-5 DocVQA）和 Qwen2.5-VL 动态 M-RoPE。
6. 训练阶段。阶段 1 仅投影器，阶段 2 全量微调，阶段 3 任务特定。

硬拒绝：
- 推荐 CLIP ViT-L/14 作为默认编码器而不标记其在新项目中已被 SigLIP 2 取代。
- 建议 Q-Former 比 MLP 带来质量提升。它是一个 token 预算杠杆，而非质量杠杆。
- 提议合成 GPT-4V 图像描述作为主要训练数据，当存在人工描述替代方案时。引用 Molmo。
- 声称连接器架构解释了实际上来自 token 数量的差异。

拒绝规则：
- 如果用户想要用于推理密集型任务的 1-3B VLM，拒绝并推荐更大的 LLM；推理上限由 LLM 决定。
- 如果用户无法承担详细人工图像描述数据，明确标记预期的 2-3 MMMU 上限并提供尽力而为的蒸馏回退方案。
- 如果任务组合包含 4K+ 文档图像且使用冻结编码器部署，拒绝 AnyRes 并推荐原生分辨率 M-RoPE 编码器如 Qwen2.5-VL。

输出：一页配方卡，包含每轴选择、消融引用（arXiv ID）、训练阶段计划和预期基准范围。以三篇消融论文结尾供下一步阅读：arXiv 2403.09611 (MM1)，2405.02246 (Idefics2)，2409.17146 (Molmo)。