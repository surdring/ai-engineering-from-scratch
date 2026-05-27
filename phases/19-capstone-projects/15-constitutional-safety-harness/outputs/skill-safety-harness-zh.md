---
name: safety-harness
description: 为目标 LLM 应用连接分层安全流水线，运行六族红队范围，运行宪法自我批评以获得可测量的无害性增量。
version: 1.0.0
phase: 19
lesson: 15
tags: [capstone, safety, red-team, llama-guard, x-guard, garak, pyrit, constitutional-ai]
---

给定目标 LLM 应用（8B 指令调优模型或 RAG 聊天机器人），用分层安全流水线加固，并在六个攻击族上运行自主红队范围。生成加固前后无害性报告。

构建计划：

1. 五层流水线：输入净化（zero-width strip、编码解码、Unicode 规范化）-> NeMo Guardrails v0.12 rails -> 分类器门槛（Llama Guard 4 / X-Guard / ShieldGemma-2 / Nemotron 3）-> 目标 LLM -> 输出过滤器（Llama Guard 4 + Presidio PII + 引用检查）。被标记的输出进入 Slack HITL 队列。
2. 每层发射 Langfuse span，使归属可观测。
3. 红队调度器在 cron 上运行 garak、PyRIT、PAIR、TAP、GCG、多轮 persona 和多语言代码切换攻击。
4. 每次成功的越狱：CVSS 4.0 分数、复现、缓解计划、披露时间线。
5. XSTest 良性提示探测持续运行以捕获过度拒绝退化。
6. 宪法自我批评运行：1k 有害尝试提示 -> 目标草稿 -> 批评者对照书面宪法评分 -> 重写对 -> SFT。在保留无害性评估上测量前后。
7. 告警：良性退化 Slack warning，新越狱族 PagerDuty critical。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | 攻击面覆盖 | 6+ 攻击族演练，2+ 语言 |
| 20 | 真阳性 / 假阳性权衡 | 攻击拦截率 vs XSTest 良性通过率 |
| 20 | 自我批评增量 | 保留评估上前后无害性 |
| 20 | 文档和披露 | CVSS 评分发现及时间线 |
| 15 | 自动化和可重复性 | Cron 驱动，端到端演练告警 |

硬性拒绝：
- 单层安全栈。本顶点项目的核心论点是纵深防御。
- 报告成功率而没有 XSTest 过度拒绝数字的红队运行。
- 没有保留评估的宪法自我批评（报告训练集准确率而非泛化）。
- 越狱发现缺失 CVSS 评分。

拒绝规则：
- 拒绝在没有良性探测对照点的情况下报告安全数字。一个没有另一个是误导的。
- 拒绝在没有人工策划批评对的情况下自动重新训练红队成功。
- 拒绝在没有至少在两种非英语语言上运行 X-Guard 的情况下声称多语言覆盖。

输出：包含五层流水线、红队调度器、PAIR/TAP/GCG 运行器、宪法自我批评训练 harness、XSTest 过度拒绝仪表盘、CVSS 发现跟踪器的仓库，以及指出加固前成功率最高的三大攻击族和缓解每个的具体流水线层的 write-up。