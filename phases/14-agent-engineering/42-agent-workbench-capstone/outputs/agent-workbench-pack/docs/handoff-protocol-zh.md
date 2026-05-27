# 交接协议

每次会话结束时产生一个交接数据包，包含：

- summary（摘要）
- changed_files（变更文件）
- commands_run（运行的命令）
- failed_attempts（失败尝试）
- open_risks（开放风险，含严重级别 + 详情）
- next_action（下一步动作，一个具体步骤）
- verdict_pointer（验证 + 审查报告的路径）

数据包同时以 handoff.md（面向人类）和 handoff.json（面向下一个智能体）发布。
缺失字段会阻止会话结束钩子。