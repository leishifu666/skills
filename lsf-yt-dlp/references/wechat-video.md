# 微信视频号与 Windows 后端

内置 qiaomu-download v1.2.0 的视频号适配，覆盖本地 API 取媒体、下载、按需解密、真实编码与完整解码验证；可选固定在线解析。支持 `https://weixin.qq.com/sph/<token>` 分享链接。普通微信文章/图片不是此入口。

## 使用

```powershell
$skill = Join-Path $env:USERPROFILE '.codex/skills/lsf-yt-dlp'
python -X utf8 "$skill/scripts/download.py" download '视频号分享链接' --dir ./outputs
```

先只读检查本机 `127.0.0.1:2022`，再尝试已配置且已连接的后端。默认尝试不同编码候选；只要一份加 `--single-version`。候选编码来自 ffprobe，不能凭清晰度名称猜编码或宣称原画。画质硬上限暂不支持，不能静默忽略用户的上限要求。

- `manual_action_required`：只让用户手动在电脑微信重新打开目标视频并播放，不需要点击下载；完成后同一命令加 `--wait-page 90` 继续。
- `wechat_setup_required`：没有本地 API，按下节配置。
- `local_configuration`：检查登记的 backend/config/ffmpeg 文件路径。
- `local_download` / `online_resolver`：此次未得到通过校验的文件；报告失败，不循环请求。

脚本不自动操作微信，不启动已有后端、不安装证书、不改变系统代理。签名媒体地址、解密 key 只在本次进程内处理，不写入报告或元数据文件。解密器需要通过命令参数接收 key，限当前本机任务使用；不得采集并公开原始命令行。

## Windows 本地后端

锁定上游 `ltaoo/wx_channels_download` 的 `v260714`，Windows x86_64/arm64 包名和 SHA-256 在 `scripts/wechat/release-lock.json`。安装器支持 Windows 平台检测、防路径越界和文件校验；只下载并解压，**不会启动 EXE**。

上游该版本为 MIT + Commons Clause，安装前读其 [LICENSE](https://github.com/ltaoo/wx_channels_download/blob/v260714/LICENSE)。只有用户授权安装且审阅对应许可后执行：

```powershell
python -X utf8 "$skill/scripts/wechat/install_backend.py" --accept-upstream-license
```

默认数据目录为 `%LOCALAPPDATA%\lsf-yt-dlp\wechat`，可用 `LSF_WX_VIDEO_HOME` 指定。复用旧部署可显式设置 `QIAOMU_WX_VIDEO_HOME`。安装结果返回 `install_dir`；在该目录查找实际 EXE 与配置，不假定解压后只有一层。缓存复用时复核记录的文件哈希，不覆盖未知/不完整安装。

登记已经存在的文件，路径替换成实际值：

```powershell
python -X utf8 "$skill/scripts/wechat_adapter.py" configure `
  --backend 'D:\实际后端目录\wx_video_download.exe' `
  --config 'D:\实际后端目录\config.yaml' `
  --ffmpeg 'D:\实际FFmpeg目录\ffmpeg.exe'
```

此命令只写本地 `local-settings.json` 中的路径，不覆盖不同的已有配置，也不会启动后端。配置目录/证书私钥保存在当前用户受保护目录；Windows 使用 NTFS ACL，不能用 `chmod 0600` 的成功返回证明保密。接入时检查实际 ACL，不把凭据保存在共享目录或 skill 目录。

**首次运行上游 EXE 可能安装证书并修改代理。** 已核对上游 Windows 说明与配置：`proxy.system`、`proxy.skipInstallRootCert`、`proxy.upstreamProxy` 会影响系统接入；下载/解压授权不等于证书信任或代理修改授权。需要这些操作时：

1. 核对该版本配置和 `--help`，分别说明证书信任及代理修改的影响，沿用已有授权，否则先取得对应授权。
2. 使用本机独立 CA，不能信任带公开私钥的共享证书。不得照搬 macOS 的 `security`/`networksetup` 命令。
3. Windows 先保存当前用户 Internet Settings 中 `ProxyEnable`、`ProxyServer`、`ProxyOverride`、`AutoConfigURL` 等相关值的**存在性、类型和值**，区分 WinINET 与 WinHTTP；保留用户原有代理/PAC。用专用受保护的任务状态目录保存快照。
4. 若由任务启动后端，使用隐藏进程并记录 PID、可执行路径；在成功、失败和中断后恢复本次实际改动的代理，再停止属于本次的后端。若设置已被用户/其他程序改动，不能盲目覆盖。验证原代理状态与联网，不自动删除证书或用户配置。

这套 skill 提供现有后端接入及安装器，**没有封装自动证书/代理冷启动**。需要首次系统接入时按上述边界执行，不能报告已自动配置。

## 可选在线解析

固定解析器为 `sph.litao.workers.dev` 和 `wx-dl.qiaomu.ai`。用户明确授权将本次分享 URL 发给这两个服务后，才执行：

```powershell
python -X utf8 "$skill/scripts/download.py" download '视频号分享链接' --wechat-online allowed
```

只发送分享 URL，不发送 Cookie/登录态/本地文件。直接调用在线组件也要求 `--allow-share-url`，默认不能隐式联网解析。按固定顺序每个解析器最多一次，拒绝解析器重定向和跨允许域的媒体重定向。媒体要求完整传输、ffprobe 与完整解码通过，发布时原子防覆盖。

Windows 本地回归验证不等于真实微信下载成功。只有用户提供真实链接、可用后端与所需接入条件后，才可报告端到端视频号验证结果。
