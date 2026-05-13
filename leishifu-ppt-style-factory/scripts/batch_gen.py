#!/usr/bin/env python3
"""批量生成三个风格的所有配图，自带重试和间隔"""
import subprocess, sys, time, os

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generate_images.py")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 风格后缀
SUFFIX_A = "Editorial fashion photography, high contrast, bold saturated blue and red color palette, dramatic lighting, magazine cover quality."
SUFFIX_B = "Street dance culture, urban energy, neon green accents on black, graffiti style, dynamic motion, raw and energetic."
SUFFIX_C = "Dark fine art portrait photography, moody cinematic lighting, deep shadows, warm undertones, film grain, intimate and haunting."

COMMON = "主体居中但保留边距，画面密度中等。只保留核心图形/画面本身，不要生成页眉、页脚、标题、页码、角标、署名、装饰边框、水印。"

TASKS = [
    # === A · New Reign ===
    ("new-reign/p1-cover.png", "Fashion model portrait on vivid blue background, confident pose, editorial lighting, bold fashion outfit. " + SUFFIX_A + " " + COMMON, "1024x1024"),
    ("new-reign/p2-concept.png", "Creative fashion concept photo, model with dramatic pose, artistic composition, high fashion styling, studio shot. " + SUFFIX_A + " " + COMMON, "1024x1024"),
    ("new-reign/p3-tracklist.png", "Artistic portrait with dramatic side lighting, dark moody background, music album aesthetic, singer in spotlight. " + SUFFIX_A + " " + COMMON, "1024x1024"),
    ("new-reign/p4-single.png", "Dynamic fashion photo, model in motion, flowing fabric, vivid blue and red lighting, energetic and powerful. " + SUFFIX_A + " " + COMMON, "1024x1024"),
    ("new-reign/p5-artist.png", "Striking close-up portrait, bold makeup, confident gaze, red accent lighting, editorial beauty shot. " + SUFFIX_A + " " + COMMON, "1024x1024"),
    ("new-reign/p6-grid1.png", "Fashion editorial full body shot, model in avant-garde outfit, geometric background, high contrast. " + SUFFIX_A + " " + COMMON, "1024x1024"),
    ("new-reign/p6-grid2.png", "Fashion editorial shot, model with dramatic silhouette, artistic pose, blue toned lighting. " + SUFFIX_A + " " + COMMON, "1024x1024"),
    ("new-reign/p7-tour.png", "Concert stage with dramatic blue and red lighting, wide angle, crowd silhouettes, fog and spotlights. " + SUFFIX_A + " " + COMMON, "1024x1024"),
    # === B · Street Dance ===
    ("street-dance/p1-cover.png", "Street dancer mid-move in urban setting, neon green lighting, dynamic freeze frame, hip hop style. " + SUFFIX_B + " " + COMMON, "1024x1024"),
    ("street-dance/p2-about.png", "Group of street dancers posing together, urban backdrop, confident team photo, streetwear fashion. " + SUFFIX_B + " " + COMMON, "1024x1024"),
    ("street-dance/p3-classes.png", "Dance class in session, instructor demonstrating moves, mirror wall reflection, studio lights. " + SUFFIX_B + " " + COMMON, "1024x1024"),
    ("street-dance/p4-instructor.png", "Solo breaker doing a power move, spinning on floor, dramatic spotlight, dust particles in air. " + SUFFIX_B + " " + COMMON, "1024x1024"),
    ("street-dance/p6-gallery1.png", "Popping dancer with sharp isolation moves, colorful neon backdrop, motion blur effect. " + SUFFIX_B + " " + COMMON, "1024x1024"),
    ("street-dance/p6-gallery2.png", "Locking dancer in funky pose, retro inspired, urban rooftop setting, golden hour lighting. " + SUFFIX_B + " " + COMMON, "1024x1024"),
    ("street-dance/p6-gallery3.png", "Hip hop choreography group shot in formation, synchronized movement, studio setting with mirrors. " + SUFFIX_B + " " + COMMON, "1024x1024"),
    ("street-dance/p6-gallery4.png", "Street dancer freestyle in abandoned warehouse, raw concrete walls, dramatic side light. " + SUFFIX_B + " " + COMMON, "1024x1024"),
    ("street-dance/p7-pricing.png", "Dance battle scene, two dancers facing off, crowd circle around them, intense energy. " + SUFFIX_B + " " + COMMON, "1024x1024"),
    # === C · Dark Photographer ===
    ("dark-photographer/p1-cover.png", "Atmospheric dark portrait, face emerging from deep shadows, dramatic chiaroscuro lighting, fine art quality. " + SUFFIX_C + " " + COMMON, "1024x1024"),
    ("dark-photographer/p2-about.png", "Photographer in dark studio, holding camera, surrounded by equipment, atmospheric lighting, self portrait. " + SUFFIX_C + " " + COMMON, "1024x1024"),
    ("dark-photographer/p3-gallery1.png", "Fine art portrait, person with closed eyes, serene expression, dark background, painterly lighting. " + SUFFIX_C + " " + COMMON, "1024x1024"),
    ("dark-photographer/p3-gallery2.png", "Artistic portrait with dramatic hair movement, wind effect, dark moody studio, cinematic quality. " + SUFFIX_C + " " + COMMON, "1024x1024"),
    ("dark-photographer/p4-main.png", "Powerful full body portrait, figure in dark clothing against dark background, single beam of light. " + SUFFIX_C + " " + COMMON, "1024x1024"),
    ("dark-photographer/p4-side1.png", "Intimate close-up portrait, hands framing face, emotional expression, warm toned shadows. " + SUFFIX_C + " " + COMMON, "1024x1024"),
    ("dark-photographer/p4-side2.png", "Profile portrait silhouette, rim lighting only, elegant neck line, minimalist dark art. " + SUFFIX_C + " " + COMMON, "1024x1024"),
    ("dark-photographer/p6-faq.png", "Contemplative portrait with subject looking away, window light, dust particles, melancholic mood. " + SUFFIX_C + " " + COMMON, "1024x1024"),
    ("dark-photographer/p7-testimonial.png", "Double exposure portrait, overlapping faces, artistic experimental photography, dark ethereal. " + SUFFIX_C + " " + COMMON, "1024x1024"),
    ("dark-photographer/p8-contact.png", "Dark studio portrait, subject seated, relaxed pose, single warm light source, intimate atmosphere. " + SUFFIX_C + " " + COMMON, "1024x1024"),
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
    print(f"=== Batch generating {total} images ===\n")
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
        # cooldown between requests
        if i < total - 1:
            time.sleep(5)

    print(f"\n=== Done: {done}/{total} succeeded ===")
    if failed:
        print(f"Failed ({len(failed)}):")
        for f in failed:
            print(f"  - {f}")
    sys.exit(0 if not failed else 1)

if __name__ == "__main__":
    main()
