# 食品与饮料模式

可复用的提示词模板:美食摄影、饮料活动、烹饪插画。每个模式用 `{variables}` 定制。默认模型:GPT Image 2 (5 段式格式),除非另有说明。

---

## 奢华巧克力品牌活动

用于高端巧克力或甜点品牌视觉 — 情绪化、有质感,色彩与氛围受控。可适配不同情绪变体(暗黑沉浸、明亮匠人、大地风物起源叙事)。

<!-- Source concept: luxury chocolate brand campaign with variant moods and tactile surfaces -->

```
Scene: {surface_material} surface, {lighting_mood} lighting setup — {light_description}, thin atmospheric haze at background edge, color palette restricted to {palette}
Subject: {product_arrangement} — {product_count} pieces of {chocolate_type} arranged in {arrangement_style}
Important Details: visible snap edge on broken piece revealing {interior_texture}, fine cocoa powder dusted across surface (concentrated near product, fading to clean edges), {garnish_elements} placed deliberately as art direction not garnish, one piece mid-break with clean fracture line, surface texture of chocolate shows {surface_quality}, camera angle {camera_angle}, shallow depth of field with sharpest focus on the broken piece
Use Case: luxury chocolate brand campaign, print ad, packaging insert
Constraints: no human hands, no utensils, no wrappers or packaging visible, no text, cocoa dust must look natural not dumped, maximum {product_count} chocolate pieces, no melting

Mood variant — {mood_name}:
{mood_modifier}
```

**关键调节项:**
- `{surface_material}` — 深色板岩、原色胡桃木、黑大理石、皱褶牛皮纸
- `{lighting_mood}` — 戏剧性明暗对照 / 柔和的漫射暖光 / 冷窗光
- `{light_description}` — 左上方单一硬主光 / 环绕柔光箱 / 透过羊皮纸背光
- `{palette}` — 深棕 #3E2723 + 金 #C9A84C + 黑 / 暖赤陶 #A0522D + 奶油 #FFF8E7 / 祖母绿 #2D6A4F + 铜 #B87333
- `{chocolate_type}` — 单一产地 72% 黑巧、含抹茶纹路白巧、红宝石巧克力
- `{interior_texture}` — 光滑甘纳许芯、脆坚果糖层、海盐焦糖陷
- `{garnish_elements}` — 单根香草荚、盐之花晶体、食用金箔碎片、干树莓
- `{arrangement_style}` — 对角线瀑布、紧簇布局右侧留白、单行
- `{mood_name} / {mood_modifier}` — "Dark Indulgence": 拉高对比、加深阴影、加一缕烟雾 / "Bright Artisan": 阴天日光、提黑、粉彩强调 / "Origin Story": 大地原色、麻布质感、旁边放生可可豆

**推荐模型:** GPT Image 2 (`quality: high`) — 断口细节与可可粉精度

---

## 高级时尚饮料活动板

用于高端饮料品牌活动:以结构化板式布局结合生活方式与产品 — 模特图 + hero 产品 + 产品阵容。

<!-- Source concept: fashion-meets-beverage campaign board with model, hero product, and lineup -->

```
Scene: horizontal triptych layout on single canvas — left panel (45% width), center panel (30%), right panel (25%), thin {divider_color} dividers (2px), unified {color_temperature} color temperature
Subject: {beverage_brand} campaign board featuring {model_description} and {product_name}
Important Details:
  Left panel (lifestyle): {model_description} at {location}, holding {product_name} at {hold_position}, {model_action}, shot on {film_aesthetic} — environment tells the brand story
  Center panel (hero): {product_name} bottle/can beauty shot, {product_angle} angle, {product_surface} surface, single key light with {highlight_style}, condensation droplets on glass/can surface, label sharp and legible
  Right panel (lineup): {lineup_count} product variants arranged in a {lineup_arrangement}, same lighting as center panel but pulled back wider, each label variant distinguishable by color ({variant_colors})
  Typography: none in image
Use Case: brand campaign presentation, pitch deck, retail POS
Constraints: model does not look directly at product (natural interaction), product label consistent and legible in all panels, lighting temperature cohesive, no floating elements, condensation looks physical not painted on
```

**关键调节项:** `{product_name}`、`{beverage_brand}`、`{model_description}`、`{location}` (阳光屋顶酒吧、大理石厨房台面、泳池边)、`{hold_position}` (喝到一半、垂在髋部、随动作举起)、`{model_action}` (笑谈中、看画外、行走)、`{film_aesthetic}` (暖 Kodak Portra 感、干净数字、冷编辑风)、`{product_angle}` (四分之三正面、正对、轻微低角度)、`{product_surface}` (湿黑石、磨砂玻璃架、白大理石)、`{lineup_count}` (3-5)、`{variant_colors}` (琥珀/红宝石/金、薄荷/柠檬/浆果)、`{divider_color}` (#FFFFFF、#1A1A1A)

**推荐模型:** GPT Image 2 (`quality: high`) — 标签可读性与面板一致性

---

## 超写实美食海报模板

用于美食主海报 — 餐厅、外卖应用、菜单板 — 美食即整个构图,含可填充内容槽。

<!-- Source concept: hyper-realistic food poster with controlled composition slots -->

```
Scene: {background_treatment}, {atmosphere_effect}, overall tone {color_tone}
Subject: {dish_name} — {dish_description}, plated on {plate_description}, centered in frame
Important Details:
  Plating: {plating_details}
  Steam/moisture: {steam_detail}
  Garnish: {garnish_detail} placed at {garnish_position}
  Surface: {table_surface}, visible texture extending to frame edges
  Props: {prop_list} — arranged {prop_arrangement}
  Camera: overhead ({overhead_angle}) OR {camera_angle}, {lens_feel}
  Lighting: {food_lighting} — highlights on {highlight_targets}
Use Case: restaurant poster, delivery app hero, menu board, food magazine cover
Constraints: food must look freshly prepared (not cold or sat-out), no human hands or utensils in active use (props only), colors must be appetizing — no blue cast, no desaturated tones on the food itself, {plate_description} must not compete with the dish
```

**关键调节项:**
- `{dish_name}` / `{dish_description}` — 以诱人物理细节描述的主打美食
- `{plate_description}` — 哑光白陶瓷、深色炻器、质朴木盘、香蕉叶
- `{plating_details}` — 2 点钟方向酱汁飞弧、10 点钟方向微型芽菜、芝麻散撒
- `{steam_detail}` — 中间上升的可见蒸汽缕、旁边玻璃上的冷凝、无蒸汽
- `{garnish_detail}` — 单叶罗勒、辣椒碎散撒、柑橘皮卷
- `{table_surface}` — 陈年橡木、深混凝土、带灰纹白大理石
- `{prop_list}` — 亚麻餐巾、复古叉、小碗酱汁、散撒香草
- `{food_lighting}` — 左上方暖向光带补光反弹、正午硬光、情绪化侧光
- `{background_treatment}` — 暗角、干净明亮、乡村模糊
- `{camera_angle}` — 45 度四分之三、正对平视、俯视平铺

**推荐模型:** GPT Image 2 (`quality: high`) — 蒸汽、冷凝与食材纹理保真

---

## 博物学食品标本剖面

用于教育性食品内容、食材特写或匠人品牌叙事 — 以 19 世纪博物学版画风格把食物渲染成科学插画。

<!-- Source concept: Audubon-style naturalist botanical/food specimen illustration with cross-section -->

A detailed naturalist illustration of {food_item} rendered in the style of 19th-century scientific specimen plates. The composition shows the item in three states arranged vertically on an aged {paper_color} parchment background: whole specimen at top with botanical accuracy, lateral cross-section at center revealing internal structure ({internal_details}), and an exploded detail of {detail_element} at bottom with fine ink annotation lines pointing to key features. Drawn with precise {medium_description} — visible hatching for shadow, stippling for texture, thin ink outlines. Color is naturalistic but slightly muted as if from a hand-tinted lithograph. A thin decorative border frames the composition. Small italic Latin-style label "{latin_label}" at the bottom in serif font, {ink_color} ink. Format: 3:4.

**关键调节项:** `{food_item}` (石榴、酸种面包、和牛肋眼、可可荚)、`{internal_details}` (带红宝石籽粒的籽室、不规则气孔的包心结构、雪花脂肪分布)、`{detail_element}` (单粒籽实解剖、外皮分层、脂肪晶体结构)、`{paper_color}` (暖奶油 #FDF5E6、冷象牙 #FFFFF0)、`{medium_description}` (水彩晕染加墨线、石墨加彩铅、纯墨尽量少色)、`{latin_label}` (一个俏皮的拉丁化名称)、`{ink_color}` (褐染 #704214、印度黑 #1A1A1A)

**推荐模型:** NB2 — 博物插画风格,植物图版美学的图像接地

---

## 城市美食地图插画

用于餐厅指南、美食节材料、旅行内容或本地美食特写 — 鸟瞰插画地图呈现一座城市的特色美食。

<!-- Source concept: hand-drawn illustrated food map of a city with dish icons and landmarks -->

A hand-drawn illustrated bird's-eye map of {city_name} showing its food culture. The map covers the {area_description} with simplified but recognizable {landmark_list} drawn in a loose ink-and-watercolor style. Scattered across the map are {dish_count} illustrated food items representing local specialties — each dish ({dish_list}) drawn at exaggerated scale hovering near its neighborhood, rendered in warm appetizing watercolor with visible brushstrokes. Streets are thin ink lines with {street_style}. Water features rendered in soft {water_color} wash. The overall palette is {palette_description}. A decorative hand-lettered title "{MAP_TITLE}" sits in a banner at the top. Small hand-written labels mark each dish and neighborhood. Style references vintage travel poster illustration meets editorial food drawing. Format: {aspect_ratio}.

**关键调节项:** `{city_name}`、`{area_description}` (中心 5 公里、老城街区、滨水区)、`{landmark_list}` (主教堂、中央市场、河桥)、`{dish_count}` (6-10)、`{dish_list}` (集市旁的抓饭、老城的烤包子、公园旁的烤肉串)、`{street_style}` (轻微歪斜的手绘、干净但简化)、`{water_color}` (蔚蓝 #0077B6、青绿 #2A9D8F)、`{palette_description}` (暖赤陶与奶油、食物全饱和色;冷蓝绿配暖食点缀)、`{MAP_TITLE}` ("A Taster's Guide to {city_name}")、`{aspect_ratio}` (3:4、1:1)

**推荐模型:** NB2 — 真实城市地标的图像接地 + 插画风格

### Nano Banana 版本:

```
A hand-drawn illustrated bird's-eye food map of {city_name}, covering the {area_description}. Simplified but recognizable {landmark_list} are drawn in loose ink-and-watercolor style. {dish_count} local dishes ({dish_list}) float at exaggerated scale near their neighborhoods, each painted in warm appetizing watercolor with visible brushstrokes. Streets are thin freehand ink lines. Water features in soft {water_color} wash. A hand-lettered banner at top reads "{MAP_TITLE}". Small hand-written labels mark dishes and neighborhoods. Style mixes vintage travel poster illustration with editorial food drawing. Palette: {palette_description}. Format: {aspect_ratio}.
```

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
