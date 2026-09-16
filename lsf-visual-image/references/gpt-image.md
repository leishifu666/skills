# GPT Image 2.5 — 专属规则

OpenAI 当前提供 `gpt-image-2.5-flare`（日常快速生成）与 `gpt-image-2.5-sunburst`（精确编辑）。用户已指定模型时保留其选择；旧版迁移单独核对参数。来源：[Flare](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare)、[Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)，核对于 2026-09-16。

## 提示词结构 — 5 段式

复杂提示词可按以下五段组织，便于区分内容与约束；简单请求不强制凑五段，遵从用户要求的语言和长度。

```
Scene: location, time of day, background, environment
Subject: primary focus — who or what is central
Important Details: materials, textures, lighting, camera angle, mood, composition
Use Case: editorial, product mockup, UI, poster, infographic
Constraints: what must NOT change/appear (no watermarks, preserve face, no extra text)
```

### 强制末尾收束语

所有为 GPT Image 系列编写的生图提示词,都必须在提示词正文的最后原样追加以下句子。它用于抑制细节碎裂、材质断裂、异常锐化与局部纹理崩坏,不得缩写、改写或遗漏:

```text
画面干净通透，材质完整自然，纹理平滑统一，主体清晰，背景层次分明，避免过度锐化、色斑、噪点、碎纹、崩坏和畸变。
```

这句话放在全部 `Constraints` 内容之后,作为整个 Prompt 的最后一句;不要把它放进 `Notes`、负面提示词或提示词外的说明中。

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

GPT Image 2.5 对措辞质量特别敏感。Vague praise = 结果降级。

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
| `quality: xhigh` | 有明确未满足的细节需求时试用 |
| `quality: max` | 更高质量仍未满足要求且预算允许时试用 |

接口默认是 `auto`；`medium` 是可选的比较起点而非 API 默认值。草稿可选 `low`，按实际结果逐档比较，不把旧版同名档位的效果或成本直接套用到 2.5。

## 尺寸 (gpt-image-2.5-flare)

- 最长边: ≤3840px
- 两边: 均为 16 的倍数
- 宽高比: 最大 3:1 (long:short)
- 总像素: 655 360 – 8 294 400
- 超过 2560×1440 的分辨率仍属实验性；不把可接受参数等同于效果保证。

**常见尺寸:**
- 竖幅 1024×1536
- 横幅 1536×1024
- 方形 1024×1024
- 2K 2560×1440
- 4K 3840×2160 或 2160×3840（实验性）

支持 `size: auto`；透明背景需 `background: transparent` 搭配 PNG/WebP，并检查真实 alpha。尺寸与参数依据：[官方生成指南](https://developers.openai.com/api/docs/guides/image-generation)。

> 1:8 / 8:1 之类的极限比例 GPT Image 2.5 **不支持** — 用 Nano Banana。

## 图内文字

- 字面文本用 `"..."` 或 ALL CAPS。
- 明确文字出现次数，避免标题或标签被重复。
- 字体、字号、颜色、位置 — 明确指定。
- 复杂单词与品牌:逐字母拼写。
- 防垃圾:「**no extra words, no duplicate text, no watermarks**」。
- 防不可读小字:「**100 percent readable and physically believable**」。
- 小号/密集/多字体 → 必须 `quality: high`。

<a id="editing--двухколоночная-логика"></a>
## 编辑 — 双栏逻辑

OpenAI 使用 `images.edit` / `v1/images/edits`。第三方平台的模型 ID、端点与掩膜字段单独查其当前文档，不把某个代理商参数当作通用接口。

```
Change: [single concrete change]
Preserve: face, identity, pose, lighting, framing, background, geometry, text, layout
Constraints: no extra objects, no redesign, no drift
```

**编辑规则:**
- **每轮只做一处编辑。** 不要一次改所有东西。
- **每轮重复 preserve list。** 否则漂移。
- **外科手术式编辑:** 明确列出不要动的项 (saturation、contrast、layout、arrows、labels、camera angle)。
- 局部编辑可使用所选接口支持的掩膜；是否提供及字段名以该接口文档为准。

### 编辑模式

**虚拟试穿:**「Change garments only. Preserve exact face, body shape, pose, hair, expression, background, camera angle. Match lighting/shadows so outfit looks naturally worn.」

**物体移除:**「Remove [X]. Preserve everything outside the edited region.」不要在提示词里混入未经当前端点核实的 `input_fidelity` 参数。

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

GPT Image 2.5 能自行补全语境:「Bethel, NY, August 1969」→ 推出 Woodstock 美学。用法:给历史/文化锚点,不要逐条罗列细节。

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

- 保留任务意图，但分别核对可用模型、quality、尺寸、透明度及编辑接口。
- 迁移后 — 检查质量、延迟、重试率;做调优。
- 不把旧版模型作为未经核实的低价默认推荐；成本按当前平台报价与实际输入/输出量评估。

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
