# 本地技能更新与备份记录 · 2026-09-29

检查 `.agents/skills` 和 `.codex/skills` 中的用户技能，依据来源元数据、安装锁文件及 Git 仓库核对上游；按文件差异合并更新，保留本地汉化、使用边界和定制。

备份包含 264 个顶层技能目录、399 个 `SKILL.md` 入口（含嵌套技能与示例，不能视为 399 个独立启用技能）。同路径且内容不同的 5 个 Codex 文件另存于 `.client-variants/codex/`，恢复说明见该目录上一级 README。

本次更新 gstack、Humanizer-zh、visual-skills、Hypit、Agent Reach、Last30Days，以及 14 组飞书技能内容。另 14 组飞书下载包摘要有变，解包后的内容无实质差异，仅刷新本地安装记录。

## 来源核对结果

以下提交是本次查询时的上游快照。核对到较新提交不等于整包替换；具体处理如下。

| 上游 | 核对提交 | 处理 |
| --- | --- | --- |
| [SpaceZephyr/creator-buddy](https://github.com/SpaceZephyr/creator-buddy) | [edf46c567f](https://github.com/SpaceZephyr/creator-buddy/commit/edf46c567ff54b72ee2157d06f3a02dbd67aaa9c) | 记录的上游版本与当前提交一致，保留本地适配。 |
| [garrytan/gstack](https://github.com/garrytan/gstack) | [65bfb0ce49](https://github.com/garrytan/gstack/commit/65bfb0ce49da807698359ca033a05709e342c684) | 更新到 1.91.6.0；三方合并源码，重新生成技能入口；保留本地协作与隐私规则。 |
| [img2threejs/img2threejs](https://github.com/img2threejs/img2threejs) | [6e60b5e224](https://github.com/img2threejs/img2threejs/commit/6e60b5e22419464b4853e01ddb6c0e6f6659a733) | 记录的上游版本与当前提交一致，保留本地适配。 |
| [leishifu666/lsf-clock-editorial-poster](https://github.com/leishifu666/lsf-clock-editorial-poster) | [bc7aca8c0e](https://github.com/leishifu666/lsf-clock-editorial-poster/commit/bc7aca8c0e73f71ea21f5040cb0102d8a11bd320) | 记录的上游版本与当前提交一致，保留本地适配。 |
| [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) | [f4518a8eab](https://github.com/op7418/Humanizer-zh/commit/f4518a8eab97b8bfebc66a89d34320a89bef6930) | 合并新版编辑指南、文件保护要求和检查脚本，保留中文工作模式。 |
| [oil-oil/oil-codex-title](https://github.com/oil-oil/oil-codex-title) | [ae1c9e2706](https://github.com/oil-oil/oil-codex-title/commit/ae1c9e27061dfdb84dd1ce918ee3e341b58a0d3f) | 记录的上游版本与当前提交一致，保留本地适配。 |
| [LifelongLazyLearner/qu-ai-wei](https://github.com/LifelongLazyLearner/qu-ai-wei) | [1d32e803f0](https://github.com/LifelongLazyLearner/qu-ai-wei/commit/1d32e803f091ec90808a69683ebf49e8a970a5e7) | 记录的上游版本与当前提交一致，保留本地适配。 |
| [smixs/visual-skills](https://github.com/smixs/visual-skills) | [92be33a5a7](https://github.com/smixs/visual-skills/commit/92be33a5a73325fb3d8e0c73b22744b114e2a90e) | 合并新增参考与 de-slop 指南，保留汉化和客户端差异。 |
| [imraywang/wewrite](https://github.com/imraywang/wewrite) | [3d9e335ab9](https://github.com/imraywang/wewrite/commit/3d9e335ab9e180474308acb214c76e8d1113cc29) | 上游新增为 star-history 文档图片，已安装技能无需更新。 |
| [larashero3-dotcom/writing-dna-skill](https://github.com/larashero3-dotcom/writing-dna-skill) | [ee3d97ee27](https://github.com/larashero3-dotcom/writing-dna-skill/commit/ee3d97ee27268004b5187d97711161f44fc4aae4) | 记录的上游版本与当前提交一致，保留本地适配。 |
| [popopo-99/zy-cinematic-realism](https://github.com/popopo-99/zy-cinematic-realism) | [e78c9669d8](https://github.com/popopo-99/zy-cinematic-realism/commit/e78c9669d84373e60c2c9d60cf578184ae4b8c3a) | 记录的上游版本与当前提交一致，保留本地适配。 |
| [eze-is/web-access](https://github.com/eze-is/web-access) | [33eef84a55](https://github.com/eze-is/web-access/commit/33eef84a55b1919396a80e7a55650a07bb83f590) | 记录的上游版本与当前提交一致，保留本地适配。 |
| [anthropics/skills](https://github.com/anthropics/skills) | [8a1541c4a3](https://github.com/anthropics/skills/commit/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4) | 上游差异涉及未安装的 claude-api 技能；已安装部分无需更新。 |
| [KKKKhazix/Khazix-Skills](https://github.com/KKKKhazix/Khazix-Skills) | [b81ad3b442](https://github.com/KKKKhazix/Khazix-Skills/commit/b81ad3b442e778bb7bf27047034c1d0d9f0637ff) | 上游仓库历史及内容已重写，无法安全对应本地旧版；保留本地定制，未覆盖。 |
| [op7418/Document-illustrator-skill](https://github.com/op7418/Document-illustrator-skill) | [8344815d40](https://github.com/op7418/Document-illustrator-skill/commit/8344815d407cc25cc04c327557f36ed839f0aaef) | 记录的上游版本与当前提交一致，保留本地适配。 |
| [img2threejs/plugin-character](https://github.com/img2threejs/plugin-character) | [d8750638f9](https://github.com/img2threejs/plugin-character/commit/d8750638f9fc092714e7fcb4941053514455295d) | 记录的上游版本与当前提交一致，保留本地适配。 |
| [img2threejs/plugin-cs2](https://github.com/img2threejs/plugin-cs2) | [e5e29ba532](https://github.com/img2threejs/plugin-cs2/commit/e5e29ba53290a18809907d0b90992aba6e8ce975) | 记录的上游版本与当前提交一致，保留本地适配。 |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | [8da1f03018](https://github.com/hardikpandya/stop-slop/commit/8da1f030185bdfe8471220585162991eaeb970e9) | 记录的上游版本与当前提交一致，保留本地适配。 |
| [img2threejs/img2](https://github.com/img2threejs/img2) | [7aa41b37ee](https://github.com/img2threejs/img2/commit/7aa41b37ee24dde844390bb05eca76b709e91599) | 记录的上游版本与当前提交一致，保留本地适配。 |
| [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | [c91369c449](https://github.com/op7418/guizang-ppt-skill/commit/c91369c449d34755d320a8b81d0734000d99d1ab) | 记录的上游版本与当前提交一致，保留本地适配。 |
| [hypit-ai/hypit](https://github.com/hypit-ai/hypit) | [b00532e413](https://github.com/hypit-ai/hypit/commit/b00532e413d83845b631df25f2319017541db0ac) | 更新到 0.2.16；更新参考路由与合成规则，保留本地中文入口。 |
| [Remocn/remocn](https://github.com/Remocn/remocn) | [7b1e6dadf2](https://github.com/Remocn/remocn/commit/7b1e6dadf21243bf6369f1392c8e898b8b40943e) | 已安装技能目录树哈希一致，无需更新。 |
| [remotion-dev/skills](https://github.com/remotion-dev/skills) | [cf49eff5d4](https://github.com/remotion-dev/skills/commit/cf49eff5d4463b33966b6618c83f7295797dd028) | 8 个已安装技能目录树哈希一致，无需更新。 |
| [ibelick/ui-skills](https://github.com/ibelick/ui-skills) | [dc7ab32093](https://github.com/ibelick/ui-skills/commit/dc7ab3209341b2075c495983899b11f6d204e41b) | 核对技能目录及本地定制；近期上游变化不要求替换现有技能，保留。 |
| [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | [a19a171fa9](https://github.com/Panniantong/Agent-Reach/commit/a19a171fa980a0785849596492e0af4db800c82f) | 更新技能与平台参考文档；未安装或升级各平台外部服务、登录凭据。 |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | [084662b501](https://github.com/mvanhorn/last30days-skill/commit/084662b501fb0dba95bd55eff0c258d35e0dc499) | 更新主要技能运行脚本到 3.25.0；保留本地授权边界。独立 open 变体保留。 |
| [oil-oil/oil-cover](https://github.com/oil-oil/oil-cover) | [f6bffe73db](https://github.com/oil-oil/oil-cover/commit/f6bffe73dbe17b03c10c1b24b4aab3540bac7345) | 72 个源文件与上游一致；入口与文档为本地定制，保留。 |
| [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) | [27d29232f1](https://github.com/larashero3-dotcom/lieflat-less-ai-tone/commit/27d29232f10124db904ca9c0536d0b67cb3b2833) | 核对当前上游，作为 writing-dna 本地适配保留；不以提交差异自动覆盖。 |

## 飞书官方技能包

按安装记录的官方包地址下载并逐文件比对；本地中文名称、标题和简介保留。

| 技能 | 结果 |
| --- | --- |
| lark-approval | 内容一致；刷新包摘要 |
| lark-apps | 更新内容 |
| lark-attendance | 内容一致；刷新包摘要 |
| lark-base | 更新内容 |
| lark-calendar | 更新内容 |
| lark-contact | 内容一致；刷新包摘要 |
| lark-doc | 更新内容 |
| lark-drive | 更新内容 |
| lark-event | 更新内容 |
| lark-im | 更新内容 |
| lark-mail | 更新内容 |
| lark-markdown | 更新内容 |
| lark-meeting | 更新内容 |
| lark-minutes | 内容一致；刷新包摘要 |
| lark-note | 内容一致；刷新包摘要 |
| lark-okr | 内容一致；刷新包摘要 |
| lark-openapi-explorer | 内容一致；刷新包摘要 |
| lark-shared | 内容一致；刷新包摘要 |
| lark-sheets | 更新内容 |
| lark-skill-maker | 内容一致；刷新包摘要 |
| lark-slides | 更新内容 |
| lark-task | 更新内容 |
| lark-vc | 内容一致；刷新包摘要 |
| lark-vc-agent | 内容一致；刷新包摘要 |
| lark-whiteboard | 内容一致；刷新包摘要 |
| lark-wiki | 更新内容 |
| lark-workflow-meeting-summary | 内容一致；刷新包摘要 |
| lark-workflow-standup-report | 内容一致；刷新包摘要 |

## 检查结果

- 196 个受影响技能入口的 YAML 解析通过。
- 296 个 Python 文件语法检查通过；Humanizer 的正、负样例结构检查通过。
- 受检查的 Humanizer、Hypit、visual-skills、Agent Reach 入口相对链接无缺失。
- gstack 的入口生成、模块导入、Codex 模型契约相关测试：14 项通过。
- gstack 浏览器 CLI 与 Node 服务包构建通过，实际 Windows CLI `--help` 通过；未做真实网页会话及全部平台、原生扩展的端到端验证。
- Last30Days CLI 帮助及无网络 mock 运行通过；未调用付费搜索或访问登录 Cookie。

## 备份边界与未更新项

- 系统内置 `.system` 和插件缓存由 Codex 管理，不作为用户技能复制或覆盖；本次未核验插件市场是否另有新版。
- 无可验证上游的自建技能保留现状并备份，不能宣称它们已与外部最新版一致。
- Khazix 上游重写后的对应关系不明，保留旧版；重度定制的独立变体保留，未强行套用新版。
- 本次技能快照不纳入个人记忆、任务历史、凭据、登录态、环境密钥、缓存、依赖安装目录、机器专属配置和本机构建产物；技能自带且运行所需的 vendor 包保留。超过 25 MiB 的本地新文件不纳入备份；原文件保留。仓库原有的非技能项目 `edict/` 保持远端原样，不在本次更新范围。
- 内容扫描命中的 30 项均核对为公开上游测试样例或示例配置，不是本机凭据。隐私文件排除针对本次快照，不改写 Git 历史。
- 上游新增参考资料可能保留原语言；已有中文入口及定制未被整包英文版替换。

## 全局规则

Codex 当前全局 `AGENTS.md` 已同步至 [codex-global-rules](https://github.com/leishifu666/codex-global-rules)，提交 [9c0db5c](https://github.com/leishifu666/codex-global-rules/commit/9c0db5cdac094928fdf2104ccc10f03fec08b1f7)。只提交规则文件，未提交 Codex 账号或本机配置。

技能备份目标为现有 [leishifu666/skills](https://github.com/leishifu666/skills) 仓库。更新在原始技能目录完成，发布使用独立 Git 索引组织快照，保留原工作分支和用户已有暂存状态。
