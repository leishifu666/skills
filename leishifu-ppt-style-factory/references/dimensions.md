# 16 维度风格定义 · 完整规格

每个维度都是风格 DNA 的一环，缺一不可。提取不到的维度用合理默认值补全，并标记为"⚡推断"。

---

## D1 · 配色体系

风格的底盘。ink 是文字色，paper 是背景色，tint 是各自的淡化变体（用于卡片背景、分隔线等）。

```json
{
  "ink": "#e0e0e0",
  "ink-rgb": "224,224,224",
  "paper": "#0a0a0a",
  "paper-rgb": "10,10,10",
  "paper-tint": "#1a1a1a",
  "ink-tint": "#333333"
}
```

**rgb 字段为什么要单独给？** 因为 CSS 里 `rgba(var(--ink-rgb), 0.5)` 这种写法需要纯数字的 rgb 值。

---

## D2 · 强调色体系

强调色是视觉锚点——按钮、高亮、数据图表、重要数字都靠它。accent-alt 用于需要第二个对比色的场景（比如对比图表的第二条线）。

```json
{
  "accent": "#00ffd5",
  "accent-rgb": "0,255,213",
  "accent-alt": "#ff2d95",
  "color-warn": "#ff6b35",
  "color-success": "#2ecc71",
  "color-info": "#3498db"
}
```

---

## D3 · 标题字体

标题字体定义了风格的"脸"。衬线=人文、非衬线=现代、手写=创意。中文标题需要专门的 CJK 字体，不能用 fallback。

```json
{
  "heading": "Playfair Display, Noto Serif SC, serif",
  "headingStyle": "serif",
  "cjkHeading": "Noto Serif SC",
  "headingImport": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@300;600&family=Noto+Serif+SC:wght@300;600&display=swap"
}
```

headingStyle 取值：`serif` | `sans-serif` | `handwritten` | `display` | `monospace`

---

## D4 · 正文字体

正文追求可读性，等宽字体用于数据/代码/元信息。

```json
{
  "body": "Inter, Noto Sans SC, sans-serif",
  "cjkBody": "Noto Sans SC",
  "mono": "JetBrains Mono, monospace",
  "bodyImport": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Noto+Sans+SC:wght@300;400;600&family=JetBrains+Mono:wght@400&display=swap"
}
```

---

## D5 · 字重体系

字重搭配直接影响视觉层级。hero 用极轻字重（200）撑大面积时更优雅，标题用 300-600，正文 400。

```json
{
  "headingWeight": 300,
  "headingBoldWeight": 600,
  "bodyWeight": 400,
  "bodyLightWeight": 300,
  "emphasisWeight": 600,
  "heroWeight": 200
}
```

---

## D6 · 字号比例

用 `min()` 和 `clamp()` 做响应式字号。中文方块字视觉面积比西文大，hero 字号需要单独分档。

```json
{
  "heroSize": "min(7.4vw, 13vh)",
  "xlSize": "clamp(2rem, 3.6vw, 4.2rem)",
  "mdSize": "clamp(1.4rem, 2vw, 2.4rem)",
  "subSize": "clamp(1rem, 1.4vw, 1.6rem)",
  "bodySize": "clamp(0.95rem, 1.1vw, 1.15rem)",
  "cjkHeroRules": {
    "1line_lte8": "min(6.4vw, 11.2vh)",
    "2line_lte8": "min(5.8vw, 10.2vh)",
    "2line_9to12": "min(5.2vw, 9.2vh)",
    "3line_plus": "min(4.6vw, 8.2vh)"
  }
}
```

---

## D7 · 间距密度

间距决定页面呼吸感。紧凑适合信息密集型（数据仪表板），宽松适合叙事型（杂志、故事）。

```json
{
  "density": "standard",
  "cardPadding": "clamp(1.6rem, 2.4vw, 2.8rem)",
  "sectionGap": "clamp(2rem, 3vw, 4rem)",
  "componentGap": "clamp(0.8rem, 1.2vw, 1.6rem)",
  "slidePadding": "clamp(2.4rem, 4vw, 5.6rem)",
  "navSafeBottom": "4.5rem"
}
```

density 取值：`compact` | `standard` | `spacious`

---

## D8 · 背景风格

PPT 的氛围层。WebGL 背景给页面增加质感，但不能抢文字的戏。heroOnly=true 表示只有 hero 页显示背景效果。

```json
{
  "type": "fluid",
  "color": "accent",
  "opacity": 0.12,
  "enabled": true,
  "heroOnly": true
}
```

| 类型 | 效果 | 适合 |
|------|------|------|
| `fluid` | 流体色散 | 人文、杂志感 |
| `contour` | 等高线 | 科技、地理 |
| `grid-dots` | 极细网格+点阵 | 瑞士风、数据 |
| `particle` | 粒子漂浮 | 未来感、太空 |
| `solid` | 纯色无效果 | 极简、商务 |

---

## D9 · 圆角与边框

圆角控制"硬朗"还是"柔和"。瑞士风/工业风用 0px 直角，友好型产品用 8-16px 圆角。

```json
{
  "borderRadius": "0px",
  "borderRadiusLarge": "0px",
  "borderWidth": "1px",
  "borderColor": "rgba(224,224,224,0.15)",
  "borderStyle": "solid"
}
```

---

## D10 · 阴影体系

阴影影响页面的深度感。极简风格通常无阴影，靠边框或留白区分层次。

```json
{
  "level": "none",
  "shadowSm": "none",
  "shadowMd": "none",
  "shadowLg": "none",
  "shadowColor": "rgba(0,0,0,0.1)"
}
```

level 取值：`none` | `subtle` | `medium` | `heavy`

---

## D11 · 动效倾向

动效让页面有生命感，但过度动效会分散注意力。stagger 是多元素依次入场的延迟间隔。

```json
{
  "level": "standard",
  "entrance": "fade-up",
  "duration": "0.6s",
  "easing": "cubic-bezier(0.22, 1, 0.36, 1)",
  "stagger": "0.08s"
}
```

level 取值：`none` | `minimal` | `standard` | `full`
entrance 取值：`fade` | `fade-up` | `fade-left` | `scale-up` | `blur-in`

---

## D12 · 图标风格

```json
{
  "library": "lucide",
  "style": "stroke",
  "strokeWidth": 1.5,
  "size": "1.2em",
  "color": "currentColor"
}
```

style 取值：`stroke` | `filled` | `duotone`

---

## D13 · 图片处理

图片的视觉处理方式。滤镜可以统一不同来源图片的调性。

```json
{
  "borderRadius": "0px",
  "filter": "none",
  "overlay": "none",
  "defaultRatio": "16:9",
  "objectFit": "cover"
}
```

| 滤镜 | 效果 | 适合 |
|------|------|------|
| `none` | 原图 | 通用 |
| `grayscale(1)` | 黑白 | 纪实、文艺 |
| `contrast(1.1) saturate(0.9)` | 杂志感 | 电子杂志风 |
| `sepia(0.2)` | 泛黄复古 | 怀旧 |

---

## D14 · 卡片风格

内容卡片是 PPT 中最常见的容器。不同风格的卡片给人完全不同的感受。

```json
{
  "style": "outlined",
  "background": "transparent",
  "hoverEffect": "border-color-lighten",
  "activeVariant": "card-outlined"
}
```

| 类型 | 效果 | 适合 |
|------|------|------|
| `outlined` | 边框卡片 | 瑞士风、极简 |
| `filled` | 填色卡片 | 标准、商务 |
| `glass` | 毛玻璃 | 未来感、科技 |
| `elevated` | 投影卡片 | Material、友好 |

---

## D15 · 装饰元素

装饰是风格的"印花"，用在角落或背景上。密度太高会喧宾夺主。

```json
{
  "pattern": "dot-matrix",
  "density": "sparse",
  "position": "corner",
  "opacity": 0.08,
  "color": "ink"
}
```

| 图案 | 效果 | 适合 |
|------|------|------|
| `dot-matrix` | 实心点阵 | 瑞士风、数据 |
| `ring-matrix` | 描边圆阵 | 科技、轻量 |
| `cross-matrix` | × 网格 | 工业、街头 |
| `lines` | 平行线 | 学术、条纹 |
| `geometric` | 几何图形 | 包豪斯、孟菲斯 |
| `none` | 无装饰 | 极简、侘寂 |

---

## D16 · 视觉气质 & 适用场景

风格的灵魂总结。aestheticTags 是搜索和推荐的索引，bestFor/notFor 帮用户判断这个风格适不适合自己的场景。

```json
{
  "aestheticTags": ["科技", "极简", "信息驱动"],
  "moodBoard": "Massimo Vignelli + Helvetica Forever",
  "bestFor": ["科技产品发布", "数据汇报", "工程分享"],
  "notFor": ["人文故事", "文学分享"],
  "era": "modern"
}
```

era 取值：`classic` | `modern` | `futuristic` | `retro` | `timeless`

---

## 完整风格 JSON 模板

```json
{
  "name": "leishifu-{slug}",
  "displayName": "风格显示名",
  "author": "leishifu",
  "createdAt": "YYYY-MM-DD",
  "version": "1.0.0",
  "source": { "type": "...", "ref": "..." },
  "d01_colors": {},
  "d02_accents": {},
  "d03_headingFont": {},
  "d04_bodyFont": {},
  "d05_fontWeight": {},
  "d06_fontSize": {},
  "d07_spacing": {},
  "d08_background": {},
  "d09_border": {},
  "d10_shadow": {},
  "d11_animation": {},
  "d12_icon": {},
  "d13_image": {},
  "d14_card": {},
  "d15_decoration": {},
  "d16_mood": {}
}
```
