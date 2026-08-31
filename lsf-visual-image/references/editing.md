# 图像编辑

通用模式。编辑逻辑因模型而异:

- **Nano Banana:** 对话式,无需蒙版。「Keep X same, change Y」。对物理与材质理解良好。
- **GPT Image 2:** 双栏逻辑 **Change / Preserve / Constraints**。每轮重复 preserve list,否则漂移。可选 `mask_image_url` 做点状编辑。identity preservation 最佳。见 [gpt-image.md](gpt-image.md#editing--двухколоночная-логика)。

通用规则:**每轮一次编辑**,不要一次改所有东西。

## 移除物体
```
Remove [OBJECT] from this image.
Fill with [LOGICAL REPLACEMENT] matching surroundings.
Keep [PRESERVED ELEMENTS] exactly the same.
```

示例:
- "Remove tourists, fill with cobblestones"
- "Remove car, extend street naturally"

## 添加物体
```
Add [OBJECT] to this image.
Position: [LOCATION]
Style: matching existing lighting
Scale: [RELATIVE SIZE]
```

## 光线控制
```
Change lighting to [NEW LIGHTING].
Keep subject and composition same.
```

词汇:
- Golden hour / sunset / warm backlight
- Overcast / soft / diffused
- Night / dramatic / single source
- Rim lighting / silhouette

## 季节/天气
```
Turn scene into [SEASON/WEATHER].
Keep architecture exactly same.
Adjust: [snow/leaves/reflections/sky]
```

## 上色

**照片:**
```
Colorize this B&W photograph.
Era-appropriate colors for [DECADE].
Skin tones: natural, realistic
```

**漫画:**
```
Colorize this manga panel.
Style: [vibrant anime / muted realistic]
Effects: [glowing/neon] for energy elements
Maintain: line art integrity
```

## 修复
```
Restore this damaged photograph.
Fix: [tears/scratches/fading/stains]
Enhance: sharpness, contrast
Preserve: original character and grain
```

## 本地化
```
Translate all [SOURCE] text to [TARGET].
Keep everything else same.
Maintain: font style, sizing, position
```

文化适配:
```
Localize this [ORIGINAL] ad to [TARGET MARKET].
Background: [NEW LOCATION]
Translate: text to [LANGUAGE]
Keep: brand elements, core composition
```

## 物理感知

NBP 理解材质:
```
Fill this glass with [LIQUID].
Add: refraction, meniscus, condensation
Match: existing lighting
```

```
Add [MATERIAL] texture to [SURFACE].
Properties: [matte/glossy], [rough/smooth]
```

## 对话式微调

初次编辑后:
- "Make it warmer"
- "Increase contrast"
- "Soften the edges"
- "Add more detail to shadows"

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
