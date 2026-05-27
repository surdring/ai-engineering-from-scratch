---
name: hybrid-memory
description: 生成一个 Mem0 形态的三存储记忆系统（向量 + KV + 图），包含融合评分器、作用域分类和时间失效机制。
version: 1.0.0
phase: 14
lesson: 09
tags: [memory, mem0, vector, graph, kv, fusion, scope]
---

给定一个目标运行时、一个向量后端（Qdrant、pgvector、Chroma、sqlite-vec）、一个 KV 后端（Postgres、Redis、dict）和一个图后端（Neo4j、内存边），生成一个融合记忆系统。

生成内容：

1. 三个存储类，位于 `add(text, user_id, session_id, scope, importance, tags)` 门面之后。写入时，提取器将 `text` 分解为记录、KV 三元组和图三元组。没有一个存储是可选的。
2. 一个融合评分器 `score = w_rel * relevance + w_imp * importance + w_rec * recency`。将三个权重全部暴露为可配置的。按产品调优，而非按调用。
3. 作用域分类：`user`、`session`、`agent`。检索必须尊重作用域。用户查询绝不能泄露其他用户的记录。
4. 时间失效。矛盾时标记旧边/记录为无效；绝不删除。暴露 `search(query, as_of=timestamp)` 用于历史查询。
5. 一个提取器接口。默认可以是 LLM 驱动的；允许为测试使用确定性正则表达式回退。限制每次 `add()` 的图边数以防止爆炸。

硬性拒绝：

- 将单存储记忆描述为「Mem0 形态」。纯向量、纯 KV、纯图产品可以，但不是混合记忆。不要错误命名。
- 没有每个作用域的权重或显式 `scope=` 过滤器的跨作用域检索。作用域泄露是合规和隐私事件。
- 在矛盾时删除。使无效并加时间戳。删除会隐藏错误并破坏审计。

拒绝规则：

- 如果用户要求「不要重要性加权」，拒绝。在百万条记录上做扁平相关性排序是注定会失败的检索方式。
- 如果图后端没有冲突检测器，拒绝将结果系统称为「Mem0 形态」。降级名称。
- 如果产品涉及 PII（医疗、法律、HR），拒绝交付带有未经产品所有者审核的提取器。

输出：每个存储一个文件，外加 `memory.py`（门面）、`config.py`（权重）、`README.md`，解释融合权重、作用域策略、提取器约定和失效语义。结尾的「下一步阅读」指向第 10 课如果智能体需要学习新技能，第 23 课如果记忆操作需要 OTel span，或第 27 课关于检索时的不可信输入处理。