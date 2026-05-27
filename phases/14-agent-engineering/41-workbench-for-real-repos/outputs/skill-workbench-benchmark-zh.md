---
name: workbench-benchmark
description: 在项目自己的示例应用上运行同一任务，分别通过仅提示和工作台引导的流水线，并生成五结果的前后对比报告。
version: 1.0.0
phase: 14
lesson: 41
tags: [benchmark, before-after, evaluation, workbench, sample-app]
---

给定一个仓库、一个智能体产品和一个小型示例应用，生成一个可移植的评估夹具，比较仅提示与工作台引导的流水线。

生成：

1. `eval/sample_app/`——一个从项目领域抽取的最小可行示例应用。
2. `eval/run_prompt_only.py` 和 `eval/run_workbench.py`，每个接收任务描述并返回 `TaskOutcome`。
3. `eval/report.py`，运行两个流水线并写入 `before-after-report.md` 和 `comparison.json`。
4. CI 工作流，当工作台结果在固定任务套件上回归时失败。
5. `docs/benchmark.md`，解释五个结果以及什么算回归。

硬性拒绝：

- 只有一个流水线的基准测试。比较是全部意义。
- 没有分母的百分比形式结果。始终报告 `n / m`。
- 智能体产品曾在其上训练的示例应用。使用领域调优的夹具。
- 隐藏假阴性的报告。仅提示更快的任务必须被枚举。

拒绝规则：

- 如果项目没有验收命令，拒绝交付基准测试。没有东西可以衡量。
- 如果工作台流水线在中位数任务上花费超过仅提示流水线的 3 倍时间，提出该发现；工作台需要简化，而非换模型。
- 如果夹具无法离线运行，拒绝接入 CI。网络不稳定性会破坏比较。

输出结构：

```
<repo>/
├── eval/
│   ├── sample_app/
│   ├── run_prompt_only.py
│   ├── run_workbench.py
│   └── report.py
├── outputs/eval/
│   ├── before-after-report.md
│   └── comparison.json
├── docs/benchmark.md
└── .github/workflows/benchmark.yml
```

结尾的「下一步阅读」指向：

- 第 42 课了解打包工作台流水线使用的每个表面的顶点包。
- 第 19 课（SWE-bench、GAIA、AgentBench）了解此补充的宏观基准。
- 第 30 课（评估驱动智能体开发）了解基准接入后的持续评估循环。