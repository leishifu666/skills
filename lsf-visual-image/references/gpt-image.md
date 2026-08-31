# GPT Image 2 — 专属规则

生产默认 OpenAI：`gpt-image-2`。仅迁移用：`gpt-image-1.5`、`gpt-image-1`。预算版：`gpt-image-1-mini`。

## 提示词结构 — 5 段式

GPT Image 2 对按段落划分最敏感。用标签写,不要写成一整块文本。

```
Scene: location, time of day, background, environment
Subject: primary focus — who or what is central
Important Details: materials, textures, lighting, camera angle, mood, composition
Use Case: editorial, product mockup, UI, poster, infographic
Constraints: what must NOT change/appear (no watermarks, preserve face, no extra text)
```

>「The fifth slot is where most mediocre prompts fail silently.」没有明确 constraints,模型就会漂移。

### 最小示例

```
Scene: small Lisbon florist storefront at blue hour, wet cobblestones
Subject: woman in navy apron locking the front door, half-turned to camera
Important Details: warm interior glow spilling onto pavement, 50mm feel,
  soft contact shadows, brushed brass door handle, "Florista" hand-painted sign
Use Case: editorial photography
Constraints: no extra signage, no people in background, no text other than the sign
```

## Anti-Slop 规则

GPT Image 2 对措辞质量特别敏感。Vague praise = 结果降级。

| ❌ 不要写 | ✅ 要写 |
|-----------|---------|
| stunning, incredible, epic, gorgeous, masterpiece | overcast daylight, brushed aluminum, chipped paint, 50mm feel |
|「minimalist brutalist luxury photoreal」(风格标签堆砌) |「cream background, heavy black sans-serif, asymmetrical type block, one hero object, generous negative space」 |
|「像苹果广告」 | 具体的视觉事实 |
| 冲淡功能要求的氛围语言 | 直白声明:「image must contain a transit kiosk」 |

## 质量设置 — 保真度 / 延迟的杠杆

| 设置 | 何时用 |
|---------|-------|
| `quality: low` | 大量生成、预览、探索、延迟敏感、草稿 |
| `quality: medium` | **默认起点** |
| `quality: high` | 小号/密集文字、信息图、人像、身份敏感编辑、品牌素材 |

从 `low` 开始,按需升级。往往 `low` 已经足够。

## 尺寸 (gpt-image-2)

- 最长边: <3840px
- 两边: 均为 16 的倍数
- 宽高比: 最大 3:1 (long:short)
- 总像素: 655 360 – 8 294 400
- 可靠上限: 2560×1440

**常见尺寸:**
- 竖幅 1024×1536
- 横幅 1536×1024
- 方形 1024×1024
- 2K 2560×1440

> 1:8 / 8:1 之类的极限比例 GPT Image 2 **不支持** — 用 Nano Banana。

## 图内文字

- 字面文本用 `"..."` 或 ALL CAPS。
- 字体、字号、颜色、位置 — 明确指定。
- 复杂单词与品牌:逐字母拼写。
- 防垃圾:「**no extra words, no duplicate text, no watermarks**」。
- 防不可读小字:「**100 percent readable and physically believable**」。
- 小号/密集/多字体 → 必须 `quality: high`。

<a id="editing--двухколоночная-логика"></a>
## 编辑 — 双栏逻辑

Endpoint：`openai/gpt-image-2/edit`（在 fal.ai 上）或通过 OpenAI API 的对应端点。

```
Change: [single concrete change]
Preserve: face, identity, pose, lighting, framing, background, geometry, text, layout
Constraints: no extra objects, no redesign, no drift
```

**编辑规则:**
- **每轮只做一处编辑。** 不要一次改所有东西。
- **每轮重复 preserve list。** 否则漂移。
- **外科手术式编辑:** 明确列出不要动的项 (saturation、contrast、layout、arrows、labels、camera angle)。
- 可选:`mask_image_url` 做点状编辑。

### 编辑模式

**虚拟试穿:**「Change garments only. Preserve exact face, body shape, pose, hair, expression, background, camera angle. Match lighting/shadows so outfit looks naturally worn.」

**物体移除:**「Remove [X]. Do not change anything else. Use `input_fidelity: high` to maintain surrounding context」(仅 gpt-image-1.5/1,gpt-image-2 默认高保真)。

**光照/天气替换:**「Change ONLY environmental conditions: lighting direction/quality, shadows, atmosphere, precipitation. Preserve identity, geometry, camera angle, object placement.」

**室内换装:**「Swap [furniture]. Preserve camera angle, lighting, shadows, surrounding context. Photorealistic contact shadows.」

## 多图 — 至多 16 张参考图

按**角色**编号,不只按序号:
```
Image 1: base scene
Image 2: jacket reference (apply only the jacket fabric/cut to subject in Image 1)
Image 3: lighting reference (apply golden-hour quality from Image 3)
```

## 风格迁移

不要写抽象词(「minimalist」、「editorial」)。点名参考图的具体视觉属性:调色板、边缘处理、轮廓、阴影处理、平面逻辑。

## 世界知识

GPT Image 2 能自行补全语境:「Bethel, NY, August 1969」→ 推出 Woodstock 美学。用法:给历史/文化锚点,不要逐条罗列细节。

## 迭代策略

- 从**干净**的基础提示词开始。
- 每轮一处修改。「Make lighting warmer」、「remove extra tree」、「restore original background」。
- 漂移时 — 重新列出不变量。
- 长提示词 — 分标签段落,不要一张大饼。

## 用例模板

### 写实编辑大片
```
Scene: [location, time, weather]
Subject: [who, action, framing]
Important Details: [lens feel, light source, surface wear, imperfections, real texture]
Use Case: editorial photograph, looks like a real photo
Constraints: no glamorization, no heavy retouching, no studio gloss
```

### 产品模型(干净背景)
```
Scene: plain white opaque background
Subject: [product] centered
Important Details: crisp silhouette, no halos/fringing, light contact shadow,
  preserve label legibility exactly, preserve geometry
Use Case: product mockup
Constraints: no restyling, only background removal + light polish
```

### UI 模型
```
Scene: [device frame, e.g. iPhone 15 Pro]
Subject: [screen/app name] — describe AS IF IT EXISTS, not concept art
Important Details: layout, hierarchy, real interface elements, exact copy in quotes,
  typography behavior, spacing, state
Use Case: shipped product screenshot
Constraints: no sketch language, no placeholder text, no Lorem Ipsum
Quality: high (for small UI text)
```

### 带文字的营销创意
```
Scene: [environment]
Subject: [hero element]
Important Details: [composition, palette, mood]
Use Case: ad creative for [audience]
Text: "EXACT HEADLINE" in [font style], [color], [position]
      "exact subhead" in [font style], [color], [position]
Constraints: no extra text, no duplicate text, no watermarks, no unrelated logos
Quality: high
```

### 信息图 / 图表
```
Title: "[TITLE]"
Content flow: [step 1] → [step 2] → [step 3]
Visual format: [layout type — flowchart, pyramid, isometric, etc.]
Use Case: educational infographic for [audience]
Constraints: readable labels at all sizes, clear hierarchy, no clutter,
  no decorative noise, ample whitespace
Quality: high
Size: 1536×1024
```

## 从旧版 GPT-Image 迁移

- 提示词基本可以原样迁移。
- 迁移后 — 检查质量、延迟、重试率;做调优。
- `gpt-image-1-mini` — 仅当重点是把低风险任务的批次价格降下来时。

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
