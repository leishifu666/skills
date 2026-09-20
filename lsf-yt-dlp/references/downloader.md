# Windows 下载脚本

使用 Python 3.10+ 和已有的 yt-dlp、ffmpeg、ffprobe；路径包含中文或空格时保留 PowerShell 引号。脚本没有额外 pip 依赖。以当前任务为工作目录，不能 cd 到 skill 后让输出落进 skill。

```powershell
$skill = Join-Path $env:USERPROFILE '.codex/skills/lsf-yt-dlp'
$script = Join-Path $skill 'scripts/download.py'
python -X utf8 $script doctor
python -X utf8 $script info 'HTTPS链接'
python -X utf8 $script download 'HTTPS链接' --quality 1080p --dir ./outputs
python -X utf8 $script audio 'HTTPS链接' --dir ./outputs
python -X utf8 $script subtitles 'HTTPS链接' --langs 'zh-Hans,en' --dir ./outputs
```

`doctor` 只检查本地依赖和视频号组件。`doctor --check-updates` 才查询 yt-dlp 官方版本，不安装或升级；更新按排错文档确认安装来源。GitHub 不可达只记录 `update_error`。

`--quality best|1080p|720p|480p` 的数字是**视频高度硬上限**，不够格式或提取器没有尺寸信息时失败；竖屏也按高度判断。不能为绕过失败擅自改成 best。视频号尚不提供画质上限，传非 best 会明确拒绝。合并 MP4 不保证 H.264/AAC，返回真实编码。

默认输出为当前目录 `outputs/`；`--dir` 优先于 `LSF_DOWNLOAD_OUTPUT`。普通媒体临时目录位于 `work/yt-dlp/`，正常退出或可捕获的失败后清理本次临时目录；强制杀死整个解释器可能留下临时文件。输出文件名保留 ID 和画质/音频标记，禁止覆盖。任务锁放用户本地数据目录，跨工作目录生效；空锁文件会保留，操作系统在进程退出时释放锁，不要按“锁文件存在”判断任务仍运行。

Cookie 默认 `none`。确认当前用户授权后才使用：

```powershell
python -X utf8 $script download 'HTTPS链接' --cookies-from-browser edge
python -X utf8 $script download 'HTTPS链接' --cookies-from-browser 'chrome:Profile 1'
python -X utf8 $script download 'HTTPS链接' --cookies-from-browser auto
```

显式浏览器直接使用指定会话；`auto` 表示允许在匿名提取失败后尝试一次已安装浏览器，Windows 按 Edge、Chrome、Firefox 配置目录发现，不扫描或导出 Cookie。锁定/加密错误交给用户处理，不关闭浏览器、不降级保护。

stdout 是最终 JSON，stderr 是脱敏后的进度；Windows 使用隐藏进程、UTF-8 和 Job Object，在超时/中断时终止本次子进程树。不能建立进程隔离时失败并报告，不改用不受控后台运行。

成功结果含 `files` 的绝对路径、大小、编码、时长，以及 `created`；`status=existing` 表示复用了已有文件。脚本验证视频中应有的音轨与画质上限；字幕在独立临时目录获取，检查非空和时间戳，避免把旧字幕误报为新结果。错误的 `stage` 标明 scope、metadata、download、verify、lock 等阶段。

脚本不加载用户 yt-dlp 配置。用户明确要求使用既有配置、下载列表、直播、章节、封面、原音频编码等时走原配方，不把有限脚本参数当作 yt-dlp 的能力上限。
