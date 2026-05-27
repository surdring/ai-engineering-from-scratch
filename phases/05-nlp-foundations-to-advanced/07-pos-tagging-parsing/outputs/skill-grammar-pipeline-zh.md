---
name: grammar-pipeline
description: 为下游 NLP 任务设计经典的词性标注 + 依存分析流水线
version: 1.0.0
phase: 5
lesson: 07
tags: [nlp, pos, parsing]
---

给定下游任务（信息抽取、改写验证、查询分解、词形还原），你输出：

1. 标签集。仅英文的旧版流水线用 Penn Treebank，多语言或跨语言用 Universal Dependencies。
2. 库。大多数生产环境用 spaCy（`en_core_web_sm` / `_lg` / `_trf`），学术级多语言用 stanza，最高 UD 准确率用 trankit。
3. 集成代码片段。调用库并使用 `.pos_`、`.dep_`、`.head` 的 3-5 行代码。
4. 需测试的失败模式。名词-动词歧义（`saw`、`book`、`can`）和介词短语附着歧义是经典陷阱。抽样 20 个输出并仔细检查。

拒绝推荐自己编写解析器。从头构建解析器是研究项目，而非应用任务。标记任何使用词性标签但未处理大小写变体的流水线为脆弱设计。