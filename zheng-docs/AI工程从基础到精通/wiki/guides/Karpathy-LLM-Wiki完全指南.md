# Karpathy LLM Wiki 完全指南

## 概述

2026 年 4 月，Andrej Karpathy（OpenAI 联合创始人、前 Tesla AI 总监、"vibe coding" 概念的提出者）发布了一个 GitHub Gist，提出了 **LLM Wiki** 模式——让 LLM 增量构建和维护一个持久化的个人知识库。该 Gist 在两周内获得 5000+ stars 和 4000+ forks，引发了 AI 社区的广泛讨论。

这不是一个产品，也不是一个代码仓库。Karpathy 称之为 **「idea file」（想法文件）** ：在这个 LLM Agent 时代，分享想法比分享代码更重要——因为每个人的 Agent 可以根据想法为自己的环境定制实现。

> "The document's only job is to communicate the pattern. Your LLM can figure out the rest."
> 这份文档的唯一职责是传递模式，你的 LLM 会搞定其余一切。

---

## 核心思想：Wiki > RAG

### RAG 的根本缺陷

传统 RAG（检索增强生成）的工作方式：
1. 上传文档到知识库
2. 提问时，系统检索相关片段
3. LLM 基于检索到的片段生成答案

**问题：每次提问都是从零开始重新发现知识。** 问一个需要综合 5 份文档的问题，LLM 每次都要重新找、重新拼那些片段。没有积累——今天问过的问题，明天再问还是从头来。

### LLM Wiki 的解决方案

> "Instead of just retrieving from raw documents at query time, the LLM incrementally builds and maintains a persistent wiki — a structured, interlinked collection of markdown files that sits between you and the raw sources."

**LLM 不只是在查询时检索，而是增量维护一个持久化的 Wiki。** 新增一篇文档时，LLM 会：

- 阅读文档，提取关键信息
- 将这些信息**整合进现有的 Wiki**
- 更新相关实体页面
- 修订主题摘要
- 标记新数据与旧说法矛盾的地方
- 更新交叉引用

知识被编译一次，然后持续保持最新。Cross references 已建好，矛盾已标记，综合分析已完成。Wiki 随着每次添加源和每个问题而变得越来越丰富。

### RAG vs LLM Wiki 对比

| 维度 | RAG | LLM Wiki |
|------|-----|----------|
| 知识处理时机 | 查询时（每次） | 录入时（一次） |
| 交叉引用 | 每次查询临时发现 | 预先建立并持续维护 |
| 矛盾检测 | 基本不检测 | 录入时标记 |
| 知识积累 | 无——每次从零开始 | 随源文件和查询复合增长 |
| 输出格式 | 对话回复（易失） | 持久化 Markdown 文件 |
| 维护者 | 系统（黑箱） | LLM（透明、可编辑） |
| 人的角色 | 上传 + 提问 | 策展 + 探索 + 提问 |
| 典型产品 | NotebookLM、ChatGPT 文件上传 | Karpathy LLM Wiki 模式 |

---

## 三层架构

Karpathy 定义了三个清晰的层次：

```
Raw Sources（不可变）→ LLM 读取 → Wiki（LLM 增量维护）
                                      ↑
                                  Schema（指令）
```

### Layer 1：Raw Sources（原始资料）

```
raw/
├── articles/
│   ├── 2026-03-attention-is-all-you-need-revisited.md
│   └── 2026-04-scaling-laws-update.md
├── papers/
│   ├── transformer-architecture-v2.pdf
│   └── mixture-of-experts-survey.pdf
├── repos/
│   └── llama-3-readme.md
├── data/
│   └── benchmark-results.csv
└── assets/
    └── transformer-diagram.png
```

- **你在策展**的源文件：文章、论文、图片、数据文件
- **不可变**——LLM 只能读，不能写。这是事实来源
- 这意味着你始终有原始材料可以核实——如果 LLM 在 Wiki 中出错，可以追溯到原始源并更正

### Layer 2：The Wiki（知识库本体）

```
wiki/
├── index.md              # 总目录——每页一行摘要 + 链接
├── log.md                # 时间线日志——append-only 操作记录
├── overview.md           # 高层综合概述
├── concepts/
│   ├── attention-mechanism.md
│   ├── mixture-of-experts.md
│   ├── scaling-laws.md
│   └── tokenization.md
├── entities/
│   ├── openai.md
│   └── anthropic.md
├── sources/
│   ├── summary-attention-revisited.md
│   └── summary-scaling-update.md
└── comparisons/
    └── gpt4-vs-claude-vs-gemini.md
```

- **LLM 完全掌控这一层**：创建页面、更新内容、维护交叉引用、保持一致性
- 你只读 Wiki，LLM 写 Wiki——和传统笔记软件完全不同
- 每页都应包含 [[wiki-link]] 形式的交叉引用，形成知识图谱
- Obsidian 的图谱视图是可视化 Wiki 结构的最佳工具

### Layer 3：The Schema（指令文件）

这是最关键的一层。没有 Schema，LLM 只是一个碰巧能访问文件的聊天机器人。有了 Schema，LLM 就变成了**有纪律的 Wiki 维护者**。

```markdown
# LLM Wiki Schema

## Project Structure
- `raw/` — immutable source documents. NEVER modify.
- `wiki/` — LLM-generated wiki. You own this entirely.
- `wiki/index.md` — master catalog. Update on every ingest.
- `wiki/log.md` — append-only activity log.

## Page Conventions
Every wiki page MUST have YAML frontmatter:
---
title: Page Title
type: concept | entity | source-summary | comparison
sources: [list of raw/ files referenced]
related: [list of wiki pages linked]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
---

## Ingest Workflow
When I say "ingest [filename]":
1. Read the source file in raw/
2. Discuss key takeaways with me
3. Create/update a summary page in wiki/sources/
4. Update wiki/index.md
5. Update all relevant concept and entity pages
6. Append an entry to wiki/log.md

## Query Workflow
When I ask a question:
1. Read wiki/index.md to find relevant pages
2. Read those pages
3. Synthesize an answer with [[wiki-link]] citations
4. If the answer is valuable, offer to file it as a new wiki page

## Lint Workflow
When I say "lint":
1. Check for contradictions between pages
2. Find orphan pages with no inbound links
3. List concepts mentioned but lacking own page
4. Check for stale claims superseded by newer sources
5. Suggest questions to investigate next
```

**文件名约定：**
- Claude Code → `CLAUDE.md`
- OpenAI Codex → `AGENTS.md`
- OpenCode / Pi → `OPENCODE.md`

---

## 三个核心操作

### 操作 1：Ingest（录入）

触发：你把新文档放入 `raw/` 目录，告诉 LLM 处理它。

LLM 的典型流程：
1. 读取源文件
2. 与你讨论关键要点
3. 在 `wiki/sources/` 中创建/更新摘要页
4. 更新 `wiki/index.md`
5. **更新所有相关的概念页和实体页**（一篇源文档可能涉及 10-15 个 Wiki 页面的更新）
6. 在 `wiki/log.md` 追加记录

Karpathy 的个人偏好：一次 Ingest 一篇、保持参与——他读摘要、检查更新、引导 LLM 强调什么。但也可以批量 Ingest 多篇源文件。

### 操作 2：Query（查询）

触发：你向 LLM 提问。

LLM 的流程：
1. 读取 `index.md` 找到相关页面
2. 深入阅读这些页面
3. 综合答案，附上 [[wiki-link]] 引用
4. **如果答案有价值，将其写回 Wiki 成为新页面**——这是关键洞见。你探索出的关联、分析、对比，不应该消失在对话历史里，应该累积进知识库

输出格式不限于 Markdown：对比表格、幻灯片（Marp）、图表（matplotlib）都可以。

### 操作 3：Lint（健康检查）

触发：定期让 LLM 做 Wiki 健康检查。

LLM 检查的内容：
- 页面间是否有矛盾？
- 是否有被新源文档替代的过时说法？
- 是否有孤儿页面（没有内链指向它）？
- 重要概念被提到了但没有自己的页面？
- 是否有缺失的交叉引用？
- 建议下一步探索的问题和新信息来源

---

## 两个关键文件

### index.md —— 内容目录

- 按分类组织（concepts、entities、sources、comparisons 等）
- 每行：页面链接 + 一句话摘要 + 可选元数据
- LLM 在每次 Ingest 时更新
- 查询时 LLM 先读 index 再深入相关页面
- 在中等规模下（~100 源，~数百页）效果出奇好，不需要 Embedding RAG 基础设施

### log.md —— 时间线日志

- append-only 操作记录
- 格式：`## [2026-04-02] ingest | Article Title`
- `grep "^## \[" log.md | tail -5` 可以快速查看最近 5 条操作
- 让 LLM 了解最近做了什么

---

## 工具栈

### 核心工具

| 工具 | 用途 |
|------|------|
| **LLM Agent** | Claude Code / OpenAI Codex / Cursor / OpenCode | Wiki 的「程序员」，负责读写维护 |
| **Obsidian** | Wiki 的「IDE」——浏览页面、图谱视图、链接导航 |
| **Git** | 版本控制——每次 Wiki 更新都是一次 commit |

### 推荐 Obsidian 插件

| 插件 | 用途 |
|------|------|
| **Obsidian Web Clipper** | 浏览器扩展，一键将网页转为 Markdown 保存到 raw/ |
| **Graph View**（内置） | 可视化 Wiki 的知识图谱结构 |
| **Dataview** | 基于页面 frontmatter 查询，生成动态表格/列表 |
| **Marp Slides** | 从 Markdown 直接生成演示文稿 |

### 可选增强

| 工具 | 用途 |
|------|------|
| **qmd** | 本地 Markdown 搜索引擎，混合 BM25/向量搜索 + LLM 重排序 |
| **本地图片下载** | Obsidian 设置中将附件目录设为 `raw/assets/`，绑定快捷键下载图片 |

---

## Karpathy 的典型工作流

> "I have the LLM agent open on one side and Obsidian open on the other. The LLM makes edits based on our conversation, and I browse the results in real time — following links, checking the graph view, reading the updated pages. Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

一侧是 LLM Agent（Claude Code），另一侧是 Obsidian。对话驱动编辑，实时浏览更新结果。

---

## 适用场景

Karpathy 列举的场景：

| 场景 | 说明 |
|------|------|
| **个人知识管理** | 追踪目标、健康、心理学、自我提升——录入日记、文章、播客笔记 |
| **深度研究** | 数周/数月深入研究一个主题——读论文、文章、报告，逐步构建综合 Wiki |
| **读书** | 逐章录入，建立人物、主题、情节线之间的关联，最终形成一本丰富的配套 Wiki |
| **团队/商业** | 内部 Wiki，由 Slack 讨论、会议记录、项目文档、客户通话驱动，人工审核更新 |
| **竞品分析** | 持续收集竞品信息，LLM 自动整理对比 |
| **尽职调查** | 多源资料自动综合 |
| **课程笔记** | 将课程资料整理成结构化的知识体系 |
| **兴趣深挖** | 任何需要长时间积累和组织知识的场景 |

---

## Karpathy 本人的实际数据

Karpathy 透露他用这个架构维护的 Wiki 已经达到：

- **约 100 篇文章**
- **约 40 万词**

---

## 为什么这个模式有效？

维护知识库的繁琐部分不是阅读或思考——而是记账：更新交叉引用、保持摘要最新、标记新旧矛盾、维持几十个页面之间的一致性。

人类放弃 Wiki 是因为维护负担增长快于价值增长。LLM 不会无聊，不会忘记更新交叉引用，一次可以触及 15 个文件。维护成本几乎为零。

> "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else."

人的工作是策展源材料、引导分析、提出好问题、思考一切意味着什么。LLM 的工作是其余一切。

---

## Idea File 的哲学

Karpathy 提出了一种新的分享范式——**idea file（想法文件）**：

> "The idea of the idea file is that in this era of LLM agents, there is less of a point/need of sharing the specific code/app, you just share the idea, then the other person's agent customizes & builds it for your specific needs."

在 LLM Agent 时代，分享具体代码/应用的意义降低了。你只需分享想法，对方的 Agent 会根据其特定需求定制和构建实现。

这是一种新的开源范式——不是开放代码，而是**开放想法**，由 AI Agent 来解释和实例化。

---

## 与 Memex 的关联（1945）

Karpathy 指出，这个概念与 Vannevar Bush 1945 年提出的 Memex 理念精神相通——一个个人策展的知识存储，文档之间有联想轨迹。

> "Bush's vision was closer to this than to what the web became: private, actively curated, with the connections between documents as valuable as the documents themselves."

Bush 的愿景更接近这个模式，而非万维网的形态：私有的、主动策展的，文档之间的连接与文档本身同等有价值。Bush 当年无法解决的是**谁来做维护**的问题，而 LLM 解决了这一点。

---

## 社区生态与发展

Gist 发布后，社区涌现出大量实现：

| 项目 | Stars | 特点 |
|------|-------|------|
| SamurAIGPT/llm-wiki-agent | ~1,965 | 多平台支持（Claude Code / Codex / Gemini CLI），录入时即检测矛盾 |
| AgriciDaniel/claude-obsidian | ~1,480 | 10 项专门技能，热缓存层实现跨会话上下文保持，6 种预设模式 |
| nashsu/llm_wiki | ~1,150 | 纯 Python 实现，支持本地模型 |
| coregit.dev LLM Wiki | 商业化 | 基于 Git 的版本化 Wiki，语义搜索 + 知识图谱 API |

---

## 局限性

1. **规模上限**：~1000 页以下效果最佳，超过此规模可能需要引入搜索基础设施
2. **幻觉风险**：LLM 生成的 Wiki 内容需要定期人工审核，特别是在关键事实上
3. **每次 Token 成本**：Ingest 操作 Token 消耗高（一篇源可能触发 10-15 页更新），但 Query 成本低
4. **需要 Agent 能力**：依赖 Claude Code、Codex 等具备文件操作能力的 Agent，普通聊天界面无法胜任
5. **社区争议**：有评论者指出，完全由 LLM 维护的 Markdown 文件夹被称为「Wiki」存在范畴错误——因为没有多人协作编辑

---

## 快速上手指南

### Step 1：创建目录结构

```bash
mkdir -p my-wiki/{raw/{articles,papers,assets},wiki/{concepts,entities,sources,comparisons}}
```

### Step 2：编写 Schema 文件

将上述 CLAUDE.md（或 AGENTS.md）模板复制到项目根目录，根据你的需求调整。

### Step 3：放入第一篇源文件并告知 Agent

把 Karpathy 的 Gist 原文复制给 Agent：

```
请帮我基于 Karpathy 的 LLM Wiki 模式建立一个知识库。
主题：[你的研究主题]
Schema 文件：CLAUDE.md

以下是 Karpathy 的 idea file：
[paste the full gist content]
```

### Step 4：录入第一份源文件

```
ingest raw/articles/my-first-article.md
```

### Step 5：探索和提问

```
这个主题的核心概念有哪些？帮我整理一个 overview。
```

### Step 6：定期维护

```
lint——检查 Wiki 健康状况
```

---

## 关键资源

- 原始 Gist：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Karpathy 原推：https://twitter.com/karpathy/status/2039805659525644595
- Idea File 推文：https://twitter.com/karpathy/status/2040470801506541998
- Obsidian：https://obsidian.md
- qmd 搜索引擎：https://github.com/tobi/qmd

---

## 一句话总结

**停止把 LLM 当作「回答问题的工具」，开始把它当作「持续维护知识库的司书」。知识在录入时编译一次，之后永久可用——这是 RAG 做不到的。**