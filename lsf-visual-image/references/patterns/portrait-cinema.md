# 人像与电影模式

可复用的提示词模板:电影感人像、氛围人物摄影、情绪驱动的人像。每个模式用 `{variables}` 定制。默认模型:GPT Image 2.5 (5 段式格式),除非另有说明。

---

## 黄金时刻街上逆光人像

用于温暖、情感化的街头人像,带强烈逆光光晕 — 编辑大片、个人品牌、专辑封面。

<!-- Source concept: golden hour backlit street portrait with lens flare and warm atmospheric haze -->

```
Scene: {street_description} at golden hour, sun positioned directly behind subject (5-10 degrees above horizon line), warm amber light flooding the street, slight atmospheric haze diffusing the backlight
Subject: {person_description}, standing at {position_in_street}, body angled three-quarter to camera, face turned toward lens with {expression}
Important Details: strong rim light outlining hair and shoulders in warm gold (#FFAA33), face lit primarily by bounce light from {bounce_surface} on the opposite side — softer and cooler than the backlight, shallow depth of field rendering background into warm bokeh circles, {clothing_detail} catches backlight along edges showing fabric texture, visible lens flare — one or two hexagonal flare artifacts near frame edge (organic, not excessive), long shadow cast toward camera on {ground_surface}, skin rendered naturally with warm undertones — no heavy smoothing, visible pores, {color_grade}
Use Case: editorial portrait, personal brand photography, album art
Constraints: face must be visible and well-exposed despite backlight (not silhouetted), no reflectors or studio equipment visible, lens flare limited to one or two subtle artifacts — not a starburst explosion, no added text, no vignette
```

**关键调节项:** `{street_description}` (带石墙的欧洲窄巷、两旁椴树的宽阔大道、砖墙工业后巷)、`{person_description}`、`{expression}` (安静的自信、闭唇浅笑、沉思凝视)、`{bounce_surface}` (奶油色粉刷墙、停放的白色面包车、沙色建筑)、`{clothing_detail}` (亚麻衬衫领、皮夹克肩缝、围巾边缘)、`{ground_surface}` (湿润鹅卵石、干沥青、压实泥土)、`{color_grade}` (Kodak Portra 400 的暖感、微提黑位带琥珀色偏、干净数码感配暖白平衡)

**推荐模型:** GPT Image 2.5 — 逆光曝光控制与皮肤渲染

---

## 便利店霓虹人像

用于混合人造光源下的都市夜景人像 — 头顶日光灯管与彩色霓虹招牌在人物脸部形成色彩的推拉对比。

<!-- Source concept: convenience store / bodega neon portrait — fluorescent + neon mixed light on face -->

```
Scene: exterior of a {store_type} at night, shot through or near the front window/entrance, overhead fluorescent tubes casting flat {fluorescent_color} light from inside, {neon_sign_description} mounted on the wall/window casting {neon_color} glow on one side of the subject's face
Subject: {person_description}, {pose_description}, positioned at the threshold between interior fluorescent zone and exterior neon zone — split lighting across the face
Important Details: face receives {fluorescent_color} fill from the store interior on one side and {neon_color} accent from signage on the other — the two colors mix on the nose bridge and chin, visible product shelves or cooler glow softly in background bokeh, {clothing_description} absorbs and reflects the two light sources differently, condensation or grime on window glass if shot through it (subtle, not obscuring), wet pavement outside reflects both light sources in streaks, shallow depth of field with subject sharp, background a mosaic of colored bokeh, {camera_feel}
Use Case: urban editorial, music press portrait, fashion story, short film still
Constraints: face clearly visible — neither light source blows out features, neon sign text (if present) is secondary to the portrait not the focal point, no additional light sources beyond what exists in the scene, no heavy color grading beyond what the practical lights create naturally, no motion blur
```

**关键调节项:** `{store_type}` (韩式便利店、社区小杂货店 bodega、深夜药店、24 小时自助洗衣店)、`{fluorescent_color}` (冷蓝白、偏绿白、暖钨丝)、`{neon_sign_description}` (红色 "OPEN" 招牌、蓝色啤酒品牌 logo、粉色手写体字样)、`{neon_color}` (红 #FF2D2D、蓝 #3366FF、粉 #FF69B4、绿 #39FF14)、`{person_description}`、`{pose_description}` (倚靠门框、坐在翻倒的板条箱上、双手插兜站立)、`{clothing_description}` (吸光的深色卫衣、反射两种颜色的白色 T 恤、镜面反射的皮革)、`{camera_feel}` (Cinestill 800T 霓虹光晕、干净的夜间数码、Fujifilm 色彩科学)

**推荐模型:** GPT Image 2.5 (`quality: high`) — 皮肤上双光源色彩的精确渲染

---

## 单色故障剪影人像

用于前卫、科技感的人像 — 艺术家资料照、电子音乐媒体宣传、科技品牌活动。高对比黑白,带选择性的红色数字故障元素。

<!-- Source concept: monochrome profile portrait with digital glitch artifacts and red accent color -->

```
Scene: pure black background (#000000), no environment — subject emerges from darkness
Subject: {person_description} in sharp profile (facing {direction}), head and upper shoulders only, high-contrast black-and-white rendering
Important Details: extreme contrast — skin highlights blow to near-white, shadows fall to pure black with minimal midtone graduation, {hair_detail} silhouetted against black, one eye visible in profile with a single catchlight, horizontal glitch displacement lines cutting across the image at {glitch_positions} — each line offsets a thin horizontal slice (4-8px) to the right by 10-20px, the displaced slices rendered in {accent_color} (#FF0000 default) while the rest remains monochrome, fine horizontal scan lines across entire image (subtle, CRT monitor texture), grain: heavy high-ISO film grain throughout, jaw line and nose bridge are the sharpest elements in frame
Use Case: artist press photo, electronic music EP cover, tech brand portrait, social media profile
Constraints: glitch lines must look digital (clean horizontal displacement, not organic), accent color appears ONLY in the displaced glitch slices — no other colored elements, maximum {max_glitch_lines} glitch lines to avoid visual noise, face must remain recognizable despite artifacts, no text, background is solid black — no gradient or texture
```

**关键调节项:** `{person_description}`、`{direction}` (左、右)、`{hair_detail}` (显露头骨轮廓的紧贴寸头、及肩长发带逆光下飞散的发丝、向后束起的发髻)、`{glitch_positions}` (横穿眼部、横穿嘴部、横穿额头 — 指定 2-3 个位置)、`{accent_color}` (#FF0000 红、#00FF41 终端绿、#FF00FF 品红)、`{max_glitch_lines}` (3-5)

**推荐模型:** GPT Image 2.5 — 高对比单色渲染与受控的故障定位

---

## 日系负片天台人像

用于情绪化、氛围感人像,带有过曝负片的特质 — 低饱和色彩、抬升的阴影与褪色记忆的感觉。适合编辑大片、独立杂志或个人项目。

<!-- Source concept: Japanese negative film aesthetic — overexposed, muted tones, rooftop setting -->

A waist-up portrait of {person_description} on a {rooftop_description}. They stand near the edge railing, {pose_description}, with the {city_skyline} visible behind them but washed out and desaturated by {sky_condition}. Shot on expired Japanese negative film — colors shifted toward {color_shift}, highlights blown soft and chalky, shadows lifted with visible grain in the flat midtones. Skin tones slightly green-yellow as if the film has aged. {clothing_description} reads as muted tones, almost monochromatic against the overexposed sky. Wind moves {wind_detail}. The mood is nostalgic and transient — a memory captured on deteriorating film stock. Eye-level framing, subject slightly off-center toward {frame_position}. Format: {aspect_ratio}.

**关键调节项:** `{person_description}`、`{rooftop_description}` (混凝土公寓楼天台、带排风管的工业仓库屋顶、带铁丝网的学校楼屋顶)、`{pose_description}` (倚着栏杆看向镜头、转身望向天际线、坐在边缘屈膝抱腿)、`{city_skyline}` (东京中层公寓楼群、带电线杆的泛亚城市)、`{sky_condition}` (阴天白空、雾蒙蒙的午后阳光)、`{color_shift}` (青绿偏色、黄琥珀偏色)、`{clothing_description}` (超大复古防风衣、纯白 T 恤、藏蓝工装夹克)、`{wind_detail}` (吹过脸颊的头发、夹克下摆、衣领)、`{frame_position}` (左三分之一、右三分之一)、`{aspect_ratio}` (3:2、4:5)

**推荐模型:** NB2 — 模拟胶片颗粒仿真与氛围情绪

---

## 梦幻水下超现实人像

用于美妆活动、概念艺术或专辑视觉 — 人物漂浮于清澈水体中,周围环绕半透明的水生元素。

<!-- Source concept: surreal underwater portrait with translucent fish and dreamy caustic light -->

```
Scene: clear {water_color} water filling the entire frame, caustic light patterns rippling across the subject from above (sunlight through water surface), no visible pool walls or floor — infinite aquatic void
Subject: {person_description}, floating in a relaxed {pose_description}, eyes {eye_state}, hair fanning out in all directions as if weightless, {clothing_description} billowing and suspended in the water
Important Details: {fish_count} translucent {fish_type} swimming in a loose school around the subject — each fish semi-transparent with visible skeletal structure and iridescent scales catching the caustic light, light rays penetrating from above in {light_pattern}, fine air bubbles rising from near the subject's {bubble_source}, fabric of clothing moves independently from the body — folds and hems suspended in mid-drift, skin has a subtle cool {water_tint} cast from the water, overall palette is {palette}, composition framed as a {shot_type}
Use Case: beauty campaign, album cover, conceptual art print, fashion editorial
Constraints: subject's face must be clearly visible and serene (not distressed or holding breath with effort), fish are translucent — not solid opaque tropical fish, no visible water surface edge or pool tiles, no scuba gear or goggles, bubbles are small and delicate not large air pockets, underwater physics must be consistent (everything floats)
```

**关键调节项:** `{water_color}` (深蔚蓝 #0077B6、浅蓝绿 #AFEEEE、深青 #004D4D)、`{person_description}`、`{pose_description}` (双臂微张如缓慢自由下落、蜷缩的胎儿姿势、单臂向上伸向光源)、`{eye_state}` (轻轻闭合、睁眼凝望上方光线、直视镜头)、`{clothing_description}` (飘逸的白色真丝长裙、宽松亚麻衬衫与长裤、半透明欧根纱披巾)、`{fish_count}` (5-8)、`{fish_type}` (水母、小型礁鱼、细长玻璃猫鱼)、`{light_pattern}` (右上方平行的上帝光、分散斑驳的焦散光、单束集中光柱)、`{bubble_source}` (唇边、指尖、布料边缘)、`{water_tint}` (蓝绿色、海蓝色)、`{palette}` (青绿+象牙白、深蓝+金、海沫绿+腮红粉)、`{shot_type}` (全身竖幅、居中半身、带下方留白的三分之四构图)

**推荐模型:** NBP — 复杂物理效果(漂浮的头发、布料、鱼的半透明与焦散光)

### Nano Banana 版本:

```
A surreal underwater portrait of {person_description} floating in a relaxed {pose_description} in clear {water_color} water. Eyes {eye_state}, hair fans out weightlessly in all directions. {clothing_description} billows and suspends in the current, folds drifting independently. {fish_count} translucent {fish_type} swim in a loose school around the subject — each semi-transparent with visible skeletal structure and iridescent scales catching caustic light from above. Sunlight penetrates from the surface in {light_pattern}, casting rippling patterns across skin and fabric. Fine air bubbles rise from the subject's {bubble_source}. Skin has a subtle cool {water_tint} cast. No pool walls, no surface edge visible — infinite aquatic void. Serene and dreamlike. Palette: {palette}. Format: 4:5.
```

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
