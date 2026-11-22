#!/usr/bin/env python3
"""news-image-20261121: Saturday 21 November 2026 in one picture.

A front page (1024x1024) in the style of the 19 Nov winner: illustrated
story cards, a dotted world map, briefs, and a date check strip.
Deterministic: no network, no clock, no randomness. Pillow only.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")

CREAM = (246, 241, 227)
NAVY = (16, 36, 62)
RED = (193, 39, 45)
GOLD = (217, 164, 65)
INK = (20, 33, 61)
BODY = (58, 58, 54)
GREY = (120, 116, 106)
CARD_BORDER = (216, 210, 192)
WHITE = (255, 255, 255)
SLATE = (58, 72, 92)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap_text(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def fit_headline(text, max_w, max_lines=2, start=18, minimum=13):
    size = start
    while size > minimum:
        f = font(SERIF_B, size)
        if len(wrap_text(text, f, max_w)) <= max_lines:
            return f
        size -= 1
    return font(SERIF_B, minimum)


def truncate(text, fnt, max_w):
    if fnt.getlength(text) <= max_w:
        return text
    while text and fnt.getlength(text + "...") > max_w:
        text = text[:-1]
    return text + "..."


def draw_italic(img, x, y, text, fnt, fill):
    """Fake italic by shearing a rendered text layer."""
    w = int(fnt.getlength(text)) + 16
    h = fnt.size + 12
    tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.text((8, 6), text, font=fnt, fill=fill + (255,))
    sheared = tmp.transform((w, h), Image.AFFINE, (1, -0.16, 0, 0, 1, 0),
                            resample=Image.BILINEAR)
    img.paste(sheared, (int(x) - 8, int(y) - 6), sheared)


# ---------------------------------------------------------------------------
# Illustrations: flat vector-style drawings, one per story card.
# Each takes (draw, x, y, w, h) and paints inside that box.
# ---------------------------------------------------------------------------

def ill_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(27, 42, 74))
    for sx, sy in [(0.12, 0.2), (0.3, 0.12), (0.55, 0.25), (0.75, 0.15), (0.9, 0.3)]:
        d.ellipse([x + sx * w - 1, y + sy * h - 1, x + sx * w + 1, y + sy * h + 1],
                  fill=(255, 255, 255))
    d.rectangle([x, y + h * 0.55, x + w * 0.35, y + h], fill=(12, 20, 40))
    d.rectangle([x + w * 0.4, y + h * 0.45, x + w * 0.62, y + h], fill=(12, 20, 40))
    d.rectangle([x + w * 0.68, y + h * 0.6, x + w, y + h], fill=(12, 20, 40))
    for wx, wy in [(0.08, 0.62), (0.2, 0.7), (0.45, 0.55), (0.52, 0.65),
                   (0.75, 0.7), (0.85, 0.66)]:
        d.rectangle([x + wx * w, y + wy * h, x + wx * w + 3, y + wy * h + 4],
                    fill=(255, 214, 120))
    cx, cy = x + w * 0.72, y + h * 0.42
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(255, 140, 40))
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 210, 90))
    dx, dy = x + w * 0.25, y + h * 0.22
    d.ellipse([dx - 3, dy - 2, dx + 3, dy + 2], fill=(200, 200, 200))
    d.line([dx - 10, dy - 6, dx + 10, dy - 6], fill=(200, 200, 200), width=2)
    d.line([dx - 10, dy + 6, dx + 10, dy + 6], fill=(200, 200, 200), width=2)
    d.ellipse([dx - 12, dy - 8, dx - 7, dy - 4], fill=(220, 220, 220))
    d.ellipse([dx + 7, dy - 8, dx + 12, dy - 4], fill=(220, 220, 220))


def ill_kryvyi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.6], fill=(214, 120, 60))
    d.rectangle([x, y + h * 0.6, x + w, y + h], fill=(60, 45, 40))
    d.rectangle([x + w * 0.08, y + h * 0.42, x + w * 0.3, y + h * 0.62],
                fill=(50, 35, 32))
    d.rectangle([x + w * 0.55, y + h * 0.35, x + w * 0.8, y + h * 0.62],
                fill=(50, 35, 32))
    for bx, by, r in [(0.2, 0.35, 12), (0.68, 0.28, 14)]:
        cx, cy = x + bx * w, y + by * h
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 190, 60))
        d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55],
                  fill=(255, 240, 160))
    for sx, sy, r in [(0.2, 0.18, 8), (0.68, 0.12, 9), (0.3, 0.1, 6)]:
        d.ellipse([x + sx * w - r, y + sy * h - r, x + sx * w + r, y + sy * h + r],
                  fill=(120, 110, 105))


def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(158, 205, 225))
    d.ellipse([x + w * 0.8, y + h * 0.08, x + w * 0.95, y + h * 0.3],
              fill=(255, 214, 90))
    cx, cy, r = x + w * 0.38, y + h * 0.52, min(w, h) * 0.3
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 139, 87))
    d.ellipse([cx - r * 0.6, cy - r * 0.4, cx - r * 0.1, cy + r * 0.2],
              fill=(120, 200, 140))
    d.ellipse([cx + r * 0.1, cy - r * 0.7, cx + r * 0.6, cy - r * 0.1],
              fill=(120, 200, 140))
    d.rectangle([x + w * 0.62, y + h * 0.62, x + w * 0.95, y + h * 0.95],
                fill=(245, 245, 240))
    d.polygon([(x + w * 0.6, y + h * 0.62), (x + w * 0.78, y + h * 0.45),
               (x + w * 0.97, y + h * 0.62)], fill=(193, 39, 45))


def ill_mexico(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.62], fill=(240, 200, 130))
    d.ellipse([x + w * 0.75, y + h * 0.06, x + w * 0.92, y + h * 0.32],
              fill=(255, 170, 60))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(196, 140, 80))
    cx = x + w * 0.2
    d.rectangle([cx - 5, y + h * 0.3, cx + 5, y + h * 0.85],
                fill=(46, 139, 87))
    d.rectangle([cx - 18, y + h * 0.5, cx - 8, y + h * 0.62],
                fill=(46, 139, 87))
    d.rectangle([cx + 8, y + h * 0.42, cx + 18, y + h * 0.55],
                fill=(46, 139, 87))
    bx, by = x + w * 0.72, y + h * 0.68
    d.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=(217, 164, 65))
    d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=(255, 220, 130))


def ill_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 220, 200))
    d.polygon([(x, y + h), (x + w * 0.3, y + h * 0.25), (x + w * 0.6, y + h)],
              fill=(140, 110, 80))
    d.polygon([(x + w * 0.4, y + h), (x + w * 0.7, y + h * 0.15), (x + w, y + h)],
              fill=(110, 85, 60))
    d.polygon([(x + w * 0.24, y + h * 0.38), (x + w * 0.3, y + h * 0.25),
               (x + w * 0.36, y + h * 0.38)], fill=(255, 255, 255))
    d.polygon([(x + w * 0.64, y + h * 0.3), (x + w * 0.7, y + h * 0.15),
               (x + w * 0.76, y + h * 0.3)], fill=(255, 255, 255))
    d.rectangle([x + w * 0.06, y + h * 0.62, x + w * 0.94, y + h * 0.9],
                fill=(255, 255, 255))
    pts = []
    for i in range(41):
        px = x + w * 0.08 + i * (w * 0.84 / 40)
        amp = [0, 6, -8, 14, -16, 10, -6, 4, 0][i - 16] if 16 <= i <= 24 else 0
        pts.append((px, y + h * 0.76 + amp))
    d.line(pts, fill=(193, 39, 45), width=2)


def ill_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.4], fill=(255, 150, 60))
    d.rectangle([x, y + h * 0.4, x + w, y + h * 0.7], fill=(255, 110, 110))
    d.rectangle([x, y + h * 0.7, x + w, y + h], fill=(60, 40, 70))
    d.ellipse([x + w * 0.42, y + h * 0.12, x + w * 0.58, y + h * 0.38],
              fill=(255, 230, 150))
    d.rectangle([x, y + h * 0.55, x + w * 0.3, y + h], fill=(40, 25, 50))
    d.rectangle([x + w * 0.35, y + h * 0.45, x + w * 0.6, y + h], fill=(40, 25, 50))
    d.rectangle([x + w * 0.65, y + h * 0.6, x + w, y + h], fill=(40, 25, 50))
    cx, cy = x + w * 0.5, y + h * 0.82
    cw = min(w * 0.22, 60)
    d.rounded_rectangle([cx - cw, cy - 9, cx + cw, cy + 9], radius=8,
                        fill=(30, 30, 34))
    d.ellipse([cx - cw * 0.7, cy - 4, cx - cw * 0.7 + 8, cy + 4],
              fill=(120, 120, 130))
    d.ellipse([cx + cw * 0.7 - 8, cy - 4, cx + cw * 0.7, cy + 4],
              fill=(120, 120, 130))
    for bx, by, c in [(0.45, -4, (255, 80, 80)), (0.55, 0, (80, 200, 120)),
                      (0.45, 4, (80, 140, 255)), (0.35, 0, (255, 220, 80))]:
        d.ellipse([cx + bx * cw - 3, cy + by - 3, cx + bx * cw + 3, cy + by + 3],
                  fill=c)


def ill_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 12, 26))
    for sx, sy in [(0.08, 0.15), (0.2, 0.3), (0.85, 0.2), (0.92, 0.45),
                   (0.7, 0.1), (0.15, 0.6)]:
        d.ellipse([x + sx * w - 1, y + sy * h - 1, x + sx * w + 1, y + sy * h + 1],
                  fill=(255, 255, 255))
    d.ellipse([x + w * 0.05, y + h * 0.15, x + w * 0.95, y + h * 0.85],
              outline=(120, 130, 160), width=1)
    cx, cy, r = x + w * 0.4, y + h * 0.5, min(w, h) * 0.26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(176, 148, 120))
    for ox, oy, orr in [(0.3, 0.35, 3), (0.6, 0.6, 4), (0.45, 0.7, 2.5)]:
        d.ellipse([cx + (ox - 0.5) * 2 * r - orr, cy + (oy - 0.5) * 2 * r - orr,
                   cx + (ox - 0.5) * 2 * r + orr, cy + (oy - 0.5) * 2 * r + orr],
                  fill=(140, 115, 92))
    sx, sy = x + w * 0.78, y + h * 0.28
    d.polygon([(sx, sy - 8), (sx + 8, sy + 6), (sx - 8, sy + 6)],
              fill=(230, 230, 230))
    d.rectangle([sx - 14, sy + 2, sx + 14, sy + 6], fill=(120, 160, 220))


def ill_riemann(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 84, 60))
    d.rectangle([x, y, x + w, y + h], outline=(120, 90, 60), width=3)
    d.text((x + w * 0.08, y + h * 0.1), "ζ(s) = 0", font=font(SERIF_B, 19),
           fill=(255, 255, 255))
    d.text((x + w * 0.55, y + h * 0.14), "Re(s) = ½", font=font(SERIF, 14),
           fill=(255, 255, 255))
    d.text((x + w * 0.08, y + h * 0.52), "π(x) ~ Li(x)", font=font(SERIF, 14),
           fill=(255, 255, 255))
    d.line([(x + w * 0.62, y + h * 0.62), (x + w * 0.72, y + h * 0.82),
            (x + w * 0.92, y + h * 0.45)], fill=(120, 220, 130), width=4)


def ill_basra(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.7], fill=(200, 200, 195))
    d.rectangle([x, y + h * 0.7, x + w, y + h], fill=(90, 85, 80))
    d.polygon([(x + w * 0.12, y + h * 0.72), (x + w * 0.18, y + h * 0.3),
               (x + w * 0.3, y + h * 0.3), (x + w * 0.36, y + h * 0.72)],
              fill=(150, 148, 142))
    d.polygon([(x + w * 0.42, y + h * 0.72), (x + w * 0.48, y + h * 0.25),
               (x + w * 0.6, y + h * 0.25), (x + w * 0.66, y + h * 0.72)],
              fill=(150, 148, 142))
    d.rectangle([x + w * 0.72, y + h * 0.35, x + w * 0.78, y + h * 0.72],
                fill=(120, 118, 112))
    for fx, fr in [(0.24, 10), (0.54, 12), (0.75, 8)]:
        cx, cy = x + fx * w, y + h * 0.78
        d.ellipse([cx - fr, cy - fr * 1.2, cx + fr, cy + fr * 0.6],
                  fill=(255, 120, 30))
        d.ellipse([cx - fr * 0.55, cy - fr * 0.7, cx + fr * 0.55, cy + fr * 0.4],
                  fill=(255, 210, 80))
    d.ellipse([x + w * 0.72, y + h * 0.12, x + w * 0.82, y + h * 0.3],
              fill=(110, 108, 105))


def ill_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    for sx, sy in [(0.1, 0.2), (0.85, 0.15), (0.6, 0.3)]:
        d.ellipse([x + sx * w - 1, y + sy * h - 1, x + sx * w + 1, y + sy * h + 1],
                  fill=(255, 255, 255))
    d.line([x + w * 0.1, y + h * 0.85, x + w * 0.35, y + h * 0.25],
           fill=(255, 180, 80), width=2)
    d.ellipse([x + w * 0.35 - 3, y + h * 0.25 - 3, x + w * 0.35 + 3,
               y + h * 0.25 + 3], fill=(255, 240, 180))
    d.line([x + w * 0.55, y + h * 0.9, x + w * 0.75, y + h * 0.35],
           fill=(255, 180, 80), width=2)
    d.ellipse([x + w * 0.75 - 3, y + h * 0.35 - 3, x + w * 0.75 + 3,
               y + h * 0.35 + 3], fill=(255, 240, 180))
    cx, cy = x + w * 0.68, y + h * 0.3
    d.line([cx - 14, cy, cx + 14, cy], fill=(255, 220, 120), width=2)
    d.line([cx, cy - 14, cx, cy + 14], fill=(255, 220, 120), width=2)
    d.line([cx - 10, cy - 10, cx + 10, cy + 10], fill=(255, 220, 120), width=2)
    d.line([cx - 10, cy + 10, cx + 10, cy - 10], fill=(255, 220, 120), width=2)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 240, 180))
    d.rectangle([x, y + h * 0.72, x + w * 0.35, y + h], fill=(8, 12, 26))
    d.rectangle([x + w * 0.4, y + h * 0.62, x + w * 0.62, y + h], fill=(8, 12, 26))
    d.rectangle([x + w * 0.68, y + h * 0.75, x + w, y + h], fill=(8, 12, 26))


def ill_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.65], fill=(210, 200, 180))
    d.rectangle([x, y + h * 0.65, x + w, y + h], fill=(120, 110, 100))
    d.rectangle([x + w * 0.06, y + h * 0.4, x + w * 0.28, y + h * 0.68],
                fill=(90, 85, 80))
    d.rectangle([x + w * 0.34, y + h * 0.3, x + w * 0.58, y + h * 0.68],
                fill=(100, 95, 88))
    d.rectangle([x + w * 0.64, y + h * 0.45, x + w * 0.92, y + h * 0.68],
                fill=(90, 85, 80))
    for wx, wy in [(0.1, 0.45), (0.18, 0.5), (0.4, 0.38), (0.48, 0.48),
                   (0.7, 0.5), (0.8, 0.55)]:
        d.rectangle([x + wx * w, y + wy * h, x + wx * w + 3, y + wy * h + 4],
                    fill=(60, 55, 50))
    for sx, sy, r in [(0.45, 0.18, 9), (0.47, 0.08, 7), (0.75, 0.22, 8)]:
        d.ellipse([x + sx * w - r, y + sy * h - r, x + sx * w + r, y + sy * h + r],
                  fill=(140, 135, 128))
    d.ellipse([x + w * 0.42, y + h * 0.55, x + w * 0.58, y + h * 0.72],
              fill=(255, 140, 50))

# ---------------------------------------------------------------------------
# Content: 19 verified stories, all Saturday 21 November 2026.
# ---------------------------------------------------------------------------

# (num, category, colour, headline, summary, source, illustration)
CARDS = [
    (1, "DRONE STRIKE", (193, 39, 45), "Drones strike Kyiv overnight",
     "Two hurt, one in hospital; water cut in five districts.",
     "KYIV24 · KLITSCHKO", ill_kyiv),
    (2, "MISSILE", (179, 71, 0), "Double-tap strike kills 2",
     "Boy, 7, and a paramedic, 20, die; 60 wounded.",
     "AP", ill_kryvyi),
    (3, "CLIMATE", (31, 122, 92), "Antalya talks run past deadline",
     "No deal yet; draft strips fossil fuels and $120bn aid.",
     "REUTERS · AP", ill_cop31),
    (4, "CARTEL", (122, 74, 33), "'El Chapo Isidro' captured",
     "FBI Top 10 fugitive seized in Sinaloa; 11 killed.",
     "REUTERS · AP · CNN · WSJ", ill_mexico),
    (5, "QUAKE", (90, 80, 140), "M6.7 quake hits Junín",
     "Felt in Lima; no casualties reported. Depth 108 km.",
     "USGS", ill_peru),
    (6, "GAMES", (142, 42, 142), "GTA VI: $3.79bn day one",
     "32.5m copies; biggest entertainment launch ever.",
     "TAKE-TWO", ill_gta),
    (7, "SPACE", (46, 58, 140), "Into orbit after 8 years",
     "ESA-JAXA probe arrives after 8 years, 10bn km.",
     "ESA · NATURE", ill_mercury),
    (8, "MATHS", (46, 107, 52), "'The proof checks out'",
     "Lean community verifies the Riemann claim on Saturday.",
     "WSJ", ill_riemann),
    (9, "FIRE", (217, 93, 0), "Power station fire kills 4",
     "Gas pipeline blaze halts Hartha plant; 30 injured.",
     "REUTERS", ill_basra),
    (10, "DEFENCE", (47, 93, 138), "Houthis fire 3 missiles at Riyadh",
     "All intercepted; second attack in days.",
     "REUTERS", ill_riyadh),
    (11, "WAR", (122, 31, 43), "Israeli strike kills 4 in Gaza City",
     "Three die in a food-aid van; one shot in Jabalia.",
     "REUTERS · AFP", ill_gaza),
]

# (num, category, headline, summary, source)
BRIEFS = [
    (12, "GEN Z", "Protests sweep 25+ nations",
     "Day of action continues; Italy strike.", "CNN"),
    (13, "DENGUE", "Mosquitoes cut dengue 69%",
     "Wolbachia trial in Brazil, 5,700 kids.", "AP"),
    (14, "EU–INDONESIA", "Trade deal after 10 years",
     "Brussels pact cuts tariffs; from 2027.", "REUTERS"),
    (15, "GENEVA", "'Killer robot' talks stall",
     "No UN binding rules; talks go on.", "AP · NPR"),
    (16, "SPAIN", "New poll: PP 0.9 pts ahead",
     "Right leads before Nov 29 election.", "MORE IN COMMON"),
    (17, "CANADA", "No shift in US military ties",
     "Ottawa rejects rift after Hegseth memo.", "REUTERS"),
    (18, "LOS ANGELES", "M3.3 quake off San Pedro",
     "538 felt reports off San Pedro.", "USGS"),
    (19, "BALTIC", "Russian cargo ship ablaze",
     "Sparta 2 hit by drones off Finland.", "NY POST · REUTERS"),
]

# Dotted-map landmask: ellipses on a 96 x 48 grid (cx, cy, rx, ry).
LAND = [
    (17, 9, 13, 6), (24, 16, 4, 2), (32, 4, 4, 2.5), (27, 27, 6.5, 10),
    (49, 8, 6, 4.5), (45, 6, 1.8, 1.8), (52, 22, 8, 10), (70, 9, 15, 7),
    (66, 16, 4, 5), (76, 20, 5, 3), (79, 26, 7, 2), (82, 34, 7, 4.5),
    (86, 11, 1.8, 3.5), (90, 38, 1.5, 2.5),
]

# (story num, grid x, grid y) — nudged apart for legibility.
PINS = [
    (1, 53, 8), (2, 57, 11), (3, 51, 14), (4, 19, 17), (5, 28, 27),
    (6, 28, 13), (9, 63, 13), (10, 60, 19), (11, 56, 16),
]


def is_land(gx, gy):
    for cx, cy, rx, ry in LAND:
        if ((gx - cx) / rx) ** 2 + ((gy - cy) / ry) ** 2 <= 1:
            return True
    return False


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

def draw_card(d, x, y, w, h, num, cat, color, headline, summary, source, ill):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=CARD_BORDER, width=1)
    ill_h = 74
    ill(d, x + 1, y + 1, w - 2, ill_h - 1)
    bx, by, br = x + 16, y + ill_h, 11
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=color,
              outline=WHITE, width=2)
    nf = font(SANS_B, 13)
    tw = nf.getlength(str(num))
    d.text((bx - tw / 2, by - 7), str(num), font=nf, fill=WHITE)
    d.text((x + 32, y + ill_h + 4), cat, font=font(SANS_B, 10), fill=color)
    hx, hw = x + 10, w - 20
    hf = fit_headline(headline, hw, 2, 18 if w > 300 else 16)
    lines = wrap_text(headline, hf, hw)[:2]
    yy = draw_lines(d, hx, y + ill_h + 18, lines, hf, INK, hf.size + 3)
    sf = font(SANS, 12)
    slines = wrap_text(summary, sf, hw)[:2]
    draw_lines(d, hx, yy + 2, slines, sf, BODY, 15)
    d.text((hx, y + h - 10), source, font=font(SANS, 9), fill=GREY)


def draw_masthead(d):
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.rectangle([10, 8, 82, 84], fill=RED)
    for txt, yy, size in [("NOV", 12, 16), ("21", 30, 30), ("SAT", 62, 15)]:
        f = font(SANS_B, size)
        d.text((46 - f.getlength(txt) / 2, yy), txt, font=f, fill=WHITE)
    f = font(SANS_B, 14)
    t = "THE DAY IN WORLD NEWS"
    d.text(((W - f.getlength(t)) / 2, 12), t, font=f, fill=GOLD)
    f = font(SERIF_B, 38)
    t = "Saturday 21 November 2026"
    d.text(((W - f.getlength(t)) / 2, 30), t, font=f, fill=WHITE)
    for txt, yy, col in [("19 STORIES", 14, WHITE), ("4 CONTINENTS", 36, WHITE),
                         ("ONE PAGE", 58, GOLD)]:
        f = font(SANS_B, 14)
        d.text((1014 - f.getlength(txt), yy), txt, font=f, fill=col)


def draw_map(d, x, y, w, h):
    d.text((x, y), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=INK)
    mx, my, mw, mh = x + 4, y + 26, w - 8, h - 62
    cols, rows = 96, 48
    cw, ch = mw / cols, mh / rows
    for gy in range(rows):
        for gx in range(cols):
            if is_land(gx, gy):
                cx = mx + (gx + 0.5) * cw
                cy = my + (gy + 0.5) * ch
                d.ellipse([cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5], fill=SLATE)
    pf = font(SANS_B, 10)
    for num, gx, gy in PINS:
        cx = mx + (gx + 0.5) * cw
        cy = my + (gy + 0.5) * ch
        r = 7
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                  outline=WHITE, width=1)
        tw = pf.getlength(str(num))
        d.text((cx - tw / 2, cy - 5), str(num), font=pf, fill=WHITE)
    lf = font(SANS, 10)
    d.text((x, y + h - 34),
           "1 KYIV · 2 KRYVYI RIH · 3 ANTALYA · 4 GUASAVE", font=lf, fill=BODY)
    d.text((x, y + h - 18),
           "5 JUNÍN · 6 NEW YORK · 9 BASRA · 10 RIYADH · 11 GAZA",
           font=lf, fill=BODY)


def draw_briefs(d, x, y, w, h):
    d.text((x, y), "ALSO ON SATURDAY 21 NOVEMBER", font=font(SANS_B, 13),
           fill=INK)
    col_w = (w - 12) // 2
    for i, (num, cat, head, summ, src) in enumerate(BRIEFS):
        col, row = i % 2, i // 2
        bx = x + col * (col_w + 12)
        by = y + 28 + row * 52
        d.text((bx, by), str(num), font=font(SANS_B, 13), fill=RED)
        hf = font(SANS_B, 12)
        head_txt = truncate(head, hf, col_w - 26)
        d.text((bx + 26, by), head_txt, font=hf, fill=INK)
        sf = font(SANS, 10)
        d.text((bx + 26, by + 17), truncate(summ, sf, col_w - 26),
               font=sf, fill=BODY)
        d.text((bx + 26, by + 32), src, font=font(SANS, 9), fill=GREY)


def draw_bottom(d):
    # date check strip
    d.rectangle([10, 924, 1014, 962], fill=WHITE, outline=RED, width=2)
    lab = "DATE CHECK — NOT 21 NOVEMBER:  "
    lf = font(SANS_B, 12)
    body = ("Friday's market crash (S&P −3.7%) · Kyiv bridge barrage · "
            "Bayer $7.25bn deal · FBI/USDA hack · Rinderknecht verdict · "
            "Myanmar ICJ ruling (19 Nov) · UK drones (19 Nov) — "
            "all 20 Nov or earlier.")
    bf = font(SANS, 12)
    max_w = 1014 - 10 - 16 - lf.getlength(lab)
    lines = wrap_text(body, bf, max_w)
    d.text((18, 930), lab, font=lf, fill=RED)
    lx = 18 + lf.getlength(lab)
    draw_lines(d, lx, 930, lines[:2], bf, BODY, 15)
    # footer
    ff = font(SANS, 10)
    t = ("All 19 stories happened, or were first reported, on Saturday "
         "21 November 2026. Sources: Reuters · AP · AFP · CNN · USGS · ESA · "
         "Take-Two · Kyiv24. Original drawings.")
    d.text(((W - ff.getlength(t)) / 2, 972), t, font=ff, fill=GREY)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    tf = font(SERIF, 16)
    tag = ("Everything on this page happened, or was first reported, on "
           "Saturday 21 November 2026.")
    draw_italic(img, (W - tf.getlength(tag)) / 2, 100, tag, tf, BODY)
    xs1 = [10, 347, 684]
    for i, c in enumerate(CARDS[0:3]):
        draw_card(d, xs1[i], 124, 329, 180, *c)
    xs2 = [10, 263, 516, 769]
    for i, c in enumerate(CARDS[3:7]):
        draw_card(d, xs2[i], 310, 245, 180, *c)
    for i, c in enumerate(CARDS[7:11]):
        draw_card(d, xs2[i], 496, 245, 180, *c)
    draw_map(d, 10, 682, 490, 236)
    draw_briefs(d, 510, 682, 504, 236)
    draw_bottom(d)
    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, "entry.png"))


if __name__ == "__main__":
    main()
