# 环境与排错

## 发现与依赖

Windows 用 `Get-Command yt-dlp,ffmpeg,ffprobe,node,deno -ErrorAction SilentlyContinue`；其他系统用等效命令。按需检查版本，不硬编码个人路径。

FFmpeg/ffprobe 用于合并、音频提取、字幕转换和切片；不在 PATH 时可指定 `--ffmpeg-location`。需要可执行程序，不是同名 Python 包。

YouTube 完整支持需要兼容 JS 运行时与 EJS。已有兼容 Node 可加 `--js-runtimes node`。2026-09-17 官方文档要求 Node >= 22；后续按 [EJS 文档](https://github.com/yt-dlp/yt-dlp/wiki/EJS) 查证。官方独立包通常含 EJS；pip 安装需依赖组。不能仅凭 `.exe` 判断是独立包，pip/uv 启动器也可能是 exe。

## 按症状查证

| 症状 | 调查与处理 |
|---|---|
| 提取器近期失效 | 查当前版本与站点官方说明，确认修复，再按原安装方式更新 |
| JS/challenge 失败 | 核对运行时启用情况、EJS 存在与版本匹配，仅补实际缺项 |
| 403/PO Token 提示 | 查具体客户端与格式，读 [PO Token Guide](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide)，不硬编码旧客户端或 token |
| 登录/私有内容 | 核对权限，用用户已授权的登录态 |
| 429/稍后重试 | 降速、减少并发或等待，持续同因失败停止本轮重试 |
| 无目标格式 | `-F` 对照过滤，不静默放宽硬要求 |
| 视频无声 | ffprobe 看音轨，检查合并日志与 FFmpeg |
| 无字幕文件 | 核对语言和人工/自动字幕，无字幕时交接转写工具 |
| 网络/证书 | 检查域名、既有代理、系统时间和证书链，不默认关闭 TLS 校验 |
| Windows 文件失败 | 查长度、字符、空间与占用；缩短模板，按需 `--windows-filenames` |

可用 `--verbose --simulate` 诊断，原始日志留私有工作目录，分享前移除 Cookie、代理、签名 URL 等敏感信息。不用 `--print-traffic` 收集无关详情。依据证据改条件，持续相同错误时说明缺项而不是循环试参数。

## Cookies

任务需要且已有授权时，用 `--cookies-from-browser edge` / `chrome` / `firefox` 并选正确 profile，或 `--cookies` 读用户提供的 Netscape 文件。浏览器加密/占用可能导致读取失败，不自动关闭浏览器或降低凭据保护。

不把 Cookie 粘到对话、写进 skill、提交或打包；不默认同时使用 `--cookies-from-browser` 与 `--cookies` 导出整个 Cookie 库。已有相关授权不反复索取。[官方说明](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp)

## 安装更新

仅在任务需要且授权涵盖时执行。先区分独立包、pip、uv tool、包管理器，再按原来源操作，不用系统 pip 更新另一隔离环境。

- 官方独立二进制：`yt-dlp -U`。
- pip：用对应 Python 执行 `-m pip install -U 'yt-dlp[default]'`。
- stable 有已知站点故障时，按官方建议考虑 nightly；记录原版本，遵循用户版本策略，不每次自动切通道。
- 新安装来源与校验以 [官方安装文档](https://github.com/yt-dlp/yt-dlp/wiki/Installation) 为准。

明确区分参数解析、离线媒体测试、真实站点提取和真实下载，不用一种验证代替另一种。
