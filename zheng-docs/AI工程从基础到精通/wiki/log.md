# 操作日志

> append-only 记录。格式：`## [日期] 操作类型 | 描述`

## [2026-05-26] init | 知识库初始化

基于 Karpathy LLM Wiki 模式初始化知识库：
- 创建三层架构：阶段目录（原始资料层）= 阶段目录，Wiki 层 = wiki/，Schema = CLAUDE.md
- 20 个阶段目录，431 篇文档来自 phases 中文版
- 建立 wiki/index.md 总目录
- 建立 wiki/overview.md 高层综合
- 建立 wiki/concepts/ 核心概念页
- 建立 wiki/log.md 本日志

## [2026-05-26] create | CLAUDE.md Schema

写入 Schema 文件，定义 Wiki 结构、页面约定、三个核心操作（Ingest/Query/Lint）的工作流。