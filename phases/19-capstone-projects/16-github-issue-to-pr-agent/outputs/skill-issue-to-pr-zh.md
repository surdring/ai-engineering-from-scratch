---
name: issue-to-pr
description: 构建异步 GitHub issue 转 PR 智能体，在云沙箱中运行，复现构建、验证测试并打开可审阅的 PR，同时严格遵守每个仓库的预算限制。
version: 1.0.0
phase: 19
lesson: 16
tags: [capstone, async-agent, github, fargate, daytona, swe-bench, budget, safety]
---

给定一个带有标记为 `@agent fix this` 的 issue 的 GitHub 仓库，交付一个自托管云智能体，将每个标记的 issue 转化为具有限定凭据和受限成本的可审阅 PR。

构建计划：

1. 带细粒度令牌的 GitHub App：issues rw、PR write、contents rw、workflows read。不允许 force-push。main 分支保护防止直接写入。
2. Webhook 接收器（Lambda 或 Fly.io）过滤标签 / PR 评论事件并入队到 SQS。
3. 调度器强制执行每个仓库每天的资金和 PR 数量上限；为每个允许的作业启动 ECS Fargate 任务。
4. 环境推断：从仓库内容检测语言 + 包管理器 + 运行时。不存在则动态合成 Dockerfile。
5. 每个任务一个 Daytona 或 E2B 沙箱。将仓库克隆到全新的 `git worktree` + agent 分支中。
6. 智能体循环（基于 Claude Opus 4.7 或 GPT-5.4-Codex 的 mini-swe-agent 或 SWE-agent v2）。工具：ripgrep、tree-sitter repo-map、read_file、edit_file、run_tests、git。上限：$20、30 回合、30 分钟。
7. 验证：沙箱内完整 CI；通过 jacoco / coverage.py 测量覆盖率增量；若增量低于 -2% 则标记 `needs-review`；若 CI 失败则暂停。
8. 通过 GitHub API 打开 PR，附带理由、diff 摘要、trace URL、成本、回合数。
9. 可观测性：每个 PR 的 Langfuse trace；密钥日志脱敏；每个仓库的预算仪表盘。
10. 在 30 个种子内部 issue 上评估；在三个 issue 的共享子集上与 Cursor Background Agents 和 AWS Remote SWE Agents 进行对比。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | 30 个 issue 的通过率 | 端到端成功（CI 绿色 + 覆盖率 OK） |
| 20 | PR 质量 | Diff 大小、覆盖率增量、风格一致性 |
| 20 | 每个解决 issue 的成本和延迟 | $/PR 和 wall-clock/PR |
| 20 | 安全性 | 受限令牌、每个仓库预算、无 force-push、凭据卫生 |
| 15 | 运维者 UX | 理由注释、重试能力、@-mention 跟进 |

硬性拒绝：

- 任何可以 force-push 的智能体。硬性排除。
- 跳过预算检查的调度器。失控循环是经典的失败模式。
- 在沙箱内未通过完整 CI 的情况下打开的 PR。
- trace 存档包含未脱敏的令牌或 PII（个人身份信息）。

拒绝规则：

- 拒绝在没有 main 分支保护的情况下安装。
- 拒绝在没有每个仓库每日预算（美元和 PR 数量）的情况下运行。
- 拒绝自动重试失败的运行；所有重试需要人工重新应用标签。

输出：包含 GitHub App、webhook 接收器、调度器 + 预算账本、Fargate 任务定义、沙箱生命周期管理器、mini-swe-agent 循环、30 issue 评估运行、与 Cursor Background Agents 和 AWS Remote SWE Agents 的并排比较，以及一份指出三大构建推断失败模式和减少每个的 Dockerfile 合成更改的 write-up 的仓库。