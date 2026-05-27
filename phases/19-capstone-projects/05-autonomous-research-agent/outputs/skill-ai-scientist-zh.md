---
name: ai-scientist
description: 构建自主研究智能体，运行实验树搜索、编写带视觉评判的 LaTeX 论文，并通过沙箱逃逸红队测试。
version: 1.0.0
phase: 19
lesson: 05
tags: [capstone, autonomous-agent, ai-scientist, sakana, langgraph, sandbox, research]
---

给定种子想法、狭窄领域和 $30 计算预算，构建一个运行实验树搜索、撰写可审阅 LaTeX 论文并生成可复现捆绑包的智能体。

构建计划：

1. 文献阶段：Semantic Scholar Graph API + OpenAlex；在 FAISS 中缓存摘要；生成 1 页领域摘要。
2. 树搜索：在实验节点上实现最佳优先扩展，`expand(node) -> children`（每个子节点一个配置编辑）和 `score(node) = novelty*0.4 + quality*0.5 + budget*0.1`。
3. 每节点沙箱：每个实验运行 `docker run --network=none --memory=8g --cpus=2 --pids-limit=256 --read-only` 或 E2B 等效；确定性种子；强制资源上限。
4. 规划-执行-验证：验证步骤检查损失收敛、基线运行、消融实验隔离了声明。
5. 撰写器：生成 LaTeX，编译为 PDF，将 PDF 馈入 Claude Opus 4.7 视觉模式进行排版和声明-证据对齐的评判，最多迭代 3 次。
6. 审阅者集成：五位裁判（Opus 4.7、GPT-5.4、Gemini 3 Pro、DeepSeek R1、Qwen3-Max）按 NeurIPS 评分标准（新颖性、严谨性、清晰度、可复现性、影响力）评分；均值 < 4.0 返回撰写器。
7. 红队：集成对抗任务（fork bomb、文件系统逃逸、LLM 编写的网络调用）。确认全部被阻止。生成 `red_team.md`。
8. 可复现捆绑包：paper.pdf + review.md + tree-search trace JSON + seeds + W&B run links + sandbox config + 一行重跑命令。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | 论文质量 | 对照同一主题已发表研讨会论文的盲审评分标准 |
| 20 | 实验严谨性 | 基线、种子、消融实验；每个声明都有结果表中的单元格支撑 |
| 20 | 成本和计算纪律 | 每篇论文 $30 上限强制执行，Langfuse 追踪 |
| 20 | 安全性 | 沙箱红队通过；网络策略和紧急开关已验证并有日志记录 |
| 15 | 可复现性 | 一条命令重跑用相同种子复现论文 |

硬性拒绝：
- 在沙箱外运行的实验。整个顶点项目的核心论点是执行是被包含的。
- 不重新阅读编译后 PDF 的撰写步骤（视觉评判是承重的）。
- 没有基线、种子或消融实验章节的论文。
- 仅作为事后警告而非硬上限执行的成本预算。

拒绝规则：
- 拒绝在没有显式人工覆盖的情况下发布审阅者均值低于 4.0/5 的论文。
- 拒绝在需要沙箱内网络访问的种子想法上运行。改为添加单独的只读数据集卷。
- 拒绝重跑红队未被执行和记录的论文。

输出：包含树搜索引擎、沙箱策略、撰写器/审阅者循环、三个带可复现捆绑包的示例运行、红队报告、成本账本 CSV 的仓库，以及记录你复现了哪些 Sakana v2 失败模式以及缓解措施如何生效的 write-up。