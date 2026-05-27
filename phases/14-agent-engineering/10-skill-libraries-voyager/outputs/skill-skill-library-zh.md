---
name: skill-library
description: 生成一个 Voyager 形态的技能库，包含注册、相似度检索、组合执行和失败驱动的精炼。
version: 1.0.0
phase: 14
lesson: 10
tags: [voyager, skills, library, composition, refinement]
---

给定一个目标运行时和一个领域，生成一个支持 Voyager 三个组件的技能库：课程钩子、可检索技能存储、迭代精炼。

生成内容：

1. `Skill` 类型，包含 `name`、`description`、`code`、`version`、`tags`、`depends_on`、`history`。每次写入记录先前的代码。
2. `SkillLibrary`，包含 `register(skill, dedup=True)`（新增或版本递增）、`search(query, top_k, tag_filter)`、`get(name)`、`topo_order(name)`（依赖解析）、`execute(name, context)`（拓扑运行）。
3. 检索必须使用嵌入相似度或 BM25，而非对整个库进行 LLM 评分。允许在 top-k 短列表上进行 LLM 重排序。
4. 执行必须按技能捕获异常，并将其呈现到追踪中作为精炼循环可以消费的反馈。
5. 一个精炼钩子：`execute` 失败后，运行时收集（task、skill_name、error、env_state），传递给模型，然后在重写的技能上调用 `register`。版本递增；历史保留旧代码。

硬性拒绝：

- 技能是散文字符串而非代码的库。技能必须是可执行的。散文属于 `description`。
- 没有拓扑排序的组合。没有环检测的深度优先搜索会在技能 DAG 上失败。
- 静默版本覆盖。每次精炼必须递增 `version` 并将旧代码推送到 `history` 以进行审计。

拒绝规则：

- 如果目标运行时没有技能执行的沙箱，对涉及生产系统的领域拒绝。在交付前要求沙箱（第 09 课原则）。
- 如果用户要求「每次失败自动重试而不精炼」，拒绝。不精炼的重试会放大错误而非修复错误。
- 如果库超出约 200 个技能且使用扁平检索，拒绝称其为「生产就绪」。先添加标签过滤器和层次命名空间。

输出：`skill.py`、`library.py`、`execute.py`、`refine.py`，以及一个 `README.md`，解释去重规则、检索后端、精炼提示和版本策略。结尾的「下一步阅读」指向第 17 课关于 Claude Agent SDK 集成，第 16 课关于 OpenAI Agents SDK 工具转换，或第 30 课关于评估技能库质量。