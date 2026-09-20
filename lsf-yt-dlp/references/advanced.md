# 高级任务

按需读：批量筛选、片段章节、直播、网络调度、SponsorBlock、程序集成。

## 批量、筛选与去重

目录预览，不取每条完整信息：

```powershell
yt-dlp --ignore-config --flat-playlist --playlist-items '1:20' -J -- '列表链接'
```

条数只是示例，以用户范围为准。flat 模式字段可能缺失。

```powershell
yt-dlp --ignore-config --playlist-items '1:10' --download-archive 'work/yt-dlp-archive.txt' --no-overwrites -P outputs -P 'temp:work/yt-dlp' -o '%(playlist_title).100B/%(playlist_index)03d - %(title).140B [%(id)s].%(ext)s' --print 'after_move:filepath' -- '列表链接'
```

- URL 文件：`--batch-file 'work/urls.txt'`，一行一条。单视频清单可加 `--no-playlist`，仍要检查纯列表 URL。
- 日期范围：`--dateafter 20260101 --datebefore 20260131`；依据提取器上传日期，缺失不能猜。
- 非直播且小于 20 分钟：`--match-filters '!is_live & duration < 1200'`。表达式内 `&` 是 AND；重复多个 `--match-filters` 是 OR。
- `--max-downloads N` 是本次完成数限制；触发上限可能非零退出，结合日志区分预期终止与失败。
- `--download-archive` 记录媒体标识，不是内容哈希，不保证旧文件仍在。音频/视频/不同画质使用不同记录，防止所需产物被误跳过。
- 不默认加 `--force-write-archive`，模拟/仅取字幕不应误记媒体下载完成。持续增量时把记录放用户指定持久位置。
- 只有明确列表按新到旧且无缺口才用 `--break-on-existing`，否则旧条目后仍可能有新条目。
- 批量可继续后续条目，但不使用 `--ignore-errors` 掩盖后处理失败。交付实际成功与失败清单。

## 片段与章节

```powershell
yt-dlp --ignore-config --no-playlist --no-overwrites -P outputs -o '%(title).140B [%(id)s] %(section_start)s-%(section_end)s.%(ext)s' --download-sections '*00:01:20-00:02:10' -- '视频链接'
```

需要 FFmpeg；不保证所有协议只传输所选区间。关键帧可能造成边界误差，严格切点可加 `--force-keyframes-at-cuts`，会重编码。检查时长，严格要求时还查首尾画面。

有章节信息时：`--split-chapters` 拆分，`--download-sections '章节名称正则'` 选择，`--remove-chapters '章节名称正则'` 删除。拆分输出用 `-o 'chapter:%(title).120B [%(id)s] - %(section_number)03d %(section_title).80B.%(ext)s'`。先读章节，不把无章节视频当作已自动识别。

## 直播

可从当前时刻录制；`--live-from-start` 是部分站点的实验功能，核对当前范围，不保证补回全部历史。`--wait-for-video` 仅在用户要求等待开播时用。

直播和等待需要结束条件，沿用用户给定时长/限制；缺失且会成为无界任务时询问。yt-dlp 不是调度器；定时检查和长期后台任务用环境自动化能力，不偷偷创建常驻进程。

## 网络与速度

- `--limit-rate 2M` 控制字节下载速率；`--concurrent-fragments 2` 仅是分片并发，不是批量视频并发。
- `--sleep-requests`、`--sleep-interval` / `--max-sleep-interval`、`--sleep-subtitles` 控制不同阶段；批量可查本机 `-t sleep` 预设按需使用。
- `--retries`、`--fragment-retries`、`--extractor-retries` 设置有限重试，不默认 infinite。
- `--proxy` 使用用户指定或已有授权代理，不猜端口，不在报告中展示代理密码。

## SponsorBlock 与插件

要标记片段用 `--sponsorblock-mark`，要删除用 `--sponsorblock-remove`，查当前类别。它会查询外部 SponsorBlock 服务，社区数据不保证准确，默认不删除内容。

站点/后处理插件仅在任务实际依赖时引入；先核对来源和官方插件文档，插件可以运行代码，普通下载无需安装插件。

## 程序集成

CLI 用参数数组，例如 `subprocess.run([...], shell=False)`。读取 `-J`、`--print`、`--progress-template`，不解析普通进度日志。

Python 环境已有包时：

```python
import yt_dlp
with yt_dlp.YoutubeDL({'noplaylist': True}) as ydl:
    info = ydl.extract_info(url, download=False)
    data = ydl.sanitize_info(info)
```

返回值不可直接假定 JSON 可序列化，使用 `sanitize_info`。CLI 可用不等于当前 Python 可 import。新 API 参数查 `YoutubeDL` 或官方 `devscripts/cli_to_api.py`，不机械改写 CLI 开关成字典键。

官方：[嵌入](https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp)、[FAQ](https://github.com/yt-dlp/yt-dlp/wiki/FAQ)。
