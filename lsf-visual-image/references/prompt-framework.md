# 提示词框架

构建提示词的通用清单。适用于**两大家族**模型。差异见:
- [nano-banana.md](nano-banana.md) — NB 专属 (grounding、extreme ratios、thinking mode、JSON)
- [gpt-image.md](gpt-image.md) — GPT Image 2 (5-slot template、anti-slop、quality settings)
- [models.md](models.md) — 何时选哪种模型

## 任务类型(技能)

先确定任务类型——它决定提示词策略:

| 类型 | 何时使用 | 关键要素 |
|------|-------------------|-------------------|
| **Photorealistic** | 人物、产品、场景的照片 | 光线、材质、氛围 |
| **Illustration** | 贴纸、图标、插画 | 风格、轮廓、调色板 |
| **Product/Commercial** | 产品拍摄 | 表面、反射、构图 |
| **Minimalist** | 负空间 | 去除什么比添加什么更重要 |
| **Sequential** | 漫画、分镜 | 面板、过渡、叙事 |
| **Editing** | 修改现有内容 | 改变什么的明确指令 |
| **Style Transfer** | 风格迁移 | 参考图 + 新内容 |
| **Composite** | 合并元素 | 连贯性、光线、比例 |
| **Text Rendering** | 图内文字 | 精确引号、位置、字重 |

## 通用元素(清单)

过一遍清单——不必全写,但值得检查:

**必填:**
- **主体** - 谁是/什么是焦点
- **语境** - 用途(决定风格)

**视情况:**
- **动作** - 发生了什么
- **环境** - 在哪里发生
- **相机** - 景别 (close-up、wide shot 等)
- **光线** - 光型
- **情绪** - 场景的情感
- **材质** - 表面质感
- **调色板** - 颜色(最好用 hex)
- **格式** - 宽高比

> ⚠️ **镜头参数** (50mm、85mm、f/2.8、ISO):
> - **Nano Banana** — 忽略数字,写描述(「shallow depth of field」)
> - **GPT Image 2** — 允许「50mm feel」作为 high-level look,但不能作为精确物理模拟

## 细节模式(模式)

**简洁** - 一句话,用于快速迭代:
```
Minimalist poster: white background, single red apple, centered, dramatic shadow.
```

**标准** - 1-2 段,控制与灵活性的平衡:
```
Create a product shot for premium headphones marketing.

Matte black headphones on dark slate surface. Single spotlight from upper left creates dramatic shadow. Background gradient from #1a1a1a to pure black.

Format: 16:9
```

**详细** - 复杂场景的细节最大化:
```
Create a cinematic wide shot for sci-fi film concept art.

Setting: Abandoned space station observation deck. Massive curved window spans entire wall, revealing dying red giant star filling half the frame. Station interior in deep shadow except where crimson light bleeds through.

Subject: Lone astronaut in weathered EVA suit, helmet off, sitting on debris pile. Back to camera, facing the star. Pose suggests exhaustion and acceptance.

Atmosphere: Dust particles float in zero-g, catching red light. Abandoned equipment scattered - coffee cup frozen mid-float, papers suspended. Frost crystals on interior surfaces where life support failed.

Mood: Melancholic beauty, end of an era
Lighting: Volumetric god rays from star through window
Format: 2.39:1 cinemascope
```

## 输出结构

编写提示词时给出:

**1. Prompt** - 可直接使用的

**2. Parameters** - 若非标准:
- 宽高比 (非 1:1 时)
- 分辨率 (需要 2K/4K 时)

**3. Exclusions** - 排除项(可选):
> 用正面表述!NBP 更能理解 "clean background" 而非 "no clutter"

**4. Assumptions** - 用户未指定时你的推断

## 快速决策树

```
要创建什么?
├── 真实物体/人物的照片 → Photorealistic
├── 绘画/插画 → Illustration
├── 待售商品 → Product/Commercial
├── 大量留白 → Minimalist
├── 多个画面/故事 → Sequential
├── 修改现有照片 → Editing
├── "像这张图一样" → Style Transfer
├── 合并多个元素 → Composite
└── 文字是主角 → Text Rendering
```

> 图像接地 (在互联网上查找真实地点) 与极限比例 (1:8、8:1、4:1) — 仅 Nano Banana。见 [nano-banana.md](nano-banana.md)。

## 按类型示例

### Photorealistic
```
Portrait of a weathered fisherman, 60s, deep wrinkles and sun-damaged skin.
Early morning golden hour on wooden dock.
Holding fresh catch, genuine smile of satisfaction.
Background: misty harbor, fishing boats soft focus.
Mood: authentic, documentary style
```

### Product/Commercial
```
Product shot: luxury watch on raw concrete slab.
Single hard light from upper right, creating defined shadow.
Watch face at 10:10 position, metal bracelet draped naturally.
Background: gradient gray, vignette edges.
Style: high-end catalog, editorial
Format: 4:5
```

### Minimalist
```
Single origami crane, red paper, centered.
Pure white infinite background.
Soft diffused light, barely visible shadow.
Extreme negative space - crane occupies <10% of frame.
Format: 1:1
```

### Text Rendering
```
Motivational poster for gym.

Background: dark textured concrete, subtle vignette.

Text:
"DISCIPLINE" in extra bold, white, centered upper third
"beats talent" in thin weight, #808080, centered below

Small icon: minimal dumbbell silhouette, bottom center
Format: 9:16 (stories)
```

## 参数化模板

用 `{variable}` 模式构造可复用提示词。提示词结构保持稳定 — 只替换需要变的部分。

### 语法

变量写法:`{name, default="value"}`。未提供值时用默认值。没有默认值时变量必填。

### 模板

```
Scene: {location, default="small Lisbon florist storefront at blue hour"}
Subject: {person, default="woman in navy apron"} {action, default="locking the front door"}
Important Details: {lighting}, {lens_feel, default="50mm feel"}, {key_texture}
Use Case: {use_case, default="editorial photography"}
Constraints: {constraints, default="no extra signage, no people in background"}
```

### 使用方法

1. **只替换变化的部分** — 其余取自默认值
2. **结构稳定** — 槽位顺序对所有变体一致,模型收到统一格式
3. **批量生成** — 适合系列:同一风格下的产品角度、角色姿势、地点

### 使用示例

**产品拍摄系列**(只变产品与纹理):
```
Scene: {location, default="marble kitchen counter, morning light"}
Subject: {product} on {surface, default="raw linen cloth"}
Important Details: {lighting, default="soft window light from left"}, {lens_feel, default="85mm feel"}, {key_texture}
Use Case: {use_case, default="e-commerce hero shot"}
Constraints: {constraints, default="clean background, no props except surface"}
```

**角色姿势系列**(变动作与情绪):
```
Scene: {location, default="industrial loft studio"}
Subject: {person, default="man in black turtleneck"} {action}
Important Details: {lighting, default="single softbox, camera right"}, {lens_feel, default="50mm feel"}, {key_texture, default="fabric texture visible"}
Use Case: {use_case, default="fashion editorial"}
Constraints: {constraints, default="no visible logos, neutral expression"}
```

## 电影级详细模式

标准详细 — 5-7 行。**Cinematic verbose** — 更高一档,用于需要细节最大化的场合:hero shots、关键视觉、campaign 主视觉。

### 何时使用

- 活动最终视觉,而非迭代稿
- 落地页或封面的 hero shot
- 要放大到所有格式的 key visual
- 每像素都有价值的作品集工作

### 微细节清单

在标准 detailed 基础上叠加 —— 是额外图层,不是替代:

1. **Surface wear & aging**(表面磨损与老化) — "chipped paint on window frame, hairline scratches on metal surface, green patina on copper fittings, oxidation marks on iron hinges"
2. **Micro-textures**(微观纹理) — "visible pores on skin, individual hair strands catching backlight, fabric weave pattern on linen shirt, grain of weathered wood"
3. **Atmospheric particles**(大气颗粒) — "dust motes suspended in light beam, steam wisps rising from coffee cup, pollen floating in golden hour air, fine rain droplets on glass surface"
4. **Specular behavior**(高光行为) — "specular highlights on metal edges of watch, caustic reflections dancing inside glass bottle, wet surface sheen on cobblestones after rain"
5. **Fabric & material drape**(织物与材质垂坠) — "natural fabric folds at elbow crease, gravity pull on loose linen garment, weight distribution visible in heavy wool coat"
6. **Contact shadows**(接触阴影) — "soft contact shadow where cup meets saucer, ambient occlusion in crevices of stone wall, dark line where book spine meets table"
7. **Environmental reflections**(环境反射) — "building reflections in wet pavement, sky gradient in chrome bumper surface, warm neon glow on skin from nearby sign"
8. **Motion cues**(运动线索) — "slight motion blur on trailing hair strand, frozen splash droplet from espresso pour, wind-displaced fabric edge of scarf"

### 前后对比

**标准详细:**
```
Create a cinematic portrait for coffee brand campaign.

Setting: Small Italian café, early morning. Espresso machine prominent in background.
Subject: Barista in white shirt, mid-pour, focused expression.
Atmosphere: Steam rising, warm tones, golden morning light through window.
Mood: Craftsmanship, ritual, quiet dedication
Lighting: Warm directional light from left window
Format: 4:5
```

**电影级详细:**
```
Create a cinematic portrait for coffee brand campaign.

Setting: Small Italian café, early morning. Brass-and-chrome La Marzocca espresso machine in background, oxidation marks on steam wand, hairline scratches on drip tray from years of use. Chipped paint on wooden window frame behind machine.

Subject: Barista in white linen shirt — fabric weave pattern visible, natural folds at rolled-up sleeves, gravity pull on loose collar. Mid-pour with focused expression, visible pores on forehead, individual eyebrow hairs catching backlight.

Atmosphere: Steam wisps rising from espresso cup, dust motes suspended in morning light beam cutting through window. Fine coffee grounds scattered on worn marble counter — soft contact shadow where cup meets saucer. Wet surface sheen on freshly wiped counter edge.

Details: Specular highlights on chrome portafilter handle. Caustic reflections dancing inside glass water carafe on shelf. Warm neon glow of "APERTO" sign reflecting on barista's forearm. Slight motion blur on trailing steam, frozen droplet mid-drip from group head.

Mood: Craftsmanship, ritual, quiet dedication
Lighting: Warm directional light from left window, volumetric through steam
Format: 4:5
```

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
