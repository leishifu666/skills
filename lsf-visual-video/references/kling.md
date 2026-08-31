# Kling 参考（快手）

## 目录

1. Kling 是什么
2. 版本与元素上限
3. **Kling 3.0——多镜头、原生音频、15 秒（用户在用 3.0 时先读）**
4. 提示词公式（1.x – 2.x）
5. 各模型提示词长度
6. 负面提示词（专用字段，特殊规则）
7. 元素库与 Element Binding（1.x – 2.x 独有）
8. Motion Brush（独有）
9. Motion Control（2.6 Pro，独有）
10. 图生视频法则
11. 失败模式与修复
12. 骨架与示例

---

## 1. Kling 是什么

真实物理、角色动画、经参考图实现一致性方面很强。生成快。最适合社媒即用片段和常驻角色场景。

**Kling 3.0** 根本上改变了模型定位——现在它用多镜头输出（每次生成最多 6 个镜头）与 Seedance 竞争，用原生对白和口型同步与 Veo 竞争。见第 3 节。

## 2. 版本与元素上限

Kling 各模型能处理的单条提示词中独立元素数量差异巨大。塞太多会产出融化脸、坏手或静止动作。

- **Kling 1.6.** 简化提示词。保持极简。
- **Kling 2.1 Pro.** 30fps 1080p。Motion Brush。尾帧控制。
- **Kling 2.5 Turbo Pro.** 最多 3-4 个独立元素。
- **Kling 2.6 Pro.** 5-7 个元素。Motion Control。角色一致性用 Element Binding。
- **Kling 3.0.** 一次生成内多镜头（最多 6 个）。带对白与口型同步的原生音频。15 秒连续输出。原生 4K，最高 60 fps。角色与场景一致性最强。两档：v3/pro 和 v3/standard。
- **Kling 3.0 Turbo**（2026 年 6 月）。速度/价格档：基础价含音频、头部口播的口型同步明显更好、3-15 秒，但上限 1080p——无 4K。
- **Kling 3.0 Omni**（2026 年 6 月）。参考+剪辑旗舰（API 别名 `o3`）：最强输入理解、3-15 秒剪辑管道 4K 进出、带声音绑定的 Elements 3.0（见第 7 节）。

不确定用户的版本就问。1.x – 2.x（第 4-9 节）与 3.0（第 3 节）的提示词协议不同。

## 3. Kling 3.0——多镜头、原生音频、15 秒

Kling 3.0 是另一种生物。它理解电影化意图，不只是视觉描述。提示词读起来像场景指令，不是物件清单。

### 相比 2.x 的变化

| 能力 | 1.x – 2.6 | **3.0** |
|---|---|---|
| 一次生成内多镜头 | 否（单条连续长镜头） | **是——最多 6 个镜头** |
| 原生音频 | 有限/关闭 | **是——对白、环境音、声线** |
| 口型同步 | 无 | **是——跨多角色场景连贯** |
| 最大时长 | 5-10 秒 | **最长 15 秒** |
| 角色标记 | 经元素库 + 参考图 | **经提示词内 `[Character A: ...]` 标签**（仍支持参考） |
| 电影化语言理解 | 部分 | **完整——能读"shot-reverse-shot"、"POV"、"tracking shot"、"macro close-up"** |

### 五层提示词结构

```text
Scene  →  Characters  →  Action  →  Camera  →  Audio
```

每层用带显式标签的流畅散文写作。

### 尽早锚定主体

在**提示词开头**、任何镜头描述之前引入每个角色和关键物件。使用唯一一致的标识符——同一标签贯穿所有镜头存活：

```text
[Character A: Exhausted Partner — late 40s, gray-streaked beard, navy peacoat, hollow eyes]
[Character B: Female Investor — early 30s, sharp blazer, calm posture]
```

然后在镜头描述里以 "Character A" / "Character B" 引用。这比每个镜头重新描述角色更好地锁定身份。

### 多镜头语法（按镜头思考，不是按片段）

```text
[Character A: ...]
[Character B: ...]

Master intent: tense negotiation in a glass-walled office at dusk.

Shot 1 (0-3s). Wide tracking shot. Character A enters frame from left, crosses to the table.
Shot 2 (3-6s). Profile close-up on Character A. He sets down a brown leather folder.
Shot 3 (6-9s). Shot-reverse-shot. Cut to Character B's face. She does not blink.
Shot 4 (9-12s). Macro insert on her hand tightening around a fountain pen.
Shot 5 (12-15s). Two-shot, low angle, both reflected in the glass wall behind them.

Camera. Slow, deliberate. Sony FX6 feel, 35mm and 85mm.
Lighting. Cold blue dusk through floor-to-ceiling windows. Single amber desk lamp.
Audio. Distant city ambience. No music. Footsteps on hardwood. Pen clicks on paper.
```

每个镜头必须回答：**取景 + 主体 + 动作**。空镜头描述（"static frame, ambient mood"）会塌缩成单条连续长镜头。

### 对白协议（P1-P4）

任何说话戏，遵守这四条规则。fal.ai 指南称它们为 P1、P2、P3、P4。

**P1. 结构化命名。** 每个角色用唯一标识符。
- ✓ `[Character A: Black-suited Agent]` 和 `[Character B: Female Assistant]`
- ✗ "[Agent] says... Then, he says..."

**P2. 对白前先视觉锚定。** 先把对白绑定到一个独特动作。
- ✓ "Character A pulls a folded note from his pocket and reads aloud: 'It's not what you think.'"
- ✗ "Character A says 'It's not what you think.'"（无视觉锚点 → 口型同步漂移）

**P3. 声线写在标签里。** 内联指定情绪/质感。
- ✓ `[Character A, raspy deep voice]: "We're out of time."`
- ✓ `[Character B, clear fearful voice]: "Don't open it."`
- ✗ `[Man]: "We're out of time."`（含糊——模型选通用声线）

**P4. 台词间的时间控制。** 用连接词防止对白融合。
- ✓ "Character A: 'I won't ask again.' **Immediately,** Character B: 'You don't have to.'"
- ✗ 两条连续 `[Character X]: "..."` 无转场（模型会重叠它们）

### 3.0 图生视频——先锁，再动

输入图充当身份、版式和图上文字的锚点。提示词保持简短并聚焦动作。描述**场景如何从图片演化**，而非图里有什么。

```text
Preserve identity, wardrobe, and the storefront sign exactly.
[Character A: same person from the image]
Shot 1 (0-2s). She turns her head toward camera, exhales.
Shot 2 (2-5s). Slow push-in to a tight close-up. Wind catches her hair.
Audio. Distant traffic, wind through awnings, a soft bell from inside the shop.
```

### 3.0 真正懂的电影化词汇

直接使用这些术语——模型把它们当指令，不是调味料：

- 取景：profile shot、three-quarter、macro insert、two-shot、OTS、POV、low angle、high angle、Dutch
- 剪辑：shot-reverse-shot、match cut、smash cut、J-cut、L-cut
- 运镜：tracking、dolly、push-in、pull-out、whip pan、crane、handheld、orbital / 360 spin、Steadicam、drone-like aerial。复合可行："pan right while tilting up"。
- 镜头质感：35mm、50mm、85mm、100mm macro、anamorphic 40mm
- 模型服从的节奏词："ultra-slow motion"（2-3 秒感）、"slow and deliberate"（5-8 秒）、"moderate"（3-5 秒）、"quick snap"（1-2 秒）；精确时间也可行（"5-second dolly zoom"）。
- 角度承载情绪：low angle = 支配，high angle = 脆弱，eye-level = 中性。按 `dramaturgy.md` §6 的权力动态选，不要随机。
- Kling 应用里，Master Shot 预设（"Move Forward and Zoom Up" 等）比手写运镜散文更稳且省积分——标准运镜用预设，有动机的运镜用散文。

### 默认模型选择

命中以下任何一项——**用 Kling 3.0 而不是更早的 Kling**：
- 多镜头对白场景
- 10-15 秒连续叙事
- 需要口型同步
- 多角色带不同声线
- 图生视频且图上文字必须清晰可读

3.0 家族内：预算内的头部口播和对白 → **Turbo**（单位美元最佳口型同步、含音频、1080p 上限）；参考重型或剪辑工作、4K 交付 → **Omni**；其余 → 基础 3.0。

其余一切（单片段、无对白、< 10 秒、经参考图角色锁定、Motion Brush）——旧版本仍可用且更便宜。

### API 参数（3.0，fal/官方）

- `cfg_scale` 0-1，默认 0.5。0.3-0.4 = 创作自由，0.7-1.0 = 严格遵从提示词（产品/解释类工作）。
- `duration` —— 各镜头时长之和必须 ≤ 15 秒。
- `aspect_ratio` —— 16:9 / 9:16 / 1:1。
- `generate_audio` —— 布尔。没有"no music"开关：模型连负面提示词都无视地铺音乐。要纯净音频就关闭音频生成或后期剥离音轨。

## 4. 提示词公式（1.x – 2.x）

用于 1.6、2.1 Pro、2.5 Turbo Pro、2.6 Pro：

```text
Subject (with specific details)
+ Subject Movement (one clean verb phrase)
+ Scene (3-5 elements max)
+ Camera Language
+ Lighting
+ Atmosphere
```

用流畅散文写。Kling 1.x – 2.x 不喜欢碎片化标签式输入。

Kling 3.0 改用第 3 节的多镜头结构。

## 5. 各模型提示词长度

- 1.6. 保持简单、极少。
- 2.5 Turbo Pro. 最多 3-4 个元素。50-80 词。
- 2.6 Pro. 5-7 个元素。50-80 词。
- 3.0. 欢迎更长提示词——多镜头需要显式结构（见第 3 节）。每镜头计划约 30-60 词。
- 图生视频（任意版本）。20-40 词。更短、聚焦动作。

1.x – 2.x 上的长提示词 = 融化输出。无情压缩。3.0 上，结构胜过长度。

## 6. 负面提示词（关键规则）

Kling 有专用负面提示词字段。该字段自动把输入解释为排除项。不要写"no X"。写事物本身。

差。"no robots"
好。"robots"

差。"no blurry faces, no distorted hands"
好。"blurry faces, distorted hands, melted features"

常见有效负面词。

```text
low resolution, blurry, distorted hands, extra fingers, melted face, watermark, subtitles, logo, text overlay, jitter, shaking camera, deformed
```

清单保持短。长负面堆栈降低动作与细节。

## 7. 元素库与 Element Binding（1.x – 2.x）

为了跨生成的角色一致性，Kling 有元素库。上传角色不同角度的 3-4 张参考图。

必需角度。

- Front（正面）
- Side (profile)（侧面）
- Three-quarter（四分之三侧面）

然后在图生视频设置里开启 "Bind Elements" 锁定特征。这给 AI 一个经得起运镜平移和光线变化的视觉锚点。

源图规则。

- 1080p 或更高。
- 均匀照明。避免硬阴影。AI 可能把它们当永久面部特征。
- 无文字或水印。
- 干净无杂乱的背景。
- 主体居中。
- 对比好。

Kling 3.0——元素库仍有效，但提示词内 `[Character A: ...]` 标签（见第 3 节）通常单独就够。

### Elements 3.0（Omni）

3.0 Omni 上元素系统更深：

- 角色元素要么是一段**3-8 秒视频**（模型提取外观和声音），要么最多 **4 张多角度静帧**（正面、四分之三、侧面、背面），加可选**声音绑定**（5-30 秒音频片段）。一旦绑定，声音就属于该主体——不要在提示词里重新描述它。
- 把角色/产品/地点**一次性**定义为元素，然后在散文中打标签：`@Grace picks up the folder`。提示词只承载动作与运镜；身份活在元素里。
- 画框内容纳 3+ 个不同角色而无特征融合——但只有**每个**都有自己的元素时才行。
- 该特性的代价：多位实践者报告一旦启用元素/参考，画质可见下降。只在一致性真正重要时用元素；一次性片段用提示词内标签更干净。

## 8. Motion Brush（独有）

独立动画一张图的至多 6 个区域。每个区域有独立运动路径。

关键规则。文字提示词必须与画笔运动匹配。若你把河流刷成流动、却写"stagnant pond"，模型会自我撕裂。让提示词动词与画笔方向对齐。

## 9. Motion Control（2.6 Pro，独有）

从参考视频复制动作。需要特定表演或编排（舞蹈、武术、特定步态）时用它。提示词只聚焦主体描述，动作交给参考。

## 10. 图生视频法则

提示词保持短（20-40 词）。只聚焦动作。不要复述模型已看到的静态元素。

包含显式连贯性提示。Kling 对"preserve X"指令反应良好。

示例。

```text
Preserve silhouette and label text. Slow tracking shot from the side. She turns her head toward camera. Wind catches her hair. 35mm, golden hour rim light.
```

Kling 3.0 图生视频——见第 3 节（"3.0 图生视频——先锁，再动"）。

## 11. 失败模式与修复

### 静态场景中随机运镜漂移

修复。写 "locked static frame" 或 "camera fixed, no movement."

### 提示词超模型容量，输出融化

修复。裁到模型合适的元素数。Turbo 3-4 个，2.6 Pro 5-7 个。

### 角色脸在两次生成间变化

修复。向元素库上传 3-4 张参考图。在设置里用 Bind Elements。

### 负面提示词被无视

修复。在负面字段里把"no X"重写为"X"。

### Motion Brush 伪影

修复。检查文字提示词动词是否匹配画笔方向。与动作矛盾就重写文字。

### 元素过载融化手

修复。简化。能合并就合并元素。砍掉次要描述。

### Kling 3.0 把多镜头塌缩成单条连续长镜头

修复。显式化镜头边界：`Shot 1 (0-3s). ... Shot 2 (3-6s). ...`。每个镜头描述必须包含不同取景或机位。相邻两镜头共享取景与机位时，模型会合并它们。

### Kling 3.0 对白口型同步漂移

修复。应用 P2——在台词之前把对白绑定到独特视觉动作（"Character A pulls a folded note from his pocket and reads aloud:"）。然后在连续台词间加 P4 连接词（"Immediately,"）。

### Kling 3.0 选错声线

修复。应用 P3——把声线放进说话人标签：`[Character A, raspy deep voice]:`。泛泛的 `[Man]:` / `[Woman]:` 标签会得到通用声线。

### 启用元素/参考时画质下降

修复。只保留必要的参考；一次性片段优先用提示词内 `[Character A: ...]` 标签而非元素。接受权衡：元素买来的是一致性，不是保真度。

### 两个相似角色一帧内融脸

修复。给每个角色自己的元素（或自己的标签身份块）。绝不让两个说话角色共享一个视觉描述。

### 快动作上的变形伪影

修复。用慢动作生成、后期加速——模型在更慢的内部运动下能保持几何。

### 提示词写了"no music"还是有音乐出现

修复。用负面提示词压音乐不可靠。关掉 `generate_audio` 生成并在后期加声音，或剥离音乐轨。

## 12. 骨架

### 文生视频（1.x – 2.x）

```text
[Subject with identity anchor]. [Subject movement in one clean verb phrase]. Scene. [3-5 environment elements]. Camera. [one movement + lens]. Lighting. [source + quality]. Atmosphere. [mood].

Negative field. blurry, distorted hands, extra fingers, melted face, watermark, subtitles, jitter.
```

### 图生视频

```text
Preserve [silhouette / label / specific feature]. [Camera movement, one lens]. [One or two motion verbs]. [Atmospheric cue, light change].

Negative field. blurry, distorted hands, melted face, jitter.
```

### 工作示例。时尚，图生视频（2.6 Pro）

```text
Preserve silhouette and fabric texture. Slow lateral tracking, 85mm. She turns her head toward camera, exhales through her nose, hair catches golden hour wind. Warm rim light. Confident stillness.

Negative field. blurry, distorted hands, extra fingers, melted face, watermark, motion blur, jitter.
```

### 多镜头带对白（Kling 3.0）

```text
[Character A: Investigator — late 30s, navy raincoat, tired blue eyes, three-day stubble]
[Character B: Witness — early 20s, oversized hoodie, hands wrapped around a paper cup, eyes red from crying]

Master intent: a 12-second interrogation in a fluorescent-lit precinct break room at 2am. The investigator holds back, the witness breaks.

Shot 1 (0-3s). Two-shot, eye level, 35mm. Character A sits across from Character B. Static frame.
Shot 2 (3-6s). OTS over Character A's shoulder. Character B's hands tighten on the paper cup.
Shot 3 (6-9s). Profile close-up on Character A. He slides a photo across the table.
[Character A, low even voice]: "You were there."
Shot 4 (9-12s). Reverse — close-up on Character B. She does not look up.
Immediately, [Character B, fragile broken voice]: "I didn't see anything."

Camera. Locked frames, no movement except the slide of the photo. Sony FX6 feel.
Lighting. Cold overhead fluorescent, slight flicker. Pale skin, hard shadows under the eyes.
Audio. Distant police radio chatter, the buzz of the fluorescent tube, a vending machine humming in the corridor. No music.

Negative field. blurry, distorted hands, extra fingers, melted face, watermark, subtitles, jitter, dialogue overlap.
```

---

*作者：Serge Shima（[t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)）· 许可：CC BY 4.0 —— 需注明出处 · 来源：[smixs/visual-skills](https://github.com/smixs/visual-skills)*
