# Seedance 2.5——生产参考（字节跳动，2026-07-31 官方指南）

先读 `seedance.md` 了解家族基础（细节法则、多镜头语法、11 块骨架）。本文件覆盖 2.5 新增的内容：官方提示词公式、50 槽参考系统、视频编辑、延展、超长模式和白模流程。来源：官方即梦（Dreamina/Jimeng）用户指南与提示词指南（均于 2026-07-31 发布），并经首周实践者测试交叉验证。

## 目录

1. 2.5 改变了什么
2. 规格与硬限制
3. 官方提示词公式
4. 音频、对白与文字的语法标记
5. 参考纪律（50 槽系统）
6. 30 秒结构：阶段与结束状态
7. 防塌缩骨架（3 模块）
8. 真实人物公式（防 AI 脸）
9. 运镜语言
10. 转场
11. 通过后果与触发器实现物理
12. 视频编辑（局部重渲染）
13. 视频延展
14. Ultra Long 模式（30-180 秒）
15. 白模与绿幕
16. 分镜网格与关键帧
17. 失败模式与修复
18. 成本经济与模型选择
19. 工作示例（官方，逐字）

---

## 1. 2.5 改变了什么

- **30 秒原生单遍片段。** 一次生成、一条连续弧线、无需拼接。延展推到 60 秒；独立 Ultra Long 模式到 180 秒（见第 13-14 节）。
- **50 个多模态参考**（30 图 + 10 视频 + 10 音频），逐资产职责绑定。模型理解哪个资产负责角色、场景、道具、运镜或节奏——前提是你告诉它。
- **真实人物是招牌特性**，不是负担：真实毛孔、克制微表演、11 种语言多语种口型同步。2.0 时代的人脸警示不适用。
- **负面命令变可靠了。** "Pure video, no subtitles, no background music"现在真的能压制随机字幕和多余配乐——经典的 1.x/2.0 失败被修复。
- **秒级时间戳控制。** `[0-4s] ...` 节拍窗口按时间执行，不只是排序。
- **编辑已存在的视频**（局部重渲染、背景替换、语言重配音）和**延展**它都是正式模式，不是变通方案。
- **白模控制**：白模 3D 预可视化视频（或绿幕素材）锁定运镜路径、舞台调度与走位；Blender/Maya 插件直接上传到即梦。

入口：即梦（jimeng.jianying.com——Omni Reference / Smart Edit / Long Video / First & Last Frames）、豆包（Pro 订阅）、小云雀（xyq.jianying.com——角色库、3D 导演台、片段重拍）。

## 2. 规格与硬限制

| 参数 | 2.0 | 2.5 |
|---|---|---|
| 单遍生成时长 | 最长 15s | 最长 **30s**（duration `-1` 或 4-30） |
| 每请求图片数 | 9 | **30**（每张 ≤4K、≤30 MB） |
| 视频参考 | 3 段，总长 ≤15s | **10 段**，单段 2-30s、**总长 ≤30s** |
| 音频参考 | 3 段，总长 ≤15s | **10 段，总长 ≤30s**；现支持纯音频输入 |
| 输出分辨率 | 最高 4K | 即梦网页端 **480p / 720p** |
| 时间戳 | 仅顺序提示 | 精确到秒 |

生成参数（时长、宽高比、分辨率）在生成页或 API 设置——**它们不属于提示词**。1.x/2.0 的 CLI 尾巴（`--resolution ... --duration ...`）不是 2.5 语法。例外：Ultra Long 模式在提示词顶部重申时长与比例。

自动锁定参数：视频编辑把比例和时长锁定到输入（±0.3s）；首/尾帧把比例锁定到首图（不匹配的尾帧会被拉伸）；延展锁定比例，时长可设。

## 3. 官方提示词公式

任何 2.5 提示词的基础公式：

```text
<Subject> performs <primary action or event> in <scene and environment>.
The visuals feature <visual style>.
Use <shot size, camera angle, camera movement, or cuts>.
Audio includes <dialogue, ambience, sound effects, or music>.
```

任何组件都可省略。对长提示词或重型参考工作，宏公式：

```text
Complete prompt = [reference declaration] + [one-line summary] + [plot by timeline] + [global tail]
```

- **参考声明。** 按上传顺序列出每个资产 + 它的职责（角色/声音/动作/场景）。见第 5 节。
- **一句话摘要。** 主体 + 地点 + 事件 + 类型/风格 + 特殊运镜处理。
- **按时间线讲故事。** 每个节拍：➕ 正向内容（画面+运镜+动作+对白+音效）和 ➖ 局部禁令（"no subtitles"、"no BGM"）。
- **全局尾巴。** 重申必须保持的全局项（机位、环境、声音、灯光）并重复全局禁令。

在提示词中多次重复 @ 同一资产——官方指南说重复提及提升精度。

## 4. 音频、对白与文字的语法标记

2.5 有专用标记。用它们——不要用松散散文描述音频：

| 内容 | 标记 | 示例 |
|---|---|---|
| 音乐 | `( )` | `(Soft, rhythmic piano music plays in the background)` |
| 音效 | `< >` | `<A bell rings in the distance>` |
| 对白 | `{ }` | `{Hello, welcome back.}` |
| 字幕/标题 | `【 】` | `【Chapter One: Departure】` |

对白语言强化——公式为`对白语言 + 地域变体或口音 + 表达方式 + 说话人 + {台词}`：

```text
Dialogue language: authentic Los Angeles English. The young man says in natural
Los Angeles vernacular: {No way, you actually made it.}
The girl says softly in Japanese: {もう大丈夫です}
```

唇形、语速与面部一次通过即匹配指定语言——这在全部 11 种支持语言中都成立，含混合语言场景。

## 5. 参考纪律（50 槽系统）

50 槽的意义不是把素材倒进去。**每个素材的职责必须写在提示词里。** 不要依赖图片内部的文字标签；不要让模型去推断映射。

职责模板：

```text
@Image 1 defines <subject>'s <appearance, clothing, structure, or material>.
@Video 1 defines <motion, camera movement, or pacing>.
@Audio 1 defines <character or sound type>'s <voice, dialogue, ambience, or music>.
```

规则：

- **逐主体绑定。** `<Character A> corresponds to @Image 1. Use only the appearance, hairstyle, and clothing.` 官方禁止的写法："@Images 1 through 4 define four characters respectively"——它从未说明哪个是哪个。
- **加排除项**，防任何外溢： "Do not use the image background." / "Do not use the people in the image." / "Do not use the person's identity, clothing, or scene from the video."
- **不要复述参考已定义的内容。** 若参考视频定义了动作，只说明要继承哪些属性——逐动作重新描述会与参考冲突。
- 常驻角色的 **Subject Profile**：

```text
[Subject Profile: Conservator]
Appearance and clothing: @Image 1.
Fixed prop: <Sample Case> from @Image 5.
Locations: <Conservation Lab> and <Gallery>.
Motion references: the case-opening motion from @Video 1.
Do not use: other characters' clothing. Do not give this character <Record Board>.
```

- **按场景选参考**，不要一次全选：`Scene 1 | Use: <list>. Event: ... End state: ...`
- 同一角色的两种状态（变身前后）= **两个独立图片槽**，各自绑定到自己的时间范围。预期这是最不稳定的绑定——为重抽留预算。

官方稳定性甜区：

| 输入 | 最佳 | 可能但不稳 |
|---|---|---|
| 参考视频/音频中的主体数 | 1-5 | 6-10 |
| 参考片段时长 | 每主体 5-10s | 更长 |
| 参考图片中的主体数 | 1-8 | 9-12 |
| 多视角组合图 | ≤5 主体：任意 | >5 主体：仅单视角；每个视角独立图片优于拼贴 |
| 视频编辑源时长 | ≤20s | 更长会卡住 |

## 6. 30 秒结构：阶段与结束状态

把片段划分为连续阶段。**每阶段一次主状态变化，且必须写明可见的结束状态**——结束状态就是模型的目标方向（这就是 U11 最终画面法则的阶段版）。

```text
[Generation Goal] Generate a <video type>. The central subject is <subject>,
and the primary event is <story summary>.
[Stage 1] Initial state: ... Primary event: <one primary action>. End state: <visible state>.
[Stage 2] Continue from the previous stage: <what must remain unchanged>.
          Primary event: ... End state: ...
[Stage 3] Primary event: <closing event>. End state: <final visible state>.
[Maintain Consistency] Keep <identity, count, clothing, prop ownership,
spatial direction, audio relationships> consistent.
```

时间戳规则：

- 时间范围是事件的**时间预算，不是剪切点**。范围必须连续且不重叠。
- **窗口至少 3 秒。** 更短的窗口执行不可靠。
- **每窗口一个核心动作 + 一次运镜。** 不要要求频率（"一秒三个动作"）。
- 只在关键处用秒级精度：关键交接、入场、转场、节拍落点。`At 5 seconds, the camera whip-pans left and completes the transition.` 相对触发器同样有效：`Three seconds after the character presses the button, the room lights turn off.`
- 窗口内容太少 = 模型自由发挥；太多 = 过度剪切和遗漏。让内容量与预算匹配。

## 7. 防塌缩骨架（3 模块）

戏剧性 30 秒工作的官方结构。它映射到我们的 11 块骨架，但更精简：

```text
<One-line tone summary — the logline>

[Module 1 — Reference layer]
Strictly keep @Image 1's face and features consistent. Keep @Image 2's
composition / blockout / spatial relations. Strictly lock character blocking.

[Module 2 — Global settings ("worldview + anti-collapse")]
Base environment & texture (emphasize extreme, realistic physical texture).
Visual style (film look, depth of field, lighting).
Camera language.
Character styling (use the section 8 formula).
Performance core (the acting register for the whole piece).
Prohibitions: <sound bans> + <subtitle bans> + <behavior bans> + <known collapse points>.

[Module 3 — Timestamped storyboard]
[start-end s] [beat name] — physical directives (shot size, composition,
micro-actions) + emotional subtext.
```

支撑这个骨架的两项技术：

- **禁止清单要具体，不要笼统。** 官方告别示例："No exaggerated crying, no fast cuts, no large body movements, no extra dialogue, no BGM, no runny nose, no premature dropping of tears." 禁止这场戏可能塌缩的确切方式。
- **指令 + 潜台词。** 物理指令之后，向模型解释*为什么*发生这个动作："Emotion analysis: she is not complaining — she is waiting for him to confirm an answer she already guessed." 模型知道意图时表演更好。这是官方指南的标志性技巧，直接与我们细节法则兼容。

## 8. 真实人物公式（防 AI 脸）

```text
Character = [age / ethnicity] + [skin tone / skin texture] + [3-4 facial details]
          + [gaze / soul] + [hairstyle / hair color] + [clothing / fabric]
          + [build / emotion / aura]
```

- **强加保真后缀：** "retaining real fine pores and skin texture"（可选雀斑、瑕疵）。这一句就是官方防塑料肌修复。
- 面部细节要 3-4 个具体点：眼型、眉骨、鼻梁、唇、下颌线。
- 眼神/灵魂 = 眼睛承载的情绪，与面部几何独立。
- 动画角色同样适用——换纹理寄存器即可。

一次情绪转变，**2-4 个可观察线索就够**（眼球移动、眉部紧绷、嘴、呼吸、吞咽、手）。多了像表演过猛；抽象情绪词留了太多空间。

## 9. 运镜语言

官方直接理解的术语：extreme wide / wide / medium / close-up / extreme close-up；push in、pull out、pan、lateral move、follow shot、orbit、dive、dolly out、tilt、handheld shake；low angle、overhead、first-person；one-take shot、dolly zoom、aerial、FPV、bullet time、bounce speed ramp。

较生僻术语：保留术语**并**翻译成可观察变化：`术语 + 目标主体 + 视觉变化 + 前景/背景关系 + 方向或速度`。完整模式与词汇见 `camera-lighting-vocabulary.md` §10。

光圈与焦距数字允许，但用文字描述可见结果才是真正引导模型的东西。

## 10. 转场

转场词汇（natural cut、fade、dissolve、flash、wipe、occlusion mask、match cut、action/whip cut、motion-relay、zoom-through、ink-wash）见 `camera-lighting-vocabulary.md` §11。Seedance 专属用法：

```text
cut = [transition type] + [basic constraints] + [cut logic]
```

- 总是附上咒语：**"prohibit rigid cutting, prohibit objects appearing out of thin air"**——这是官方防跳切条款，在每条转场模板中重复出现。
- 转场可以**委托**："From [natural cut / occlusion mask / ink-wash / match cut], choose the one that best fits the style of this film."
- 不许提前触发的顺序门效果："The ink-wash effect must only appear AFTER 25 seconds, triggered by the 'click' sound — absolutely no premature appearance."

## 11. 通过后果与触发器实现物理

2.5 渲染真实物理并与音频耦合。用四招利用它：

1. **开头声明物理体制。** "Rain reflections on metal, water splashed by tires, and the specular refraction of exhaust flames must strictly obey real-world physics."
2. **叙述后果，不只是动作。** 轮胎掀起水幕；撞击把桥面崩成蛛网状裂纹；冲击波把雨吹成一个扩张的环。每一步强制下一步的动作链（"hand grips jar → lid actually unscrews"）同时兼任 QA——断裂链条瞬间暴露失败的生成。
3. **负面约束已知失败。** "No soft-body or mollusk-like twisting of the mecha structure (must maintain metallic rigidity)." "The amber stays attached to the palm and must not clip through the fingers."
4. **用触发器门控事件。** "Three seconds after she presses the button..." / "only when he says {now}..."——对与表演相关的内容，触发器胜过裸秒数。

## 12. 视频编辑（局部重渲染）

2.5 能编辑已有视频：替换主体、换背景、去水印、换口播语言——其他一切保持不变。规范模式：

```text
[Edit Goal] Edit @Video 1. Within <entire video or time range>,
<add / remove / replace / adjust> <object, region, or audio category>.
[Source Video Role] @Video 1 is the sole editing master. It defines <characters,
scene, actions, composition, camera movement, occlusion, audio, and event order>.
[Target Material Role] @Image 1 defines <attributes of the replacement>.
[Edit Scope] Modify only <object, region, time range, or audio category>.
[Content to Preserve] Keep <everything that must not change> from @Video 1.
```

- **主体替换**加一个 `[Timeline Inheritance]` 块："<Target> inherits every appearance, motion, occlusion, and exit of <original>, including timing, duration, path, and speed changes." 用兜底句收尾："Except for the object explicitly modified above, keep all other people, props, scene content, camera movements, cuts, and event order from @Video 1 unchanged."
- **保留条款开头。** 对拍摄素材，先枚举所有要保留的东西再写任何改动——细到焦距、宽高比和地板透视："Fully preserve from @Video 1 the person's identity, face, hair, skin tone, lip movement, original voice, speech rhythm, expression, gestures, camera position, focal length, aspect ratio, wall and floor perspective, and total duration." 保留清单越长，漂移越少。
- **时间锚定到台词而不是秒数**，当源含旁白时："When they say {now look at my hand}, a golden amber appears in the palm." 声音就是时间线。
- **先切长源。** 编辑在 ≤20s 片段上效果最好；更长的源会卡住或失败。
- **纯音频编辑**可行："Remove only the original background music. Keep the dialogue, lip sync, ambience, and action sound effects; preserve the visuals and editing rhythm."
- **本地化模式**——一次拍摄、逐市场重配音："Replace the Chinese narration in @Video 1 with natural fluent Spanish, and replace the presenter with a Spanish woman. Keep the original camera movement, blocking, performance pacing, scene, and product; preserve the overall audio-visual rhythm."
- 背景替换范围："modify only the background outside the subject's silhouette."

## 13. 视频延展

任何 ≤30s 片段每次延展 4-30 秒，可嵌套重复，**硬上限 60 秒**。新提示词只适用于追加段；原帧不动。必需动词：extend forward / extend backward / continue。

向前：

```text
Extend @Video 1 forward. The first frame of the extended segment directly
continues from the last frame of @Video 1. Maintain continuity in <pose,
prop position, background, camera position, lighting, motion direction>.
Then, <new content>.
Keep each subject as the same continuous instance throughout: do not duplicate
or split it, and keep the person's appearance stable.
```

向后（前置一个开头）：描述前面的事件，然后把 @Video 1 的**第一帧定义为延展的显式结束状态**。坑：只属于源视频的素材必须标记——"<X> must not appear early in the backward extension"——否则之后出现的角色会泄漏进过去。

- 边界帧视觉连接，不要求像素一致。
- 即使不重新提供参考，延展也保持角色样貌、美术风格**和声线**——纯情节延展提示词有效。
- 社区验证的最小延展提示词："Extend the video. Keep character identity, facial structure, body proportions, lighting, art style, and the space fully unchanged. Only change camera movement; do not redesign character or action."

## 14. Ultra Long 模式（30-180 秒）

独立模式（与延展不同）：一次提交，30-180 秒。在提示词顶部重申时长与宽高比。两种可用寄存器：

- **时间戳式**（1 分钟氛围片）：带分窗禁令的窗口节拍——"0-20s (quiet opening): fixed camera... no shake, no characters enter, hard cuts prohibited."
- **叙事流**（3 分钟片）：行内参考的松散事件链——官方 3 分钟示例是一个猫服务员 vlog，列出整天节拍，按职责分配 12 张图片参考，以"No subtitles throughout, no background music."收尾。

提前规划节奏——没有时间戳或节拍链，后半段会漂移。底层管道逐段生成，**把每段最后约 3 秒作为下一段的参考**——这就是交接平滑的原因，也是中间某段弱会向前传播的原因。小云雀上同一机制驱动链式延展到 90 秒，外加**片段重拍**：在时间线上选一段糟糕区间，只重新生成它，其余部分保持一致——修弹出物体和错过表情最便宜的办法。

## 15. 白模与绿幕

可控性之王：先在 3D 里锁定空间、运镜与走位，让模型渲染材质与光。两种粒度：

- **粗白模**——用基础几何体作为"动态骨架"（轨迹、走位、运镜路径、剪切、光变）。**把每个几何体映射到一个参考**："The tall cylinder in @Video 1 corresponds to <Guide>. The rectangular block corresponds to <Display Cart>." 排除渲染风格："Do not use its gray geometry or empty scene." 最佳实践：**粗白模不要带四肢或翅膀的模型**——除非你写出完整的肢体运动序列，否则它们会变得僵硬。
- **精白模**——完整 3D 动画；模型只重渲染材质、色彩与风格："@Video 1 is a fine blockout reference. Preserve structure, action, spatial layout, camera position, camera movement, and cuts. Do not use its original gray materials or empty background. Re-render <subject> as <final subject>..." **先清理视口截图**：移除路径线、坐标轴、控制器和相机视锥。目前粗白模优于精白模。

流程笔记：

- Blender/Maya 插件（"Clay Renderer"/白模渲染上传器）渲染白模并直接上传到即梦作为参考视频。Blender ≥3.6 可用；不支持 C4D/3ds Max。给白模物体上色编码不可靠——用提示词文字而非材质颜色区分几何体。
- 没有 3D 软件？小云雀的 3D 导演台可从概念图重建白模，提供动作/运镜/道具库，让你**在视口拖画运镜路径**，然后替你渲染预可视化片段。
- **运镜路径图也能当图片参考**：提供一张俯视路线草图作为 @Image N，写"follow the camera route in @Image N"。
- **绿幕，双向**：上传绿幕素材 + 场景参考（"composite the person naturally into the classroom from @Image 2"），或把现有视频背景*变成*绿幕供下游合成（"Change all the white backgrounds into green screen backgrounds. Remove the sound, keep it muted."）。

## 16. 分镜网格与关键帧

- **分镜网格作为输入**：一张图，官方 ≤15 格（实践者推到 50），干净线稿、少量文字。声明阅读顺序并排除风格："@Image 1 provides a 12-panel storyboard grid for shot order and approximate composition. Read it left to right, top to bottom. Do not use the grid's line-art style, text labels, or placeholder characters." 然后 `Shot 1: ... Shot N: ...`
- **多关键帧序列**："Use @Image 1 through @Image N as keyframes in this order"，每图一个关键状态。独立图片比网格对齐更好。关键帧控制阶段顺序和关键状态，不是精确帧。
- **首 + 尾帧**在 omni-reference 模式下可用——分别声明每个锚点（"@Image 1 is the first frame... @Image 2 is the last frame..."），绝不合并声明。要求相同宽高比。
- 这就是 `lsf-visual-image` 技能接入的地方：来自 `animatic-keyframes.md` 的角色设定表和关键帧成为参考包。

## 17. 失败模式与修复

### 多人场景中的双胞胎/脸部融合
修复。逐主体绑定（第 5 节）+ 显式差异化："Their movements are not synchronized. Clothing colors, hairstyles, and facial features must all be distinct. No identical clones in the background."

### 同一角色的两种状态出现在错误时间
变身前/后的槽位令模型困惑。修复。显式将每个状态绑定到其时间范围；为重抽留预算——这是 2.5 中最不稳定的绑定。

### 随机字幕或多余的 BGM
修复。"Pure video, no subtitles, no background music"——2.5 中可靠。在全局尾巴里重复。

### 塑料 AI 皮肤
修复。"Retaining real fine pores and skin texture" + 生产语言，而不是"hyperrealistic 8k"。

### 长上下文可信度下滑
超过 30 秒，模型可能把可信物体放在不可能的位置（干混凝土上的货轮）。修复。在全局尾巴中写清世界的硬约束；交付前核查完整时间线——错误藏在后半段。

### 拒绝保持单镜头的长镜头
2.5 是过度执行型：它比对手完成更多指令，但即便被告知"one continuous take"也可能随意剪切。修复。"One continuous shot, no cuts of any kind" + 一条从不诱发剪切的运镜路径；若蒙太奇仍渗入，降到 10-15 秒窗口，那里单镜头稳定。

### 编辑模式卡住或无视指令
修复。源 ≤20s（先切）；把 @Video 1 命名为"the sole editing master"；每次通过只设一个编辑目标。

## 18. 成本经济与模型选择

- 成本真实：即梦上一条 30s/720p 约 500-700 积分。生产预算必须假设重抽、延展和片段重拍——能修就用编辑/延展/重拍，不要整条重新生成。480p 打草稿，720p 收尾。
- 对比 MiniMax H3（本发布窗口的另一前沿模型）：**H3 是疏漏型，Seedance 2.5 是过度执行型**——H3 交付更电影化的整体，但会漏清单上的镜头；2.5 几乎执行每条指令，但可能误用参考或破坏全局约束。要时间戳精度、密集镜头编排、50 参考包和编辑/白模工具链选 2.5；当每积分的整体电影化连贯性比指令遵从更重要时，选 H3（或 Kling/Veo）。

## 19. 工作示例（官方，逐字）

### A. 克制微表演——《江畔告别》（29 秒单镜头）

情绪表演的旗舰官方示例。节选；真正要抄的是结构：

```text
29-Second One-Shot (Ancient Costume Woman's Riverside Farewell)

[Global Scene Setting] Early morning by the river, a blurred small boat in the
background, a lonely farewell. Quiet, restrained. Cinematic, shallow depth of
field, soft natural light. The camera holds a close-up of the woman, imitating
the subjective POV of "him" standing opposite her. Subtle handheld breathing,
one continuous shot with no fast cuts.

[Character Styling] [Age/Ethnicity] 22-year-old East Asian woman, classical
gentle cinematic face. [Skin] Cool-toned fair skin, delicate and moist,
retaining realistic fine pores and natural skin texture. [Facial Features]
Slender elegant eyes (slightly moist), relaxed brows, delicate straight nose
bridge, full lips with a faint gentle smile, soft jawline. [Eyes/Soul] Deeply
affectionate gaze, eyes shimmering like spring water. [Hair] Jet-black hair in
a casual classical low bun, a plain jade hairpin. [Clothing] Minimalist pure
white cross-collar Hanfu. [Physique/Aura] Slender, delicate narrow shoulders,
gentle classical romantic aura.

[Core Performance] Restrained and nuanced. Capture the shifting gaze, the rise
and fall of breathing, slight lip trembling, subtle brow movements, nostril
changes, throat swallowing, and the natural process of a tear sliding down.

[Negative Prompts] No exaggerated crying, no fast cuts, no large body
movements, no extra dialogue, no BGM, no runny nose, no premature dropping
of tears.

[Emotion and Action Storyboard]
Stage 1: 0-3s [Questioning]. She looks directly into the lens, lips slightly
parted, and whispers: {Are you really leaving?} Emotion analysis: she is not
complaining — she is waiting for him to confirm an answer she already guessed.
Stage 2: 3-10s [Resignation] — swallowing the bitterness. ...
Stage 3: 11-17s [Remembering] — a 0.5-second dead-silent pause; her lips twitch
then press together, jaw tightens, throat swallows.
Stage 4: 18-23s [Regret] — she lowers her eyes, and only then do the tears
begin to fall. She shakes her head slightly, almost imperceptibly.
Stage 5: 24-29s [Letting Go] — extreme close-up. She forms a gentle smile and
says in a barely audible but steadied voice: {You can go.} (On the word "go"
there is a faint tremble, forcefully suppressed.)
```

每个阶段：一次状态变化、物理指令、情绪潜台词，禁止清单点名*这场*戏的确切塌缩模式。

### B. 物理与禁令——科幻机甲追逐（30 秒单镜头）

```text
30-Second One-Shot (Sci-Fi Mecha Chase and Transformation)

[Global Setting] A cyberpunk cross-sea bridge in 2077, heavy rain. Emphasize
extreme, realistic physical textures: rain reflections on metal, water
splashed by tires, and the specular refraction of exhaust flames must strictly
obey real-world physics. Hardcore sci-fi cinematic feel, high-contrast neon
(cyber-pink and icy blue), high-speed shutter. High-speed drone POV, one
continuous shot. Subject: a silver-and-black concept mecha motorcycle.

[Negative Prompts] No soft-body or mollusk-like twisting/clipping of the mecha
structure during movement (must maintain metallic rigidity); no human
entities; strictly remove irrelevant subtitles; force mute / no default BGM;
avoid copyrighted IP elements like Transformers or Tron.

[Timestamp Storyboard]
[00:00-00:08] [Extreme Speed] The camera skims the waterlogged road; the
spinning wide tires kick up massive water curtains meters high. Camera
subtext: convey speed through the physical interaction of rain, puddle
reflections and engine flames.
[00:09-00:16] [Evasion] The tires grind the road, sparking orange friction
sparks, executing a tight "S" curve.
[00:17-00:24] [Mid-Air Reassembly] During slow-mo hang time the armor flips,
deconstructs, and reassembles — strictly rejecting "noodle-like" soft-body
transformation.
[00:25-00:30] [Heavy Landing] The tonnage impact shatters the bridge surface
into a spider-web pattern; the shockwave blows the surrounding rain away in
an expanding ring. A frozen "superhero landing" as the final image.
```

开头声明物理体制，每个节拍叙述一个后果，每条禁令都精确打击这种素材的已知失败。

### C. 参考编排——博物馆盗窃单镜头（17 个参考，译自即梦手册案例）

```text
Photoreal suspense-film texture. Set at the museum charity gala of @Image 10;
main hall structure, twin staircases and central exhibit stay consistent
throughout; sub-spaces reference @Image 11 and @Image 12; lighting and
materials reference @Image 15 and @Image 17. Follow the camera route in
@Image 16; smart auto-cutting, cinema-grade camera moves.

[0-4s] Camera advances behind the shoulder of the @Image 4 waiter carrying
the @Image 14 silver champagne tray through the main hall; the @Image 5
curator greets guests at the staircase; the @Image 6 reporter raises a
camera. The @Image 1 blue-diamond necklace sits in its glass case.
[4-8s] The @Image 7 woman in red brushes past the @Image 8 magician in black
tails, who smiles faintly at the lens; the @Image 9 security chief watches
beside the case.
[8-11s] The chandelier dies; the hall snaps to the crimson emergency lighting
of @Image 13; the crowd falls silent; <a soft clink from the case>, then
<a short alarm>. (Low strings and heartbeat stop together) — keep only an
inhale, the glass clink and the alarm.
[11-16s] Close-ups in sequence: the curator frozen, the reporter raising the
camera, the woman in red stepping back. Lights return to warm gold; cut back
to the case — glass intact, the @Image 1 diamond gone.
[16-20s] Slow push toward the magician's lowered right hand; a tiny blue
glint inside his silver cuff; he lifts his eyes to the lens and smiles.

No subtitles, no logo, no watermark.
```

十七个参考，每个按场景绑定职责；运镜编排以路线图（@Image 16）而不是散文提供；声音用 `< >` 和 `( )` 标记按节拍设计。

---

*作者：Serge Shima（[t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)）· 许可：CC BY 4.0 —— 需注明出处 · 来源：[smixs/visual-skills](https://github.com/smixs/visual-skills)*
