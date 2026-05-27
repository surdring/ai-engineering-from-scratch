---
name: verification-gate
description: 生成一个确定性验证门控，将范围、规则和反馈产物组合为每任务的 verification_report.json，加上拒绝合并不带绿色裁决的 CI 接线。
version: 1.0.0
phase: 14
lesson: 38
tags: [verification, gate, deterministic, ci, override-log]
---

给定一个项目的验收标准和现有工作台产物，生成验证门控和覆盖审计日志。

生成：

1. `tools/verify_agent.py`，暴露 `verify(task_id, artifacts) -> VerdictReport`。纯函数，确定性，无 LLM 调用。
2. `outputs/verification/<task_id>.json` 作为单一的裁决真相源。
3. `tools/override.py`，将签名覆盖条目追加到 `outputs/verification/overrides.jsonl`（必须包含 reason、user id、timestamp、finding code）。
4. CI 工作流，在 `passed: false` 时失败并在行内显示报告。
5. `docs/verification.md`，列出每个检查、其严重级别、来源产物和覆盖策略。

硬性拒绝：

- 调用 LLM 的检查。门控是确定性的管道工作；LLM 判断属于审查者。
- 智能体可以在没有签名条目的情况下走的覆盖路径。覆盖仅限人类。
- 省略其所消费的产物路径的验证报告。报告必须可审计。
- 工作流可以静默降级的阻塞严重级别发现。严重级别在写入时固定，而非读取时。

拒绝规则：

- 如果项目没有验收命令，拒绝交付门控直到存在一个。不能证明任何事的门控是表演。
- 如果规则报告不存在，拒绝跳过规则检查；失败关闭。
- 如果反馈日志不存在，拒绝跳过验收检查；缺失日志本身就是阻塞项。
- 如果覆盖条目不受版本控制，拒绝接入覆盖路径；非正式的覆盖会使门控失效。

输出结构：

```
<repo>/
├── tools/
│   ├── verify_agent.py
│   └── override.py
├── outputs/verification/
│   ├── overrides.jsonl
│   └── <task_id>.json
├── docs/verification.md
└── .github/workflows/verify.yml
```

结尾的「下一步阅读」指向：

- 第 39 课了解在绿色裁决之后接手的审查智能体。
- 第 40 课了解在数据包中包含裁决的交接生成器。
- 第 41 课了解对真实风格示例应用运行门控。