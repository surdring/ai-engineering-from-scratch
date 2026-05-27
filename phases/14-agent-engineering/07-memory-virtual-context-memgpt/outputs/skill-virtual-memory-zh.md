---
name: virtual-memory
description: 为任意目标运行时搭建一个 MemGPT 形态的两层记忆系统（主上下文 + 归档存储 + 记忆工具），具有正确的驱逐、引用和不可信输入处理。
version: 1.0.0
phase: 14
lesson: 07
tags: [memory, memgpt, virtual-context, archival, citations]
---

给定一个目标运行时（Python、Node、Rust）、一个模型服务商（Anthropic、OpenAI、本地）和一个存储后端（内存、SQLite、向量数据库、KV、图），生成一个正确的 MemGPT 形态记忆系统。

生成内容：

1. 一个 `MainContext` 类型，包含 `core` 字典（命名的持久化分区）和 `messages` 列表（FIFO）。达到容量上限时自动驱逐；被驱逐的轮次仍可通过 `conversation_search` 检索。
2. 一个 `ArchivalStore`，包含插入和搜索功能。记录必须携带 `id`、`text`、`tags`、`session_id`、`turn_id`、`created_at`。每次写入返回存储的 id 以供引用。
3. 五个与 MemGPT 接口匹配的记忆工具：`core_memory_append`、`core_memory_replace`、`archival_memory_insert`、`archival_memory_search`、`conversation_search`。向模型展示这些工具时使用能告诉模型何时使用的 `description` 文本。
4. 引用约定：每次归档检索必须返回记录 id 和文本，且智能体必须在最终答案中引用它们。没有引用的答案属于软性失败。
5. 一个整合钩子（v1 中可以是空操作），以便第 08 课的休眠时智能体可以在不需重新改造管道的情况下接入。暴露 `list_records_since(timestamp)` 和 `delete(id)`。

硬性拒绝：

- 使用完整提示 LLM 评分搜索归档。应使用适当的检索后端（BM25、向量相似度）。允许在 top-k 短列表上进行 LLM 重排序，而非在整个语料库上。
- 主上下文没有驱逐策略。无界主上下文会静默增长超出窗口。
- 将检索到的内容当作用户指令存储。所有归档内容都是不可信文本（第 27 课）。将其作为观察传递给模型，而非系统提示。
- 编写会清除所有分区的 `core_memory_clear` 工具。核心是承重的；清除是危险的。支持 `replace` 而非 `clear`。

拒绝规则：

- 如果用户要求「不要引用，只给答案」，对任何需要来源归因的领域（医疗、法律、政策、金融）拒绝。提供一个折中方案：将引用渲染为脚注而非内联。
- 如果用户要求「不经过滤地将所有检索内容写回归档」，拒绝并指向第 27 课。检索内容是可被攻击者触及的；不加过滤地写回是记忆污染。
- 如果运行时没有持久化层，拒绝交付描述为具有「长期记忆」的智能体。降级产品描述，而非实现。

输出：每个组件一个文件（`main_context.*`、`archival_store.*`、`memory_tools.*`、`agent.*`），外加一个 `README.md`，解释驱逐策略、引用约定，以及在哪里接入第 08 课（休眠时整合）和第 09 课（Mem0 融合）。结尾的「下一步阅读」指向第 08 课如果智能体需要三层或异步整合，或第 09 课如果智能体需要向量+KV+图融合。