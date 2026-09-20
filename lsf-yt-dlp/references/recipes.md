# 采集配方

PowerShell 示例；替换实际 URL。其他 shell 用对应参数传递方式。

```powershell
$url = '用户提供的链接'
$base = @('--ignore-config', '--no-playlist')
# 需要 JavaScript 且已有兼容 Node 时：
# $base += @('--js-runtimes', 'node')
$save = @('-P', 'outputs', '-P', 'temp:work/yt-dlp', '--no-overwrites', '-o', '%(title).160B [%(id)s].%(ext)s')
```

## 查询

按需选一项，不默认全部运行：

```powershell
yt-dlp @base -J -- $url
yt-dlp @base -F -- $url
yt-dlp @base --list-subs -- $url
yt-dlp @base --list-thumbnails -- $url
yt-dlp @base --print '%(title)s | %(duration)s | %(uploader)s' -- $url
```

JSON 可能有临时媒体 URL，只取所需字段。标题、时长、上传者、上传日期、章节与互动数据可能缺失，不补造数值。

## 视频与格式

最佳可用画质，分离轨道合并需要 FFmpeg：

```powershell
yt-dlp @base @save --print 'after_move:filepath' -- $url
```

最高 1080p 硬上限，支持分离轨道与单文件回退：

```powershell
yt-dlp @base @save -f 'bv*[height<=1080]+ba/b[height<=1080]' --print 'after_move:filepath' -- $url
```

没有合适格式应报告，不能静默突破上限。MP4 容器可核对本机帮助后用 `-t mp4`。若要求 H.264 + AAC，先 `-F` 确认对应轨道，再用格式 ID/编码过滤；没有时说明需转码。

`--merge-output-format mp4` 只影响发生合并时的容器。`--remux-video mp4` 不改编码，可能因不兼容失败。`--recode-video mp4` 也不保证所有原本已是 MP4 的文件转换成指定编码。不要用扩展名证明设备兼容性。

## 音频

取最佳音频，尽量保留源编码：

```powershell
yt-dlp @base @save -f 'ba/b' -x --audio-format best --print 'after_move:filepath' -- $url
```

指定 MP3：

```powershell
yt-dlp @base @save -f 'ba/b' -x --audio-format mp3 --audio-quality 0 --print 'after_move:filepath' -- $url
```

提取/转换需 FFmpeg 与 ffprobe。转 FLAC/WAV 不恢复源文件已损失的音质；为转写取音频时按转写工具要求选择格式。

## 字幕

先列语言，选用户要求的准确代码；中英文范围示例：

```powershell
yt-dlp @base @save --skip-download --write-subs --write-auto-subs --sub-langs 'zh.*,en.*' --convert-subs srt -- $url
```

转换 SRT 需要 FFmpeg；只要原始字幕时去掉转换参数。正则可能匹配很多自动翻译版本，语言列表已知时选具体代码。同语言人工字幕优先；区分人工、自动识别和自动翻译。无字幕可能是正常结果，检查文件而不只看退出码。

同时取视频并嵌字幕：去掉 `--skip-download`，增加 `--embed-subs`，核对容器兼容性。嵌入字幕通常是可切换轨道，不是烧录画面。

## 封面、简介、元数据与评论

```powershell
yt-dlp @base @save --skip-download --write-thumbnail --write-description -- $url
```

需要时添加 `--write-info-json`，内部 JSON 放私有工作目录，公开前筛选字段。封面可用 `--convert-thumbnails jpg` 转换。按用户需要选 `--embed-thumbnail`、`--embed-metadata`、`--embed-chapters`，注意容器支持。

要评论才启用 `--write-comments --write-info-json`；评论数量限制查当前站点 extractor 参数，不承诺全量或虚构通用数量开关。

## 验证

```powershell
ffprobe -v error -show_entries 'format=duration,format_name:stream=codec_type,codec_name,width,height' -of json '实际媒体文件路径'
```

字幕检查正文和时间戳；字段缺失与零值分开处理。配方基于本机 `yt-dlp 2026.07.04 --help` 与[官方参数说明](https://github.com/yt-dlp/yt-dlp#usage-and-options)，后续以当前版本为准。
