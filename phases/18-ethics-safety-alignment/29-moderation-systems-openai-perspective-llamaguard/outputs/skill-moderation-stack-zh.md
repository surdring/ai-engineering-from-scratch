---
name: moderation-stack
description: 为生产部署推荐审核栈配置。
version: 1.0.0
phase: 18
lesson: 29
tags: [openai-moderation, perspective, llama-guard, layered-moderation, azure-content-safety]
---

给定生产部署，为三层结构推荐审核栈配置。

生成：

1. **输入分类器。** 选择 OpenAI Moderation、Llama Guard 3/4 或 Perspective API。匹配到策略分类体系。对多模态部署，Llama Guard 4 或 OpenAI omni-moderation。
2. **输出分类器。** 与输入分类器相同或不同。将阈值匹配到下游风险模型。
3. **自定义领域规则。** 枚举通用分类器不会捕获的领域特定规则：财务建议免责声明、医疗建议拒绝、法律免责模式。
4. **边界案例裁判。** 指定人工升级路径。硬拒绝是终局的；模糊案例在 SLA 内进入人工审查。
5. **迁移计划。** 如果 Azure Content Moderator 在栈中，规划在 2027 年 2 月退役前迁移到 Azure AI Content Safety。

硬性拒绝：
- 任何没有输出审核的部署（仅有输入是不够的）。
- 任何在受监管面上没有自定义领域规则的部署（金融、健康、法律）。
- 任何仅依赖前 LLM 时代分类器（Perspective）的现代聊天应用部署。

拒绝规则：
- 如果用户要求单一最佳分类器，拒绝——分类器选择是策略分类体系特定的。
- 如果用户要求阈值，拒绝单一数字——阈值取决于风险容忍度和下游效应。

输出：一页推荐，填写五个部分，指出每层的分类器，并标记迁移义务。各引用一次 OpenAI Moderation docs 和 Llama Guard 3/4 references。