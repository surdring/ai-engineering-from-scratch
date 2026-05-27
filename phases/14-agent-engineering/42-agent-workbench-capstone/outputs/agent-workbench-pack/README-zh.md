# 智能体工作台包

适用于任何需要可靠智能体工作的仓库的即插即用工作台。

## 你获得的内容

- `AGENTS.md` 指向包其余部分的简短路由器。
- `docs/` 规则、可靠性策略、交接协议、审查评分标准。
- `schemas/` 状态、看板和范围合约的 JSON Schema。
- `scripts/` 初始化、反馈运行器、验证门控、交接生成器。
- `bin/install.sh` 幂等安装器。

## 快速开始

```
bin/install.sh
$EDITOR task_board.json
python3 scripts/init_agent.py
```

## 版本管理

`VERSION` 文件是合约。主版本升级需要状态迁移。