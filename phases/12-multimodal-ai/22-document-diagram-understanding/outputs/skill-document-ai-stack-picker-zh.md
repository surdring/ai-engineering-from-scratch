---
name: document-ai-stack-picker
description: 基于领域、规模、监管需求为文档 AI 项目在 OCR 流水线、无 OCR 专业模型和 VLM 原生方案之间选择技术栈
version: 1.0.0
phase: 12
lesson: 22
tags: [document-ai, ocr, donut, nougat, paligemma, vlm-native]
---

给定文档 AI 项目（领域：发票 / 科学论文 / 表单 / 混合；规模：每日页数；质量门槛；监管需求），选择技术栈并生成参考配置。

生成：

1. 技术栈选择。Era 1（OCR 流水线 + LayoutLMv3）、Era 2（Donut / Nougat 无 OCR）、Era 3（VLM 原生）或混合方案。
2. 每页成本估计。所选技术栈下的 token 数量和延迟。
3. 准确率预期。DocVQA + ChartQA + 领域特定基准。
4. 手写策略。对成本不敏感用 VLM 原生；大规模用专用 TrOCR + 路由。
5. 数学/LaTeX 输出。科学论文用 Nougat；其他用 VLM。
6. 监管回退方案。带交叉检查审计日志的混合方案。

硬拒绝：
- 不做成本分析就为 >100 万页/天提议 VLM 原生。2576px 每页的 token 成本很高。
- 为监管工作流推荐单模型方案而不提供审计路径。
- 声称 Nougat 处理扫描发票。不 — 它是科学论文专用。

拒绝规则：
- 如果规模 >1000 万页/天，拒绝 Era 3 并推荐 Era 1 配合 Era 3 作为抽样验证器。
- 如果领域是手写密集的，拒绝 OCR 流水线并推荐 VLM 原生 + 手写专用模型（TrOCR）。
- 如果方程需要 LaTeX 保真度，要求在流程中加入 Nougat。

输出：一页计划，包含技术栈、成本、准确率、手写策略、数学、监管。以 arXiv 2308.13418 (Nougat)、2204.08387 (LayoutLMv3)、2111.15664 (Donut) 结尾。