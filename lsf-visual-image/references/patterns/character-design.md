# 角色设计模式

可复用的提示词模板:角色三视图、表情表、服装变体、手办/卡片格式。每个模式用 `{variables}` 定制。默认模型:GPT Image 2.5 (5 段式格式),除非另有说明。

> 本文件负责“怎样展示已经确定的角色”。如果用户要从零设计身份、随机创建角色或解决模板化 AI 脸,必须先读 [character-identity-design.md](../character-identity-design.md),生成约 10 个锁定锚点后再填入本文件模板。服装变体、表情变化等模板只在用户明确授权对应变化时使用;否则身份档案中的所有锚点保持不变。

---

## 角色三视图 (3 视图)

用于游戏或动画前期制作 — 在单一白色画布上呈现角色的正面、侧面、背面,带色卡标注与身高参考线。

<!-- Source concept: character model sheet / turnaround sheet for 3D modelers and animators -->

```
Scene: clean white background, flat even lighting with no cast shadows, thin horizontal height reference lines in #CCCCCC spanning the full width at head, shoulder, waist, knee, and foot level
Subject: {character_name} — {character_description} — shown in three views arranged left to right: front view (facing camera), three-quarter side view (turned 75 degrees right), back view (facing away)
Important Details: all three views share identical proportions and vertical alignment along the height lines, feet on the same baseline, arms relaxed at sides for clear silhouette reading, color callout annotations — small circles of each key color ({color_1} {hex_1}, {color_2} {hex_2}, {color_3} {hex_3}) connected by thin #999999 leader lines to the corresponding material on the front view, fine line weight for height markers, clothing folds and seam lines consistent across all three angles
Use Case: game character pre-production, animation model sheet, 3D reference handoff
Constraints: no background elements, no props in hands, no dramatic poses — neutral standing pose only, all three views must depict the exact same character with identical outfit and proportions, no drop shadows, no gradient backgrounds
```

**关键调节项:** `{character_name}`、`{character_description}` (年龄、体形、发型、服装 — 要具体)、`{color_1}`/`{hex_1}` 至 `{color_3}`/`{hex_3}` (色卡标注的关键调色板颜色,如夹克藏青 #1B2A4A、皮肤暖米色 #D4A574、头发赭红 #8B3A2F)

**推荐模型:** GPT Image 2.5 (`quality: high`) — 身高参考线与色卡文字需要精确渲染

---

## 表情表

用于为同一角色生成 6–9 个面部表情的网格 — 头部角度与美术风格一致,每张脸下方有情绪标签。

<!-- Source concept: character expression/emotion reference sheet for animation or visual novel production -->

```
Scene: white background, 3x3 grid (or 3x2 for 6 expressions) with thin #DDDDDD divider lines, each cell contains one head-and-shoulders portrait
Subject: {character_name} — {character_description} — same head angle (three-quarter left), same hairstyle, same lighting across all cells
Important Details:
  Cell 1: neutral — relaxed brow, closed mouth, calm eyes. Label: "NEUTRAL"
  Cell 2: happy — genuine smile reaching the eyes, raised cheeks. Label: "HAPPY"
  Cell 3: angry — furrowed brow, clenched jaw, narrowed eyes. Label: "ANGRY"
  Cell 4: sad — downturned mouth, glistening eyes, slightly lowered head. Label: "SAD"
  Cell 5: surprised — wide eyes, raised eyebrows, open mouth. Label: "SURPRISED"
  Cell 6: disgusted — wrinkled nose, upper lip raised, squinted eyes. Label: "DISGUSTED"
  {extra_expressions}
  Labels in small {label_font} beneath each cell, #555555 text
  Consistent {art_style} rendering across all cells — skin tone, line weight, shading approach identical
Use Case: animation expression reference, visual novel sprite guide, game character documentation
Constraints: same character identity in every cell — no variation in hair, accessories, skin tone, or clothing between expressions, head angle stays fixed, no hand gestures, labels must be legible
```

**关键调节项:** `{character_name}`、`{character_description}` (脸型、肤色、发型、特征标志)、`{art_style}` (干净赛璐璐日式动画、绘画感半写实、扁平矢量插画)、`{label_font}` (窄体无衬线、等宽、圆体无衬线)、`{extra_expressions}` (添加 7-9 格:如 "Cell 7: smirk — one corner of mouth raised, knowing look. Label: 'SMIRK'")

**推荐模型:** GPT Image 2.5 (`quality: high`) — 文字标签与跨 9 格一致的面部身份需要精确控制

---

## 服装变体网格

用于展示一个角色的多套服装/戏装 — 时尚探索、游戏皮肤概念、服装设计。

<!-- Source concept: character costume/skin variant sheet for fashion or game design -->

```
Scene: light neutral background ({bg_color}), {grid_layout} grid, thin white gaps between cells, soft even front lighting in every cell
Subject: {character_name} — {character_description} — same pose ({pose_description}) in every cell, only the outfit changes
Important Details:
  Cell 1: {outfit_1_name} — {outfit_1_description}
  Cell 2: {outfit_2_name} — {outfit_2_description}
  Cell 3: {outfit_3_name} — {outfit_3_description}
  Cell 4: {outfit_4_name} — {outfit_4_description}
  Cell 5: {outfit_5_name} — {outfit_5_description}
  Cell 6: {outfit_6_name} — {outfit_6_description}
  Outfit name in small bold sans-serif centered below each cell, #333333 text
  Character body proportions, face, hairstyle, and skin tone identical across all cells — only clothing and accessories differ
Use Case: game skin lineup, fashion mood board, costume design exploration
Constraints: same character identity and pose in every cell, no background scenery — character only, outfit labels must be readable, no overlapping garments between cells, {grid_layout} layout must be uniform
```

**关键调节项:** `{character_name}`、`{character_description}` (体形、脸、头发 — 锚定身份)、`{bg_color}` (#F0F0F0 浅灰、#FFF8F0 暖奶油、#E8EDF2 冷蓝灰)、`{grid_layout}` (2x3 或 3x3)、`{pose_description}` (双手叉腰、放松站立、单手抬起)、`{outfit_N_name}` / `{outfit_N_description}` (如 "Street Casual" — oversized denim jacket, white tee, black cargo pants, chunky sneakers)

**推荐模型:** GPT Image 2.5 (`quality: medium`) — 角色一致性优先;仅当服装标签需要精细可读时才用 `high`

---

## Q版 / 迷你全身手办

用于把写实角色变成可爱的 3D 收藏手办 — 大头、紧凑身体、多个姿势做不同活动。

<!-- Source concept: chibi/super-deformed vinyl collectible figurine with consistent identity across poses -->

```
Scene: soft gradient background ({bg_gradient}), studio product lighting with rim light from behind and soft fill from front, subtle ground shadow beneath each figurine
Subject: chibi-style 3D collectible figurine of {character_name} — {character_description_simplified} — large head (roughly 1:2 head-to-body ratio), rounded limbs, smooth matte vinyl surface, {num_poses} poses arranged in a row
Important Details:
  Pose 1: {pose_1_description}
  Pose 2: {pose_2_description}
  Pose 3: {pose_3_description}
  {extra_poses}
  Face retains recognizable features from the original character — {face_markers} — simplified into the chibi style with large round eyes and small nose/mouth
  Outfit matches the original: {outfit_simplified} — colors preserved ({color_palette}), details reduced to clean shapes
  Each figurine sits on a small circular base ({base_color} matte finish)
  Vinyl toy aesthetic — visible seam line at sides, slight glossy highlight on forehead and cheeks
Use Case: merchandise concept, social media avatar set, fan collectible design
Constraints: consistent face and outfit across all poses, chibi proportions must stay uniform (no realistic proportions creeping in), no text on bases, smooth render — not cel-shaded, matte vinyl material throughout
```

**关键调节项:** `{character_name}`、`{character_description_simplified}` (只保留关键服装与发型)、`{face_markers}` (如圆框眼镜、左颊伤疤、绿眼睛)、`{color_palette}` (2-3 个主色的 hex 值)、`{bg_gradient}` (#F5F0EB 到 #FFFFFF 暖色、#E0E8F0 到 #FFFFFF 冷色)、`{num_poses}` (3-5)、`{pose_N_description}` (如盘腿看书、双手挥手、手持咖啡杯)、`{base_color}` (白、黑、匹配角色主色)

**推荐模型:** GPT Image 2.5 (`quality: medium`) — 光滑 3D 乙烯表面在 medium 下渲染良好;`high` 用于可营销的特写

### Nano Banana 版本:

```
A row of {num_poses} chibi-style 3D vinyl collectible figurines of {character_name}, each in a different pose. Large head (1:2 head-to-body ratio), rounded limbs, smooth matte vinyl surface with visible seam lines and subtle glossy highlights on the forehead. Face retains {face_markers} simplified into chibi proportions with large round eyes. Outfit: {outfit_simplified} in {color_palette}. Poses left to right: {pose_1_description}, {pose_2_description}, {pose_3_description}. Each figurine on a small circular {base_color} matte base. Soft gradient background ({bg_gradient}), studio product lighting with rim light from behind and soft fill from front, subtle ground shadow. Format: 16:9.
```

---

## 日系角色卡

用于完整角色参考卡:头像、全身、关键道具、调色板 — 在白色背景上以专业概念图布局组织。

<!-- Source concept: anime/game character reference sheet with stats, items, and palette swatches -->

```
Scene: white background, organized reference card layout divided into clear sections with thin #CCCCCC separator lines
Subject: {character_name} — {character_description} — anime-style rendering with clean line art and flat cel shading
Important Details:
  Left section (40% width): full-body standing pose, front-facing, arms slightly away from body to show full outfit, feet visible, confident neutral expression
  Upper-right section: portrait bust — head and shoulders, three-quarter angle, detailed face rendering showing {face_details}
  Mid-right section: {num_items} key items arranged in a row — {item_1}, {item_2}, {item_3} — each drawn at consistent scale with thin outline, labeled in small text below
  Lower-right section: color palette — {num_swatches} rectangular swatches in a horizontal strip showing the character's key colors ({swatch_colors}), hex code below each swatch
  Bottom strip: brief stat block or bio text in clean sans-serif — "Name: {character_name} | Class: {class} | Height: {height} | Affiliation: {affiliation}"
  Consistent line weight and shading style across all sections
Use Case: game character documentation, light novel illustration guide, animation production reference
Constraints: unified anime art style across all sections — portrait and full body must be the same character with identical design, items must match what the character wears/carries in the full body view, no decorative borders or ornamental frames, text must be legible at screen resolution
```

**关键调节项:** `{character_name}`、`{character_description}` (详细:发色/发型、瞳色、服装层次、配饰)、`{face_details}` (独特面部特征 — 如异色瞳、面部纹身、锋利下颌线)、`{item_1}`/`{item_2}`/`{item_3}` (标志性武器、配饰、道具)、`{swatch_colors}` (如午夜蓝 #191970、樱桃红 #C41E3A、银 #C0C0C0、暖肤色 #E8B89D)、`{num_swatches}` (4-6)、`{class}` / `{height}` / `{affiliation}` (属性栏字段)

**推荐模型:** GPT Image 2.5 (`quality: high`) — 含 hex 码、标签与属性栏的文字密集布局需要精确渲染

### Nano Banana 版本:

```
An anime-style character reference card for {character_name} on a white background. Left side: full-body standing pose, front-facing, clean cel-shaded anime rendering — {character_description}. Upper right: portrait bust at three-quarter angle showing {face_details}. Mid-right: key items laid out in a row — {item_1}, {item_2}, {item_3} — each drawn consistently and labeled. Lower right: horizontal color palette strip with {num_swatches} rectangular swatches ({swatch_colors}). Clean layout with thin gray separator lines between sections. Professional concept art quality, consistent line weight throughout. Format: 3:4.
```

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
