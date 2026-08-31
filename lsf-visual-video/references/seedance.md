# Seedance 参考（字节跳动）

## 目录

1. Seedance 是什么
2. 版本与规格
3. CLI 参数（仅 1.x / 2.0）
4. 细节法则（先读）
5. 6 步提示词公式（快速场景）
6. 生产级骨架（11 块）——用于剧情/多镜头工作
7. 5 秒镜头时间线（节奏模板）
8. 多镜头语法（独有能力）
9. 防糊守护块（当 Seedance 把剪切糊掉时）
10. `@img1` 角色参考语法
11. 运镜（9 个预设）
12. 负面提示词处理
13. 图生视频法则
14. 音频（1.5+）
15. 失败模式与修复
16. 工作示例。15 秒悲喜剧，3 × 5s 片段
17. Seedance 2.5 → 读 `seedance-25.md`

---

## 1. Seedance 是什么

字节跳动的视频模型，拥有在**一次生成**中产出多个独立镜头的独有能力。唯一能把迷你蒙太奇塞进一条 5-10 秒片段的主流模型。电影化动态好，广告和短叙事很强。

## 2. 版本与规格

- Seedance 1.0 Pro。1080p，5-10 秒（API 最长 12 秒）。多镜头能力强。
- Seedance 1.0 Lite。720p，更快、更便宜。
- Seedance 1.5 Pro。加入原生音频与口型同步。
- Seedance 2.0。动态改进、音频更好、9 个运镜预设、有限负面提示词支持、通过 `@` 标签最多 12 个参考输入。2026 年 6 月起：原生 4K、10-bit 色彩。2.0 Mini：约快 2 倍、便宜约 30%，用于草稿与批量。
- **Seedance 2.5**（2026-07-31 发布）。原生 30 秒单遍片段，通过延展最长 60 秒，Ultra Long 模式 30-180 秒。50 个多模态参考输入（30 图 + 10 视频 + 10 音频）、视频编辑（局部重渲染）、3D 白模相机走位、支持 11 种语言多语种口型同步的真实人物。**完整生产参考：`seedance-25.md`。**

分辨率。480p、720p、1080p；2.0 增加原生 4K；2.5 在即梦输出 480p/720p。
宽高比。16:9、4:3、1:1、3:4、9:16、21:9、9:21。
帧率。24-30 fps。

**家族内选型：** 一条连续 15-30 秒弧线、重型参考包、编辑/延展现有素材 → 2.5（真实人物和口型同步是其招牌特性——下面 2.0 时代的人脸警示不适用于它）。仅 2.0 管道上的以人为中心的剧情 → 1.5 Pro（2026 深度伪造整治后，2.0 对人脸及名人相似内容过滤极激进）。短片段中的场景、建筑、产品、蒙太奇 → 2.0。便宜草稿 → 2.0 Mini，然后把合格稿高画质重渲染。

## 3. CLI 参数（仅 1.x / 2.0）

追加在提示词末尾。

```text
--resolution 1080p --duration 5 --camerafixed false --seed 42
```

- `--resolution`. 480p | 720p | 1080p
- `--duration`. 2 到 12（Pro）
- `--camerafixed`. true 锁定相机。false 允许运动。
- `--seed`. 用于可复现性

**不是 2.5 语法。** 2.5 上，时长/宽高比/分辨率在生成页或 API 设置，不进入提示词（例外：Ultra Long 模式在提示词顶部重申时长与比例——见 `seedance-25.md` §2）。

## 4. 细节法则（先读这个）

> **细节强化情绪。懒惰杀死提示词。**

Seedance 不渲染抽象。它渲染**具体实体性质**。每个形容词必须是感官事实。每种情绪必须落在身体上。每个镜头至少要拥有三个具体细节：

1. **一个环境压力。** 冰箱冷蓝光。沸水上的蒸汽。湿沥青。闪烁的荧光灯。滴水的水龙头。空调风里呼吸的窗帘。
2. **一个身体微观动作。** 下颌锁紧。手指敲台面。攥叉子的指节发白。嘴唇抿成一条线。他用力咽了一下。
3. **一个声音锚点或视觉母题。** 2.3 秒处的腹鸣。暗色手机屏上的倒影。打在同一扇窗玻璃上的雨。

镜头一个都没有——它就是填充物。删掉或重写。

禁用、产生糊状的懒惰表达：
- "cinematic, professional, high quality, masterpiece"
- "beautiful lighting"
- "epic scene"
- "amazing visuals"
- "he is sad / he is angry"（无实体转化）

这条规则很硬。Seedance 多镜头提示词失败，不是模型的问题，而是编剧在单个镜头上偷懒了。一个单薄镜头拖垮整段序列。

## 5. 6 步提示词公式（快速场景）

用于单一清晰动作的单镜头 5 秒片段。

```text
Subject. [Who or what]
Motion. [Present-tense verb, one clear action]
Camera. [Movement + framing + lens]
Environment. [Where, props, atmosphere]
Lighting. [Direction + quality + color]
Style. [Realism level, genre reference]
```

用完整句子写，不要标签。Seedance 偏好语法清晰的散文。对剧情/多镜头/角色锁定工作，**改用第 6 节的生产级骨架。**

## 6. 生产级骨架（11 块）

用于任何戏剧作品、多镜头广告、MV 片段或角色锁定片段。每个块对应一种特定失败模式。跳过一块就把那种失败带了回来。

```text
[1] Character lock.
    Use @img1 as the main character reference and preserve the exact same person
    across the whole clip: <face shape, eye color, hair, facial hair, build, distinctive
    features>. Dress him in <exact wardrobe>. No nudity. No glasses (unless reference).
    No extra characters.

[2] Length + genre + editing intent.
    Generate a <duration>-second multi-shot <genre> sequence with <fast / slow / staircase>
    dynamic editing.

[3] Story (one paragraph).
    <Concrete physical events of this clip in present tense. What changes from start to
    end. Name the break point.>

[4] Visual style.
    <Palette, contrast, grain, color temperature, what to avoid (e.g. "no warm yellow
    tones"). Texture cues — realistic skin, food detail, fabric, surfaces.>

[5] Camera style.
    <Camera body / look (e.g. Sony FX3 handheld). Lenses with purpose:
    35mm / 50mm for medium, 85mm for emotional close-ups, 100mm macro for inserts,
    24mm for wide silhouettes. Handheld micro-shake or static. Strict cuts between
    shots. No continuous take.>

[6] Editing style.
    <Hard cuts vs match cuts. Rhythmic escalation. Where the pause lands. Where the
    impact hits. The rhythmic staircase: long → shorter → shorter → pause → impact.>

[7] Audio.
    <Diegetic sounds in order: ambient, micro-actions, impact, silence moment, final
    cue. Examples: stomach growl, refrigerator hum, fork clink, wet thud, abrupt
    silence, distant city ambience. No dialogue / No subtitles / No on-screen text.>

[8] Shot-by-shot timeline.
    Shot 1, 0.0–X.X sec: <framing, lens, camera move, action, environment detail,
                           emotion translated into body>.
    Shot 2, X.X–Y.Y sec: <...>.
    ...
    (See section 7 for the 5-second rhythm template.)

[9] Lighting (recap and specifics).
    <Main source, fill, rim. Direction. Color temperature. What it carries
    psychologically — judgment, isolation, hope, grief.>

[10] Composition.
    <Where the subject sits in frame across shots. Negative space. Reflections.
    Silhouettes. Foreground obstruction. The final image must be named.>

[11] Output specs.
    <Exact duration. Aspect ratio. Realism level. CLI: --resolution 1080p
    --duration 5 --camerafixed false>
```

为什么是 11 块而不是 6 块？每块预防一种特定 Seedance 失败：身份漂移、长镜头塌缩、情绪涂抹、镜头混乱、音频不匹配、节奏漂移。便宜保险。

## 7. 5 秒镜头时间线（节奏模板）

对 5 秒多镜头片段，模型在**5 个镜头节拍**按戏剧微弧线展开时表现最好。把这个时间作为默认脚手架：

```text
0.0–0.8 sec  | Establish     | extreme close-up or insert that anchors emotion / situation
0.8–1.6 sec  | Action        | medium shot, hero moves or reacts
1.6–2.5 sec  | Turn          | new framing reveals the shift (POV, OTS, rack focus)
2.5–3.6 sec  | Reaction      | tight close-up, slow push-in, emotion lands on the body
3.6–5.0 sec  | Climax / hero | hero shot, low angle, slow-mo if earned, final image
```

10 秒片段：结构翻倍，或在高潮前插入一个停顿（停顿胜过速度）。15 秒以上故事：拆成 3 × 5s 片段在剪辑器拼接——在较短的生成中 Seedance 比一条长镜头更可靠。

## 8. 多镜头语法（独有）

Seedance 读出单条提示词内的显式剪切标记，并生成由可见剪切连接的独立镜头。这是它最强的一张牌。单次生成内需要蒙太奇时用它。

支持的剪切标记。

```text
Shot 1. [description]
Cut to. [description]
Camera cut to. [description]
Camera switching. [description]
Lens switch to. [description]
```

行内时间线语法。

```text
[Shot A description] -> Cut to -> [Shot B description] -> Camera cut to -> [Shot C description]
```

示例。

```text
Shot 1. Medium close-up on a tired man in a kitchen. He opens the refrigerator.
Cut to. Macro insert. His hand reaches toward a single sausage on an empty shelf.
Cut to. Over-the-shoulder shot. The fridge light paints his face cold blue.
```

5 秒片段用 2-3 个镜头做紧凑电影化蒙太奇；仅当每个节拍都很短且实体上截然不同时才用 4-5 个镜头节拍（见第 7 节）。硬上限：每次生成 5 个镜头——超过后模型会丢弃或压缩镜头。按时长匹配镜头数（4 个镜头需要 10-15 秒，不是 5 秒）。每个镜头必须与相邻镜头共享一个锚点——同一角色、同一地点或同一灯光配方——否则模型产出断连的片段而不是序列。

## 9. 防糊守护块

Seedance 有时会无视剪切、产出单条连续长镜头，把多个镜头涂抹成一个移动的画面，或让角色身份沿时间线漂移。当它发生时、或在重型多镜头工作预防性地，把这块放在提示词的**最顶部**（块 [1] 之前）：

```text
Important direction:
This must be a clearly edited multi-shot sequence with visible cuts between shots.
Do not generate a single continuous take. Each shot must have a different camera angle
and different framing. Use rapid montage pacing with rhythmic escalation. Keep the same
character appearance throughout. Preserve the same clothing, face, body type, facial
hair, and hairstyle in every shot. The tone is <serious cinematic drama / tragicomedy /
documentary realism / etc.>.
```

这是任何 Seedance 提示词中杠杆率最高的一段。模型在上一次尝试中产糊时，随时加上它。

## 10. `@img1` 角色参考语法

Seedance 2.0 支持用 `@img1`、`@img2` 等行内图片参考。用它锁定主角的相似度，跨多镜头片段的所有镜头、并跨多条拼接片段。

```text
Use @img1 as the main character reference and preserve the exact same man across the
whole clip: <full identity block: face, eyes, hair, facial hair, build, distinctive
features, wardrobe>. No nudity. No glasses (unless in reference). No extra characters.
```

规则。

- 提到 `@img1` 之后必须跟上完整身份块。模型需要文字描述作为备份信号——单靠图片会漂移。
- 在拼接序列的**每条**片段里重复身份块。把每次生成当作在给一位新实习生做brief。
- 多参考（角色+场景、角色+服装）时，逐个标注：`@img1` 是主角，`@img2` 是地点参考，`@img3` 是服装参考。然后行内说明各自职责。
- 2.0 也接受 `@Video1`（动作/风格参考，480-720p）和 `@Audio1`（配音/音乐）标签——用散文说明每个参考的职责，例如"@Audio1 plays as the voiceover"。限制：2.0 共 12 个文件（最多 9 图、3 视频、3 音频）；2.5 最多 50 个。

## 11. 运镜（9 个预设）

- Dolly Out。揭示上下文，拉远。
- Dolly In。推近主体，构建紧张。
- Pan Left / Pan Right。水平揭示，风景、队列。
- Tilt Up / Tilt Down。垂直揭示。
- Tracking。跟随移动主体。
- Crane / Aerial。宏大尺度，建立场景。
- Handheld。纪录片、亲密、UGC。
- Zoom In / Zoom Out。紧张或细节。
- Hitchcock Zoom。"dolly out while zooming in"，眩晕效果。
- Static（通过 `--camerafixed true`）。锁定画面。

克制组合。5 秒内多次运镜很少能干净完成。

## 12. 负面提示词

Seedance 1.0 Pro **不支持**负面提示词。`--no blur` 这类语法无效。

Seedance 2.0 加了有限负面提示词支持，但脆弱且常被无视。

1.x/2.0 的绕行。始终反转成正向表达。不写"no yellow tones"，写"cold blue-gray palette with desaturated skin tones."不写"no distorted hands"，写"anatomically correct hands with clear finger separation."

**Seedance 2.5 修好了这一点。** 直接禁令是可靠的："pure video, no subtitles, no background music"真正能压制它们，具体的禁止清单（"no exaggerated crying, no fast cuts"）是 2.5 官方提示词结构的核心部分。见 `seedance-25.md` §7。

## 13. 图生视频法则

使用参考图时，**不要**描述图中已可见的元素。模型看得见。只描述动作和运镜。复述静态元素会制造身份漂移。

差。"A man in red shirt stands in kitchen. He walks to the fridge."
好。"He slowly walks toward the fridge, opens it with hesitation, freezes when he sees the empty shelves. Tracking shot from behind, 35mm."

## 14. 音频（1.5+）

Seedance 1.5 Pro、2.0 和 2.5 生成原生音频并支持口型同步。在提示词正文中包含音频提示——把提示词当作声音 brief。

```text
Audio. fridge hum, distant rain on window, one stomach growl at 2.3 sec, final silence.
```

规则：

- 对白在 1.5/2.0 上放**双引号**里——模型会配音、生成声线并把口型同步到剪切。写明表达方式："Play her line dry and a little proud, his quiet and worn out."**2.5 上用专用标记**：对白用 `{ }`、音效用 `< >`、音乐用 `( )`、标题用 `【 】`（见 `seedance-25.md` §4）。
- 台词要短。长独白会漂移出同步——拆成多句并用剪切保持同步。对以台词为先的工作仍不如 Veo 稳。
- 不想要配乐时显式写 **"no music"**——否则模型会在一切下面铺一段广告型配乐。
- 字幕：描述配音后，要求"text along the bottom edge, timed to the voice"。

## 15. 失败模式与修复

### 要求多镜头却产出单条连续长镜头

修复。加显式 "Cut to" 标记。写 "multi-shot sequence with visible hard cuts. Do not generate a single continuous take."

### 镜头间角色漂移

修复。在提示词内每个镜头边界重复完整身份块。

### 5 秒以下动作被无视

修复。任何含多动作或运镜的场景最短时长 5 秒。

### 负面措辞被无视

修复。用正向替代。Seedance 1.0 无负面解析器。

### 5 秒内 4+ 镜头多镜头失败

修复。紧凑电影化控制在每 5 秒片段 2-3 个镜头，或按第 7 节时间线做 4-5 个短节拍。需要更多镜头就拆成多次生成。

### 情绪涂抹/"看起来都一样"

修复。每个镜头需要独特的情绪功能（Establish / Power / Pressure / Detail / Reaction / Shift / Impact / Aftermath——见 dramaturgy.md §10，第 2 层）。若相邻两个镜头功能相同，模型会把它们平均成同一画面。每次剪切都要变化功能与取景。

### 懒惰抽象措辞产出死气沉沉的片段

修复。应用细节法则（第 4 节）。审计草稿：每个镜头必须有一个环境压力、一个微观动作、一个声音或视觉母题锚点。把"dramatic"、"intense"、"beautiful"这类形容词换成具体实体事实。

### 人脸被拒绝或劣化（2.0）

2026 深度伪造整治后，2.0 对人脸、头盔、太阳镜及任何类似受保护 IP 或名人相似度的内容过滤极激。修复。把人脸密集的剧情路由到 Seedance 2.5（真实人物是招牌特性）、1.5 Pro、Kling 或 Veo；2.0 留给场景、建筑、产品和蒙太奇工作。只用自有或合成角色参考——IP/名人过滤在 2.5 上同样存在。

## 16. 工作示例。15 秒悲喜剧，3 × 5s 片段

15 秒叙事**永远**不是一条提示词。它是三条自包含的 5 秒提示词，每条带完整角色锁定、完整视觉风格、完整音频块和不同的戏剧功能。在剪辑器里拼接。

### 故事脊柱
- 节拍 1（片段 A，0-5 秒）。饥饿。主角打开近乎空的冰箱。发现一根孤独的香肠。绝望翻转为希望。
- 节拍 2（片段 B，5-10 秒）。烹饪。锅、水、火、香肠、咕嘟声、期待，用叉子挑起香肠的主角镜头。
- 节拍 3（片段 C，10-15 秒）。灾难。香肠滑落、掉地、湿闷一响。窗。卧室。饿着入睡。切黑。

### 片段 A。饥饿（应用生产级骨架）

```text
Important direction:
This must be a clearly edited multi-shot sequence with visible cuts between shots.
Do not generate a single continuous take. Each shot must have a different camera angle
and different framing. Use rapid montage pacing.

Use @img1 as the main character reference and preserve the exact same man across the
whole clip: bald head, gray-green eyes, round expressive face, moustache, long black
braided goatee, short dark side hair tufts, slightly overweight build, tragicomic face.
Dress him in a dark oversized T-shirt and dark sweatpants. No nudity. No glasses.
No extra characters.

Generate a 5-second multi-shot tragicomic cinematic sequence with fast dynamic editing.

Story:
The man is hungry at night. He suddenly goes to the refrigerator, opens it, feels
disappointment because it is almost empty, then notices one lonely sausage and becomes
instantly hopeful.

Visual style:
Cold night kitchen. Blue-green refrigerator light. Desaturated colors. No warm yellow
tones. Slightly harsh LED reflections. Realistic cinematic look. High contrast but
natural skin texture. Subtle film grain. Realistic food detail.

Camera style:
Sony FX3 handheld look. 35mm and 50mm lenses for medium and close shots. 100mm macro
for inserts. Handheld micro-shake. Visible cuts between shots.

Editing style:
Fast montage with hard cuts. Each shot a different angle and framing. Tense rhythm,
escalating to the moment of discovery.

Audio:
Deep stomach growl, soft room tone, refrigerator hum, quiet footsteps, fridge door
sound. No dialogue. No subtitles. No on-screen text.

Shot 1, 0.0–0.8 sec. Extreme close-up of the man's eyes in darkness. He is awake,
hungry, tense. Static close shot, faint blue ambient light.
Shot 2, 0.8–1.6 sec. Medium handheld side shot. He sits up and walks fast to the
kitchen. Slight shake, push-in.
Shot 3, 1.6–2.6 sec. POV from inside the refrigerator. The door opens toward camera.
Cold blue-green light hits his face. Shelves almost empty. His face drops.
Shot 4, 2.6–3.5 sec. Rapid inserts: empty shelf, empty container, lonely sauce stain,
his sad eyes, his hand moving items aside.
Shot 5, 3.5–5.0 sec. Macro insert of one single sausage in the corner. Rack focus
from empty shelf to sausage. Smash cut to a slightly low-angle close-up of his face.
His eyes widen, despair flips to joy, tiny victorious smile.

Lighting:
Dark apartment, very low ambient fill. Main source is cold refrigerator light,
blue-green, top-front. Strong contrast. No warm kitchen light.

Composition:
Tight close-ups and inserts. Negative space inside the empty fridge. Final face shot
heroic and absurd.

--resolution 1080p --duration 5 --camerafixed false
```

片段 B 和 C 采用相同结构，带各自的故事段落、镜头列表与最终画面。角色锁定与视觉风格块在每条片段里**逐字**重复——Seedance 在生成之间没有记忆。

### 旧版单片段骨架（为快速场景保留）

单镜头非剧情镜头或快速测试，原始 6 步骨架仍可用：

```text
Subject. [identity block with face, hair, clothing, distinguishing features].
Motion. [one clear present-tense action for the scene].
Camera. Shot 1. [framing, lens, movement]. Cut to. Shot 2. [framing, lens, movement]. Cut to. Shot 3. [framing, lens, movement].
Environment. [location, time of day, props, weather].
Lighting. [dominant source, direction, quality, color].
Style. [realism level, genre reference, palette].
Audio. [ambient, SFX, silence moments]. (1.5+ only)
Continuity. [what must remain constant across shots].

--resolution 1080p --duration 5 --camerafixed false
```

对剧情、多镜头、角色锁定或拼接片段工作——一律用第 6 节的生产级 11 块骨架。

## 17. Seedance 2.5 → 读 `seedance-25.md`

2.5 改变了工作流：过去要 3-6 条拼接片段的 15-30 秒叙事，现在是单次生成带一条连续弧线，可延长到 60 秒，另有独立 Ultra Long 模式到 180 秒。戏构不变——`dramaturgy.md` §10 的节拍图搬进单条提示词。

所有 2.5 专属内容都在 **`seedance-25.md`**：官方提示词公式、`( ) < > { } 【 】` 标记、50 槽参考纪律、阶段+结束状态、视频编辑、延展、Ultra Long、白模/绿幕流程、官方工作示例。任何 2.5 生产任务，写提示词前先读那份文件。

---

*作者：Serge Shima（[t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)）· 许可：CC BY 4.0 —— 需注明出处 · 来源：[smixs/visual-skills](https://github.com/smixs/visual-skills)*
