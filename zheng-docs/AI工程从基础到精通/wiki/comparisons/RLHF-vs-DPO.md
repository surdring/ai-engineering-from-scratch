# RLHF vs DPO：LLM 对齐的两条路径

## 概述

RLHF 和 DPO 都是让 LLM 对齐人类偏好的方法。RLHF 是经典的二阶段方法（先训 Reward Model，再 PPO 优化），DPO 是 2023 年提出的一阶段简化方法。

## 详细对比

| 维度 | RLHF | DPO |
|------|------|-----|
| 阶段数 | 3（SFT → RM → PPO） | 2（SFT → DPO） |
| 是否需要 Reward Model | 需要单独训练 | 不需要 |
| 训练难度 | 高（RL 训练不稳定） | 低（监督学习风格） |
| 在线/离线 | 需要在线采样 | 纯离线 |
| 超参数敏感度 | 高 | 低 |
| 对偏好数据的利用 | 通过 RM 间接利用 | 直接优化偏好 |
| 可扩展性 | PPO 扩展到大规模困难 | 更容易扩展 |
| 奖励 Hacking | 可能发生（优化 proxy reward） | 较少 |
| 代表模型 | InstructGPT, GPT-4, Claude 2 | Llama 3, Zephyr, Qwen |
| 开源友好度 | 低（PPO 调试复杂） | 高（简化训练） |

## 何时选择哪种？

**选择 RLHF：**
- 需要在线探索（生成新回答并学习）
- 多轮交互场景
- 有成熟的基础设施支持 PPO 训练
- 对对齐质量要求极高（大厂场景）

**选择 DPO：**
- 团队规模小，希望快速实验
- 偏好数据集已经收集好
- 不需要在线采样
- 开源项目、学术研究

## 混合方案：Iterative DPO

现代实践中，越来越多团队采用「迭代 DPO」：
1. 用当前模型生成回答
2. 收集标注者对回答的偏好
3. 在新偏好数据上 DPO
4. 重复 1-3

这结合了 DPO 的稳定性和 RLHF 的在线探索优势。

## 相关文档

- [[../10-llms-from-scratch/07_rlhf-from-scratch]] — 从零实现 RLHF
- [[../10-llms-from-scratch/08_direct-preference-optimization]] — DPO 详解
- [[../10-llms-from-scratch/09_rlhf-vs-dpo-which-when]] — 原文详细对比
- [[../concepts/强化学习]] — RL 理论基础