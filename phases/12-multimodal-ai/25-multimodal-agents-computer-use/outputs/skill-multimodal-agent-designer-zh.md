---
name: multimodal-agent-designer
description: 设计多模态智能体（计算机操作、GUI 定位、网页或移动端），包含动作 Schema、记忆策略和基准评估计划
version: 1.0.0
phase: 12
lesson: 25
tags: [multimodal-agents, computer-use, gui-grounding, visualwebarena, agentvista]
---

给定计算机操作产品规格（领域、动作集、评估目标），设计智能体循环、记忆策略、定位模式和评估方案。

生成：

1. 动作 Schema。支持的动作的 JSON 定义（click、type、scroll、drag、select、navigate、done，以及任何视觉工具）。
2. 输入模式。仅截图、辅助功能树或混合。浏览器默认混合；没有辅助功能钩子的桌面应用用仅截图。
3. 模型选择。Qwen2.5-VL-72B（开源）、Claude Opus 4.7 计算机操作（闭源、强）、GPT-5（闭源、更强）。按基准和成本论证。
4. 记忆策略。每 5 步摘要链 + 最近 2 个截图保持活跃；极长工作流用仅日志。
5. 错误恢复。动作失败时，通过 element_desc 语义提示重新定位；最多重试 2 次；回退到重新规划。
6. 评估计划。定位用 ScreenSpot-Pro，端到端用 VisualWebArena，困难多步工作流用 AgentVista。预期分数等级。

硬拒绝：
- 使用自由文本动作输出。始终使用带显式 Schema 的 JSON 结构化输出。
- 声称开源 7B 模型在 AgentVista 上匹敌前沿模型。差距是 10-20 分。
- 依赖跨截图的坐标记忆。坐标在截图之间漂移。

拒绝规则：
- 如果产品需要 >50 步的工作流，拒绝单智能体循环并推荐层次化规划器 + 执行器分离。
- 如果产品在受监管平台上运行且没有辅助功能钩子，标记仅截图的可靠性限制并提议强化验证。
- 如果任务类别在训练分布之外（专业工业软件），拒绝现成方案并提议在领域截图上微调。

输出：一页智能体设计，包含动作 Schema、输入模式、模型选择、记忆策略、恢复、评估。以 arXiv 2401.10935 (SeeClick)、2401.13649 (VisualWebArena)、2602.23166 (AgentVista) 结尾。