# UI 效果图与社交媒体模式

可复用的提示词模板:社交媒体广告、应用商店素材、仪表盘效果图和视觉分析板。每个模式用 `{variables}` 定制。默认模型:GPT Image 2.5 (5 段式格式),除非另有说明。

---

## Instagram Story 广告 (9:16)

用于面向 Instagram Story 的竖版产品或品牌广告 — 主视觉产品、粗体标题与底部的上滑 CTA 区域。

<!-- Source concept: Instagram Story ad with glassmorphism elements and gradient background -->

```
Scene: vertical 9:16 canvas, smooth gradient background from {gradient_top} to {gradient_bottom}, soft ambient glow behind the product
Subject: {product_name} — {product_description} — centered in the upper two-thirds of the frame, angled slightly for dimension
Important Details: two glassmorphism panels (frosted translucent white, 20% opacity, subtle border highlight at #FFFFFF30) flanking the product — one floating left, one floating right, slightly rotated, adding depth layers. Bold headline "{headline_text}" in {headline_font} at the top third, white or light-colored text with subtle drop shadow for readability. Small subtext "{subtext}" below the headline in lighter weight. Bottom 15% of canvas left as swipe-up CTA zone — thin upward-pointing chevron icon and "{cta_text}" in small caps, both in white. Product casts a soft colored shadow matching the gradient onto the background. Scattered {accent_elements} (glass spheres, soft bokeh circles, translucent geometric shapes) at 10-15% opacity for texture.
Use Case: Instagram Story ad, vertical social media placement, mobile-first brand campaign
Constraints: text must be legible on mobile screens (minimum visual weight), no text in the bottom 5% (system UI overlap zone), product must be the clear focal point, no more than 3 accent elements, glassmorphism panels must not obscure the product
```

**关键调节项:** `{product_name}`、`{product_description}` (形状、材质、颜色)、`{gradient_top}` / `{gradient_bottom}` (如 #6C3CE1 紫到 #1A1A2E 深藏蓝、#FF6B6B 珊瑚到 #FFE66D 暖黄)、`{headline_text}`、`{headline_font}` (粗压缩无衬线、圆润几何体)、`{subtext}`、`{cta_text}` (如 "Swipe Up"、"Shop Now"、"Learn More")、`{accent_elements}` (半透明球体、柔和光斑、悬浮几何碎片)

**推荐模型:** GPT Image 2.5 (`quality: high`) — 标题文字可读性与毛玻璃透明效果需要精确渲染

---

## 社交媒体信息流帖子 (1:1)

用于 Instagram 或 Facebook 的方形帖子 — 金句卡片、功能公告或产品亮点,居中布局。

<!-- Source concept: square social media post with brand color palette and centered typography -->

```
Scene: square 1:1 canvas, solid or subtle textured background in {bg_color}, clean centered composition
Subject: {post_type} — {content_description}
Important Details:
  Background: {bg_treatment} (solid color, subtle noise texture at 3% opacity, or soft radial gradient from {bg_color} center to slightly darker edges)
  Primary text: "{primary_text}" in {primary_font}, {text_color}, centered horizontally, positioned in the upper half with comfortable margins (at least 10% padding from edges)
  Supporting element: {supporting_element} — positioned below the primary text, providing visual weight and context
  Brand strip: thin horizontal line or subtle divider in {accent_color} separating the primary content from a bottom section containing "{brand_name}" in small caps and {brand_mark} (logo mark or wordmark)
  Overall palette restricted to {palette} — no colors outside this set
  Text sized for legibility at phone-screen scale — primary text large enough to read in a thumbnail feed scroll
Use Case: Instagram feed post, Facebook post, LinkedIn visual, social media content calendar
Constraints: all text must remain legible at 320px display width, no decorative elements that compete with the message, centered balanced layout, no more than two type sizes (headline + body or headline + brand), background must not reduce text contrast below WCAG AA
```

**关键调节项:** `{post_type}` (金句卡片、产品功能、公告、数据亮点)、`{content_description}`、`{primary_text}`、`{primary_font}` (几何无衬线、现代衬线、手写点缀)、`{text_color}` (深底用 #FFFFFF、浅底用 #1A1A1A)、`{bg_color}` / `{bg_treatment}`、`{accent_color}`、`{brand_name}`、`{brand_mark}`、`{palette}` (如藏蓝 #1B2A4A、金 #C9A84C、白 #FFFFFF)、`{supporting_element}` (产品照片、图标插画、大号数据数字)

**推荐模型:** GPT Image 2.5 (`quality: high`) — 文字密集型版式;小尺寸下的可读性至关重要

---

## 应用商店截图

用于制作精美的 App Store 或 Google Play 上架截图 — 设备外框内嵌应用 UI、功能标题与干净的渐变背景。

<!-- Source concept: App Store marketing screenshot with iPhone device frame and feature callout -->

```
Scene: vertical canvas, smooth gradient background from {gradient_top} to {gradient_bottom}, centered composition
Subject: {device_type} device frame displaying {app_name} UI — {screen_description}
Important Details:
  Device: realistic {device_type} bezel (space black / silver / natural titanium) with accurate corner radius and button placement, screen showing {screen_content} with proper iOS/Android status bar at top
  Headline: "{feature_headline}" in bold {headline_font}, positioned {headline_position} the device frame, {headline_color} text, 2-3 words maximum per line for impact
  Optional subheadline: "{subheadline}" in lighter weight below the headline, 60% opacity of headline color
  Device shadow: soft diffused shadow below the device, matching the gradient color (not pure black)
  Screen UI: {ui_description} — realistic interface elements with proper spacing, {ui_style} design system, readable text within the screen (even if small)
  Device centered vertically with equal breathing room above and below
Use Case: App Store product page, Google Play listing, app marketing material
Constraints: device bezel must look physically accurate (not a flat rectangle), screen content must be realistic and internally consistent UI (not random shapes), headline text must not overlap the device, gradient background only — no patterns or photos behind the device, one device only
```

**Key levers:** `{device_type}` (iPhone 16 Pro, Pixel 9, Galaxy S25), `{app_name}`, `{screen_description}` (brief: what the screen shows), `{screen_content}` / `{ui_description}` (detailed: specific UI elements visible), `{ui_style}` (iOS native, Material 3, custom dark theme), `{feature_headline}`, `{headline_font}` (SF Pro Display, condensed geometric), `{headline_position}` (above, below), `{headline_color}`, `{subheadline}`, `{gradient_top}` / `{gradient_bottom}` (e.g. #1A1A2E to #0D0D1A for dark, #F0F4FF to #FFFFFF for light)

**Recommended model:** GPT Image 2.5 (`quality: high`) — device bezel precision, small UI text, and headline legibility all demand high quality

---

## Dashboard Design Mockup

Use for realistic analytics dashboard mockups — dark or light theme with data visualizations, KPI cards, and sidebar navigation.

<!-- Source concept: analytics dashboard UI mockup with charts, cards, and navigation -->

```
Scene: full-screen desktop UI mockup, {theme_mode} theme, clean {design_system} design system
Subject: {dashboard_title} — analytics dashboard showing {data_domain} metrics
Important Details:
  Sidebar (left, 220px visual width): dark ({sidebar_bg}) vertical navigation with icon + label pairs for {nav_items}, active item highlighted with {accent_color} left border and slightly lighter background, collapsed user avatar and app logo at top
  Top bar: breadcrumb or page title "{page_title}" in medium weight, date range selector showing "{date_range}", notification bell icon with dot indicator
  KPI row (top of main area): {num_kpis} metric cards in a horizontal row — each card shows metric name in small caps, large number value, and a small trend indicator (green upward arrow or red downward arrow with percentage), card background {card_bg}
  Chart area (main): {chart_layout}
    Chart 1: {chart_1_type} showing {chart_1_data} — using {chart_1_colors}
    Chart 2: {chart_2_type} showing {chart_2_data} — using {chart_2_colors}
  Secondary section: {secondary_widget} (data table with alternating row colors, recent activity feed, or geographic heat map)
  Proper visual hierarchy — KPI numbers largest, chart labels smaller, navigation text smallest
  Realistic data values throughout — no placeholder "lorem ipsum" or obviously fake numbers
Use Case: SaaS product marketing, investor deck, UI/UX portfolio, feature specification
Constraints: data must look plausible (proper scales, reasonable percentages, formatted numbers), charts must use proper axes and labels, no overlapping UI elements, sidebar must not bleed into main content, {theme_mode} theme applied consistently — no mixing dark sidebar with light charts unless intentional
```

**Key levers:** `{theme_mode}` (dark / light), `{design_system}` (minimal flat, glassmorphism cards, shadowed Material), `{dashboard_title}`, `{data_domain}` (SaaS revenue, e-commerce orders, marketing campaign, IoT sensor monitoring), `{sidebar_bg}` (#0F1117 dark, #FFFFFF light), `{accent_color}` (#6366F1 indigo, #10B981 emerald, #F59E0B amber), `{nav_items}` (Dashboard, Analytics, Users, Settings, Reports), `{num_kpis}` (3-5), `{chart_1_type}` / `{chart_2_type}` (line chart, grouped bar chart, donut chart, area chart), `{chart_1_colors}` / `{chart_2_colors}` (hex values), `{card_bg}` (#1E1E2E dark card, #FFFFFF light card), `{secondary_widget}`

**Recommended model:** GPT Image 2.5 (`quality: high`) — dense text (labels, numbers, navigation), precise chart rendering, and small UI elements require high fidelity

### Nano Banana version:

```
A {theme_mode}-themed analytics dashboard UI mockup for {dashboard_title}. Left sidebar ({sidebar_bg}) with navigation icons for {nav_items}, active item highlighted in {accent_color}. Top area: {num_kpis} KPI metric cards showing large numbers with trend arrows. Main area: {chart_1_type} visualizing {chart_1_data} in {chart_1_colors}, alongside a {chart_2_type} showing {chart_2_data}. Below: {secondary_widget}. Clean {design_system} design system, realistic plausible data values throughout, proper visual hierarchy. Desktop fullscreen layout. Format: 16:9.
```

---

## Personal Color Analysis Board

Use to create a visual color analysis graphic from a portrait — seasonal palette classification, clothing color comparisons, and accessory recommendations in an organized layout.

<!-- Source concept: personal color analysis / seasonal color palette board with side-by-side comparisons -->

```
Scene: white background, organized multi-section layout with thin #E0E0E0 divider lines, clean editorial formatting
Subject: personal color analysis board for {subject_description}
Important Details:
  Section 1 — Portrait & Season (top, full width): {subject_description} portrait photo (head and shoulders, natural lighting, neutral expression) on the left. To the right: season classification "{season_type}" in medium bold text, with a 4x3 grid of small color swatches showing the {num_palette} best colors for this season type ({palette_colors}), each swatch labeled with its name in tiny text below
  Section 2 — Clothing Comparison (middle): two side-by-side panels. Left panel "{good_label}": the subject wearing a top in {flattering_color} — skin looks healthy, face appears lifted and bright. Right panel "{bad_label}": the same subject wearing a top in {unflattering_color} — skin appears washed out or sallow. Small caption under each explaining the effect in 5-8 words
  Section 3 — Recommendations (bottom): horizontal strip with {num_recs} small squares — each showing a recommended item ({rec_items}) in one of the palette colors, with a one-word label below (e.g. "Scarf", "Blazer", "Lipstick", "Frames")
  Visual-first design — images and swatches dominate, text is short labels only
  Clean editorial feel, no decorative flourishes
Use Case: personal styling consultation, color analysis service deliverable, fashion content
Constraints: same person in all panels showing the subject, swatches must be solid flat color (no gradients), labels are short (1-3 words max), no paragraphs of body text, layout must feel organized and scannable, no overlapping sections
```

**Key levers:** `{subject_description}` (age, skin tone, hair color, eye color — needed for accurate seasonal analysis), `{season_type}` (Warm Spring, Cool Summer, Warm Autumn, Cool Winter — or sub-seasons like Soft Autumn, Bright Winter), `{palette_colors}` (12 hex values matching the season, e.g. Warm Autumn: rust #B7410E, olive #708238, mustard #E1AD01, burgundy #722F37...), `{num_palette}` (12), `{flattering_color}` / `{unflattering_color}` (specific colors with hex), `{good_label}` / `{bad_label}` (e.g. "Warm Coral" / "Cool Pink"), `{num_recs}` (4-6), `{rec_items}` (scarf in olive, blazer in navy, lipstick in warm rose, eyeglass frames in tortoise)

**Recommended model:** GPT Image 2.5 (`quality: high`) — color accuracy of palette swatches is critical, plus small text labels throughout

### Nano Banana version:

```
A personal color analysis board on a white background for {subject_description}. Top section: portrait of the subject on the left, seasonal classification "{season_type}" on the right with a grid of {num_palette} color palette swatches ({palette_colors}). Middle section: side-by-side comparison — left shows the subject in a {flattering_color} top looking healthy and bright ("{good_label}"), right shows the same subject in {unflattering_color} looking washed out ("{bad_label}"). Bottom strip: {num_recs} recommended items ({rec_items}) each in a palette color with one-word labels. Clean editorial layout, visual-first with minimal text, thin gray dividers between sections. Format: 3:4.
```

---

*Author: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · License: CC BY 4.0 — attribution required · Source: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
