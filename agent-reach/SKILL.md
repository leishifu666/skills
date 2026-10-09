---
name: agent-reach
title: 联网调研
description: 通过 Agent Reach 的平台后端检索社交内容、视频字幕和网页资料；需要这些专用后端时使用。
triggers:
- research: 调研/全网调研/帮我调研/研究一下/research/深入了解
- search: 搜/查/找/search/搜索/查一下/帮我搜/看看大家怎么说
- social:
  - 小红书: xiaohongshu/xhs/小红书/红书
  - Twitter: twitter/推特/x.com/推文
  - B站: bilibili/b站/哔哩哔哩
  - V2EX: v2ex
  - Reddit: reddit
  - Facebook: facebook/fb/facebook groups
  - Instagram: instagram/ig
- career: 招聘/职位/求职/linkedin/领英/找工作
- dev: github/代码/仓库/gh/issue/pr/分支/commit
- web: 网页/链接/文章/rss/读一下/打开这个
- video: youtube/视频/播客/字幕/小宇宙/转录/yt
- finance: 雪球/股票/stock/xueqiu/行情/基金
metadata:
  openclaw:
    homepage: https://github.com/Panniantong/Agent-Reach
github_url: https://github.com/Panniantong/Agent-Reach
github_hash: 94f06c1969dfc1834001269d79d3ad0972d9dee6
---

# Agent Reach — 互联网能力路由器

按目标平台选择已配置的后端；已有专用连接器或直接读取工具能完成任务时，优先使用它们。

## 常驻规则（全程适用）

1. **动手前先体检**：多后端/登录态平台（小红书/Reddit/B站/Twitter/Facebook/Instagram/Boss直聘）先跑
   `agent-reach doctor --json`。`active_backend` 有值时按它选命令组；`active_backend: null`
   表示 Doctor 为避免触发浏览器 Cookie 读取或远端写入而没有做实时验证，不代表后端不存在。
   Doctor 结果是「某一时刻的快照」，通道/登录态可能已变化；执行只读命令前若怀疑失效，
   按对应 reference 的「体检与恢复」runbook 重新确认（如 career.md 的 Boss直聘 CDP 排查）。
2. **声明你在用什么**：开始干活前说一句「使用 agent-reach 的 X 平台 / Y 后端」。
3. **失败按 references 里的重试链处理**，不要瞎猜命令。
4. 多平台调研按问题选择有价值的来源；仅在有独立子任务且允许委派时使用子代理。
5. 仅在用户要求维护或兼容性问题确有需要时检查版本，不把更新检查加入普通调研收尾。

## 路由表

| 用户意图 | 分类 | 详细文档 |
|---------|------|---------|
| 网页搜索/代码搜索 | search | [references/search.md](references/search.md) |
| 小红书/推特/B站/V2EX/Reddit/Facebook/Instagram | social | [references/social.md](references/social.md) |
| 招聘/职位/LinkedIn/Boss直聘 | career | [references/career.md](references/career.md) |
| GitHub/代码 | dev | [references/dev.md](references/dev.md) |
| 网页/文章/RSS | web | [references/web.md](references/web.md) |
| YouTube/B站/播客字幕 | video | [references/video.md](references/video.md) |
| 雪球/股票行情 | finance | [references/finance.md](references/finance.md) |

## 零配置快速命令

```bash
# Exa 网页搜索
mcporter call exa.web_search_exa query="query" numResults=5

# 通用网页阅读
curl -s "https://r.jina.ai/URL"

# GitHub 搜索
gh search repos "query" --sort stars --limit 10

# YouTube 字幕（注意：B站不要用 yt-dlp，失败重试链见 video.md）
yt-dlp --write-sub --write-auto-sub --skip-download -o "/tmp/%(id)s" "URL"

# V2EX 热门
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"

# B站搜索（bili-cli，无需登录）
bili search "query" --type video -n 5
```

## 需登录态的平台（按 doctor 的 active_backend 选命令）

Twitter 注意：`agent-reach configure twitter-cookies` 保存的 Cookie 只供
`doctor` 检查配置是否齐全；`doctor` 不执行 `twitter status`，也不会设置当前
Shell。直接运行 `twitter` 前，必须在子进程环境中显式提供
`TWITTER_AUTH_TOKEN` 和 `TWITTER_CT0`，不得在日志或命令回显中暴露值。

小红书注意：Agent Reach 不替用户登录，也不读取浏览器 Cookie。OpenCLI 只用
用户已有且明确控制的 Chrome 会话；没有现成会话时不要自动登录，改用
Cookie-Editor 手工导出后配置 xiaohongshu-mcp / 存量工具。

Boss直聘配置触发：当用户说“帮我配 Boss直聘”时，先读取 `references/career.md`
的 Boss 章节，然后在获得安装授权后运行
`agent-reach install --env=local --system --channels=boss`。Agent 负责按系统启动
只绑定 `127.0.0.1:9222` 的专用 Chrome；**拉起后第一步是暂停并让用户肉眼确认**
窗口内是已登录状态（右上角有头像），未登录则让用户登录/扫码，用户确认后再运行
`boss --cdp-url http://localhost:9222 login --cdp` 和 `agent-reach doctor` 验收。
不要让用户自己研究端口参数。
专用 Chrome profile 必须长期复用，不要每次创建，也不要默认改用日常主 Chrome。

判断 CDP 浏览器登录态**不要信 `boss status`**（它只校验本地 session.enc，与
浏览器登录态互不代表），以 `agent-reach doctor` 的浏览器 cookie 探测（wt2）
为准，并配合用户肉眼确认。绝不用当前页 URL 判断登录态：
`security-check` / `zhipin-security` / `_security_check` 安全校验页是 Boss 反爬挑战，
与登录无关——已登录也会出现（带 CDP 调试端口的 Chrome 几乎必现）。看到它不要
当成“未登录”，先跑 `agent-reach doctor` 看浏览器 cookie，再决定是否需要用户登录。
搜索报 `AUTH_EXPIRED` 即浏览器未登录的 ground truth：直接走登录流程 + `login --cdp`，
不要往安全校验方向解释。

执行搜索时必须使用
`boss --browser-source existing-browser --cdp-url http://localhost:9222 search ...`；
遇到 `ENVIRONMENT_RISK` 立即停止，不刷新、不重新登录、不自动重试。

```bash
# Twitter 搜索（twitter-cli 首选；失败重试链见 social.md）
twitter search "query" -n 10

# Reddit（无零配置路径：OpenCLI 或 rdt-cli，必须登录态）
opencli reddit search "query" -f yaml   # 桌面
rdt search "query" --limit 10            # 存量/服务器

# 小红书（桌面首选 OpenCLI）
opencli xiaohongshu search "query" -f yaml

# Facebook / Instagram（桌面 OpenCLI，复用浏览器登录态）
opencli facebook search "query" -f yaml
opencli facebook groups -f yaml
opencli instagram search "query" -f yaml       # 搜用户
opencli instagram user USERNAME -f yaml        # 读指定用户最近帖子
```

## 环境检查


```bash
# 检查可用 channel 与每个平台当前激活的后端
agent-reach doctor --json
```

## OpenCLI 适配器发现

路由表没有覆盖用户需要的平台或命令时，先用 `opencli list` 查已有适配器，再用
`opencli <平台> --help` 查看公开命令。发现适配器只证明命令存在，不证明登录态或
目标内容可用；仅在用户任务明确需要该平台时执行只读命令，并以实际非空内容验收。

## 工作区规则

**不要在 agent workspace 创建文件。** 使用 `/tmp/` 存放临时输出，`~/.agent-reach/` 存放持久数据。

## 详细文档

根据用户需求，阅读对应的详细文档：

- [搜索工具](references/search.md) — Exa AI 搜索
- [社交媒体](references/social.md) — 小红书, Twitter, B站, V2EX, Reddit, Facebook, Instagram（多后端/登录态命令组）
- [职场招聘](references/career.md) — LinkedIn, Boss直聘
- [开发工具](references/dev.md) — GitHub CLI
- [网页阅读](references/web.md) — Jina Reader, RSS
- [视频播客](references/video.md) — YouTube, B站, 小宇宙
- [金融行情](references/finance.md) — 雪球股票行情、搜索、热门内容

## 配置渠道

如果某个 channel 需要配置，获取安装指南：
https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md

用户只需提供 cookies，其他配置由 agent 完成。

## 本地兼容性

本次更新技能说明与参考文件，不修改后端登录态或 CLI 安装。使用新增通道前检查当前 `agent-reach` 与后端命令是否支持；缺失能力时说明，不把文档更新当作运行成功。
