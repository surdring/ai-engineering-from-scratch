---
name: reviewer-agent
description: 搭建一个审查智能体角色，包含五维评分标准，读取构建者产物，生成结构化审查报告，从已写好的页面而非空白页面开始人工审查。
version: 1.0.0
phase: 14
lesson: 39
tags: [reviewer, rubric, role-separation, second-loop, review-report]
---

给定一个已经在生成工作台产物的构建者智能体，搭建一个读取这些产物并写入结构化报告的审查者。

生成：

1. `agents/reviewer.md`，包含审查者系统提示：只读访问、五维评分标准、每个分数必须引用产物路径。
2. `tools/reviewer.py`，从工作台加载 `ReviewerInputs` 并按维度运行 LLM 评分器。
3. `outputs/review/<task_id>.json` 作为规范的审查报告路径。
4. `docs/reviewer-rubric.md`，列出五个维度、每个维度回答的问题以及 0-1-2 锚点描述。
5. CI 步骤，每当构建者任务关闭时将审查报告作为 PR 评论发布。

硬性拒绝：

- 对 diff 有写访问权限的审查者。构建者和审查者之间的差距是全部信号；折叠它会破坏可靠性。
- 每个分数没有锚点描述的评分标准。「从 0 到 2 打分」没有锚点会沦为凭感觉。
- 省略引用的审查报告。每个分数必须指向一个文件或追踪条目。
- 共享构建者的系统提示。相同模型可以；相同提示不行。

拒绝规则：

- 如果构建者没有生成验证报告，拒绝运行审查者。在接受之前必须先通过验收，才值得要求判断。
- 如果项目少于三个已关闭任务，拒绝声明评分标准已校准。将首批报告保存为校准集。
- 如果要求审查者在低于最低置信度的情况下评分，拒绝并将不确定维度提交给人类。

输出结构：

```
<repo>/
├── agents/reviewer.md
├── tools/reviewer.py
├── outputs/review/
│   └── <task_id>.json
├── docs/reviewer-rubric.md
└── .github/workflows/review.yml
```

结尾的「下一步阅读」指向：

- 第 40 课了解结合验证 + 审查的交接数据包。
- 第 41 课了解端到端锻炼构建者/审查者分离的真实风格任务。
- 第 05 课（Self-Refine 和 CRITIC）了解本课所改进的单智能体自审基线。