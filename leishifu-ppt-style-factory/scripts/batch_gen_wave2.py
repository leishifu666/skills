#!/usr/bin/env python3
"""批量生成第二波四个风格的所有配图（riot-fest / flavor-magazine / structura / verde-organic）"""
import subprocess, sys, time, os

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generate_images.py")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 风格后缀
SUFFIX_D = "Memphis design, Pop art style, bold saturated colors (hot pink, cyan, yellow, purple, green), playful geometric patterns, energetic festival poster aesthetic, maximalist and expressive."
SUFFIX_E = "Warm food photography, dark moody background, rich warm tones, editorial magazine quality, appetizing and inviting, Bon Appetit / Kinfolk aesthetic, shallow depth of field."
SUFFIX_F = "Architectural photography, minimalist composition, concrete and glass, dramatic shadows, desaturated tones, Swiss design influence, Tadao Ando / Peter Zumthor aesthetic."
SUFFIX_G = "Organic natural photography, warm earth tones, soft golden hour lighting, botanical elements, sustainable lifestyle, calm and grounded, Kinfolk / Aesop aesthetic."

COMMON = "主体居中但保留边距，画面密度中等。只保留核心图形/画面本身，不要生成页眉、页脚、标题、页码、角标、署名、装饰边框、水印。"
MULTI = "这是一组图片中的一张，请保持与同组图片相同的画面比例、元素大小、边距、色调和密度。" + COMMON

TASKS = [
    # === D · Riot Fest (8 images) ===
    ("riot-fest/p1-cover.png",
     "Music festival crowd scene at night, massive stage with colorful lights (pink, cyan, yellow), energetic atmosphere, hands raised, confetti. " + SUFFIX_D + " " + COMMON,
     "1920x1080"),
    ("riot-fest/p2-lineup.png",
     "Live music performance, singer on stage with dramatic colored lighting, crowd silhouettes, dynamic energy, concert photography. " + SUFFIX_D + " " + COMMON,
     "1152x1080"),
    ("riot-fest/p4-schedule.png",
     "Festival crowd cheering with colored smoke bombs, daytime outdoor music festival, vibrant energy, aerial perspective. " + SUFFIX_D + " " + COMMON,
     "960x1080"),
    ("riot-fest/p5-experience.png",
     "Immersive art installation at music festival, large scale colorful geometric sculptures, people interacting, night time with neon lights. " + SUFFIX_D + " " + COMMON,
     "1920x1080"),
    ("riot-fest/p8-contact.png",
     "Music festival closing scene, fireworks over main stage, crowd celebration, night sky lit with colorful lights, epic wide angle. " + SUFFIX_D + " " + COMMON,
     "1920x1080"),

    # === E · Flavor Magazine (10 images) ===
    ("flavor-magazine/p1-cover.png",
     "Elegant food still life on dark wooden table, artisan bread, olive oil, fresh herbs, warm side lighting, steam rising, editorial food photography. " + SUFFIX_E + " " + COMMON,
     "1920x1080"),
    ("flavor-magazine/p2-feature.png",
     "Freshly baked sourdough bread, crispy golden crust with open crumb visible, rustic wooden board, flour dusted, warm morning light. " + SUFFIX_E + " " + COMMON,
     "1056x1080"),
    ("flavor-magazine/p3-recipe.png",
     "Slow roasted cherry tomatoes in baking dish, glistening with olive oil, fresh herbs scattered, rustic kitchen setting, overhead shot. " + SUFFIX_E + " " + COMMON,
     "1056x1080"),
    ("flavor-magazine/p4-gallery1.png",
     "Crème brûlée dessert with caramelized sugar top, elegant plating on dark ceramic plate, soft warm lighting, macro detail. " + SUFFIX_E + " " + MULTI,
     "640x1080"),
    ("flavor-magazine/p4-gallery2.png",
     "Fresh oysters on ice platter with lemon wedges, sea salt crystals, dark slate surface, dramatic top-down lighting. " + SUFFIX_E + " " + MULTI,
     "640x1080"),
    ("flavor-magazine/p4-gallery3.png",
     "Artisan sourdough loaves stacked on wooden shelf, bakery setting, golden crust detail, warm ambient light. " + SUFFIX_E + " " + MULTI,
     "640x1080"),
    ("flavor-magazine/p5-chef.png",
     "Portrait of Asian chef in dark kitchen, white chef coat, focused expression, preparing food, warm dramatic side lighting, editorial portrait. " + SUFFIX_E + " " + COMMON,
     "960x1080"),
    ("flavor-magazine/p6-wine.png",
     "Wine glass and bottle on dark table, vineyard visible through window in background, warm evening light, rich burgundy tones, elegant still life. " + SUFFIX_E + " " + COMMON,
     "1920x1080"),
    ("flavor-magazine/p8-closing.png",
     "Intimate restaurant interior, candlelit tables, warm ambiance, dark wood and brass details, soft bokeh lights, inviting atmosphere. " + SUFFIX_E + " " + COMMON,
     "1920x1080"),

    # === F · Structura (10 images) ===
    ("structura/p1-cover.png",
     "Minimalist concrete building exterior, dramatic shadows, clear sky, brutalist architecture, strong geometric lines, monumental scale. " + SUFFIX_F + " " + COMMON,
     "1920x1080"),
    ("structura/p2-philosophy.png",
     "Interior of concrete building with dramatic light shaft, beam of sunlight cutting through darkness, minimal furniture, zen-like space. " + SUFFIX_F + " " + COMMON,
     "1152x1080"),
    ("structura/p3-main.png",
     "Modern pavilion in landscape, glass and concrete, reflecting pool, clean lines, evening golden hour, architectural masterpiece. " + SUFFIX_F + " " + COMMON,
     "1152x1080"),
    ("structura/p3-side1.png",
     "Residential architecture, modern house with large glass windows, wooden elements, natural setting, mountain backdrop. " + SUFFIX_F + " " + MULTI,
     "768x540"),
    ("structura/p3-side2.png",
     "Museum interior, white walls with subtle lighting, long corridor perspective, minimalist exhibition space. " + SUFFIX_F + " " + MULTI,
     "768x540"),
    ("structura/p6-project1.png",
     "Glass house in forest setting, full height windows, minimalist interior visible, morning mist, peaceful retreat. " + SUFFIX_F + " " + MULTI,
     "640x480"),
    ("structura/p6-project2.png",
     "Contemporary art gallery exterior, dark concrete facade with singular dramatic entrance, night lighting, architectural drama. " + SUFFIX_F + " " + MULTI,
     "640x480"),
    ("structura/p6-project3.png",
     "Twisted office tower, modern skyscraper with rotating floor plates, glass curtain wall, dramatic sky background, urban context. " + SUFFIX_F + " " + MULTI,
     "640x480"),
    ("structura/p7-team.png",
     "Architecture studio workspace, large tables with models and drawings, industrial space with high ceilings, team working, natural light. " + SUFFIX_F + " " + COMMON,
     "1056x1080"),
    ("structura/p8-contact.png",
     "Architectural detail close-up, concrete texture meeting glass edge, abstract geometric composition, light and shadow play. " + SUFFIX_F + " " + COMMON,
     "960x1080"),

    # === G · Verde Organic (10 images) ===
    ("verde-organic/p1-cover.png",
     "Organic farm landscape at golden hour, rolling green hills, rows of crops, warm sunlight, peaceful and abundant, aerial view. " + SUFFIX_G + " " + COMMON,
     "1920x1080"),
    ("verde-organic/p2-story.png",
     "Farmer hands holding fresh organic vegetables in garden, close-up, rich soil visible, morning dew, warm natural light. " + SUFFIX_G + " " + COMMON,
     "1056x1080"),
    ("verde-organic/p3-product1.png",
     "Artisan tea ceremony setup, dried tea leaves in ceramic bowl, bamboo utensils, wooden table, soft natural light, meditative atmosphere. " + SUFFIX_G + " " + MULTI,
     "960x1080"),
    ("verde-organic/p3-product2.png",
     "Honey jar with honeycomb and wooden dipper, wildflowers in background, rustic wooden surface, warm golden tones, natural still life. " + SUFFIX_G + " " + MULTI,
     "960x1080"),
    ("verde-organic/p4-value1.png",
     "Close-up of organic seedlings growing in rich dark soil, morning dew drops, macro photography, green and earth tones. " + SUFFIX_G + " " + MULTI,
     "640x480"),
    ("verde-organic/p4-value2.png",
     "Eco-friendly packaging materials, kraft paper boxes, dried botanicals, cotton bags, flat lay on linen surface, sustainable design. " + SUFFIX_G + " " + MULTI,
     "640x480"),
    ("verde-organic/p4-value3.png",
     "Rural farming community, farmers in field together, cooperative harvest scene, warm afternoon light, authentic and joyful. " + SUFFIX_G + " " + MULTI,
     "640x480"),
    ("verde-organic/p7-products.png",
     "Organic product collection flat lay, tea tins, honey jars, grain bags, ceramic bowls, botanical decorations, warm neutral background. " + SUFFIX_G + " " + COMMON,
     "1056x1080"),
    ("verde-organic/p8-closing.png",
     "Peaceful terraced rice fields at sunset, distant mountains, golden light, birds flying, serene and hopeful landscape. " + SUFFIX_G + " " + COMMON,
     "1920x1080"),
]

def run(output, prompt, size, attempt=1):
    full_path = os.path.join(BASE, "images", output)
    if os.path.exists(full_path) and os.path.getsize(full_path) > 100000:
        print(f"  SKIP {output} (already exists, {os.path.getsize(full_path)//1024}KB)")
        return True
    cmd = [sys.executable, SCRIPT, "--prompt", prompt, "--output", f"images/{output}", "--size", size]
    try:
        r = subprocess.run(cmd, cwd=BASE, timeout=360, capture_output=True, text=True)
        if r.returncode == 0:
            print(f"  OK   {output}")
            return True
        else:
            err = r.stderr[-200:] if r.stderr else "unknown"
            print(f"  FAIL {output} (attempt {attempt}): {err.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT {output} (attempt {attempt})")
        return False

def main():
    total = len(TASKS)
    done = 0
    failed = []
    print(f"=== Batch Wave 2: generating {total} images for 4 styles ===\n")
    for i, (out, prompt, size) in enumerate(TASKS):
        print(f"[{i+1}/{total}] {out}")
        ok = False
        for attempt in range(1, 4):
            ok = run(out, prompt, size, attempt)
            if ok:
                break
            wait = 15 * attempt
            print(f"  Retrying in {wait}s...")
            time.sleep(wait)
        if ok:
            done += 1
        else:
            failed.append(out)
        # Cooldown between tasks
        if i < total - 1:
            time.sleep(5)

    print(f"\n=== Done: {done}/{total} succeeded ===")
    if failed:
        print(f"Failed ({len(failed)}):")
        for f in failed:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
