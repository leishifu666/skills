---
name: lsf-oil-codex-title
description: 管理 oil-codex-title 插件的话题自动命名和可选闲置归档；检查插件状态、预览或修改话题标题、暂停恢复、保护标题及配置归档。当用户要管理 Codex 话题或此插件时启用；不用于文章标题、视频标题或文件改名。
github_url: https://github.com/oil-oil/oil-codex-title
github_hash: ae1c9e27061dfdb84dd1ce918ee3e341b58a0d3f
version: 0.1.0+codex.20260918031305
created_at: 2026-09-28
entry_point: SKILL.md
dependencies: ["Python 3.10+", "Codex 本地插件"]
metadata:
  compatibility: 仅用于本地 Codex 插件；云端不支持后台入口。
---

# LSF Codex 话题命名管理

本技能管理后台命名流程。自动命名由独立 Stop Hook 执行；主对话只处理用户明确提出的设置与操作。

## 插件前置条件

目前安装的是管理技能，不等于完整插件已安装或 Hook 已获信任。单独安装技能目录不包含后台程序，因此不能据此声称自动命名已生效。执行任何插件命令前，先确认完整插件存在且信任状态明确。完整插件安装和 Hook 信任只能通过 Codex 官方插件入口完成；不要修改信任数据库或使用绕过参数。

插件脚本与文档在仓库中： https://github.com/oil-oil/oil-codex-title 。本技能里的 scripts/run.py 和 scripts/archive.py 只有在配套插件文件可定位时才能运行。

## 检查与配置

Windows 示例使用 py -3（需安装 Python Launcher）；其他系统可使用 python3。

1. 运行入口的 doctor 命令，检查 Python、Codex 路径和 App Server。若用户提供话题 ID，可用 --thread <话题 ID> 检查读取兼容性。
2. 用户明确要配置时，再运行 configure --model <模型 ID> --service-tier fast 或 --service-tier standard。模型和档位应来自用户选择或当前可用列表，不猜模型名。默认 Luna Fast，Spark 使用 standard。
3. 修正 Codex 程序位置时使用 configure --codex-bin <路径>。
4. Hook 安装、启用、信任和实际成功触发是不同状态；doctor 成功不能证明 Hook 已运行。

## 预览与改名

1. 运行 rename <话题 ID> 生成预览。
2. 用户明确要求改名时，可直接使用同一命令并追加 --apply。
3. 只有返回 renamed 并读回核验，才报告标题已写入；kept 或 unchanged 表示保留。候选结果不代表已生效，也不能证明桌面缓存已刷新。
4. locked 或 manual_title 表示标题受保护。只有用户要求覆盖保护时才运行 unlock 后重试。
5. stale_result 或 outdated_event 表示对话已更新，本次候选作废。ambiguous_title 表示标题仍与已有任务重复；补充对象信息后再试。
6. 置顶列表显示旧标题时，先读取真实标题；仅在用户请求修复后，使用宿主 set_thread_title 同步并核对。不要修改桌面私有状态文件。

## 暂停、保护与用量

- pause：暂停自动命名；写入前会再次确认暂停状态。
- resume：恢复后续轮次的自动命名。
- lock <话题 ID>：固定当前标题。
- unlock <话题 ID>：恢复自动命名。
- status：显示配置位置、启用状态和记录的话题数量。
- usage：汇总可用的逐次模型用量与保留日志中的确认跳过次数；不含管理 Agent、历史日志或未记账评测。不要重复计算缓存输入和推理输出。

首次接触话题时，插件不能判断标题是否由用户手动设置。需长期保留的旧标题应先 lock。

## 可选闲置归档

归档不由 Stop Hook 触发。只有用户要求归档或设置定期整理时才处理。归档默认关闭，首次先展示预览；用户认可规则和预览后再启用。不要重复询问已给出的授权。

插件程序负责筛选、缓存和复核；实际归档由宿主 set_thread_archived 执行。没有宿主工具时只返回预览。不得恢复已归档话题、发送消息或继续其中未完成工作。归档定时流程不能接着执行本管理话题的其他任务。

已归档话题不读取内容、不调用模型；同一内容版本的保留、不确定和失败结果不重复评估。release 会清除保护与评估缓存，只在用户明确要求重新评估时执行，不在定时流程中自动执行。

## 失败处理

命令失败时保留原标题，先处理 doctor 报告的兼容或登录问题，再重试。不要恢复原话题发送改名指令，不直接修改数据库或对话文件，也不要让主 Agent 接管后台自动命名循环。

后台日志只记录状态、标题和用量，不保存完整对话。诊断时只读取 status 返回目录中与相关话题对应的记录。
