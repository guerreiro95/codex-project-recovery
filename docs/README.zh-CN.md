# Codex Project Recovery

[English](README.en.md) · [Português](README.pt.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md)

当 **Windows 版 Codex Desktop** 的侧边栏项目消失，但对话仍能在“最近”列表中找到时，此工具可尝试恢复本地项目组织。

这是独立、非官方的社区工具。需要 Python 3.10 或更高版本，仅使用标准库。工具代码不连接网络，不包含服务器、API 或遥测。

> **先预览，再恢复。** 应用恢复会修改 Codex 的内部状态文件。请先保存备份，完全关闭应用，再显式使用 `--apply`。无法保证所有情况都能恢复，也无法绝对防止再次损坏。

## 功能和范围

工具从现有 SQLite 项目记录重建本地项目列表，保留已知历史标识符、当前偏好设置以及明确未分配项目的对话。在修改前，它保存状态文件并创建一致的 SQLite 备份。**不会直接修改原始 SQLite 数据库。**

历史备份独立于应用自身的即时 `.bak`。空列表或无效状态不会替换上次有效备份的引用。工具不能恢复已删除的源代码、已丢失的会话转录、远程或云端项目，以及其他电脑的数据。

本项目源于一次真实恢复：JSON 损坏与异常关机同时出现。这并不意味着所有项目消失问题都有同样原因。参见[技术说明](HOW_IT_WORKS.md)。

## 环境要求

- 仅支持在 Windows 10/11 上应用恢复，使用 Python 3.10+。
- 可使用 PowerShell、命令提示符或 **Windows 上的 Git Bash**。
- 需要兼容的 `state_5.sqlite`，包含 `projects`、`project_roots` 和 `threads` 表。
- 本版本不支持在 macOS、Linux 或 WSL 上应用恢复，也不支持远程/云项目。

Codex 的内部数据库结构可能变化。不兼容的结构会使工具停止操作。使用虚构数据通过测试，不等于已验证所有应用版本。

## 无需 Git：下载并预览

1. 在本仓库 GitHub 页面点击 **Code → Download ZIP**。
2. 完整解压 ZIP。不要直接在压缩包中运行文件。
3. 如未安装 Python，请从[官方网站](https://www.python.org/downloads/windows/)安装 Python 3.10+。
4. 在文件资源管理器中打开解压后的目录，在地址栏输入 `powershell`，按 Enter。
5. 先执行预览：

```powershell
py -3 .\codex_recovery.py plan --lang zh
```

如果没有 `py`，可将 `py -3` 替换为 `python`，但请确认版本至少为 3.10。双击 `codex-recovery.cmd` 也会显示预览并保留窗口。未指定 `--lang` 时默认使用英语。

## 应用恢复

1. 检查预览中的 `projects`、`recoveredAssignments` 和 `ambiguousAssignments`。多个项目指向同一目录时，不会自动猜测其归属。
2. 保存工作，完全关闭 Codex/ChatGPT（包括系统托盘中的程序），并关闭 Codex CLI 会话。
3. 在应用之外的 **Windows 外部终端**中，从解压目录执行：

```powershell
py -3 .\codex_recovery.py repair --apply --lang zh
```

4. 等待成功提示，然后重新打开 Codex，检查项目和对话。

如果出错，请保留输出中指定的备份，不要反复盲目应用修复。仍在运行的 `codex.exe` 会阻止恢复；请正常关闭会话，不要强行终止尚未保存的工作。`result.json` 只确认文件已写入，仍需在重新打开应用后检查迁移结果。

### Windows Git Bash

```bash
python ./codex_recovery.py plan --lang zh
# 保存工作并关闭桌面应用及 Codex CLI 后：
python ./codex_recovery.py repair --apply --lang zh
```

必要时改用 `py -3`。这些示例仅适用于 **Windows Git Bash**，不适用于 Linux/WSL。不要使用 `curl | bash`、未经检查的远程执行，或关闭安全保护的命令。

## 交给您的 AI/Codex

复制[中文提示词](AI_PROMPTS.md#简体中文)。先要求 AI 审查代码，再仅执行预览。如果代理在 Codex 应用内或沙盒内，应提供外部终端使用的恢复命令，不得绕过保护。

不要为了方便诊断，把凭据、真实数据库、会话转录或备份上传给远程 AI 服务。恢复可完全在本地完成。

## 备份与预防

```powershell
py -3 .\codex_recovery.py preserve --lang zh
py -3 .\codex_recovery.py backup --lang zh
py -3 .\codex_recovery.py watch --lang zh
```

`preserve` 保存当前故障材料，即使 JSON 已损坏。`backup` 为有效项目列表创建快照。`watch` 持续运行，直到按 Ctrl+C 或关闭终端。

默认备份位置是 Windows 用户目录下的 `Documents\CodexProjectRecoveryBackups`。可通过 `--backup-dir` 更改；不要选择 `.codex`、本公开仓库或共享目录。`--codex-home` 可指定 Codex 数据目录；默认使用 `CODEX_HOME` 或 `~/.codex`。

观察程序每 30 秒检查状态，每 15 分钟在受保护的项目状态变化时尝试创建新版本。错误或项目数量下降会写入 `ATTENTION.json`。工具不会显示 Windows 通知、自动恢复或自动删除历史备份。请检查磁盘空间，并在独立设备上保存另一份受保护的副本。

**公开版本不会自动安装登录启动项。** 如需登录后运行，可创建指向 `python.exe` 的快捷方式，参数为脚本完整路径和 `watch --lang zh`，然后放入 **Win+R → `shell:startup`** 打开的文件夹。请保持脚本位置不变，并且仅运行一个观察程序。备份依赖观察程序运行；潜在数据丢失窗口最长为 15 分钟。

如果要恢复指定快照，请先关闭所有写入程序并保存当前状态，再用该快照中经过验证的 `global-state.json` 手动替换主 JSON 和 `.bak`。**不要用旧数据库整体覆盖包含新对话的数据库。** 本版本没有自动快照恢复命令；如有疑问，请使用脱敏信息寻求帮助。

## 语言、隐私与贡献

仓库主页默认显示英文，并在同一 README 中提供可展开的完整翻译。命令行支持 `--lang pt|en|zh|es`；JSON 字段名和部分底层错误保持英文。简体中文使用 `zh`/`zh-CN`，而不是 `CH`。

公开源代码不会授予他人访问您电脑或私人仓库的权限。每位用户只在自己的机器上操作自己的数据。生成的备份可能含有私密项目名、路径、元数据和对话索引。虽然不会复制 `auth.json` 或会话转录，其他备份内容仍然需要保密。

请勿公开 `.codex`、数据库、备份、未脱敏日志或私人截图。`.gitignore` 能减少误提交，**但不能阻止浏览器手动上传，也不能删除已公开的历史记录**。参见[安全说明](../SECURITY.md)。

测试命令：`python -m unittest discover -s tests -v`。GitHub CI 在 Windows 和 Linux 上运行虚构数据测试；这不意味着支持 Linux 恢复。欢迎[参与贡献](../CONTRIBUTING.md)。采用 [MIT 许可证](../LICENSE)。本项目与 OpenAI 无隶属关系，也不提供官方支持。
