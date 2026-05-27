---
name: devops-agent
description: 构建 Kubernetes 排障智能体，遍历集群知识图谱，排名根因，并通过 Slack 对每个修复进行把关。
version: 1.0.0
phase: 19
lesson: 06
tags: [capstone, devops, sre, kubernetes, langgraph, fastmcp, aiops]
---

给定 K8s 集群和告警源（PagerDuty 或 Alertmanager），构建一个在五分钟内生成排名根因假设的智能体，并通过 Slack 审批卡片对每个修复进行把关。

构建计划：

1. 每 30s 将 kube-state-metrics 摄取到 Neo4j 或 kuzu。构建 Pod、Deployment、Service、Node、PVC、HPA 以及到 Prometheus、Loki 和 Tempo 源的遥测叠加边的图。
2. 为 PagerDuty 和 Alertmanager 搭建 FastAPI webhook 接收器。
3. 通过 FastMCP 暴露带 StreamableHTTP 传输的只读工具：kubectl get/describe、promql、logql、traceql。
4. 构建 LangGraph 根因智能体，包含三个节点：`sample`（拉取 15m 遥测）、`walk`（遍历图邻居）、`hypothesize`（按 recentness × specificity × citation count 排名候选项）。
5. 将带图路径可视化的前三个排名假设发布到 Slack 并带有审批按钮。
6. 将破坏性工具（scale、rollback、delete）放在单独的 FastMCP 服务器上，需要智能体仅在 Slack 批准后获取的审批令牌。
7. 维护仅追加审计日志：每个*考虑过的*命令、是否获批、是否执行、谁批准。
8. 构建 20 个合成事件场景（OOMKill、DNS 抖动、HPA 颠簸、PVC 满载、noisy neighbor、故障 sidecar、ConfigMap 错误上线、证书轮换、image-pull backoff、探针失败等 10 个）。按 RCA 准确率和假设时间对智能体打分。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | 场景套件上的 RCA 准确率 | 20 个合成事件中至少 80% 正确的根因 |
| 20 | 安全性 | 破坏性操作守卫从未在审计日志中无 Slack 批准即触发 |
| 20 | 假设生成时间 | 从告警到 Slack 简报 p50 低于 5 分钟 |
| 20 | 可解释性 | 每个假设都有图路径和遥测引用 |
| 15 | 集成完整性 | PagerDuty、Slack、ArgoCD、Prometheus 端到端正常工作 |

硬性拒绝：
- 具有混合只读和破坏性工具的单一 MCP 服务器的智能体。
- 任何没有遥测引用的根因分析。未引用的假设必须拒绝。
- 仅记录执行的审计日志。必须记录每个考虑过的命令。
- 不运行带种子的 20 场景套件即声称准确率。

拒绝规则：
- 拒绝在没有 Slack 人工值班批准的情况下修复。即使假设是显而易见的。
- 拒绝通过只读 MCP 暴露 `kubectl exec`、`kubectl port-forward` 或任何交互式工具。这些实际上是破坏性的。
- 拒绝在没有逐 Deployment 审批卡片的情况下跨多个 Deployment 批量应用修复。

输出：包含 FastAPI 接收器、LangGraph 智能体、只读和破坏性 MCP 服务器、Slack 集成、20 场景测试套件的仓库，与 AWS DevOps Agent 在三个共享事件上的并排比较，以及一周观察窗口中接近触发的命令（智能体*考虑过*但未执行的）的 write-up。