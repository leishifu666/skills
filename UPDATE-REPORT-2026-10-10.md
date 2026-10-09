# Skills 更新检查 · 2026-10-10

检查两个本地 Skills 根目录，按来源去重；本轮扫描的本地集合含 371 个非测试入口路径、268 个名称。嵌套入口、别名和客户端差异分别记录，不把目录数当作独立技能数。

核对 30 个已登记的 GitHub 来源和 28 个飞书包；另检查 5 个系统技能及 121 个插件缓存中的技能文件。系统与插件版本由 Codex 管理，本次只读检查，没有重装插件或修改权限。

## 已合入的变化

| 来源或技能 | 本次结果 |
| --- | --- |
| GStack | 适配 1.91.68 的运行源码、模板与现有别名；加入 PowerShell/NotebookEdit 检查、状态目录修复和新的 QA 合约，保留授权、工作目录和隐私约束 |
| Last30days | 更新到 3.27.1 的发布版运行目录；包含来源错误处理、端点保护、Windows 子进程控制等修复；保留本地后端及隐私选择 |
| Hypit | 更新 0.3.1 指引与迁移资料，改用有限 Timeline、Instant、Window、Extent、Visual Clip 与 Audio Clip；没有替用户升级视频项目的包 |
| Remotion | 合入 4.0.534 的合成注册、媒体时间、字幕分组、可编辑节点及预览规则；保留中文入口、版式约定及完整成片交付要求 |
| Remocn | 补充口播字幕选择与位置参考 |
| 造梦师 | 更新到 2.5.0，加入剧本到画面、来源事实与视觉提案区分、按用途制作概念或关键帧，以及可选项目交接 |
| Img2ThreeJS | 合入官方 0.1.1 安装器源码、固定 ref 与安装防护；保留现有视觉技能定制 |
| LSF 封面与社交卡片 | 保留三种模式及三种可选风格；先确认内容、主标题、平台、比例、风格和卡片张数；合入上游局部修改规则与 API 脚本默认模型更新 |
| Agent-Reach | 上游删除本机 conda 环境假设；本地此前已修正，本轮核对后更新来源记录 |

封面显示名为 **LSF 封面与社交卡片**，已有 `$lsf-oil-cover` 调用保持有效。文章封面与连续卡片使用内置生图流程；已有 API 配置和作者资料不重置。

## 核对后保留的部分

- 28 个飞书包摘要均未变化。
- WeWrite 只更新了星标统计图；已安装的写作技能无相关代码变化。
- UI Skills 变化集中于网站目录与数据；已安装技能源文件未变。
- Anthropic 新改动在未安装的 Claude API 技能中，没有新增安装。
- Img2 主程序仓库有变化，但两个已装插件源未变；没有把应用升级混入技能更新。
- Khazix 上游此前已改为不同项目，保留原有三个技能及本地适配，未用新项目覆盖。
- 没有可靠上游记录的本地技能保留原内容；旧版 Last30days open 扩展保留，不伪报成新版完整运行目录。

## 验证结果及范围

- 修改文件：118 个 Python 文件语法检查通过，184 个入口元数据检查通过；相关中文入口的本地引用均存在。
- 公共集合的非测试入口元数据均可解析；系统与插件缓存只读格式检查见本地记录。
- 封面：22 项测试，21 通过、1 跳过；跳过的是 Windows 不支持的 POSIX 文件权限位检查。
- GStack 文档生成：Claude 与 Codex 输出成功；生成隔离/导入测试 9 项通过。
- GStack 路径与辅助脚本：34 通过、1 POSIX 用例跳过；PowerShell、Bash、NotebookEdit 的 6 项直接输入检查通过。
- GStack 浏览器、查找器、设计、PDF 与全局发现器编译成功；Windows Node 服务包构建成功，两处原始安装均同步运行产物。CSO 原生执行器本次未构建验证。
- Last30days 与 Img2ThreeJS 的 CLI 帮助入口可运行。没有使用真实凭据发起联网研究或生图。
- 最初的 GStack Windows 广泛检查未通过，包含错误的 WSL Bash 路径、原生组件环境要求以及部分上游断言与本地定制的差异。改用 Git Bash 后通过上述相关复查；**没有把整套广泛检查标为通过**。
- Img2ThreeJS 新安装器的完整集成测试依赖 POSIX `which` 和无扩展名可执行脚本，未在本机 Windows 完成；帮助入口检查不代表完整安装成功。

## 发布与保留

更新在原始目录完成；没有创建或切换工作树。Skills 通过临时 Git 索引准备提交，保留原分支、用户暂存区与已有远程文件；只移除本轮确认已从上游删除、且本地未定制的源文件。远程原有的 31 个 Factory 适配入口继续保留，不计入本轮本地集合统计。

公共仓库不包含真实凭据、作者私人配置、记忆、日志、缓存、依赖目录或本机二进制。扫描出的 38 处凭据格式匹配均逐一匹配上游公开示例/测试源。客户端确有差异的文件补充到非激活的 `.client-variants`，历史备份保留。

Codex 全局规则同步到独立的 [codex-global-rules](https://github.com/leishifu666/codex-global-rules) 仓库，封面确认规则与当前技能一致。

## 来源检查记录

| 仓库 | 本次检查提交 | 变化 |
| --- | --- | --- |
| [SpaceZephyr/creator-buddy](https://github.com/SpaceZephyr/creator-buddy/commit/edf46c567ff54b72ee2157d06f3a02dbd67aaa9c) | `edf46c567ff5` | 无新提交 |
| [garrytan/gstack](https://github.com/garrytan/gstack/commit/20eb6202fa8ea83a882e7c0463b722cd8a31af1e) | `20eb6202fa8e` | 存在新提交，按实际文件范围处理 |
| [img2threejs/img2threejs](https://github.com/img2threejs/img2threejs/commit/d508b596cb221f1509f6e50ab68fce275a5cfb44) | `d508b596cb22` | 存在新提交，按实际文件范围处理 |
| [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh/commit/f4518a8eab97b8bfebc66a89d34320a89bef6930) | `f4518a8eab97` | 无新提交 |
| [oil-oil/oil-codex-title](https://github.com/oil-oil/oil-codex-title/commit/ae1c9e27061dfdb84dd1ce918ee3e341b58a0d3f) | `ae1c9e27061d` | 无新提交 |
| [LifelongLazyLearner/qu-ai-wei](https://github.com/LifelongLazyLearner/qu-ai-wei/commit/1d32e803f091ec90808a69683ebf49e8a970a5e7) | `1d32e803f091` | 无新提交 |
| [smixs/visual-skills](https://github.com/smixs/visual-skills/commit/92be33a5a73325fb3d8e0c73b22744b114e2a90e) | `92be33a5a733` | 无新提交 |
| [imraywang/wewrite](https://github.com/imraywang/wewrite/commit/95f4d507fb789c695c61cdf0d54bd1ee0fcfd117) | `95f4d507fb78` | 存在新提交，按实际文件范围处理 |
| [larashero3-dotcom/writing-dna-skill](https://github.com/larashero3-dotcom/writing-dna-skill/commit/ee3d97ee27268004b5187d97711161f44fc4aae4) | `ee3d97ee2726` | 无新提交 |
| [popopo-99/zy-cinematic-realism](https://github.com/popopo-99/zy-cinematic-realism/commit/9a3b36d1fb6a980ae9e21f74c86dd56bae443a4d) | `9a3b36d1fb6a` | 存在新提交，按实际文件范围处理 |
| [eze-is/web-access](https://github.com/eze-is/web-access/commit/33eef84a55b1919396a80e7a55650a07bb83f590) | `33eef84a55b1` | 无新提交 |
| [anthropics/skills](https://github.com/anthropics/skills/commit/9d630808e4add0a7146de4af9384155d5dee350a) | `9d630808e4ad` | 存在新提交，按实际文件范围处理 |
| [KKKKhazix/Khazix-Skills](https://github.com/KKKKhazix/Khazix-Skills/commit/322346ded8129436b3f64707789a73e732ae24d9) | `322346ded812` | 存在新提交，按实际文件范围处理 |
| [op7418/Document-illustrator-skill](https://github.com/op7418/Document-illustrator-skill/commit/8344815d407cc25cc04c327557f36ed839f0aaef) | `8344815d407c` | 无新提交 |
| [img2threejs/plugin-character](https://github.com/img2threejs/plugin-character/commit/d8750638f9fc092714e7fcb4941053514455295d) | `d8750638f9fc` | 无新提交 |
| [img2threejs/plugin-cs2](https://github.com/img2threejs/plugin-cs2/commit/e5e29ba53290a18809907d0b90992aba6e8ce975) | `e5e29ba53290` | 无新提交 |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop/commit/8da1f030185bdfe8471220585162991eaeb970e9) | `8da1f030185b` | 无新提交 |
| [img2threejs/img2](https://github.com/img2threejs/img2/commit/06634bdb01e884be1f23d725305bb4dee28881ad) | `06634bdb01e8` | 存在新提交，按实际文件范围处理 |
| [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill/commit/c91369c449d34755d320a8b81d0734000d99d1ab) | `c91369c449d3` | 无新提交 |
| [hypit-ai/hypit](https://github.com/hypit-ai/hypit/commit/847f43c5e4089608abeae2da0240d9edcb1b5441) | `847f43c5e408` | 存在新提交，按实际文件范围处理 |
| [Remocn/remocn](https://github.com/Remocn/remocn/commit/634682ff10f135d29b4751d9379e52ef0bcf6e21) | `634682ff10f1` | 存在新提交，按实际文件范围处理 |
| [remotion-dev/skills](https://github.com/remotion-dev/skills/commit/32b241b97f4e0e4ab61fe9a41b05e6e64503f8c5) | `32b241b97f4e` | 存在新提交，按实际文件范围处理 |
| [ibelick/ui-skills](https://github.com/ibelick/ui-skills/commit/7d7b15eefd89f69445b64bc1148cb70d3f1ada38) | `7d7b15eefd89` | 存在新提交，按实际文件范围处理 |
| [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach/commit/94f06c1969dfc1834001269d79d3ad0972d9dee6) | `94f06c1969df` | 存在新提交，按实际文件范围处理 |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill/commit/a3b73fc5f3fb3a464d6dfb7660eec7ef1dc6d366) | `a3b73fc5f3fb` | 存在新提交，按实际文件范围处理 |
| [oil-oil/oil-cover](https://github.com/oil-oil/oil-cover/commit/6ebdad44dcfbf852843ae03217b04c60c8c4cab5) | `6ebdad44dcfb` | 存在新提交，按实际文件范围处理 |
| [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone/commit/27d29232f10124db904ca9c0536d0b67cb3b2833) | `27d29232f101` | 无新提交 |
