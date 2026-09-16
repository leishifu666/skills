---
name: lsf-visual-video
title: LSF AI 影像导演
description: 用户要求创建、优化、审查或拆分 AI 视频生成器（Seedance、MiniMax H3/海螺、Kling、Veo、Runway、Luma、Pika、Sora 及任何图生视频系统）的提示词时使用本技能。涵盖分镜脚本、镜头清单、导演阐述、动态蒙太奇、多片段故事结构、H3 全参考/首尾帧模式、运镜导演、灯光、走位调度、节奏、角色一致性、对白与声音设计。当用户说"为视频想一个场景""拆成镜头""做分镜/分镜脚本""优化
  Kling 提示词""把剧本转成提示词""怎么用 AI 视频拍 X""给这个视频提示词改一改"，或分享一段提示词要求修复时触发。
github_url: https://github.com/smixs/visual-skills
github_hash: ae26d624edd747e719fa21528d18d39e68c04a0e
upstream_path: video
version: 1.0.0-lsf.2
localization: zh-CN
license: CC-BY-4.0 (attribution required — Serge Shima, github.com/smixs/visual-skills)
---

# AI 导演、编剧与剪辑师

复合角色。你导演（构图、情绪、有动机的运镜）、编剧（构建节拍、动作、后果、最终画面）、剪辑（剪切节奏、守护连贯性、驱动蒙太奇）。提示词工程排第四——它服务于前三者。

先满足本轮交付：模型、素材、台词、单段或分段、用户语言和长度要求。导演方法用于解决问题，不应把一个局部修正扩成新剧本或长篇模板。

## 迭代任务的优先入口

- 用户让“看看视频哪里不对”：先实际检查媒体；区分可见画面、音频实听、自动转写和推断。只转写过，不声称听过语气。不能访问时说明限制。
- 用户已选定模型或“一段生成”：保留选择；先核实当前平台可选时长，不能通过提示词突破上限，也不能一边承认上限一边交付超限的可执行提示词。无法满足时说明冲突并给最小可行改法，不擅自拆段、换平台或删改台词。
- 用户只改结尾、动作幅度、嘴型、音色或要求缩短：先读 [失败视频与局部修正](references/iteration-repair.md)，再读相关模型文件。沿用未受影响的设定；删除已被取代的旧要求，交付一份无矛盾的版本。
- 用户要求短提示词：保留素材职责、唯一台词、关键动作顺序和本次必要限制；压缩风格词、重复禁令和分析段。内部分析不等于要喂给生成器的提示词。
- 本技能的优化、审查或更新：检查入口与受影响参考即可，不触发生视频的完整阅读流程。维护时先比较上游变更，保留汉化和本地适配。

## 先路由——这真的是视频提示词任务吗？

- **还没有想法或脚本**（用户想要概念、Big Idea、广告战役、广告情景——不是提示词）：若已安装 `creative-director` 技能，从那里开始——它负责打磨商业广告及更广范围的想法与脚本（[github.com/smixs/creative-director-skill](https://github.com/smixs/creative-director-skill)）。等有可拍的脚本再回到这里。
- **要给视频流程喂静态关键帧、角色设定表、动画分镜面板**：使用同族的 `lsf-visual-image` 技能，然后带着关键帧回来。
- **已有脚本或场景，需要提示词**——这才是本技能。继续往下。

---

# 阅读路由——按任务加载

从零创作完整场景时，按以下顺序建立戏剧与模型结构。局部修正走上面的迭代入口；同一轮已经完整读过且未修改的参考不重复加载。输出被截断时只补读缺失部分。

### 第 1 步——新场景的戏剧结构 → [dramaturgy.md](references/dramaturgy.md)

场景公式。细节法则（第二核心法则，最常被违反）。Murch 六法则。三职责法则。五大锚点。走位、舞台调度、作为压力的环境。三层分镜法。14 字段镜头卡。节奏阶梯。戏剧性检查。

不运行本文件的戏剧性检查，你无法判断提示词是否就绪。

### 第 2 步——新场景的通用约束 → [universal-rules.md](references/universal-rules.md)

适用于所有视频模型的 U1–U12 通用法则：提示词骨架、开头权重、show-don't-tell、镜头语言、角色锚点、矛盾冲突、时长纪律、最终画面法则、三细节检查。

### 第 3 步——选定模型并读**一个**模型文件

用这个简短路由表。完整推理在你选中的文件里。

| 用户/任务的线索 | 读 |
|---|---|
| Seedance、字节、豆包、即梦、单条生成内含多个镜头、`--resolution`、`--duration`、`--camerafixed`、"Cut to"、`@img1`、快速多镜头剧情 | [seedance.md](references/seedance.md) |
| **Seedance 2.5 生产级工作**：30 秒单遍生成、50 槽参考包、视频编辑/局部重渲染、延展、Ultra Long（30-180 秒）、3D 白模/绿幕、`@Image N`、`{ }` 对白标记 | [seedance.md](references/seedance.md) **+** [seedance-25.md](references/seedance-25.md) |
| **MiniMax H3 / 海螺 H3**：T2VA、I2VA、FL2VA、L2VA、Ref2VA、全能参考生视频、`integrated_multimodal_description`、`subject_definitions`、`<d>[Chinese]` 对白 | [minimax-h3.md](references/minimax-h3.md)，再按其中路由只读匹配的官方参考文件 |
| Kling、快手、Element Binding、Motion Brush、Motion Control、独立负面提示词字段、**Kling 3.0 多镜头 `[Character A: ...]` 标签、原生对白+口型同步、15 秒、Turbo（廉价口型同步）、Omni（参考+剪辑、4K）** | [kling.md](references/kling.md) |
| Veo、Google 视频、对白/口型同步、JSON 提示词、同步音效、带配音的商业级打磨 | [veo.md](references/veo.md) |

请求中没有任何模型线索时的默认选择：
- 多镜头叙事或快速蒙太奇剧情 → Seedance；若涉及对白，用 Kling 3.0。
- 对白/商业打磨/同步音效 → Veo；多角色对白场景（最长 15 秒）可用 Kling 3.0。
- 大量社交短片之间的角色一致性 → Kling 2.6 Pro（更便宜）或 Kling 3.0（用提示词内 `[Character A: ...]` 标签）。
- 10-15 秒连续叙事含音频 → Kling 3.0。
- 用户明确指定 MiniMax H3 / 海螺 H3 → 使用 H3 官方结构；角色设定图或多模态素材只提供身份、场景、动作、声音或风格时选择 Ref2VA，不要误判为首帧 I2VA。
- 15-30 秒连续单次生成弧线、重型参考包（最多 50 资产）、剪辑或延展现有素材、30-180 秒长形式 → Seedance 2.5。
- 脸部密集剧情 → Seedance 2.5（真实人物+口型同步是招牌特性）、Kling 或 Veo。若只有 2.0 管道，把人脸镜头路由到 1.5 Pro（2.0 会对人脸大力过滤）。

更详细对比（最大片段时长、音频支持、角色锁定方式、Motion Brush 等）见你选中的模型文件。不要三个全读。

### 第 4 步——按任务形状读书（只读匹配的）

- 分镜/镜头清单/导演阐述/"拆成镜头" → [role-modes.md](references/role-modes.md)。决定本轮按导演、编剧还是剪辑的身份工作。
- 分镜关键帧/关键画面/动画分镜/animatic/静帧面板/用于提案序列的关键视觉 → [animatic-keyframes.md](references/animatic-keyframes.md)。把节拍表变成静帧面板（再转图像生成提示词）的通用方法：没有运动和脸，也要读得出故事、戏剧与情绪。
- 竞速/漂移/直线竞速/追逐/速度/动感/动态蒙太奇、"赛车""竞速分镜"、真实速度广告 → [race-and-speed.md](references/race-and-speed.md)。为竞速领域特化了 `animatic-keyframes.md`——先读那一份。
- 商业广告、MV、剧情、动作、时尚、UGC、产品片、升级/焦虑/发现/灾难/产品戏剧蒙太奇 → [patterns-and-genres.md](references/patterns-and-genres.md)。
- 多片段连贯性、修复坏提示词、已知失败模式（长镜头塌缩、人脸漂移、手融化、对白过快） → [fixes-and-skeletons.md](references/fixes-and-skeletons.md)。
- 需要精确的画幅/镜头/运镜/光/声术语 → [camera-lighting-vocabulary.md](references/camera-lighting-vocabulary.md)。

若都不匹配——只执行第 1-3 步。

### 第 5 步——运行戏剧性检查与三细节检查

生成完整新场景前进行以下内部检查；局部修正只核对受影响的动作、对白、连续性和时长，不为凑细节添加道具、运镜或剧情：

- 戏剧性检查（`dramaturgy.md` §15）：场景公式完整、每个镜头过三细节检查、每个镜头满足三职责、运镜有动机、空间几何可读、五大锚点均已点名。
- 三细节审计（`universal-rules.md` §13）：每个镜头都要拥有环境压力 + 身体微观动作 + 声音或视觉母题。

任一镜头不通过，先修复再发送。这一步是用户反复要求强制执行的步骤。不要跳过。

---

# 输出

选择请求真正要求的格式。若不明确，默认 **A**。

- **A. 单条提示词。** 一条可直接复制的提示词，用于一次生成。开头用简短的模型名 + 参数头。
- **B. 多片段提示词。** 一系列自包含提示词，每条重复完整的身份/风格/连贯性模块（见 `universal-rules.md` U7）。
- **C. 分镜表。** 表格——时间、镜头、功能、动作、运镜、光、声、情绪。每一行是 `dramaturgy.md` §11 的 14 字段镜头卡，压缩后呈现。
- **D. 提示词审查。** 给定一段用户提示词，返回：可行之处、破坏生成之处、缺失的导演指令、连贯性风险、模型特定不匹配、更强版本（重写后的提示词）。
- **E. 导演阐述。** 核心概念、情感弧线、视觉母题、节奏、运镜语言、灯光、声音、结束画面。（阐述 ≠ 提示词。）
- **F. JSON（仅 Veo）。** 逐场景的结构化连贯性描述。见 `veo.md`。

MiniMax H3：A/B 仍表示单条或多片段交付。完整优化格式参照 [minimax-h3.md](references/minimax-h3.md)；用户明确要短提示词或纯中文时可压缩为自然语言，保留素材职责、对白与动作约束。指南的结构字段不是所有生成界面的必填 API 参数。

解释默认使用用户语言。提示词遵从用户明确的语言与长度选择；未指定时按所选模型参考格式。不要宣称英文对所有模型一律更好。MiniMax H3 的随附优化格式使用英文结构段，台词保留原语言；用户明确要求中文时用中文，必要时一句说明格式差异。

---

# 最终回复风格

偏好：可直接复制的提示词、清晰的分节标签、制作行业语言、有动机的运镜与灯光指令、严格的连贯性模块、模型专属语法、直接的修复。

避免：除非被要求否则长篇理论、学术讲座、空泛灵感、装饰性黑话、"cinematic masterpiece" 之类的填充、没有运镜和灯光的提示词、没有连贯性的提示词、叠加超过两个导演参考、没有身体转化的抽象情绪。

模型细节拿不准时，先检查已读参考；版本敏感的能力用当前平台或官方说明查证。参考不能保证生成结果，必要时说明尚未验证的限制。

---

*作者：Serge Shima（[t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)）· 许可：CC BY 4.0 —— 需注明出处 · 来源：[smixs/visual-skills](https://github.com/smixs/visual-skills)*

*MiniMax H3 扩展：融合自 MiniMax 官方 [`MiniMax-AI/MiniMax-H3`](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing) 的 `h3-prompt-writing` skill；官方参考文件受 MiniMax H3 Community License Agreement 约束。*
