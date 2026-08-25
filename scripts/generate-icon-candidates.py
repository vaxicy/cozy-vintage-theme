#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 4 cozy/vintage icon candidates for Cozy Vintage Theme."""

from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "store-assets" / "icon-candidates"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Theme palette (from cozy-vintage light/dark themes)
CREAM = (253, 244, 210)
WARM_BROWN = (74, 63, 54)
SOFT_BLUE = (124, 159, 190)
MUTED_ROSE = (148, 109, 109)
WARM_GOLD = (181, 133, 58)
SAGE = (139, 158, 138)
LIGHT_CREAM = (246, 236, 207)
DARK_BROWN = (58, 47, 41)

SIZE = 128
RADIUS = 28


def rounded_square(size, color, radius):
    """Create a rounded-square background."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=color)
    return img


def center_crop_to(img, target=128):
    """Resize and center-crop to target size."""
    if img.size == (target, target):
        return img
    # Scale to fit, preserving aspect
    w, h = img.size
    scale = max(target / w, target / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    # Center crop
    left = (new_w - target) // 2
    top = (new_h - target) // 2
    return img.crop((left, top, left + target, top + target))


def save_pair(name, img):
    """Save raw (original render) and processed (128x128) versions."""
    raw_path = OUT_DIR / f"{name}-raw.png"
    proc_path = OUT_DIR / f"{name}.png"
    img.save(raw_path, "PNG")
    center_crop_to(img, SIZE).save(proc_path, "PNG")
    print(f"Saved: {raw_path.name} + {proc_path.name}")


# ---------- Candidate 1: Warm Coffee Cup ----------
def draw_coffee_cup():
    bg = rounded_square(256, CREAM, RADIUS * 2)
    d = ImageDraw.Draw(bg)

    # Cup body
    cup_color = (120, 82, 67)
    cup_top = (95, 115)
    cup_bottom = (95, 210)
    cup_w = 110
    cup_h = 95
    d.rounded_rectangle(
        [cup_top[0], cup_top[1], cup_top[0] + cup_w, cup_top[1] + cup_h],
        radius=14,
        fill=cup_color,
    )
    # Cup rim
    d.ellipse([cup_top[0] + 5, cup_top[1] - 10, cup_top[0] + cup_w - 5, cup_top[1] + 15],
              fill=(160, 115, 95))
    # Handle
    d.arc([cup_top[0] + cup_w - 5, cup_top[1] + 20, cup_top[0] + cup_w + 32, cup_top[1] + 65],
          start=270, end=90, fill=cup_color, width=10)
    # Steam lines
    steam_color = (160, 145, 120, 180)
    for x_off in (-22, 0, 22):
        d.arc([cup_top[0] + cup_w // 2 + x_off - 8, cup_top[1] - 55,
               cup_top[0] + cup_w // 2 + x_off + 8, cup_top[1] - 5],
              start=0, end=180, fill=steam_color, width=4)
    return bg.resize((SIZE, SIZE), Image.LANCZOS)


# ---------- Candidate 2: Open Book ----------
def draw_open_book():
    bg = rounded_square(256, LIGHT_CREAM, RADIUS * 2)
    d = ImageDraw.Draw(bg)

    cover = WARM_BROWN
    pages = (250, 245, 230)
    shadow = (210, 195, 165)

    cx, cy = 128, 130
    book_w, book_h = 160, 110
    # Cover
    d.rounded_rectangle(
        [cx - book_w // 2, cy - book_h // 2, cx + book_w // 2, cy + book_h // 2],
        radius=12, fill=cover
    )
    # Left page
    d.polygon([
        (cx - 6, cy - book_h // 2 + 8),
        (cx - book_w // 2 + 12, cy - book_h // 2 + 8),
        (cx - book_w // 2 + 12, cy + book_h // 2 - 8),
        (cx - 6, cy + book_h // 2 - 8),
    ], fill=pages)
    # Right page
    d.polygon([
        (cx + 6, cy - book_h // 2 + 8),
        (cx + book_w // 2 - 12, cy - book_h // 2 + 8),
        (cx + book_w // 2 - 12, cy + book_h // 2 - 8),
        (cx + 6, cy + book_h // 2 - 8),
    ], fill=pages)
    # Spine shadow
    d.line([(cx, cy - book_h // 2 + 8), (cx, cy + book_h // 2 - 8)], fill=shadow, width=4)
    # Text lines on pages
    line_color = (190, 180, 160)
    for i in range(5):
        y = cy - 25 + i * 12
        d.line([(cx - 55, y), (cx - 14, y)], fill=line_color, width=3)
        d.line([(cx + 14, y), (cx + 55, y)], fill=line_color, width=3)
    # Small heart above book
    heart_color = MUTED_ROSE
    heart_pts = []
    for t in range(100):
        # Parametric heart
        import math
        tt = t / 100.0 * 2 * math.pi
        x = 16 * math.sin(tt) ** 3
        y = -(13 * math.cos(tt) - 5 * math.cos(2 * tt) - 2 * math.cos(3 * tt) - math.cos(4 * tt))
        heart_pts.append((cx + x, cy - 85 + y * 0.55))
    d.polygon(heart_pts, fill=heart_color)
    return bg.resize((SIZE, SIZE), Image.LANCZOS)


# ---------- Candidate 3: Vintage Lamp ----------
def draw_lamp():
    bg = rounded_square(256, (90, 110, 120), RADIUS * 2)
    d = ImageDraw.Draw(bg)

    # Lamp shade
    shade_color = (230, 210, 170)
    shade_pts = [
        (88, 95), (168, 95), (188, 165), (68, 165)
    ]
    d.polygon(shade_pts, fill=shade_color)
    # Glow inside shade
    d.ellipse([108, 110, 148, 140], fill=(255, 235, 190))
    # Lamp base
    d.rounded_rectangle([118, 165, 138, 205], radius=4, fill=(60, 50, 45))
    d.rounded_rectangle([100, 200, 156, 215], radius=6, fill=(80, 70, 60))
    # Cord
    d.line([(68, 130), (45, 130)], fill=(40, 35, 32), width=4)
    # Light rays
    ray_color = (255, 235, 190, 90)
    for angle in (-30, -15, 0, 15, 30):
        import math
        rad = math.radians(angle + 90)
        x1 = 128 + 55 * math.cos(rad)
        y1 = 130 + 55 * math.sin(rad)
        x2 = 128 + 90 * math.cos(rad)
        y2 = 130 + 90 * math.sin(rad)
        d.line([(x1, y1), (x2, y2)], fill=ray_color, width=5)
    return bg.resize((SIZE, SIZE), Image.LANCZOS)


# ---------- Candidate 4: Cozy Window with Plant ----------
def draw_window():
    bg = rounded_square(256, (184, 170, 145), RADIUS * 2)
    d = ImageDraw.Draw(bg)

    # Window frame
    frame_color = (245, 235, 215)
    glass_color = (210, 220, 230)
    win_x, win_y = 58, 48
    win_w, win_h = 140, 140

    # Outer frame
    d.rounded_rectangle(
        [win_x, win_y, win_x + win_w, win_y + win_h],
        radius=10, fill=frame_color
    )
    # Glass panes
    d.rectangle([win_x + 12, win_y + 12, win_x + win_w // 2 - 4, win_y + win_h // 2 - 4], fill=glass_color)
    d.rectangle([win_x + win_w // 2 + 4, win_y + 12, win_x + win_w - 12, win_y + win_h // 2 - 4], fill=glass_color)
    d.rectangle([win_x + 12, win_y + win_h // 2 + 4, win_x + win_w // 2 - 4, win_y + win_h - 12], fill=glass_color)
    d.rectangle([win_x + win_w // 2 + 4, win_y + win_h // 2 + 4, win_x + win_w - 12, win_y + win_h - 12], fill=glass_color)
    # Cross bars
    d.line([(win_x + win_w // 2, win_y + 8), (win_x + win_w // 2, win_y + win_h - 8)], fill=frame_color, width=8)
    d.line([(win_x + 8, win_y + win_h // 2), (win_x + win_w - 8, win_y + win_h // 2)], fill=frame_color, width=8)

    # Plant pot on windowsill
    pot_color = (130, 90, 75)
    d.polygon([(win_x - 10, win_y + win_h - 5), (win_x + 35, win_y + win_h - 5),
               (win_x + 28, win_y + win_h + 35), (win_x - 3, win_y + win_h + 35)], fill=pot_color)
    # Leaves
    leaf_color = (120, 145, 110)
    stem_x = win_x + 12
    stem_base = win_y + win_h - 5
    # Stem
    d.line([(stem_x, stem_base), (stem_x, stem_base - 45)], fill=(80, 110, 70), width=4)
    # Leaves as ellipses
    d.ellipse([stem_x - 18, stem_base - 55, stem_x + 2, stem_base - 35], fill=leaf_color)
    d.ellipse([stem_x + 2, stem_base - 60, stem_x + 22, stem_base - 40], fill=leaf_color)
    d.ellipse([stem_x - 12, stem_base - 75, stem_x + 8, stem_base - 55], fill=leaf_color)

    return bg.resize((SIZE, SIZE), Image.LANCZOS)


def main():
    candidates = [
        ("candidate-1", draw_coffee_cup),
        ("candidate-2", draw_open_book),
        ("candidate-3", draw_lamp),
        ("candidate-4", draw_window),
    ]
    for name, fn in candidates:
        img = fn()
        save_pair(name, img)
    print(f"\nAll candidates saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
