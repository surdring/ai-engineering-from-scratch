---
name: benchmark-harness
description: 为代码库构建一个 SWE-bench 风格的测试夹具，包含 FAIL_TO_PASS / PASS_TO_PASS 门控、污染检查和步骤数指标。
version: 1.0.0
phase: 14
lesson: 19
tags: [swe-bench, gaia, agentbench, harness, evaluation]
---

给定一个代码库和一个（bug, fix）对列表，构建一个以真实单元测试为门控并记录运营指标的基准测试夹具。

生成：

1. 每任务定义：`(tid, description, state_before, fail_to_pass_tests, pass_to_pass_tests, solution)`。
2. 一个运行器，应用智能体的补丁，在沙箱中运行仓库的测试套件，并记录：FTP 通过数、PTP 通过数、步骤数、token、墙上时间、成本。
3. 一个污染检查：将问题文本与生成的补丁进行模式匹配；标记 >=30% 的重叠。
4. 一个报告器，以 JSON 格式输出每任务和聚合分数，加上 P50/P75/P95 步骤和成本。
5. 一个 CI 作业，在每个 PR 上运行夹具，在 >=5% 回归时失败。

硬性拒绝：

- 只报告单一聚合数字的夹具。要求每任务结果 + 分布。
- 在没有沙箱的情况下运行测试的夹具。智能体提供的补丁是不可信代码。
- 没有 PASS_TO_PASS 门控的夹具。破坏其他测试的补丁会静默地使产品退化。

拒绝规则：

- 如果用户要求「只要 FAIL_TO_PASS 分数」，拒绝。添加 PASS_TO_PASS；破坏现有测试是比遗漏修复更严重的回归。
- 如果测试没有固定到特定提交，拒绝。测试的漂移使分数在不同运行之间不可比较。
- 如果任务与训练期间见过的问题文本重叠，明确标记。

输出：`tasks.py`、`harness.py`、`contamination.py`、`report.py`、`README.md`，解释沙箱、门控、污染策略。结尾的「下一步阅读」指向第 30 课了解基于该夹具的评估驱动开发。