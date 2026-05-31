# WSL + uv Python 依赖管理指南

本指南专为 **WSL + uv** 工具链定制。WSL 系统镜像常缺失标准库，uv 具备独立于系统 Python 的包管理能力，以 uv 为第一优先级，可彻底规避传统 venv/pip 在 WSL 下的各类陷阱。

---

## 目录

- [快速安装 uv](#快速安装-uv)
- [环境初始化（仅一次）](#环境初始化仅一次)
- [核心原则：uv 优先，拒绝混用](#核心原则uv-优先拒绝混用)
- [日常依赖管理](#日常依赖管理)
- [锁定与复现](#锁定与复现)
- [故障排查速查表](#故障排查速查表)
- [关键认知纠偏](#关键认知纠偏)

---

## 快速安装 uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安装后重新打开终端，或执行：

```bash
source $HOME/.cargo/env
```

验证安装：

```bash
uv --version
```

---

## 环境初始化（仅一次）

WSL 的 Ubuntu/Debian 镜像默认精简，编译 C 扩展包（如 numpy、scipy）可能失败。首次使用前安装构建工具链：

```bash
sudo apt update && sudo apt install -y build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev curl git
```

> 这些是系统级编译依赖，不是 Python 包，不会污染虚拟环境。

创建项目虚拟环境：

```bash
uv venv
```

---

## 核心原则：uv 优先，拒绝混用

| 操作 | ✅ 推荐 (uv) | ❌ 避免 | 原因 |
|------|-------------|--------|------|
| 创建虚拟环境 | `uv venv` | `python -m venv` | uv 自带 Python 版本管理，不依赖系统 Python |
| 安装依赖 | `uv pip install` | `pip install` | 绕过 ensurepip 缺失问题，速度快 10-100 倍 |
| 运行脚本 | `uv run script.py` | `python script.py` | 自动激活环境并校验依赖完整性 |
| 导出依赖 | `uv pip freeze` | `pip freeze` | 确保与实际安装状态一致 |

> ⚠️ **铁律**：项目由 uv 初始化后，永远不要使用 `apt install python3-*` 或 `python -m pip` 安装业务依赖。系统级修复仅用于让 uv 本身正常运行。

---

## 日常依赖管理

### 安装包

激活环境后使用 uv pip：

```bash
source .venv/bin/activate
uv pip install pandas scikit-learn matplotlib
```

或不激活环境，直接指定解释器路径：

```bash
uv pip install --python .venv/bin/python pandas
```

### 处理运行时依赖报错

遇到类似 `fetch_openml requires pandas` 的 ImportError 时，直接补装即可：

```bash
uv pip install pandas
```

> 对于 AI 工程项目，pandas 几乎是必装项，建议直接安装。仅在确认不需要 DataFrame 功能时才考虑修改代码适配。

---

## 锁定与复现

```bash
# 导出精确依赖
uv pip freeze > requirements.txt

# 在新环境 / CI 中复现
uv pip install -r requirements.txt
```

> 建议将 `requirements.txt` 纳入版本控制，确保团队环境一致。

---

## 故障排查速查表

| 错误信息 | 根因 | 解决方案 |
|---------|------|---------|
| `No module named ensurepip` | WSL 阉割了标准库 | **忽略**，直接用 `uv pip install` |
| `No module named pip` | 虚拟环境内无 pip | `uv pip install pip`（仅当确实需要 pip 命令时） |
| `externally-managed-environment` | 误用了系统 Python | 确认已 `source .venv/bin/activate` 或改用 `uv run` |
| 编译报错 `gcc error` | 缺少系统构建工具 | `sudo apt install build-essential` |
| 下载超时 | PyPI 网络问题 | `uv pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple` |
| 环境彻底损坏 | 混用工具导致不一致 | `rm -rf .venv && uv venv && uv pip install -r requirements.txt` |

---

## 关键认知纠偏

1. **`ensurepip` 缺失不是问题。**  
   传统 venv 工作流中这是致命错误，但在 uv 下完全无关。uv 有自己的包安装引擎，不依赖环境内的 pip 或 ensurepip。**不要再浪费时间 `apt install python3-venv` 来修复它。**

2. **`sudo` 只用于 `apt`。**  
   任何 `uv pip install` 都不应加 `sudo`。加 `sudo` 会切换到 root 用户，脱离虚拟环境上下文，导致包安装到错误位置。

3. **重建优于修复。**  
   虚拟环境是廉价的、可丢弃的。遇到诡异问题，`rm -rf .venv` 重建永远比排查更快、更可靠。

4. **WSL ≠ Windows。**  
   不要在 Windows PowerShell 中对 WSL 路径下的 `.venv` 执行任何操作。二进制格式不兼容，会导致环境永久损坏。

---

将此指南作为项目的依赖管理基准，所有安装操作统一走 uv 路径，即可彻底告别 WSL 下的 Python 环境噩梦。