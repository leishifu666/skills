# Veo 参考（Google）

## 目录

1. Veo 是什么
2. 版本与规格
3. 提示词结构与长度
4. 对白语法（关键，独有）
5. 音效语法
6. JSON 提示词（强大，独有）
7. 图生视频（Veo 3.1）
8. 参考素材 ingredients（3.1）
9. 失败模式与修复
10. 骨架与示例

---

## 1. Veo 是什么

Google 的电影化视频模型，带**原生同步音频**。唯一一个生成与视频同步的对白、音效与音乐并原生口型同步的主流生成器。最适合商业打磨、带对白的叙事和电影化音频。

## 2. 版本与规格

- Veo 3. 文生视频、原生音频、4 / 6 / 8 秒片段。
- Veo 3.1. 增加带 First Frame 的图生视频、音频改进、参考素材 ingredients、更强的动作连贯性。

时长。4、6 或 8 秒。
对白预算。每片段口播音频最长 8 秒。

## 3. 提示词结构与长度

顺序很重要。开头放主体和相机。质量修饰词放末尾。

```text
[Subject / Action]
+ [Environment / Setting]
+ [Camera / Shot Type / Lens]
+ [Lighting / Atmosphere]
+ [Style / Quality]
+ [Audio]
+ [Duration]
```

甜区。50-200 词。

- 更短提示词 = 更多创作余地、更少控制。
- 更长提示词 = 更紧控制、更高矛盾风险。

## 4. 对白语法（关键）

Veo 是唯一渲染同步唇动与声音的模型。语法很重要。

### 必需格式

双引号 + 引导动词（says、whispers、shouts、mutters、asks）。

```text
A woman says, "Welcome to the future."
He whispers, "Don't move."
She shouts, "Get out!"
```

引导动词后加冒号也行，且往往更可靠。

```text
A woman says: "Welcome to the future."
```

### 声线修饰符

修饰符放在引导动词之前。

```text
He says in a weary voice, "We are fine. We are fine."
She whispers nervously, "I don't want to be here."
He shouts excitedly, "We did it!"
```

### 时间规则

口播音频最长 8 秒。5 秒片段塞太多词，语速会不自然地加快。把台词剪到能放下。

## 5. 音效语法

三种支持格式。按需混用。

```text
SFX: thunder cracks in the distance
Audio: rain on tin roof, distant traffic, one slow breath
(a loud thunderclap)
(key turning in a lock)
(wet footsteps on concrete)
```

用标签 `Audio:`、`Says:`、`SFX:` 把声音指令与视觉指令分开。模型需要一个显式信号说明要生成音频。

## 6. JSON 提示词（强大，独有）

Veo 解析结构化 JSON。这防止"概念渗漏"——描述情绪时意外改变物体颜色。对需要严格连贯性的复杂场景用 JSON。

### 完整模式

```json
{
  "version": "veo-3.1",
  "output": {
    "duration_sec": 8,
    "fps": 24,
    "resolution": "1080p",
    "aspect_ratio": "16:9"
  },
  "global_style": {
    "look": "cinematic naturalism",
    "color": "cold blue-gray palette, desaturated skin",
    "mood": "quiet domestic tragedy",
    "reference": "Fincher-style motivated camera"
  },
  "continuity": {
    "characters": [
      {
        "id": "man",
        "description": "40s, tired eyes, stubble, dark blue t-shirt, grey sweatpants, barefoot"
      }
    ],
    "props": ["empty refrigerator", "single sausage", "chipped white plate"],
    "lighting_constant": "cold fridge light as key"
  },
  "scenes": [
    {
      "id": "01",
      "start": "0.0",
      "end": "3.0",
      "shot": {
        "type": "medium close-up",
        "framing": "eye-level, slightly offset",
        "camera": "slow push-in, 50mm"
      },
      "action": "He opens the fridge. His face catches the cold light. His eyes stop on the empty shelf.",
      "environment": "small kitchen, 3am, rain outside window",
      "lighting": "cold fridge light as key, warm window spill as rim",
      "audio": "fridge hum, distant rain, one stomach growl"
    },
    {
      "id": "02",
      "start": "3.0",
      "end": "8.0",
      "shot": {
        "type": "extreme close-up",
        "framing": "macro insert on hand",
        "camera": "static, 100mm macro"
      },
      "action": "His hand hovers over a single sausage. He picks it up slowly, exhales.",
      "environment": "inside the fridge",
      "lighting": "cold fridge light, high contrast",
      "audio": "quiet breath, soft plastic crinkle"
    }
  ]
}
```

### 什么时候用 JSON

- 一次生成内多个场景。
- 跨镜头严格角色连贯性。
- 必须保持同色同尺寸的复杂道具。
- 当散文提示词加情绪词时主体颜色一直变。

不是每条 Veo 提示词都需要 JSON。简单片段用散文更快、常常更好。

## 7. 图生视频（Veo 3.1）

用静态图作为 First Frame。提示词引导动作和声音。

规则。

- 不要复述静态元素。
- 只描述动作、运镜、光变和音频。
- 加 "maintain the subject from the first frame" 保护身份。

示例。

```text
Maintain the subject from the first frame. Slow push-in, 50mm. She exhales, her eyes shift to the left, one strand of hair falls across her forehead. Warm rim light grows stronger.

Audio: soft breath, distant traffic, one door closing in the next room.
Duration: 6 seconds.
```

## 8. 参考素材 ingredients（3.1）

上传多张参考图（角色、地点、道具）并在提示词里打标签。

```text
The character from reference_1 walks into the location from reference_2 holding the object from reference_3.
```

需要具体角色在具体地点拿着具体物件时用。

## 9. 失败模式与修复

### 对白语速不自然加快

修复。剪台词到匹配 8 秒自然语速。朗读取检验。

### 输出缺少音频

修复。加显式 `Audio:`、`SFX:` 或 `Says:` 标签。别假设模型会从视觉描述推断音频。

### 运镜指令被无视

修复。提示词开头放运镜。"Wide aerial shot" 在开头胜过 "cinematic camera work" 在中间。

### 加情绪词时角色颜色变化

修复。改用 JSON 提示词。把角色描述锁在 continuity 块里。把情绪放在 global_style，使它不会渗入物体颜色。

### 口型同步偏移

修复。检查引导动词。"She says, ..." 优于只写引语。冒号形式常比逗号可靠。

### 提示词太长，模型挑挑拣拣

修复。压缩到 50-100 词范围。或改用 JSON——结构分离让它更能容纳长度。

## 10. 骨架

### 散文版

```text
[Subject performing action] in [environment]. [Camera framing + lens + movement]. [Lighting direction + color temperature]. [Style + mood + palette].

Audio: [ambient sounds, SFX, music texture].
Says: [character] says, "[dialogue, max 8 seconds of speech]."
SFX: [punctual sound events].

Duration: [4 / 6 / 8] seconds.
```

### JSON 版

见第 6 节。复制模式并填写。

### 工作示例。商业主角镜头

```text
A woman in a cream silk blouse stands in front of a morning window, lifting a ceramic coffee cup to her lips. Medium close-up, 85mm, slow push-in. Warm window key from frame-left, soft bounce fill from frame-right. Cinematic naturalism, creamy palette, shallow depth of field.

Audio: distant city ambience, ceramic clink, one slow breath.
Says: She whispers to herself, "One more minute."
SFX: (spoon tapping ceramic at 2 seconds).

Duration: 6 seconds.
```

---

*作者：Serge Shima（[t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)）· 许可：CC BY 4.0 —— 需注明出处 · 来源：[smixs/visual-skills](https://github.com/smixs/visual-skills)*
