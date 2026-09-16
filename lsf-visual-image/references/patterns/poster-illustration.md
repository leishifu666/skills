# 海报与插画模式

可复用的提示词模板:海报、艺术印刷品、活动拼贴与平面插画。每个模式用 `{variables}` 定制。默认模型:GPT Image 2.5 (5 段式格式),除非另有说明。

---

## 跨越两个世纪的城市(时间分割构图)

用于城市发展活动、周年纪念材料、文化展览或编辑专题 — 同一城市景观从中间一分为二,一半历史、一半现代。

<!-- Source concept: time-split composition — same city view, two eras side by side -->

```
Scene: wide establishing shot of {city_landmark_view}, frame divided vertically down the center — left half shows the scene in {historical_era}, right half shows {modern_era}
Subject: the same geographic viewpoint across two time periods, architecture and infrastructure transforming at the dividing line
Important Details:
  Left half ({historical_era}): {historical_details} — muted {historical_palette} palette, {historical_atmosphere}, period-accurate architecture, {historical_figures} going about daily life, {historical_transport}
  Right half ({modern_era}): {modern_details} — {modern_palette} palette, {modern_atmosphere}, contemporary architecture where old buildings once stood (some landmarks preserved), {modern_figures}, {modern_transport}
  Dividing line: not a hard cut — elements morph and blend across a narrow 5% transition zone (a horse-drawn cart becomes a car, a gas lamp becomes LED, cobblestones become asphalt, a tree grows taller)
  Sky transitions too: {historical_sky} on left to {modern_sky} on right
  Camera angle: elevated three-quarter view (roughly 30 degrees above street level) to show depth of both eras
Use Case: city anniversary campaign, urban development feature, cultural exhibition poster, editorial illustration
Constraints: both halves must depict the SAME geographic location (matching terrain, river, hill positions), transition zone should feel organic not pasted, scale and perspective consistent across both halves, no text unless specified, no anachronistic elements (modern items in historical half or vice versa outside the transition)
```

**关键调节项:** `{city_landmark_view}` (沿主大道望向中央广场的视角、滨河全景、从山坡俯瞰老城的视角), `{historical_era}` / `{modern_era}` (1920 年代 / 2020 年代、中世纪 / 当代、1960 年代 / 2060 年代), `{historical_details}` (鹅卵石街道、马车、手绘店铺招牌), `{modern_details}` (玻璃幕墙、屋顶花园、数字招牌), `{historical_palette}` (棕褐色与低饱和大地色、手工上色照片的质感), `{modern_palette}` (干净现代的色彩、偏冷蓝灰配暖色点缀), `{historical_atmosphere}` (煤烟薄雾、清晨柔雾), `{modern_atmosphere}` (晴空、地平线处的光污染光晕), `{historical_sky}` (暖调阴天), `{modern_sky}` (干净的渐变蓝)

**推荐模型:** NBP — 建筑变形与透视一致性的空间推理

### Nano Banana 版本:

```
A wide elevated view of {city_landmark_view}, divided vertically down the center into two eras. The left half depicts the scene in {historical_era}: {historical_details}, rendered in a muted {historical_palette} palette with {historical_atmosphere}. The right half shows {modern_era}: {modern_details} in a {modern_palette} palette under {modern_atmosphere}. At the center dividing line, elements morph organically across a narrow transition zone — a horse-drawn cart becomes a car, gas lamps become LED lights, cobblestones blend into asphalt, trees grow taller. The sky transitions from {historical_sky} on the left to {modern_sky} on the right. Both halves share the same geographic terrain and perspective. Camera angle roughly 30 degrees above street level. Format: 16:9.
```

---

## 健身拳击活动拼贴

用于运动与健身品牌活动 — 围绕拳击/格斗运动主题,将动作、细节与氛围结合的动态三联拼贴。

<!-- Source concept: 3-panel fitness/boxing campaign collage with action and detail shots -->

```
Scene: three-panel horizontal collage on {canvas_color} canvas — left panel (35%), center panel (40%), right panel (25%), {divider_style} dividers, unified {overall_tone} color tone
Subject: {athlete_description} in a boxing/training context — same person across all panels
Important Details:
  Left panel (environment): wide shot of {gym_environment}, atmospheric — {atmosphere_detail}, equipment visible but out of focus, {athlete_description} as a silhouette or distant figure warming up, mood: anticipation
  Center panel (action): medium shot, {athlete_description} mid-{action_type}, captured at peak effort — {action_detail}, sweat visible on skin and {gear_description}, sharp focus on face showing {expression}, directional hard light from {light_direction} creating dramatic shadow on the opposite side of the face, slight motion trail on the {moving_element}
  Right panel (detail): extreme close-up of {detail_subject} — {detail_description}, texture dominates the frame, {detail_lighting}
  Grain: uniform {grain_level} across all panels
  Color: {color_treatment}
Use Case: fitness brand campaign, gym poster, sportswear ad, magazine editorial spread
Constraints: same athlete across all panels (consistent identity, gear, wraps), no text or logos, no sponsor branding, center panel is the visual anchor — should feel like the decisive moment, grain must be uniform not just added to one panel
```

**关键调节项:** `{athlete_description}`、`{gym_environment}` (带重沙袋的工业风拳馆、户外混凝土训练场、昏暗的地下拳台)、`{atmosphere_detail}` (逆光中的粉笔灰、冷空气中呼出的蒸汽、高窗洒下的金色光线)、`{action_type}` (出后手直拳、重沙袋上勾拳、跳绳)、`{action_detail}` (拳头击中沙袋产生可见的冲击波纹、绳索在头顶成弧线定格)、`{gear_description}` (红色手绑带、磨损的皮革手套、不戴手套 — 缠胶带的指节)、`{expression}` (专注的强度、克制的呼气、战吼)、`{detail_subject}` (贴胶带的指节抵着红色帆布、磨损的拳击靴鞋带、汗水从下巴滴落到帆布上)、`{detail_description}` (每根胶带纤维清晰可见、皮革在弯曲处开裂、单个汗滴悬在半空)、`{color_treatment}` (低饱和配暖中间调、高对比单色配棕褐色、青橙分离色调)、`{canvas_color}` (哑光黑 #0D0D0D、深炭灰 #1A1A1A)、`{divider_style}` (2px 细白线、无分隔线 — 边缘出血)

**推荐模型:** GPT Image 2.5 — 面板间的身份一致性与汗水/纹理细节

---

## 薰衣草色智能手机主视觉广告

用于科技产品发布视觉 — 干净、以色彩主导的主视觉镜头:智能手机(或类似设备)悬浮在同色系渐变背景前,配有柔和的 3D 点缀元素。

<!-- Source concept: smartphone product launch hero in monochromatic lavender with floating accent shapes -->

```
Scene: smooth gradient background from {color_light} to {color_dark}, no hard edges, studio void environment
Subject: {device_name} floating at slight {tilt_angle}-degree angle, screen facing camera showing {screen_content}, centered vertically but offset {horizontal_position} horizontally
Important Details: device renders with physically accurate {device_finish} — visible edge chamfer catching a thin highlight line, screen content crisp and legible at this scale, {accent_element_count} soft 3D shapes floating nearby (matte {accent_shape_color} {accent_shapes} — frosted glass or soft plastic appearance, each {accent_size}), shapes are out of focus at varying depths creating a layered composition, soft omnidirectional lighting with a subtle key from upper-left, gentle device shadow projected onto the gradient ({shadow_softness}), overall color palette stays within the {color_family} family — no complementary or clashing tones
  Bottom text area: "{HEADLINE}" in {headline_weight} {headline_font_style}, {headline_color}, centered below device
  Subtext: "{SUBHEADLINE}" in thin weight, {subtext_color}, below headline
Use Case: product launch hero, website header, retail POS, digital ad
Constraints: screen content must be sharp and readable, floating shapes must not obscure the device screen, no reflections of a studio environment on screen, gradient is smooth — no banding, device proportions must match a real smartphone (no stretched or squished body), text exactly as quoted
Quality: high
```

**关键调节项:** `{device_name}`、`{color_light}` / `{color_dark}` (薰衣草紫 #E6D5F5 到 #7B4FA0、薄荷绿 #D0F0E0 到 #1B7A5A、珊瑚 #FFDDD2 到 #C44536)、`{device_finish}` (哑光铝、抛光钛、磨砂玻璃背板)、`{screen_content}` (干净的带应用图标的主屏、显示风景的相机应用、渐变壁纸)、`{accent_shapes}` (球体、圆角胶囊、柔和立方体、圆环)、`{accent_shape_color}` — 与背景同色系但更浅或更饱和、`{accent_size}` (高尔夫球到葡萄柚大小)、`{HEADLINE}` / `{SUBHEADLINE}`、`{headline_color}` (白 #FFFFFF、色系的深色调)、`{color_family}` (薰衣草紫、鼠尾草绿、暖赤陶)、`{tilt_angle}` (5-15)、`{horizontal_position}` (左三分之一、居中、右三分之一)

**推荐模型:** GPT Image 2.5 (`quality: high`) — 文字渲染、屏幕内容可读性与设备准确性

---

## 祖母绿街头时尚海报

用于品牌上新、活动公告或杂志封面 — 粗体排印与街头时尚人物在饱和色场上平分视觉比重。

<!-- Source concept: bold emerald fashion poster with oversized type and street style figure -->

```
Scene: solid {background_color} background (flat, no gradient), graphic poster composition split between typography (upper 55%) and figure (lower 60%, overlapping into the type zone)
Subject: {model_description} in {outfit_description}, full-body shot from low angle (worm's eye, approximately 15 degrees below eye level), standing with {pose_description}
Important Details: "{MAIN_TITLE}" in extra-bold extended {title_font_style}, {title_color}, filling the upper half — each letter approximately 20% of frame height, model's head and shoulders break in front of the bottom row of letters (depth layering), "{SUBTITLE}" in lightweight condensed type, {subtitle_color}, running along the bottom edge or lower-right corner, model lit by overcast flat light — even exposure, minimal shadow, fabric textures fully readable ({fabric_details}), shoes visible and grounded (not floating), {graphic_accents} if any
Use Case: fashion brand poster, event flyer, editorial magazine cover, retail window display
Constraints: title text fully legible — model overlap must not obscure more than one letter by more than 40%, no additional decorative elements unless specified in {graphic_accents}, background is flat solid color — no texture or pattern, "{MAIN_TITLE}" and "{SUBTITLE}" spelled exactly as given, model does not hold props unless specified
Quality: high
```

**关键调节项:** `{background_color}` (祖母绿 #006B3F、钴蓝 #0047AB、藏红花黄 #F4C430、亮粉 #FF1493)、`{model_description}`、`{outfit_description}` (超大皮风衣 + 厚底运动鞋、短款飞行员夹克 + 阔腿裤 + 厚底靴)、`{pose_description}` (宽站姿双臂交叉、一只手整理衣领、行走步态定格在半步之间)、`{MAIN_TITLE}` / `{SUBTITLE}`、`{title_font_style}` (几何无衬线、怪诞体、模板镂空体)、`{title_color}` (#FFFFFF、#000000、奶油白 #FFF5E1)、`{subtitle_color}` (与标题同色但 60% 不透明度)、`{fabric_details}` (皮革可见颗粒、灯芯绒棱纹、丹宁布锁边)、`{graphic_accents}` (无、距边缘 20px 的细白边框、左下角小 logo 标志)

**推荐模型:** GPT Image 2.5 (`quality: high`) — 排印渲染与人物-字体层次穿插

---

## 孔雀植物复古艺术印刷品

用于装饰印刷品、包装插画、壁纸设计或编辑艺术 — 以复古版画风格呈现孔雀与植物元素对称组合的构图。

<!-- Source concept: peacock botanical vintage symmetrical art print — ornamental and decorative -->

A symmetrical ornamental art print centered on a {peacock_variant} peacock in full tail display, viewed from {view_angle}. The tail feathers fan into a perfect semicircle filling the upper two-thirds of the frame, each eye-spot rendered with precise detail — iridescent {eye_colors} with fine barb texture. The peacock stands on a {base_element} at the composition's center axis. Flanking the bird symmetrically: {botanical_left} on the left mirrored by {botanical_right} on the right — leaves, stems, and blossoms curve inward framing the peacock. {additional_fauna} perch or fly near the upper corners. The entire composition sits on a {background_texture} background in {background_color}. Rendering style: {print_style} — visible {technique_marks}, rich but slightly flattened color as if from layered printing passes. Border: {border_style}. Color palette: {palette}. Format: 3:4.

**关键调节项:** `{peacock_variant}` (印度蓝、白色白化、爪哇绿)、`{view_angle}` (正面直视、向左转三分之四)、`{eye_colors}` (深蓝 #003366 + 祖母绿 #006B3F + 金 #C9A84C、单色 — 全部为藏蓝与银色系)、`{base_element}` (华丽石雕底座、开花枝条、装饰瓷砖地面)、`{botanical_left}` / `{botanical_right}` (玉兰枝、垂紫藤、西番莲藤蔓、班克木花梗)、`{additional_fauna}` (两只小蝴蝶、一对蜻蜓、无)、`{background_texture}` / `{background_color}` (做旧亚麻 #F5F0E1、深藏蓝 #0A1628、奶油羊皮纸 #FDF5E6)、`{print_style}` (手工上色铜版画、木版画、彩色石版画)、`{technique_marks}` (阴影区交叉排线、可见版调、四角套准标记)、`{border_style}` (细双线新艺术风格边框、角部装饰花饰、简单单线矩形)、`{palette}` (天然宝石色 — 祖母绿、蓝宝石、金色配奶油 / 三色限定 — 青绿、铜、黑配象牙 / 低饱和大地色 — 鼠尾草、赤陶、赭棕)

**推荐模型:** NB2 — 图像接地,确保孔雀解剖与植物物种准确

### Nano Banana 版本:

```
A symmetrical ornamental art print centered on a {peacock_variant} peacock in full tail display, viewed {view_angle}. Tail feathers fan into a perfect semicircle filling the upper two-thirds, each eye-spot rendered with iridescent {eye_colors} and fine barb texture. The peacock stands on a {base_element}. Flanking it symmetrically: {botanical_left} on the left mirrored by {botanical_right} on the right, stems and blossoms curving inward to frame the bird. {additional_fauna} near the upper corners. Background: {background_texture} in {background_color}. Style: {print_style} with visible {technique_marks} and slightly flattened color as from layered printing passes. Border: {border_style}. Palette: {palette}. Format: 3:4.
```

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
