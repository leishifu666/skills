# 电商产品摄影模式

可复用的提示词模板:产品广告、包装、商业视觉。每个模式用 `{variables}` 定制。默认模型:GPT Image 2.5 (5 段式格式),除非另有说明。

---

## 微缩景观产品广告

当你需要趣味性、抓眼球的产品视觉,微小工人与超大产品互动时使用 — 适合社媒广告与上市战役。

<!-- Source concept: miniature/tilt-shift product advertising with construction-worker scale play -->

```
Scene: clean {surface_color} tabletop studio, soft overhead diffused light, shallow depth of field with tilt-shift blur at edges
Subject: oversized {product_name} centered in frame, surrounded by miniature construction workers (1/87 scale figurines) — some climbing the packaging with tiny ladders, others operating a miniature crane to lift the cap/lid, a crew painting the label
Important Details: {product_material} surface catches key light from upper left, visible condensation/texture on product, figurines cast tiny hard shadows, warm {accent_color} hard hats on workers, fine detail on miniature tools, slightly desaturated background, eye-level camera angle
Use Case: social media product ad, Instagram carousel hero
Constraints: no text, no logos other than product label, no floating elements, product must remain recognizable and unaltered, no more than 8 figurines
```

**关键调节项:** `{product_name}`、`{product_material}` (磨砂玻璃、哑光铝、亮面塑料)、`{surface_color}` (白大理石、原色混凝土、浅色桦木)、`{accent_color}` (安全橙 #FF6600、黄 #FFD600)

**推荐模型:** GPT Image 2.5 (`quality: high`) — 精确的小人偶细节与产品标签可读性

---

## 奢华化妆品影棚拍摄

用于高端美妆或香水产品摄影 — 暗调、情绪化、触感表面,带氛围效果。

<!-- Source concept: luxury perfume/cosmetics dark-marble studio photography with condensation and smoke -->

```
Scene: dark studio, {background_surface} surface with subtle reflections, thin layer of low-hanging smoke drifting left to right, {time_mood} ambient
Subject: {product_name} bottle/tube centered, three-quarter angle, {product_finish} catching a single key light from upper right
Important Details: fine water droplets on product surface (condensation, not spray), {accent_material} accent elements flanking the product (raw stone, dried botanicals, metal shavings), volumetric haze behind product, reflection on surface below is soft and dark, color palette restricted to {palette}, contact shadow sharp near base fading to soft
Use Case: luxury brand campaign hero, print ad, website banner
Constraints: no text overlays, no human hands, background stays dark (#0a0a0a to #1a1a1a gradient), no color spill outside the defined palette, no lens flare
```

**关键调节项:** `{background_surface}` (nero marquina 大理石、湿润黑曜石板、拉丝枪灰)、`{product_finish}` (磨砂玻璃、烤漆黑、拉丝金)、`{accent_material}` (原石水晶、干薰衣草茎、黑河石)、`{palette}` (金色 #C9A84C 与黑、玫瑰 #B76E79 与奶油、祖母绿 #2D6A4F 与银)、`{time_mood}` (冷蓝、暖琥珀)

**推荐模型:** GPT Image 2.5 (`quality: high`) — 表面材质与冷凝细节

---

<a id="9-panel-tvc-storyboard-grid"></a>
## 9 面板 TVC 分镜网格

> 带时间戳的暗色变体见 [multi-panel.md](../multi-panel.md#1-9-cell-grid-storyboard)。

用于在单张图里呈现产品广告的镜头分解 — 提案、创意演示、客户审批。

<!-- Source concept: 9-panel television commercial storyboard grid with numbered frames -->

```
Scene: white canvas background, clean 3x3 grid with thin #CCCCCC divider lines (2px), each cell represents one shot in a {duration}-second commercial
Subject: {product_name} commercial storyboard — each panel is a distinct camera setup
Important Details:
  Panel 1 (wide): establishing shot of {setting}, warm natural light, product not yet visible
  Panel 2 (medium): {protagonist} notices/discovers the product on {surface}
  Panel 3 (close-up): hand reaching for {product_name}, shallow depth of field
  Panel 4 (ECU): product detail — texture of {product_material}, label readable
  Panel 5 (medium): {protagonist} using/opening the product, genuine expression
  Panel 6 (reaction): close-up face, {emotion} expression, soft key light
  Panel 7 (wide): product in context of {lifestyle_scene}
  Panel 8 (beauty shot): product hero on {beauty_surface}, studio lighting
  Panel 9 (pack shot): product centered on white with "{tagline}" below in thin sans-serif, #333333
Use Case: creative pitch deck, storyboard for TVC production
Constraints: consistent character identity across all panels, no panel numbering text, uniform lighting temperature within the narrative (panels 1-7), distinct studio lighting for panels 8-9
```

**关键调节项:** `{product_name}`、`{protagonist}` (30 多岁女性、年轻情侣、家庭)、`{setting}` (明亮厨房、户外露台、都市咖啡)、`{emotion}` (满足、惊喜、放松)、`{beauty_surface}` (白大理石、灰色渐变)、`{tagline}`、`{duration}` (15、30)

**推荐模型:** GPT Image 2.5 (`quality: high`) — 网格精度与面板 9 的文字

---

## 悬浮食材定格

用于食品、饮料或补剂产品,悬浮食材传达新鲜、风味或成分配比。

<!-- Source concept: frozen-motion ingredient explosion around product, high-speed photography aesthetic -->

```
Scene: {background_gradient} gradient backdrop, high-speed flash freeze-frame moment, clean studio environment
Subject: {product_name} container in center, tilted {tilt_angle} degrees, with {liquid_type} mid-pour arcing from the opening
Important Details: individual {ingredient_list} frozen in mid-air around the product — each element sharply focused with visible texture ({texture_details}), micro water droplets suspended alongside ingredients, single hard flash from behind (rim light on ingredients), secondary soft fill from front, liquid splash forms a clean arc with visible viscosity, product label faces camera and remains fully legible, ingredients distributed in a loose orbital pattern
Use Case: beverage packaging, food product poster, social media ad
Constraints: no ingredients overlapping the product label, no motion blur (everything frozen sharp), background must remain clean — no stray splashes hitting edges, no more than {max_ingredients} floating elements, no artificial glow effects
```

**关键调节项:** `{product_name}`、`{background_gradient}` (#F5F0EB 到 #FFFFFF 亮色、#1A0A2E 到 #0D0D0D 暗色)、`{liquid_type}` (琥珀果汁、白牛奶、绿色冰沙)、`{ingredient_list}` (草莓切片 + 薄荷叶 + 冰块、可可碎 + 榛子 + 香草荚)、`{texture_details}` (草莓切面可见籽、冰面霜花)、`{tilt_angle}` (15、25)、`{max_ingredients}` (6-8)

**推荐模型:** GPT Image 2.5 (`quality: high`) — 定格细节精度与标签可读性

---

## 充气超现实主义产品海报

用于打破常规、让人停下滑动的社媒广告,产品包装呈现被挤压、充气或物理变形,仿佛由软橡胶或乙烯制成。

<!-- Source concept: inflatable surrealism — product packaging rendered as squeezed/puffy/distorted soft objects -->

```
Scene: solid {background_color} background, soft even studio lighting with no hard shadows, slightly elevated camera angle (15 degrees above eye level)
Subject: {product_name} packaging reimagined as a puffy inflatable vinyl object — the shape is recognizable but squeezed at the middle as if gripped by an invisible hand, seams visible where vinyl panels meet, surface slightly reflective like a pool float
Important Details: {product_color_scheme} preserved on the inflated surface but stretched and slightly warped around curves, visible air valve at the bottom edge (small brass circle), subtle wrinkles where the vinyl compresses, the brand name/logo distorted by the inflation but still readable, two or three {companion_objects} nearby also inflated (matching aesthetic), environment reflection on glossy vinyl surface, cast shadow soft and diffused below
Use Case: disruptive social media ad, brand campaign poster, billboard
Constraints: product must remain identifiable despite distortion, no liquid, no particles, no humans, no text outside what exists on the packaging, vinyl texture must read as physical (not digital 3D render), background is flat color only
```

**关键调节项:** `{product_name}`、`{background_color}` (泡泡糖粉 #FFB6C1、电光蓝 #007BFF、酸性黄 #E8FF00)、`{product_color_scheme}`、`{companion_objects}` (匹配的配件、原料、品牌吉祥物元素)

**推荐模型:** NBP — 可信物理变形需要复杂空间推理

### Nano Banana 版本:

```
A product poster showing {product_name} packaging transformed into a puffy inflatable vinyl object, squeezed at the middle as if gripped by an invisible hand. The surface is slightly glossy like a pool float, with visible seams where vinyl panels meet and a small brass air valve at the base. The original {product_color_scheme} is preserved but stretched and warped around the inflated curves. Brand text is distorted by the shape but still legible. Two small {companion_objects} sit nearby, also inflated in the same vinyl style. Solid {background_color} background, soft even studio light, slightly elevated camera angle. Soft diffused shadow below. Format: 4:5.
```

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
