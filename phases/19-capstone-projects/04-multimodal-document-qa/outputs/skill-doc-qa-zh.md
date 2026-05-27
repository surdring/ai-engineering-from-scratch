---
name: doc-qa
description: 在 10k 页面上构建视觉优先的多模态文档问答系统，具有晚期交互检索和证据区域引用。
version: 1.0.0
phase: 19
lesson: 04
tags: [capstone, multimodal, rag, colpali, colqwen, late-interaction, pdf]
---

给定 PDF 语料库（10-K 文件、科学论文、扫描文档），构建使用 ColPali 风格晚期交互将页面作为图像索引的流水线，并用页面级证据区域回答问题。

构建计划：

1. 用 PyMuPDF 以 180 DPI 将每个 PDF 页面渲染为 1536x2048 PNG。
2. 用 ColQwen2.5-v0.2 或 ColQwen3-omni 嵌入每个页面。存储多向量 patch 嵌入在 Vespa、Qdrant multi-vector 或 AstraDB 中。
3. 应用 DocPruner 风格的 50% patch 修剪。验证 ViDoRe v3 上准确率下降保持在 0.5% 以下。
4. 查询时：嵌入查询令牌；计算每个页面的 patch 上的 MaxSim；排名 top-k。
5. 用 Qwen3-VL-30B 或 Gemini 2.5 Pro 综合，传递查询加 top-5 页面图像。要求引用 `(doc_id, page, region)` 锚点。
6. 对于方程或表格密集的页面，运行 Nougat 或 dots.ocr 作为可选文本通道并与图像一起馈入。
7. 构建 Next.js 15 查看器，在源页面上将证据区域作为边界框覆盖。
8. 在 ViDoRe v3 和 M3DocVQA 上评估。生成内容类型 × 方法矩阵，比较视觉优先 vs OCR-然后-文本在纯文本、表格、图表、手写和方程上的表现。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | ViDoRe v3 / M3DocVQA 准确率 | 在匹配页面上对比 OCR-然后-文本基线的基准测试 |
| 20 | 证据区域定位 | 包含答案跨度的引用区域比例 |
| 20 | 存储和延迟工程 | DocPruner 压缩、索引 p95、2s 以下答案 p95 |
| 20 | 多页推理 | 在手写标记的 100 问题多页集上的准确率 |
| 15 | 源检查 UX | 覆盖层精度、比较工具、逐页浏览器 |

硬性拒绝：
- 通过将 OCR 文本改装为单向量嵌入而宣传为「视觉优先」的 OCR 优先流水线。
- 任何丢弃 patch 级边界框因而无法渲染证据覆盖层的系统。
- 不说明 DocPruner 设置就报告的存储数字。

拒绝规则：
- 拒绝在没有专用脱敏策略的情况下索引扫描的法律合同。ColQwen 嵌入泄露内容。
- 拒绝针对用户未披露的语料库提供查询服务。审计 trail 对于受监管领域是强制性的。
- 拒绝在不基于同一语料库运行两个流水线的情况下与 OCR-然后-文本比较。

输出：包含摄取流水线、Vespa（或 Qdrant multi-vector）配置、100 问题多页评估集、查看器 UI 的仓库，以及一份包含内容类型 x 方法矩阵和 2026 年哪些内容类别仍然偏好 OCR-然后-文本的具体建议的 write-up。