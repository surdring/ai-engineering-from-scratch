---
name: handoff-generator
description: 从工作台产物生成会话结束交接数据包，生成人类可读的 Markdown 和按七个规范字段组织的机器可读 JSON。
version: 1.0.0
phase: 14
lesson: 40
tags: [handoff, generator, session-end, packet, next-action]
---

给定一个工作台（状态、裁决、审查、反馈日志、diff），生成接入智能体运行时的会话结束交接生成器。

生成：

1. `tools/generate_handoff.py`，暴露 `generate_handoff(snapshot) -> (markdown, payload)`。
2. `outputs/handoff/<session_id>/handoff.md` 和 `handoff.json`。
3. `handoff.schema.json`，覆盖七个必需字段和反馈尾部格式。
4. 会话结束钩子脚本，运行生成器并在任何字段缺失时拒绝关闭会话。
5. `docs/handoff.md`，列出七个字段、其来源和裁剪策略。

硬性拒绝：

- 没有 `next_action` 的交接。伪装成交接的状态报告会毒化下一次会话。
- 手写摘要的生成器。智能体的职责是将工作台保持在可生成状态。
- 与 JSON 分歧的 Markdown 数据包。JSON 是来源；Markdown 是 JSON 的渲染。
- 超过 30 条条目的反馈尾部。完整日志在版本控制中；数据包必须保持小。

拒绝规则：

- 如果验证报告缺失，拒绝生成数据包。没有裁决的交接是愿望。
- 如果审查报告缺失且预期有人工审查者，拒绝并要求先通过审查。
- 如果 diff 摘要为空但会话运行超过 5 分钟，在生成前提出该异常；怀疑是卡住的会话而非真正的空操作。

输出结构：

```
<repo>/
├── outputs/handoff/<session_id>/
│   ├── handoff.md
│   └── handoff.json
├── tools/generate_handoff.py
├── handoff.schema.json
└── docs/handoff.md
```

结尾的「下一步阅读」指向：

- 第 41 课了解在真实风格示例应用上的端到端练习。
- 第 42 课了解将生成器打包到顶点工作台包中。
- 第 29 课（生产运行时）了解将会话结束接入队列、事件和定时任务触发器。