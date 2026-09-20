# 来源与适配记录

迁入来源：`joeseesun/qiaomu-download` v1.2.0，提交 `399602fd67b95abe0f64c37c1bde4f1b5792a637`（2026-09-19）。相关源文件：`scripts/download.py`、`scripts/wechat_adapter.py`、`scripts/wechat/*` 和对应 tests。保留其 MIT 版权与许可于 `licenses/qiaomu-download-MIT.txt`。

可选视频号后端：`ltaoo/wx_channels_download` v260714，具有独立的 MIT + Commons Clause 许可。仓库不内嵌其二进制；安装器按固定版本和哈希获取，不能将本 skill 的 MIT 来源说明当成后端授权。

本地保留原有 `recipes.md`、`advanced.md`、`troubleshooting.md`。适配包括 Windows 文件锁、隐藏进程与进程树清理、UTF-8/中文路径、Windows 浏览器发现、默认 outputs、Cookie 显式启用、按需只读版本检查、画质硬上限、列表/直播范围拦截、产物路径核验、视频号防覆盖和私密信息控制。未迁入作者宣传资产、发布流程和自动更新前置条件。

验证命令（从当前任务目录运行，保持输出在 work）：

```powershell
$skill = Join-Path $env:USERPROFILE '.codex/skills/lsf-yt-dlp'
python -X utf8 -B -m unittest discover -s "$skill/tests" -p 'test_*.py'
python -X utf8 -B "$skill/scripts/download.py" doctor
```

测试包含本地生成媒体经真实 yt-dlp/FFmpeg 下载与验证、重复下载、画质上限、Windows 锁与超时子进程清理，以及视频号离线响应/传输/配置边界。真实微信账号、后端捕获、在线解析可用性不由离线测试证明。
