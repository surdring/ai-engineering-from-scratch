---
title: "磁盘目录分类最佳实践"
type: 指南
phase: "00-setup-and-tooling"
chapter: "14"
language: "PowerShell"
tags: [实操, 环境工具]
created: 2026-05-27
updated: 2026-05-27
---

# 磁盘目录分类最佳实践

> 让文件各归其位，找东西不再靠回忆。

## 核心理念

### 三条铁律

1. **根目录不超过 7 个文件夹** —— 越多越乱，大脑记不住
2. **嵌套不超过 4 层** —— 太深等于藏起来，不如用搜索
3. **命名用英文，不用空格** —— 命令行、脚本、环境变量通吃

### 为什么需要结构？

| 无结构 | 有结构 |
|---|---|
| 桌面堆满文件 | 文件各归其位 |
| 下载目录几千个文件混在一起 | 下载是临时收件箱，定期清空 |
| 重装系统时不知道哪些要备份 | 数据区独立，系统盘随便重装 |
| `D:\` 下面十几个名字随意的文件夹 | `D:\` 一眼看完所有分类 |

## 黄金目录模板

### 通用型（6 个根文件夹）

适用于大多数用户 —— 办公、学习、日常使用：

```
D:\
├── Apps\           # 有图形界面的软件（微信、PotPlayer、浏览器...）
├── Data\           # 个人资料（文档、照片、音乐、电子书...）
├── Downloads\      # 唯一下载入口（临时存放，定期清理）
├── Gaming\         # 游戏（平台 + 游戏本体 + MOD + 存档）
├── Tools\          # 绿色软件、便携工具、驱动安装包
└── Workspace\      # 工作/学习/代码项目
```

| 文件夹 | 放什么 | 不放什么 |
|---|---|---|
| `Apps` | Chrome、微信、IDEA、VS Code、PotPlayer | JDK、Node.js（这些归 Tools） |
| `Data` | 照片、PDF 文档、音乐、备份的聊天记录 | 软件安装包、临时下载文件 |
| `Downloads` | 浏览器下载、网盘下载的文件（收快递） | 需要长期保留的东西（移走） |
| `Gaming` | Steam、游戏本体、存档、MOD | 游戏攻略截图（归 Data） |
| `Tools` | curl、7z、JDK、Python 安装包、驱动 | 日常打开用的软件（归 Apps） |
| `Workspace` | 代码仓库、论文、项目文档、学习笔记 | 游戏、影音 |

### 开发者型（7 个根文件夹）

针对程序员、数据科学家、AI 工程师 —— 新增 `Env` 隔离开发环境：

```
D:\
├── Apps\           # 有界面的开发工具（VS Code、Cursor、IDEA）
├── Data\           # 个人文档、照片、电子书
├── Downloads\      # 临时下载（浏览器、网盘）
├── Env\            # 运行环境（JDK、Python、Node、CUDA、WSL）
├── Gaming\         # 游戏
├── Tools\          # 命令行工具、绿色软件、驱动包
└── Workspace\      # 所有代码项目、技术文档
```

**核心区别 —— `Env` 与 `Tools` 的分工：**

- **`Env`**：后台运行的、被 PATH 引用的、项目编译依赖的 —— JDK、Python 解释器、Node.js、MinGW、CUDA Toolkit
- **`Tools`**：偶尔手动运行一次的工具 —— 7z、Everything、DiskGenius、驱动安装包、系统激活工具
- **`Apps`**：每天打开、有图形界面的 —— VS Code、微信、PotPlayer、IDEA

### 开发者子目录详解

**`Workspace` 内部结构 —— 按来源/领域分类：**

```
D:\Workspace\
├── company\             # 公司项目（每个子目录一个仓库）
│   └── project-xxx\
│       ├── src\
│       ├── docs\
│       ├── tests\
│       └── README.md
├── github-projects\     # GitHub 个人项目 / 开源项目
│   └── ai-engineering-from-scratch\
├── learning\            # 学习笔记、课程作业
│   ├── deep-learning\
│   └── llm-course\
├── papers\              # 论文 PDF + 阅读笔记
├── sandbox\             # 临时实验代码（可随时删除）
└── archived\            # 已结束的旧项目（只读归档）
```

**`Apps` 内部结构 —— 按用途分组：**

```
D:\Apps\
├── Browsers\        # Chrome、Firefox、Edge
├── Chat\            # 微信、Discord、Slack
├── Dev\             # VS Code、Cursor、IDEA、GitHub Desktop
├── Media\           # PotPlayer、MPC-BE、Music
├── Office\          # WPS、Adobe Reader
└── Utils\           # Snipaste、Everything、Clash
```

**`Env` 内部结构 —— 按运行时分组：**

```
D:\Env\
├── Java\
│   └── jdk-21\
├── Python\
│   └── Python312\
├── Node\
│   └── node-v22\
├── CUDA\
│   └── cuda-12.4\
├── WSL\             # WSL2 虚拟磁盘存放位置
└── Docker\          # Docker 镜像/数据卷
```

## 分区策略

### 单硬盘（512GB-1TB SSD）

```
C: (系统)     150-200GB   # Windows + 核心驱动 + 少量常用软件
D: (数据)     剩余全部    # 所有个人数据（按上面的模板）
```

- **不要** 把单块 SSD 分成 C/D/E/F 四个区 —— 分区太多浪费空间，还容易某个区不够用
- C 盘 150GB 足够：Windows + 浏览器 + 输入法 + 驱动，记得把 `桌面`、`下载`、`文档` 挪到 D 盘

### 双硬盘（SSD + HDD）

```
C: (SSD 系统)    256/512GB  # Windows + Apps + Env（读写频繁的放 SSD）
D: (HDD 数据)    1TB+       # Data + Gaming + Downloads + Workspace 归档
E: (SSD 工作)    512GB      # Workspace（活跃项目）+ WSL（SSD 才够快）
```

- SSD 放 **需要随机读写的**：系统、编辑器、项目代码、WSL 虚拟磁盘
- HDD 放 **顺序读写 / 冷数据**：电影、音乐、照片、游戏

### Windows 11 Dev Drive（Win11 22H2+）

微软为开发者提供的专用卷，基于 ReFS 文件系统，默认关闭 Windows Defender 实时扫描，提升编译/IO 性能：

```powershell
# 设置 → 系统 → 存储 → 高级存储设置 → 磁盘和卷
# 选择 → "创建开发驱动器"
# 推荐大小：50GB+，专门放 WSL 虚拟磁盘 + Docker + 项目代码
```

## 文件命名规范

### 基本原则

```
✅ 用英文、数字、连字符、下划线
✅ 日期用 YYYY-MM-DD（按名称排序自动按时间排）
✅ 序号用前导零（01、02...10，而不是 1、2...10）
✅ 语义清晰看一眼就知道是什么

❌ 不要用中文文件夹名（命令行/PATH/脚本可能出问题）
❌ 不要用空格（命令行要加引号，麻烦）
❌ 不要用特殊字符（\ / : * ? " < > | — Windows 不允许）
❌ 不要用"最终版""新建文件夹"这种无意义命名
```

### 各类文件命名模板

| 类型 | 模板 | 示例 |
|---|---|---|
| 项目文件夹 | `项目名-用途` | `ai-engineering-from-scratch` |
| 文档 | `YYYY-MM-DD-描述-vN` | `2026-05-27-WSL2-guide-v2.docx` |
| 截图 | `YYYY-MM-DD-场景说明` | `2026-05-27-docker-error-screenshot` |
| 配置文件 | `类型-环境-用途` | `docker-compose-dev.yml` |
| 数据文件 | `数据集名-版本-日期` | `imagenet-v1-2026-05-27.csv` |

## 日常维护

### 每月一次

```powershell
# 1. 清空 Downloads（只保留最近 30 天的文件）
Get-ChildItem D:\Downloads -File | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | Remove-Item

# 2. 检查桌面是否堆了文件（桌面应该只有快捷方式）
Get-ChildItem "$env:USERPROFILE\Desktop" -File

# 3. 清理临时文件夹
cleanmgr /sageset:1
cleanmgr /sagerun:1
```

### 每季度一次

```powershell
# 1. 把 Workspace 中超过 3 个月没改动的项目移到 archived
$cutoff = (Get-Date).AddMonths(-3)
Get-ChildItem D:\Workspace -Directory | Where-Object {
    $_.LastWriteTime -lt $cutoff -and $_.Name -ne "archived"
} | Move-Item -Destination D:\Workspace\archived\

# 2. 检查磁盘空间
Get-PSDrive -PSProvider FileSystem | Select-Object Name, Used, Free

# 3. 运行磁盘清理 + 碎片整理（HDD 才需要）
Optimize-Volume -DriveLetter D -ReTrim -Verbose  # SSD
Optimize-Volume -DriveLetter D -Defrag -Verbose   # HDD
```

### 文件夹深度检查清单

```
层级 0: D:\
层级 1: D:\Workspace\
层级 2: D:\Workspace\github-projects\
层级 3: D:\Workspace\github-projects\ai-engineering-from-scratch\
层级 4: D:\Workspace\github-projects\ai-engineering-from-scratch\src\
```

**黄金法则：绝大多数文件停在 3 层以内，最多不超过 4 层。**

如果超过 4 层还觉得文件乱，说明分类方式错了 —— 应该增加根目录分类，而不是继续往深处塞。

## 从零开始：整理现有 D 盘

### 第一步：创建骨架

```powershell
# 创建黄金目录结构
$folders = @(
    "D:\Apps",
    "D:\Data",
    "D:\Downloads",
    "D:\Env",
    "D:\Tools",
    "D:\Gaming",
    "D:\Workspace"
)

foreach ($dir in $folders) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}
```

### 第二步：对照清单转移文件

| 当前目录 | 目标位置 | 说明 |
|---|---|---|
| `Program Files` | 保留 | 已在 D 盘的软件目录，不动 |
| `Program Files (x86)` | 保留 | 同上 |
| `WindowsApps` | 保留 | 系统自动管理，不动 |
| `Users` | 保留 | 用户配置文件，不动 |
| `DeliveryOptimization` | 可删 | Windows 更新缓存，磁盘清理可清除 |
| `BaiduNetdiskDownload` | → `Downloads\BaiduNetdisk` | 归类到下载入口 |
| `steamapps` | → `Gaming\` | 合并入游戏目录 |
| `SteamLibrary` | → `Gaming\SteamLibrary` | 保留原名 |
| `tools` | → `Tools\` | 合并到工具目录 |
| `wsl` | → `Env\WSL` | 开发环境统一管理 |
| `workspace` | → `Workspace\` | 合并到工作区 |
| `zhengxueen` / `下载` / `激活&驱动` | 按内容分类到对应目录 | 拆分后删除 |

### 第三步：迁移 Windows 用户文件夹到 D 盘

```powershell
# 将桌面、下载、文档等用户文件夹迁移到 D 盘
# 右键 "桌面" → 属性 → 位置 → 移动到 D:\Data\Desktop
# 右键 "下载" → 属性 → 位置 → 移动到 D:\Downloads
# 右键 "文档" → 属性 → 位置 → 移动到 D:\Data\Documents
```

这一步很重要 —— 重装系统 C 盘全清，但桌面和文档在 D 盘不会丢。

## 最终效果预览

整理完成后，D 盘根目录应该是这样：

```
D:\
├── Apps\           # 日常软件
│   ├── Browsers\
│   ├── Dev\        # VS Code, Cursor
│   ├── Chat\
│   ├── Media\
│   └── Utils\
├── Data\           # 个人资料
│   ├── Desktop\    # 桌面（已迁移）
│   ├── Documents\  # 文档（已迁移）
│   ├── Photos\
│   └── eBooks\
├── Downloads\      # 临时下载（桌面→D盘迁移后的"下载"）
├── Env\            # 开发环境
│   ├── WSL\        # WSL2 虚拟磁盘
│   ├── Docker\
│   ├── Python\
│   └── CUDA\
├── Gaming\         # 游戏
│   └── SteamLibrary\
├── Tools\          # 绿色工具 + 驱动包
│   ├── 7z\
│   ├── Everything\
│   └── drivers\
└── Workspace\      # 项目代码
    ├── ai-engineering-from-scratch\
    ├── learning\
    ├── sandbox\
    └── archived\
```

**整个根目录只有 7 个文件夹，每个用途清晰，看一眼就知道什么放哪里。**

## 避坑清单

| 不要这样做 | 原因 |
|---|---|
| 根目录直接放文件 | 根目录应该只有文件夹，文件要归入子目录 |
| 桌面堆满文件和文件夹 | 桌面应该只有快捷方式，文件放 Data 或 Downloads |
| 用中文文件夹名 | 命令行 / PATH / WSL 都可能出编码问题 |
| 文件夹嵌套超过 5 层 | 不如用搜索工具 Everything |
| 多个目录下载 | 浏览器下载 + 网盘下载 + 微信文件 —— 全指向 Downloads |
| C 盘塞满个人文件 | 重装系统就丢，C 盘只放系统和驱动 |
| 分类太细 | 超过 7 个根目录 = 没有分类，大脑记不住 |

## 参考

- [Windows 电脑文件夹手动分类指南 — CSDN](https://blog.csdn.net/weixin_56049214/article/details/158266254) — 黄金目录模板来源
- [Windows Dev Drive — Microsoft Learn](https://learn.microsoft.com/de-de/windows/dev-drive/) — 开发驱动器性能优化
- [PARA Method — Tiago Forte](https://fortelabs.com/blog/para/) — 项目/领域/资源/归档四分类法
- [Windows 文件命名最佳实践 — Glarysoft](https://www.glarysoft.com/how-to/configure-file-naming-conventions-and-organization-like-a-pro-windows-systems-guide/) — 命名规范细则