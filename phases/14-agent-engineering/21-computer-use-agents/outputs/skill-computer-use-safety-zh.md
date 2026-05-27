---
name: computer-use-safety
description: 为计算机使用智能体构建逐步安全分类器 + 确认门控，包含允许列表导航和注入标记过滤。
version: 1.0.0
phase: 14
lesson: 21
tags: [computer-use, safety, claude, openai-cua, gemini]
---

给定一个计算机使用智能体和目标应用列表，生成一个在执行前对每个动作进行分类的安全层。

生成：

1. `SafetyClassifier.assess(action, screen) -> SafetyVerdict`，包含字段 `allow`、`reason`、`needs_confirmation`。
2. 智能体可以点击的元素标签的允许列表；否则拒绝。
3. 智能体可以导航到的 URL 的允许列表；重定向出列表时拒绝。
4. 对 DOM 文本、检索内容和输入文本的注入标记过滤。任何匹配都会阻止动作。
5. 敏感动作的确认门控（登录、购买、删除、发布）。人机协同回调接口。
6. 追踪发射器：每个决策记录（action、verdict、reason）。

硬性拒绝：

- 只在第一个动作上运行的安全分类器。每个动作都必须被分类。
- 形式为 `*` 的允许列表。允许一切的允许列表不是允许列表。
- 因为模型「看起来很有信心」而跳过确认。信心不是安全。

拒绝规则：

- 如果智能体拥有没有逐步安全的计算机使用权限，拒绝交付。
- 如果智能体可以导航到任意 URL，拒绝。要求允许列表或阻止列表。
- 如果敏感动作在任何模式下绕过了确认门控，拒绝。

输出：`classifier.py`、`allowlist.py`、`confirmation.py`、`trace.py`、`README.md`，解释门控策略、注入标记和允许列表维护流程。结尾的「下一步阅读」指向第 27 课（提示注入）和第 23 课（安全决策的 OTel span 归属）。