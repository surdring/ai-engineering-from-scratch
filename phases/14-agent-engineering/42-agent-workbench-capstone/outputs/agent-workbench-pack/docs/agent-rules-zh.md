# 智能体规则

## startup/state-file-fresh（启动/状态文件新鲜）
- category: startup
- check: state_file_fresh
智能体必须在任何工具调用之前读取 agent_state.json。

## forbidden/no-out-of-scope-writes（禁止/无越界写入）
- category: forbidden
- check: no_out_of_scope_writes
绝不在活动任务的范围合约之外编辑文件。

## done/tests-pass（完成/测试通过）
- category: definition_of_done
- check: tests_pass
只有当每个验收命令返回零退出码时，任务才算完成。

## uncertainty/open-question-note（不确定性/提出问题笔记）
- category: uncertainty
- check: opened_question_when_unsure
当置信度低于阈值时，提出一个问题笔记，而非猜测。

## approval/new-dependency（审批/新依赖）
- category: approval
- check: new_dependency_approved
添加运行时依赖需要明确的人工审批。