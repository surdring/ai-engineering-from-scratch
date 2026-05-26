# AI 工程从基础到精通 — Wiki Schema

## 项目结构

知识库根目录同时作为 Obsidian Vault，用 [[wiki-links]] 连接所有页面。

```
AI工程从基础到精通/        ← Obsidian Vault 根目录
├── CLAUDE.md              ← 本文件（Schema）
├── 00-setup-and-tooling/  ← 阶段目录（原始资料层，共 20 个阶段）
│   ├── 01_dev-environment.md
│   └── ...
├── wiki/                  ← LLM 维护的 Wiki 层
│   ├── index.md           ← 总目录，按阶段列出所有页面
│   ├── log.md             ← append-only 操作日志
│   ├── overview.md        ← 知识库高层综合摘要
│   ├── concepts/          ← 跨阶段核心概念页
│   ├── entities/          ← 关键工具/框架/人物页
│   ├── sources/           ← 阶段级源文档摘要
│   ├── comparisons/       ← 对比分析页
│   └── guides/            ← 方法论指南
└── raw/                   ← 原始资料（如有）
```

## 页面约定

每篇 Wiki 页面必须有 YAML frontmatter：

```yaml
---
title: "页面标题"
type: concept | entity | source-summary | comparison | guide
phase: "关联阶段"   # 概念页可跨多个阶段
tags: [标签列表]
related: [关联wiki页面列表]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## 内容层级关系

- **阶段目录** = 原始资料层（Raw Sources），不可修改
- **Wiki 目录** = LLM 可读写层，持续维护和更新
- **阶段文件已有 frontmatter**（title, phase, chapter, tags），可被 Dataview 查询

## Ingest 工作流

当需要向知识库添加新内容时：

1. 确认新文件应放入哪个阶段目录
2. 创建新的阶段页面（格式：`{编号}_{英文名}.md`）
3. 写入规范的 YAML frontmatter + 正文内容
4. 更新 `wiki/index.md` 添加新条目
5. 如涉及跨阶段概念，更新 `wiki/concepts/` 中相关页面
6. 追加记录到 `wiki/log.md`

## Query 工作流

当提问时：

1. 先读 `wiki/index.md` 找到相关页面
2. 深入读取具体阶段页面
3. 综合答案，使用 [[相对路径]] 格式引用原文
4. 如果答案具有持久价值，将其写入 `wiki/concepts/` 或 `wiki/comparisons/`

## Lint 工作流

当执行健康检查时：

1. 检查各阶段文件 frontmatter 完整性
2. 确认 `wiki/index.md` 与文件系统一致
3. 发现跨阶段概念未被 `wiki/concepts/` 覆盖的，建议新增
4. 检查孤立概念页（无入站链接的）
5. 建议下一步可以探索的综合分析方向

## 当前 Wiki 状态

- 阶段数：20
- 总文档数：431
- 语言：中文
- 覆盖领域：从环境搭建到 AI Agent 的综合工程路线图