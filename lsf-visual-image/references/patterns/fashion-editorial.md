# 时尚编辑大片模式

可复用的提示词模板:时尚活动、lookbook、编辑大片拍摄。每个模式用 `{variables}` 定制。默认模型:GPT Image 2 (5 段式格式),除非另有说明。

---

## 三面板活动拼贴

用于时尚品牌活动主图 — 一张宽图以三联画布局结合 hero 姿势、特写细节与动作/运动。

<!-- Source concept: fashion campaign triptych collage — hero + detail + movement panels -->

```
Scene: three vertical panels side by side on a single canvas (left 40% width, right split into two stacked panels 60% height each), thin white divider lines (3px), cohesive {lighting_setup} across all panels
Subject: {model_description} wearing {outfit_description} — same person, same outfit, three perspectives
Important Details:
  Left panel (hero): full-body three-quarter pose, {model_description} standing against {background_1}, weight shifted to one hip, direct gaze at camera, medium-format film grain, {color_grade}
  Top-right panel (detail): extreme close-up of {detail_focus} — visible weave/stitching/texture of {fabric_type}, shallow depth of field, warm directional light raking across surface
  Bottom-right panel (action): mid-stride walking shot from low angle, {background_2}, coat/fabric in motion with natural drape physics, slight motion energy in hair
  Overall: cohesive warm/cool temperature of {color_temperature}, consistent skin tone rendering across panels, editorial magazine quality
Use Case: fashion brand campaign, lookbook cover, social media carousel hero
Constraints: same person with identical features in all three panels, no text, no logos, no visible studio equipment, panels must feel like one shoot not three separate photos, no heavy retouching glow
```

**关键调节项:** `{model_description}` (20 多岁东亚女性、30 岁出头运动型男性)、`{outfit_description}`、`{detail_focus}` (领口结构、袖口纽扣、皮带扣、鞋底)、`{fabric_type}` (原色丹宁、双面羊绒、水洗真丝)、`{background_1}` (混凝土墙、沙丘、工业走廊)、`{background_2}` (开阔街道、田野、屋顶)、`{color_grade}` (提黑带琥珀调、低饱和青绿)、`{color_temperature}` (暖 4000K 感、冷阴天日光)

**推荐模型:** GPT Image 2 (`quality: high`) — 面板间身份一致与面料纹理细节

---

## 2x2 编辑人像网格

用于模特试镜、casting 卡、编辑作品集页 — 同一人的四个角度呈现在干净网格中。

<!-- Source concept: 2x2 fashion portrait grid — same model, four setups -->

```
Scene: 2x2 grid on white canvas, thin {divider_color} divider lines (2px), all four cells use the same {background_type} with slight variation in angle
Subject: {model_description}, same {outfit_description} in all four frames
Important Details:
  Top-left: straight-on headshot, neutral expression, eyes to camera, even butterfly lighting
  Top-right: three-quarter profile, chin slightly lifted, single key light from camera-left creating defined cheekbone shadow
  Bottom-left: full profile silhouette, rim light from behind outlining jaw and nose, {background_type} slightly darker
  Bottom-right: candid moment — mid-laugh or adjusting {accessory}, natural movement, softer light
  All frames: {film_stock} color science, consistent {skin_tone_handling}, no heavy skin smoothing — visible pores and natural texture, shallow depth of field in all four
Use Case: fashion editorial spread, model comp card, casting portfolio
Constraints: identical person in all four frames (bone structure, skin, hair must match exactly), no makeup changes between frames, no text, no watermarks, backgrounds must feel cohesive not random
```

**关键调节项:** `{model_description}`、`{outfit_description}` (黑色高领、白亚麻衬衫领口敞开)、`{background_type}` (无缝中灰、质感石膏墙、失焦绿植)、`{divider_color}` (#FFFFFF、#E0E0E0)、`{film_stock}` (Kodak Portra 400、Fujifilm Pro 400H)、`{skin_tone_handling}` (保留暖底色、冷中性渲染)、`{accessory}` (耳环、衣领、手表)

**推荐模型:** GPT Image 2 (`quality: high`) — 四格间的身份一致是关键

---

## 超大排印的街头风海报

用于街头风上新、限量发售或都市时尚品牌活动,粗大字体主导构图。

<!-- Source concept: streetwear poster with model integrated into oversized typographic layout -->

```
Scene: solid {background_color} background, graphic poster composition, typography dominates 60% of visual space
Subject: {model_description} in {streetwear_outfit}, standing or crouching in a {pose_description}, positioned {model_position} — partially overlapping the text layers
Important Details: headline "{HEADLINE_TEXT}" in extra-bold condensed {font_style}, {text_color}, occupying upper two-thirds of frame — model breaks in front of some letters and behind others (depth interplay), secondary text "{SUBHEAD_TEXT}" in thin weight {subhead_color} near bottom edge, {lighting_type} on model creating {shadow_quality} shadows, grain overlay across entire image ({grain_intensity}), composition follows rule of thirds with model at {grid_position} intersection
Use Case: streetwear brand drop poster, social media announcement, lookbook cover
Constraints: text must be fully legible even where model overlaps, no extra text or watermarks, no decorative elements besides type and model, model does not obscure more than 30% of any single letter, "{HEADLINE_TEXT}" spelled exactly as provided
Quality: high
```

**关键调节项:** `{HEADLINE_TEXT}` (品牌名、drop 名称)、`{SUBHEAD_TEXT}` (日期、"LIMITED DROP"、系列名)、`{background_color}` (米白 #F5F1EB、混凝土灰 #8C8C8C、哑光黑 #0D0D0D)、`{text_color}` (#000000、#FF3333、#FFFFFF)、`{font_style}` (如 Druk Wide 的无衬线、粗衬线、模板体)、`{streetwear_outfit}`、`{model_position}` (中左、右三分之一)、`{lighting_type}` (生硬直闪、柔和窗光)、`{grain_intensity}` (轻微胶片颗粒、重 35mm 颗粒)

**推荐模型:** GPT Image 2 (`quality: high`) — 文字渲染与模特-字体深度穿插

---

## 复古旱冰运动装活动

用于活泼、怀旧的运动装或性能休闲装活动,使用 70-80 年代的视觉语言。

<!-- Source concept: retro roller skating / sportswear campaign with analog film aesthetic -->

A sun-drenched wide shot of {model_description} roller skating along a {location_description}. They wear {outfit_description} — the fabric catches light as they move, one leg extended mid-glide, arms relaxed and swinging naturally. The ground is smooth asphalt with painted lane markings in faded {lane_color}. Background shows {background_elements} slightly out of focus through heat haze. Shot on {film_stock} with pronounced grain and slightly lifted shadows. Color palette centers on {palette_description}. Golden hour backlight creates a warm halo around the subject and long shadow stretching toward camera. Genuine movement energy — hair and loose fabric respond to speed. Format: {aspect_ratio}.

**关键调节项:** `{model_description}`、`{outfit_description}` (珊瑚色高腰毛巾布短裤、奶油色短款拉链衫、带赛条纹的筒袜)、`{location_description}` (Venice Beach 木板路、空郊区网球场、海滨长廊)、`{film_stock}` (Kodak Gold 200、Fuji Superia 400)、`{palette_description}` (赤陶 #CC5533、奶油 #FFF5E1、天蓝 #87CEEB、芥末 #D4A017)、`{lane_color}` (褪色黄、晒白)、`{background_elements}` (棕榈树与马卡龙建筑、铁丝网与看台)、`{aspect_ratio}` (3:2、16:9)

**推荐模型:** NB2 — 自然运动、模拟胶片颗粒、氛围接地

---

## 3D 色块形状的未来感运动装编辑大片

用于前卫的运动或 techwear 编辑大片,抽象 3D 形态在模特周围创造超现实空间环境。

<!-- Source concept: futuristic sportswear editorial with organic 3D blob/sphere shapes -->

```
Scene: {studio_environment} studio space, matte {floor_color} floor extending to infinity, ambient fill light with no visible source, three to five large organic 3D blob shapes ({blob_color}, glossy smooth surface with environment reflections) floating at varying heights around the subject
Subject: {model_description} in {techwear_outfit}, posed in an athletic stance — {pose_detail}
Important Details: blobs range from basketball-sized to armchair-sized, each with smooth amoebic curves and a single specular highlight, they cast soft colored shadows onto the floor and the model's clothing, model lit by cool directional light from camera-right creating defined muscle/fabric contour, {fabric_detail} visible in the garment construction, one blob partially behind the model and one in front (spatial depth), color palette limited to {palette}, overall mood is clinical and aspirational
Use Case: sportswear lookbook, techwear campaign, editorial magazine spread
Constraints: blobs must look physically present (not composited), no text, no logos, no additional props, model remains the clear focal point despite the surrounding forms, blobs do not touch or intersect with the model's body, no motion blur
```

**关键调节项:** `{studio_environment}` (白色虚空、混凝土灰、深海军蓝)、`{floor_color}` (浅灰 #D0D0D0、炭黑 #333333)、`{blob_color}` (铬银、半透明翡翠 #00A86B、哑光珊瑚 #FF6B6B)、`{techwear_outfit}` (压胶缝运动裤 + 压缩上衣、超大防风夹克 + 机能短裤)、`{pose_detail}` (低弓步、单臂伸展查看腕部设备、跳起中)、`{fabric_detail}` (可见压胶缝、反光滚边、网眼透气板)、`{palette}` (单色 + 单一强调色、大地色 + 霓虹绿 #39FF14)

**推荐模型:** NBP — 色块摆放与反射需要复杂空间推理

### Nano Banana 版本:

```
A futuristic sportswear editorial photograph in a {studio_environment} studio space with a matte {floor_color} floor extending to infinity. {model_description} stands in an athletic {pose_detail}, wearing {techwear_outfit} with {fabric_detail}. Three to five large organic 3D blob shapes in {blob_color} with glossy smooth surfaces float at varying heights around the subject — the largest is armchair-sized, the smallest basketball-sized. Each blob has amoebic curves and casts soft colored shadows onto the floor and the model's clothes. Cool directional light from camera-right defines contour and fabric texture. One blob sits partially behind the model, one in front, creating depth. The model is the clear focal point. No text, no logos. Format: 4:5.
```

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
