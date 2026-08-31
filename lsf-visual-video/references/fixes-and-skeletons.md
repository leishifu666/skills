# 修复、清单与跨模型骨架

## 目录

1. 连贯性清单（最终输出前）
2. 常见失败与修复
3. 跨模型提示词骨架
4. 默认负面约束
5. 提示词压缩次序
6. 输出格式模板

---

## 1. 连贯性清单

把提示词发给用户前，核查。

- 镜头间同一角色（脸、身体、头发）。
- 镜头间同一服装，确切命名。
- 一致的地点逻辑。
- 物件状态演进合理（冰箱里的香肠 -> 盘中 -> 叉上 -> 地上）。
- 无多余角色。
- 无多余文字或字幕。
- 无多余 logo。
- 年龄/身体/脸一致。
- 无不可能的物件-手动作。
- 无含糊运镜指令（"cinematic camera"）。
- 无含糊灯光指令（"beautiful light"）。
- 无随机堆叠导演参考。
- 无矛盾。
- 色板用具体颜色定义。
- 最终画面明确写出。

任何一项缺失，发送前修复。

---

## 2. 常见失败与修复

### 要求蒙太奇却产出单条连续长镜头

修复。

```text
This must be a multi-shot sequence with visible hard cuts. Do not generate a single continuous take. Each beat uses a different angle and framing.
```

针对 Seedance：在提示词正文加显式 `Cut to.` 或 `Camera cut to.` 标记。

### 镜头间角色脸变化

修复。

```text
Preserve the exact character in every shot. Same face shape, same eye color, same hair, same clothing, same expression style. [repeat the full identity block]
```

针对 Kling。用 Element Binding + 3-4 张参考图（正面、侧面、四分之三）。

### 物件在场景中途消失

修复。

```text
Track the object continuously. The same object remains visible or clearly implied in every beat.
```

用一句话描述物件状态演进。"The sausage moves. fridge -> pot -> fork -> floor."

### 戏剧薄弱。场景平淡。

修复。

```text
Play the scene with full emotional seriousness. Treat the ordinary object as if it carries life-or-death meaning. No comedy pacing. No detached observation.
```

### 快速蒙太奇中凌乱随机剪切

修复。

```text
Use fast montage with clear readable action per cut. Every cut shows a distinct detail. face, hand, object, reaction, impact. Each cut must have a visible function.
```

### 对白太快（Veo）

修复。剪台词。口播文字最多 8 秒。以正常语速朗读取检验。

### 手融化/多指

针对 Kling。加到负面字段。

```text
distorted hands, extra fingers, melted face, deformed
```

针对 Seedance 和 Veo。用正向措辞。

```text
anatomically correct hands, clean finger separation, realistic proportions
```

### 灯光在片段间漂移

修复。点名主导光源与方向，并在每条片段逐字重复。

```text
Lighting constant. Cold fridge light as key from frame-right. Warm window spill as rim from frame-left. Same contrast ratio in every shot.
```

### 模型无视运镜指令

修复。把运镜移到提示词前面。

差。"A man opens a fridge. The camera is a slow push-in."
好。"Slow 50mm push-in. A man opens the fridge."

### 怪怪的 AI 脸

修复。避免"hyperrealistic 8k masterpiece"这类风格词。它们把模型推向 AI 艺术区。改用制作语言。

```text
Shot on 50mm, natural skin texture, motivated lighting, documentary feel.
```

### 多人场景中的双胞胎/脸部融合

两个或更多角色收敛成近乎相同的脸，或背景群演克隆主角。

修复。把每个主体单独绑到自己的参考（见 `universal-rules.md` U13），再强制差异化。

```text
Their movements are not synchronized. Clothing colors, hairstyles, and facial features must all be distinct. No identical clones in the background.
```

### 延展中物件或角色过早出现

向后延展（前置开头）时，属于源视频的元素会泄漏进过去。

修复。显式标记它们。

```text
<Materials that should appear only after the source video begins> must not appear early in the backward extension.
```

向前延展用标准条款："prohibit rigid cutting, prohibit objects appearing out of thin air."

### 随机字幕或不想要的背景音乐

修复。直接禁止并在提示词末尾重复禁令。

```text
Pure video, no subtitles, no background music.
```

Seedance 2.5 和 Veo 上可靠。Seedance 1.x/2.0 和 Kling 上，还要避免提起任何你不想要的屏幕上文字或配乐——一提就被召唤出来。

---

## 3. 跨模型提示词骨架

### Seedance

```text
Subject. [identity block].
Motion. [one clear present-tense action].
Camera. Shot 1. [framing, lens, movement]. Cut to. Shot 2. [framing, lens, movement]. Cut to. Shot 3. [framing, lens, movement].
Environment. [location, time, props].
Lighting. [source, direction, quality, color].
Style. [realism level, genre reference].
Audio. [ambient, SFX]. (1.5+ only)
Continuity. [what must remain constant].

--resolution 1080p --duration 5 --camerafixed false
```

### Kling 文生视频

```text
[Subject with identity anchor]. [Subject movement]. Scene. [3-5 environment elements]. Camera. [one movement + lens]. Lighting. [source + quality]. Atmosphere. [mood].

Negative field. blurry, distorted hands, extra fingers, melted face, watermark, subtitles, jitter.
```

### Kling 图生视频

```text
Preserve [silhouette / feature / label]. [Camera movement, one lens]. [One or two motion verbs]. [Atmospheric cue, light change].

Negative field. blurry, distorted hands, melted face, jitter.
```

### Veo 散文

```text
[Subject performing action] in [environment]. [Camera framing + lens + movement]. [Lighting direction + color]. [Style + mood + palette].

Audio: [ambient, SFX, music texture].
Says: [character] says, "[dialogue, max 8s of speech]."
SFX: [punctual sound events].

Duration: [4 / 6 / 8] seconds.
```

### Veo JSON

完整模式见 `references/veo.md` 第 6 节。

---

## 4. 默认负面约束

负面受支持的地方（Kling 字段、Veo 正文、Seedance 2.0 弱支持）。

```text
No subtitles. No on-screen text. No extra characters. No changing clothes. No changing face. No logos. No cartoon physics unless requested. No warm yellow tones unless requested. No random camera drift. No single-take when multi-shot is requested. No distorted hands. No extra fingers.
```

Kling 字段。改写成正向实体。"distorted hands, extra fingers, subtitles, logos, cartoon physics, random camera drift."

Seedance 1.0。把提示词正文里所有否定反转成正向措辞。

---

## 5. 提示词压缩次序

模型偏爱短提示词时（Kling 2.5 Turbo、Kling 1.6、任意图生视频），按此次序削减。

1. 保留角色连贯性。
2. 保留故事动作。
3. 保留镜头时间码（相关时）。
4. 保留灯光。
5. 保留运镜。
6. 保留剪辑语法。
7. 保留声音。
8. 删除哲思与元评论。
9. 删除多余形容词。
10. 删除导演参考。

目标。保留骨架。去掉香水。

---

## 6. 输出格式模板

### 格式 A。单条提示词

一次生成的一条可直接复制的提示词。用相应模型骨架。

### 格式 B。多片段提示词

一系列自包含提示词。每条重复完整连贯性模块。标注 `Clip 1 / 5`、`Clip 2 / 5` 等。

片段之间，加一行注释说明它们如何接在一起。"Clip 1 ends on his hand reaching into the fridge. Clip 2 opens on his hand already inside the fridge, same light."

### 格式 C。分镜表

表格，列如下。

| Time | Shot | Function | Action | Camera | Light | Sound | Emotion |
|---|---|---|---|---|---|---|---|
| 0-1s | WS | Establish | Man walks to fridge | 35mm, slow push-in | Cold fluorescent overhead | Fridge hum | Exhaustion |
| 1-2s | MCU | Reveal | He opens fridge door | 50mm, static | Cold fridge light as key | Door seal pop | Anticipation |

按片段长度调整行数。

### 格式 D。提示词审查

给定用户提示词。返回六个部分。

1. 可行之处。
2. 破坏生成之处。
3. 缺失的导演指令（运镜、灯光、连贯性）。
4. 连贯性风险。
5. 模型特定不匹配（所选模型的错误语法）。
6. 更强版本。重写的提示词，可直接复制。

### 格式 E。导演阐述

用于写任何提示词之前的概念阶段。

- 核心概念（一句话）
- 情感弧线（三个状态）
- 视觉母题（一个反复元素）
- 节奏（节奏逻辑）
- 运镜语言（主导语法）
- 灯光（主导光源）
- 声音（质感）
- 结束画面（最终帧）

### 格式 F。Veo JSON

逐场景结构化 JSON。用于复杂连贯性。见 `references/veo.md` 第 6 节。

---

*作者：Serge Shima（[t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)）· 许可：CC BY 4.0 —— 需注明出处 · 来源：[smixs/visual-skills](https://github.com/smixs/visual-skills)*
