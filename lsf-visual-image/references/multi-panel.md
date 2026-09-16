# 多面板构图

单图布局包含多个画框、面板或网格单元。不同于 [storyboards.md](storyboards.md)(一张一张顺序生成的图像),这些模式产出**一张图**、所有面板烧制在内。

核心原则:显式编号并描述每个面板。模型需要逐个面板的指令 — 像 "show multiple angles" 这样含糊的请求会产出不一致的网格。

---

<a id="1-9-cell-grid-storyboard"></a>
## 1. 九宫格分镜板

> 以产品叙事为重点的变体见 [patterns/ecommerce.md](patterns/ecommerce.md#9-panel-tvc-storyboard-grid)。

**适用场景:** TVC 或广告镜头分解 — 一张图 = 9 个带场景标题与时间戳的面板。

### 模板 (5 段式格式)

```
Scene: Dark storyboard layout — 3x3 grid of cinematic frames for a {duration}-second {product_name} commercial. Each cell has a thin dark border. Below each cell: scene number, title, and timestamp in small white sans-serif text on dark background.

Subject: {product_name} commercial storyboard showing the complete narrative arc across 9 panels.

Important Details:
Panel 1 (0:00–{t1}): {scene_1_description}
Panel 2 ({t1}–{t2}): {scene_2_description}
Panel 3 ({t2}–{t3}): {scene_3_description}
Panel 4 ({t3}–{t4}): {scene_4_description}
Panel 5 ({t4}–{t5}): {scene_5_description}
Panel 6 ({t5}–{t6}): {scene_6_description}
Panel 7 ({t6}–{t7}): {scene_7_description}
Panel 8 ({t7}–{t8}): {scene_8_description}
Panel 9 ({t8}–{duration}): {scene_9_description}

Each panel labeled below: "Scene {N}: {title}" and "{start}–{end}"

Use Case: Pre-production storyboard for video production team
Constraints: All 9 panels must be clearly separated, no merged cells, every panel must contain distinct content, timestamps must be legible, {language} titles
```

**变量:**
- `{product_name}` — 品牌/产品
- `{duration}` — 广告总时长(如 "30"、"60")
- `{t1}` 至 `{t8}` — 时间戳边界
- `{scene_1_description}` 至 `{scene_9_description}` — 每个面板的镜头描述
- `{language}` — "Chinese" / "English" / "bilingual"

**推荐尺寸:** 1536x1024 (横向)
**模型:** GPT Image 2.5 `quality: high`(文字密集 — 时间戳与标题需要可读性)
**常见坑:**
- 遗漏面板编号会导致模型合并或跳过面板
- 含糊的场景描述产生几乎相同的面板 — 每个面板必须有不同的动作、角度或主体
- 极小字体的时间戳需要 `quality: high` 才能保持可读

---

## 2. 2x2 编辑人像网格

**适用场景:** 同一人在一张图中以 4 个角度/裁切呈现,用于编辑大片或选角look。

### Template (5-slot format)

```
Scene: 2x2 grid of four editorial portraits, minimal gap between panels. {background_description}. {lighting_style}.

Subject: {subject_description} — same person in all four panels, consistent identity and wardrobe.

Important Details:
Top-left: front-facing portrait, direct eye contact, shoulders up
Top-right: extreme macro close-up of face — eyes, skin texture, freckles visible
Bottom-left: lower angle looking up, chin slightly raised, confident expression
Bottom-right: side profile, clean silhouette against background

Consistent lighting across all four panels. Skin texture realistic, no airbrushing.

Use Case: editorial photography, model portfolio, casting composite
Constraints: same person in every panel, no wardrobe changes between panels, no extra people, no text overlays
```

**变量:**
- `{subject_description}` — 年龄、外貌、服装(如 "woman in her 30s, dark curly hair, white linen shirt")
- `{background_description}` — (如 "soft gray studio backdrop")
- `{lighting_style}` — (如 "single key light from upper left, subtle fill from right")

**推荐尺寸:** 1024x1024 (方形)或 1024x1536 (竖图强调人像)
**模型:** GPT Image 2.5 `quality: medium` 或 Nano Banana Pro(两者处理写实人像都很好)
**常见坑:**
- 不在每个面板注明 "same person" — 模型可能生成四个不同的人
- 不指明哪个象限用哪个角度 — 模型任意排列
- 要求过于差异化的裁切(全身 + 超大特写)会在网格内造成比例不一致

---

## 3. 三面板活动拼贴

**适用场景:** 活动视觉的 hero shot + 特写 + 动作 — 三联画(横向或纵向)。

### 模板 (5 段式格式)

```
Scene: Three-panel {orientation} collage for {brand_name} campaign. Panels separated by thin white lines.

Subject: {model_description} showcasing {product_description}.

Important Details:
Panel 1 (left/top): Hero wide shot — full figure of model with product, environmental context, lifestyle setting
Panel 2 (center/middle): Close-up product detail — {product_detail_description}, tactile textures, sharp focus
Panel 3 (right/bottom): Action shot — model using/wearing/interacting with product, candid energy, slight motion blur on extremities

Consistent warm golden-hour lighting across all panels. Same model identity throughout.
{typography_instruction}

Use Case: social media campaign visual, brand lookbook
Constraints: same person across all panels, consistent color grading, no stock-photo stiffness, {product_name} must be visible in every panel
```

**变量:**
- `{orientation}` — "horizontal"(并排)或 "vertical"(堆叠)
- `{brand_name}`、`{product_name}`、`{product_description}` — 品牌语境
- `{model_description}` — 出现谁
- `{product_detail_description}` — 特写展示什么
- `{typography_instruction}` — 如 `Text: "{HEADLINE}" in bold condensed white, overlaid on Panel 1 lower third`,或者不需要文字时省略

**推荐尺寸:** 1536x1024 (横向三联)或 1024x1536 (纵向三联)
**模型:** GPT Image 2.5 `quality: medium` — 若需文字叠加,用 `quality: high`
**常见坑:**
- 不指定面板顺序 — "hero, close-up, action" 没有左/中/右的分配
- 室内特写与室外 hero shot 混用时光线不一致 — 指定统一光线
- 忘了提及主体一致性导致出现三个不同模特

---

## 4. 4x3 无边框网格

**适用场景:** 12 个面板讲述故事或展现情绪 — 面板间无缝隙、无缝马赛克感。

### 模板 (5 段式格式)

```
Scene: 4x3 borderless grid (4 columns, 3 rows) where each of the 12 panels is an independent image but panels share no borders, gaps, or dividers — edges touch seamlessly. Overall theme: {theme}.

Subject: {subject_description} — maintain strong subject consistency across all 12 panels.

Important Details:
Row 1: {panel_1}, {panel_2}, {panel_3}, {panel_4}
Row 2: {panel_5}, {panel_6}, {panel_7}, {panel_8}
Row 3: {panel_9}, {panel_10}, {panel_11}, {panel_12}

Style: {style_description}
Mood progression: {mood_arc}
Each panel is an independent composition but the overall grid reads as a unified artwork.

Use Case: mood board, editorial spread, social media carousel preview, album artwork
Constraints: borderless — no white lines, no black borders, no gaps between panels. Same subject identity across all panels. No text in panels.
```

**变量:**
- `{subject_description}` — 面板中出现的谁/什么
- `{theme}` — 核心概念(如 "solitude in a city"、"four seasons of a garden")
- `{panel_1}` 至 `{panel_12}` — 每格的简要镜头描述
- `{style_description}` — 视觉风格(如 "35mm film grain, desaturated palette")
- `{mood_arc}` — 能量在网格中的变化(如 "calm morning to chaotic night")

**推荐尺寸:** 1536x1024 (横向)— 保证每格有足够分辨率
**模型:** Nano Banana Pro(用思考模式处理复杂多元素构图;无需文字)
**常见坑:**
- 只说 "borderless" 不够 — 明确写 "no white lines, no black borders, no gaps"
- 12 面板挤在一张图逼近细节极限 — 保持每面板描述简短且视觉上互不相同
- 没有明确的主体一致性指令,每个面板都可能出现不同的人/物

---

## 5. 6 帧电影序列

**适用场景:** 时尚编辑大片或电影感序列 — 同一场景的多个机位集中在一张图。

### 模板 (5 段式格式)

```
Scene: 6-frame cinematic sequence arranged in a 3x2 grid. Dark film-strip aesthetic with thin black borders. {location_description}.

Subject: {subject_description}, wearing {wardrobe_description}. Same person, same outfit, same location across all 6 frames.

Important Details:
Frame 1 (top-left): Top-down bird's eye view — subject seen from directly above, full body visible against ground/floor
Frame 2 (top-center): Low angle looking up — subject towering over camera, dramatic perspective, sky/ceiling visible
Frame 3 (top-right): Wide isolation shot — subject small in frame, vast environment dominates, sense of scale
Frame 4 (bottom-left): Close-up with slight tilt — face and upper body, Dutch angle, intimate intensity
Frame 5 (bottom-center): Motion frame — subject mid-action ({motion_action}), natural motion blur on limbs
Frame 6 (bottom-right): Grounded final — medium shot, subject at rest, direct gaze, resolving the sequence

Photographer reference: {photographer_style}
Lighting: consistent {lighting_description} across all frames

Use Case: fashion editorial, film lookbook, director's shot list visualization
Constraints: same person and wardrobe in every frame, no costume changes, consistent color grading, no text overlays
```

**变量:**
- `{subject_description}` — 模特细节
- `{wardrobe_description}` — 服装
- `{location_description}` — 场景
- `{motion_action}` — 动感帧捕捉什么(如 "walking forward"、"turning sharply"、"jumping")
- `{photographer_style}` — (如 "Peter Lindbergh desaturated realism"、"Helmut Newton dramatic contrast")
- `{lighting_description}` — (如 "overcast natural light, soft shadows")

**推荐尺寸:** 1536x1024 (横向,3x2 网格)
**模型:** GPT Image 2.5 `quality: medium` 或 Nano Banana Pro
**常见坑:**
- 不逐个命名画帧 — "various angles" 太含糊,模型需要逐帧指令
- 俯视与低角度同处一格会迷惑模型 — 必须把每帧锚定在网格位置上
- 运动模糊指令必须具体("blur on hands and feet")否则模型把模糊加得到处都是

---

## 6. 前后对比分割

**适用场景:** 产品转化、改造、时间对比、翻新 — 两种状态并排。

### 模板 (5 段式格式)

```
Scene: Single image split into left and right halves with a {divider_style} dividing line down the center. Before/after comparison.

Subject: {subject_description}

Important Details:
Left half (BEFORE): {before_description} — {before_condition}
Right half (AFTER): {after_description} — {after_condition}

The transition at the center line should feel {transition_style}. Same camera angle, same framing, same background perspective in both halves — only the subject's state changes.

Use Case: {use_case}
Constraints: identical composition and camera angle on both sides, same lighting direction, no text unless specified, the dividing line must be clearly visible
```

**变量:**
- `{subject_description}` — 比较什么
- `{before_description}` / `{before_condition}` — 左侧状态(如 "faded, cracked wall with peeling paint")
- `{after_description}` / `{after_condition}` — 右侧状态(如 "freshly painted wall, smooth finish, vibrant color")
- `{divider_style}` — "thin white line" / "subtle gradient blend" / "sharp vertical cut"
- `{transition_style}` — "clean and abrupt" / "natural, as if wiping away"
- `{use_case}` — "product marketing"、"renovation portfolio"、"skincare results"

**推荐尺寸:** 1536x1024 (横向 — 让每半块有近似人像的比例)
**模型:** GPT Image 2.5 `quality: medium` — 如需文字标签("BEFORE" / "AFTER"),用 `quality: high`
**常见坑:**
- 不写 "same camera angle both sides" — 模型可能呈现两个完全不同的视角
- 没有可见分隔线,两半可能合并成一个含糊场景
- 左右分配很重要 — 永远指明哪边是 before、哪边是 after

---

## 7. 12 面板分镜海报

**适用场景:** 一张图讲完整叙事 — 3x4 网格(3 列、4 行),用于动画或视频前期制作。

### 模板 (5 段式格式)

```
Scene: 12-panel storyboard poster, 3 columns x 4 rows. Dark background with each panel in a clean rectangular frame. "{title}" in bold white text at the top of the image. Below each panel: scene number and one-line description in small white text.

Subject: {character_description} — maintain consistent character design, proportions, and colors across all 12 panels.

Important Details:
Panel 1: {scene_1} — "{caption_1}"
Panel 2: {scene_2} — "{caption_2}"
Panel 3: {scene_3} — "{caption_3}"
Panel 4: {scene_4} — "{caption_4}"
Panel 5: {scene_5} — "{caption_5}"
Panel 6: {scene_6} — "{caption_6}"
Panel 7: {scene_7} — "{caption_7}"
Panel 8: {scene_8} — "{caption_8}"
Panel 9: {scene_9} — "{caption_9}"
Panel 10: {scene_10} — "{caption_10}"
Panel 11: {scene_11} — "{caption_11}"
Panel 12: {scene_12} — "{caption_12}"

Panels read left-to-right, top-to-bottom (like a comic page). Character appearance, clothing, and color palette must stay identical across all 12 panels — only pose, expression, angle, and environment change.

Style: {art_style}

Use Case: animation pre-production, pitch deck visualization, narrative overview poster
Constraints: all 12 panels must be distinct scenes (no duplicates), character consistency is critical, scene numbers must be legible, {language} captions
Quality: high
```

**变量:**
- `{title}` — 顶部展示的项目/剧集标题
- `{character_description}` — 详细角色设计(颜色、服装、特征标志)
- `{scene_1}` 至 `{scene_12}` — 每个面板的视觉描述
- `{caption_1}` 至 `{caption_12}` — 每个面板下方的文字标签
- `{art_style}` — (如 "Pixar-style 3D"、"anime cel shading"、"watercolor illustration"、"graphic novel ink")
- `{language}` — 字幕语言

**推荐尺寸:** 1024x1536 (竖图 — 3 列 x 4 行需要纵向空间)
**模型:** GPT Image 2.5 `quality: high`(文字密集 — 场景号与字幕必须可读)
**常见坑:**
- 12 面板时角色漂移是最大风险 — 在提示词里重复角色设计细节,而不是只说 "same character"
- 提示词中无显式场景编号,面板可能随机排序
- 12 面板带字幕文字密度极大 — 每行字幕控制在 5 词以内保证可读
- 美术风格必须声明一次并统一应用;跨面板混风格 = 视觉混乱

---

## 多面板通用技巧

**面板数量 vs. 细节取舍:** 面板越多 = 每面板细节越少。4 面板可写丰富描述;12 面板需要简短而视觉互异的描述(每个 3-8 词)。

**主体一致性:** 永远包含显式指令:"same person / same character / same product across all panels." 重复关键身份标志(发色、服装、特征)而不是说 "same as before."

**网格规格:** 永远写明网格维度(如 "3x2 grid, 3 columns 2 rows")。只说 "6 panels" 而无布局指令,模型会任意排列。

**边框与间隙:** 要明确 — "thin white border between panels" 或 "borderless, no gaps." 默认行为因模型而异且不可靠。

**阅读顺序:** 明确声明:"left-to-right, top-to-bottom" 或 "numbered 1-9 starting top-left." 否则叙事流可能混乱。

**模型选择总结:**
- 面板内有文字/标签 --> GPT Image 2.5 `quality: high`
- 无文字、复杂构图 --> Nano Banana Pro
- 预算/探索 --> Nano Banana 2 或 GPT Image 2.5 `quality: low`

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
