# Nano Banana — 专属规则

三档层级。「思考型」模型 — 理解意图、物理规律、构图。

| 层级 | Model ID | 角色 |
|-----|----------|------|
| **NB2 Lite** | `gemini-3.1-flash-lite-image` | 最快最便宜（$0.034，约 4 秒），仅 1K。草稿、批量任务 |
| **NB2** (Flash) | `gemini-3.1-flash-image` | 默认主力：以 Flash 速度提供 Pro 功能（文字、4K、接地、一致性） |
| **NBP** (Pro) | `gemini-3-pro-image` | 顶级：复杂多层场景，最多 reasoning 与控制 |

## 提示词风格

自然语言，1-2 段。结构自由，但顺序有助益：
**Subject + Action + Location/context + Composition + Style**

```
A cinematic wide shot of a futuristic sports car speeding through a rainy
Tokyo street at night. Neon signs reflect off wet pavement and metallic
chassis. Format: 16:9.
```

## 不要指定的内容

- 数字镜头参数：**50mm、85mm、f/2.8、ISO 400** — NB 会忽略。改用描述：「shallow depth of field」、「wide-angle distortion」。
- Tag-soup：「cool, modern, 4k, cinematic」 — 用连贯句子写。

## 独有能力

### 图像接地 (仅 NB2)
NB2 生成前会在互联网上查找真实图像。特定地点的建筑精确性，正确的动植物种类。

```
Generate a cinematic, golden-hour photograph of [SPECIFIC REAL PLACE].
Ensure the architectural details, the spire, the surrounding square, and
the landscape are accurate to reality.
```

**有效：** 建筑、桥梁、广场、动物种类、植物种类、昆虫。
**无效：** 具体人物。

### 极限宽高比 (仅 NB2)

1:8、8:1、1:4、4:1 — 用于横幅、长页、漫画条。

```
Create a 4-panel horizontal comic strip (aspect ratio 4:1).
The story follows [CHARACTER] doing [ACTION] that ends with a twist.
Use a vibrant comic book style. Keep character design consistent.
```

标准比例：1:1、3:2、2:3、3:4、4:3、4:5、5:4、9:16、16:9、21:9。

### 思考模式

默认开启；NBP 无法关闭（模型在后端绘制至多 2 张「thought images」，不计费为图片，但 thinking 令牌收费）。NB2 有 `thinking_level: minimal | high` 杠杆（默认 `minimal`）— 以下情况调至 `high`：
- 结果含糊、需要推理
- 需要空间逻辑的复杂信息图
- 接地 + 空间推理同时进行

### 多参考图 (按层级限制)

| | NB2 Lite | NB2 | NBP |
|---|---|---|---|
| 高保真物体 | 至 14 | 至 10 | 至 6 |
| 角色一致性参考 | 无 | 至 4 | 至 5 |
| 风格参考 | 无 | 无 | 至 3 |

```
[Image 1: face]
[Image 2: outfit]
[Image 3: background]
Combine: face from Image 1, outfit style from Image 2, setting from Image 3.
Match lighting and perspective.
```

### 复杂场景用 JSON (5+ 元素)

```json
{
  "subject": {"description": "main subject", "expression": "emotion/pose"},
  "photography": {"angle": "eye-level", "shot_type": "waist-up", "aspect_ratio": "16:9"},
  "background": {"setting": "location", "lighting": "soft natural"}
}
```

## Nano Banana 的编辑

对话式，无需蒙版：

```
Remove [OBJECT] from this image.
Fill with [LOGICAL REPLACEMENT] matching surroundings.
Keep [PRESERVED ELEMENTS] exactly the same.
```

生成后迭代补充：
- 「Make it warmer」
- 「Increase contrast」
- 「Soften background, add blur」
- 「Change headline color to #3b82f6」

Interactions API 保持会话上下文 — 至多 3 次连续修改可堆叠而不丢失原图。规则「Edit, don't re-roll」：图片完成度 80% — 请求点状修改而非重新生成。

## 文字渲染

- 100+ 语言的 SOTA。
- 可点名字体：「Century Gothic 12px」、「Brush Script」、「Impact」、「Heavy blocky sans-serif」。
- 单帧多语言可用。
- Hack：复杂文字先请模型**写出文字**，再用单独提示词「把这段文字放进图片」。

## 分辨率 / 成本

| 分辨率 | 用途 |
|------------|---------------|
| 0.5K | 最便宜，批量与 A/B 变体 |
| 1K | 默认 |
| 2K | 终选 |
| 4K | 印刷、hero 素材 |

**工作流：** 先用 `0.5K` flash 跑一遍变体（或用 NB2 Lite 跑 1K）→ 精选 → 在 `2K`/`4K` 重生成优胜者。

API 中 `image_size` 必须严格大写 K（`1K`、`2K`、`4K`) — `1k` 会被拒绝。`512px` 仅 NB2 有；Lite 只有 1K。不指定尺寸时模型匹配输入，否则 1:1。

## 视频关键帧

Nano Banana 是 motion 层之前的 image 层。一切关键内容都必须在动画**之前**固定在图片上：identity、构图、宽高比、可见文字、产品状态。视频模型会放大静帧的任何歧义。

- **角色表 / hero 帧。** 先定一张角色基准帧，后续所有视频提示词都引用它。
- **宽高比一开始就用目标值。** 活动需要竖版视频 — 直接生成 9:16，而非动画后再裁剪（静默失效点）。
- **交给视频模型的是 motion brief，不是复述。** 相机运动、主体运动、背景运动、时长、frame lock、禁止变更。视频提示词不重复描述画面里已存在的内容。
- Downstream 任意：Veo 3.1、Kling 3.0、Seedance 2.0/2.5、Gemini Omni Flash（Google 标配搭档，10 秒短片）。图片批次 → 评审门 → 只有获批的静帧进入视频。

## 已知失效点

- 手和脸仍会漂移(手指、关节、likeness 漂移) — 明确的解剖指令 + 参考图 + 重生成。有报告称 NBP 人脸保持不如 NB2。
- 小字在 1K 模糊 — 密集文字用 2K+ 或 GPT Image 2.5。
- 信息图可能含事实错误数据 — 数字永远要人工核验，grounding 有帮助但不保证。
- 倾向 overcooked HDR / 过饱和 — 要求「natural contrast, no HDR look」。
- 所有生成物带 SynthID 水印（隐形）；Vertex 上另有 C2PA。

## 何时从 NB2 切换到 NBP

- NB2 应付不了复杂的多层提示词。
- 需要最多参考图并按角色分组（6 物体 + 5 角色 + 3 风格）。
- 材质与光效要求极精细的写实图。
- NBP 更慢更贵；人脸上有时不如 NB2 — 人像系列先两者都测。

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
