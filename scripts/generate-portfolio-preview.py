#!/usr/bin/env python3
"""Generate a portfolio preview.png for Cozy Vintage Theme."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
THEME_FILE = ROOT / "themes" / "cozy-vintage-dark-color-theme.json"
OUT = ROOT / "store-assets" / "preview.png"

# Load theme colors
with open(THEME_FILE, "r", encoding="utf-8") as f:
    theme = json.load(f)
c = theme["colors"]

def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# Extract key colors
bg = hex_rgb(c.get("editor.background", "#322A26"))
fg = hex_rgb(c.get("editor.foreground", "#E7D3B1"))
sidebar_bg = hex_rgb(c.get("sideBar.background", "#3A312C"))
sidebar_title = hex_rgb(c.get("sideBarTitle.foreground", "#C9B79E"))
activity_bg = hex_rgb(c.get("activityBar.background", "#2B2420"))
title_bg = hex_rgb(c.get("titleBar.activeBackground", "#2B2420"))
title_fg = hex_rgb(c.get("titleBar.activeForeground", "#E7D3B1"))
status_bg = hex_rgb(c.get("statusBar.background", "#2B2420"))
status_fg = hex_rgb(c.get("statusBar.foreground", "#E7D3B1"))
tab_active_bg = hex_rgb(c.get("tab.activeBackground", "#322A26"))
tab_inactive_bg = hex_rgb(c.get("tab.inactiveBackground", "#3A312C"))
tab_active_fg = hex_rgb(c.get("tab.activeForeground", "#E7D3B1"))
tab_inactive_fg = hex_rgb(c.get("tab.inactiveForeground", "#B49C84"))
border = hex_rgb(c.get("sideBarSectionHeader.border", "#52463F"))
accent = hex_rgb(c.get("activityBar.activeBorder", "#B0CDE6"))

# Syntax colors
comment = hex_rgb("#8A7A6B")
string = hex_rgb("#FDF4D2")
keyword = hex_rgb("#A290B7")
func = hex_rgb("#B0CDE6")
type_c = hex_rgb("#9488B0")
number = hex_rgb("#946D6D")
var_c = hex_rgb("#B49C84")

W, H = 1280, 800
img = Image.new("RGB", (W, H), bg)
d = ImageDraw.Draw(img)

# Title bar
d.rectangle([0, 0, W, 34], fill=title_bg)
# Window controls
for i, col in enumerate(["#FF5F56", "#FFBD2E", "#27C93F"]):
    cx, cy = 20 + i * 20, 17
    d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=col)
# Title text
try:
    title_font = ImageFont.truetype("segoeui.ttf", 13)
except Exception:
    title_font = ImageFont.load_default()
d.text((W//2, 17), "Cozy Vintage Theme - Visual Studio Code", fill=title_fg, font=title_font, anchor="mm")

# Activity bar left
activity_w = 48
d.rectangle([0, 34, activity_w, H-24], fill=activity_bg)
# Active indicator on first icon
d.rectangle([0, 50, 3, 84], fill=accent)
# Activity icons (simplified)
icon_y = [58, 102, 146, 190]
for iy in icon_y:
    d.rectangle([14, iy-8, 34, iy+12], fill="#6B5B51" if iy != 58 else fg)

# Sidebar
sidebar_w = 220
d.rectangle([activity_w, 34, activity_w + sidebar_w, H-24], fill=sidebar_bg)
# Sidebar title
d.text((activity_w + 14, 52), "EXPLORER", fill=sidebar_title, font=title_font)
# Files
files = [
    ("cozy-vintage-theme", True, 0),
    ("  themes", False, 1),
    ("    cozy-vintage-dark.json", False, 2),
    ("    cozy-vintage-light.json", False, 2),
    ("  package.json", False, 1),
    ("  README.md", False, 1),
    ("  CHANGELOG.md", False, 1),
]
try:
    file_font = ImageFont.truetype("segoeui.ttf", 13)
except Exception:
    file_font = ImageFont.load_default()
y = 78
for name, is_open, depth in files:
    color = fg if is_open else sidebar_title
    d.text((activity_w + 14 + depth * 12, y), name, fill=color, font=file_font)
    y += 24

# Tabs
editor_x = activity_w + sidebar_w
editor_y = 34
tab_h = 36
n_tabs = 3
for i in range(n_tabs):
    tx = editor_x + i * 160
    is_active = i == 1
    tab_bg = tab_active_bg if is_active else tab_inactive_bg
    tab_fg = tab_active_fg if is_active else tab_inactive_fg
    d.rectangle([tx, editor_y, tx + 160, editor_y + tab_h], fill=tab_bg)
    d.line([(tx, editor_y + tab_h), (tx + 160, editor_y + tab_h)], fill=border)
    names = ["welcome", "theme.json", "preview.py"]
    d.text((tx + 14, editor_y + 19), names[i], fill=tab_fg, font=title_font, anchor="lm")

# Editor content area
editor_top = editor_y + tab_h
d.rectangle([editor_x, editor_top, W, H-24], fill=bg)

# Code content
sample = [
    ("// Cozy Vintage Theme preview", comment),
    ("import { Theme } from 'vscode';", keyword),
    ("", None),
    ("const palette = {", var_c),
    ("  cream: '#FDF4D2',", string),
    ("  dustyBlue: '#B0CDE6',", string),
    ("  lavender: '#A290B7',", string),
    ("  roseBrown: '#946D6D',", string),
    ("};", var_c),
    ("", None),
    ("function applyTheme(theme: Theme) {", func),
    ("  const colors = theme.colors;", var_c),
    ("  editor.background = 0x322A26;", var_c),
    ("  return true;", keyword),
    ("}", func),
]
try:
    code_font = ImageFont.truetype("Consolas.ttf", 16)
except Exception:
    try:
        code_font = ImageFont.truetype("consola.ttf", 16)
    except Exception:
        code_font = ImageFont.load_default()
code_x = editor_x + 30
code_y = editor_top + 30
line_h = 24
for line, color in sample:
    if line:
        d.text((code_x, code_y), line, fill=color or fg, font=code_font)
    code_y += line_h

# Line numbers
for i in range(1, len(sample) + 1):
    d.text((editor_x + 10, editor_top + 30 + (i - 1) * line_h), str(i), fill="#8A7A6B", font=code_font)

# Status bar
d.rectangle([0, H-24, W, H], fill=status_bg)
d.text((14, H-12), "master*", fill=status_fg, font=title_font, anchor="lm")
d.text((W-14, H-12), "Cozy Vintage Dark | UTF-8", fill=status_fg, font=title_font, anchor="rm")

# Save
OUT.parent.mkdir(parents=True, exist_ok=True)
img = img.convert("RGB")
img.save(OUT, "PNG")
print(f"Saved preview to {OUT} ({W}x{H})")
