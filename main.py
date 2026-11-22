#!/usr/bin/env python3
"""Draw the Saturday 21 November 2026 world-news front page.

One image, 1024x1024, deterministic. Python + Pillow only, no network.
Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
Without MAKEFUN_OUTPUT_DIR it writes entry.png next to this file.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 227)
NAVY = (27, 42, 74)
RED = (192, 57, 43)
GOLD = (212, 160, 23)
INK = (28, 28, 28)
GREY = (96, 96, 96)
LINE = (216, 208, 189)
WHITE = (255, 255, 255)
MAP_DOT = (51, 65, 94)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size, fallback=None):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        if fallback:
            return ImageFont.truetype(fallback, size)
        return ImageFont.load_default()


def serif_b(size):
    return font(F_SERIF_B, size)


def serif(size):
    return font(F_SERIF, size)


def serif_i(size):
    return font(F_SERIF_I, size, fallback=F_SERIF)


def sans(size):
    return font(F_SANS, size)


def sans_b(size):
    return font(F_SANS_B, size)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def burst(d, cx, cy, r, color):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8.0
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def star4(d, cx, cy, r, color):
    d.polygon([(cx, cy - r), (cx + r * 0.28, cy - r * 0.28),
               (cx + r, cy), (cx + r * 0.28, cy + r * 0.28),
               (cx, cy + r), (cx - r * 0.28, cy + r * 0.28),
               (cx - r, cy), (cx - r * 0.28, cy - r * 0.28)], fill=color)


# ---------------------------------------------------------------- illustrations
def ill_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 35, 64))
    for sx, sy in [(0.12, 0.2), (0.3, 0.12), (0.55, 0.25), (0.8, 0.15), (0.92, 0.3)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1],
                  fill=(255, 255, 255))
    d.ellipse([x + w * 0.82 - 14, y + h * 0.18 - 14, x + w * 0.82 + 14, y + h * 0.18 + 14],
              fill=(240, 180, 60))
    for bx, bw, bh in [(0.05, 0.2, 0.45), (0.3, 0.16, 0.6), (0.5, 0.22, 0.5), (0.75, 0.18, 0.4)]:
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h], fill=(12, 18, 38))
        for wy in range(2):
            for wx in range(3):
                d.rectangle([x + w * bx + 5 + wx * 12, y + h - h * bh + 6 + wy * 12,
                             x + w * bx + 10 + wx * 12, y + h - h * bh + 11 + wy * 12],
                            fill=(250, 210, 90))
    burst(d, x + w * 0.68, y + h * 0.42, 16, (255, 140, 40))
    burst(d, x + w * 0.68, y + h * 0.42, 9, (255, 220, 90))
    d.rectangle([x + w * 0.42 - 8, y + h * 0.16 - 3, x + w * 0.42 + 8, y + h * 0.16 + 3],
                fill=(200, 200, 200))
    for dx, dy in [(-12, -8), (12, -8), (-12, 8), (12, 8)]:
        d.line([x + w * 0.42, y + h * 0.16, x + w * 0.42 + dx, y + h * 0.16 + dy],
               fill=(200, 200, 200), width=2)


def ill_kryvyi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.5], fill=(60, 30, 20))
    d.rectangle([x, y + h * 0.5, x + w, y + h], fill=(140, 70, 30))
    burst(d, x + w * 0.3, y + h * 0.42, 18, (255, 160, 40))
    burst(d, x + w * 0.3, y + h * 0.42, 10, (255, 225, 110))
    burst(d, x + w * 0.72, y + h * 0.3, 13, (255, 140, 40))
    burst(d, x + w * 0.72, y + h * 0.3, 7, (255, 220, 90))
    for ex, ey, er in [(0.18, 0.2, 12), (0.5, 0.14, 9), (0.85, 0.18, 11)]:
        d.ellipse([x + w * ex - er, y + h * ey - er * 0.7, x + w * ex + er, y + h * ey + er * 0.7],
                  fill=(120, 110, 105))
    d.rectangle([x, y + h * 0.82, x + w, y + h], fill=(30, 20, 16))
    d.rectangle([x + w * 0.1, y + h * 0.62, x + w * 0.28, y + h * 0.82], fill=(45, 30, 24))
    d.rectangle([x + w * 0.6, y + h * 0.66, x + w * 0.82, y + h * 0.82], fill=(45, 30, 24))


def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(135, 206, 235))
    d.ellipse([x + w * 0.84 - 13, y + h * 0.2 - 13, x + w * 0.84 + 13, y + h * 0.2 + 13],
              fill=(250, 215, 80))
    d.ellipse([x + w * 0.28 - 26, y + h * 0.5 - 26, x + w * 0.28 + 26, y + h * 0.5 + 26],
              fill=(70, 160, 90))
    d.ellipse([x + w * 0.22 - 10, y + h * 0.42 - 7, x + w * 0.22 + 10, y + h * 0.42 + 7],
              fill=(40, 120, 70))
    d.ellipse([x + w * 0.34 - 8, y + h * 0.6 - 6, x + w * 0.34 + 8, y + h * 0.6 + 6],
              fill=(40, 120, 70))
    d.rectangle([x + w * 0.62, y + h * 0.62, x + w * 0.95, y + h * 0.88], fill=(245, 245, 240))
    d.polygon([(x + w * 0.58, y + h * 0.62), (x + w * 0.99, y + h * 0.62),
               (x + w * 0.78, y + h * 0.42)], fill=(192, 57, 43))
    for i in range(3):
        d.rectangle([x + w * (0.66 + i * 0.09), y + h * 0.7, x + w * (0.71 + i * 0.09),
                     y + h * 0.84], fill=(27, 42, 74))


def ill_mexico(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.62], fill=(222, 184, 135))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(190, 140, 90))
    d.ellipse([x + w * 0.78 - 14, y + h * 0.24 - 14, x + w * 0.78 + 14, y + h * 0.24 + 14],
              fill=(240, 150, 50))
    d.rectangle([x + w * 0.16, y + h * 0.3, x + w * 0.16 + 10, y + h * 0.85], fill=(46, 125, 70))
    d.rectangle([x + w * 0.16 - 12, y + h * 0.48, x + w * 0.16 - 2, y + h * 0.58], fill=(46, 125, 70))
    d.rectangle([x + w * 0.26, y + h * 0.52, x + w * 0.26 + 8, y + h * 0.58], fill=(46, 125, 70))
    d.rectangle([x + w * 0.26 + 8, y + h * 0.52, x + w * 0.26 + 18, y + h * 0.6], fill=(46, 125, 70))
    star4(d, x + w * 0.62, y + h * 0.42, 16, (212, 175, 55))
    d.ellipse([x + w * 0.62 - 6, y + h * 0.42 - 6, x + w * 0.62 + 6, y + h * 0.42 + 6],
              fill=(212, 175, 55))


def ill_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 222, 238))
    d.polygon([(x, y + h), (x + w * 0.32, y + h * 0.28), (x + w * 0.62, y + h)],
              fill=(139, 109, 80))
    d.polygon([(x + w * 0.32, y + h * 0.28), (x + w * 0.24, y + h * 0.46),
               (x + w * 0.4, y + h * 0.46)], fill=(255, 255, 255))
    d.polygon([(x + w * 0.45, y + h), (x + w * 0.78, y + h * 0.2), (x + w, y + h)],
              fill=(110, 85, 60))
    d.polygon([(x + w * 0.78, y + h * 0.2), (x + w * 0.71, y + h * 0.38),
               (x + w * 0.85, y + h * 0.38)], fill=(255, 255, 255))
    d.rectangle([x + w * 0.06, y + h * 0.68, x + w * 0.94, y + h * 0.92], fill=(255, 255, 255))
    pts = [(x + w * 0.08, y + h * 0.8), (x + w * 0.2, y + h * 0.8), (x + w * 0.26, y + h * 0.72),
           (x + w * 0.32, y + h * 0.88), (x + w * 0.38, y + h * 0.74), (x + w * 0.44, y + h * 0.86),
           (x + w * 0.52, y + h * 0.7), (x + w * 0.58, y + h * 0.88), (x + w * 0.66, y + h * 0.76),
           (x + w * 0.74, y + h * 0.84), (x + w * 0.92, y + h * 0.8)]
    d.line(pts, fill=(192, 57, 43), width=3)

def ill_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.35], fill=(230, 130, 60))
    d.rectangle([x, y + h * 0.35, x + w, y + h * 0.65], fill=(200, 90, 110))
    d.rectangle([x, y + h * 0.65, x + w, y + h], fill=(90, 50, 110))
    d.ellipse([x + w * 0.7 - 12, y + h * 0.2 - 12, x + w * 0.7 + 12, y + h * 0.2 + 12],
              fill=(250, 220, 120))
    for bx, bw, bh in [(0.04, 0.14, 0.3), (0.2, 0.1, 0.42), (0.32, 0.16, 0.34),
                       (0.52, 0.12, 0.46), (0.66, 0.15, 0.36), (0.84, 0.12, 0.3)]:
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h], fill=(40, 25, 60))
        d.rectangle([x + w * bx + 3, y + h - h * bh + 4, x + w * bx + 6, y + h - h * bh + 7],
                    fill=(250, 220, 120))
    d.rounded_rectangle([x + w * 0.32, y + h * 0.62, x + w * 0.68, y + h * 0.9], radius=8,
                        fill=(30, 30, 40))
    d.ellipse([x + w * 0.38 - 4, y + h * 0.72 - 4, x + w * 0.38 + 4, y + h * 0.72 + 4],
              fill=(90, 200, 90))
    d.ellipse([x + w * 0.62 - 4, y + h * 0.72 - 4, x + w * 0.62 + 4, y + h * 0.72 + 4],
              fill=(230, 60, 60))
    d.ellipse([x + w * 0.56 - 4, y + h * 0.8 - 4, x + w * 0.56 + 4, y + h * 0.8 + 4],
              fill=(60, 140, 230))
    d.ellipse([x + w * 0.5 - 4, y + h * 0.76 - 4, x + w * 0.5 + 4, y + h * 0.76 + 4],
              fill=(240, 200, 60))


def ill_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 12, 30))
    for sx, sy in [(0.1, 0.2), (0.25, 0.12), (0.7, 0.18), (0.88, 0.3), (0.55, 0.1)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1],
                  fill=(255, 255, 255))
    d.ellipse([x + w * 0.06, y + h * 0.08, x + w * 0.94, y + h * 0.92], outline=(120, 120, 140),
              width=1)
    d.ellipse([x + w * 0.42 - 24, y + h * 0.5 - 24, x + w * 0.42 + 24, y + h * 0.5 + 24],
              fill=(178, 150, 120))
    for cx, cy, cr in [(0.36, 0.44, 5), (0.47, 0.56, 4), (0.4, 0.6, 3), (0.48, 0.42, 3)]:
        d.ellipse([x + w * cx - cr, y + h * cy - cr, x + w * cx + cr, y + h * cy + cr],
                  fill=(140, 115, 90))
    d.polygon([(x + w * 0.8, y + h * 0.3), (x + w * 0.88, y + h * 0.38),
               (x + w * 0.8, y + h * 0.42)], fill=(220, 220, 220))
    d.rectangle([x + w * 0.74, y + h * 0.34, x + w * 0.8, y + h * 0.38], fill=(180, 180, 180))


def ill_riemann(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 60, 42))
    d.rectangle([x + w * 0.04, y + h * 0.06, x + w * 0.96, y + h * 0.94], outline=(90, 110, 95),
                width=2)
    d.text((x + w * 0.07, y + h * 0.14), "\u03b6(s) = 0", font=serif_b(24),
           fill=(255, 255, 255))
    d.text((x + w * 0.07, y + h * 0.52), "Re(s) = \u00bd", font=serif(15),
           fill=(220, 230, 220))
    d.line([(x + w * 0.62, y + h * 0.55), (x + w * 0.7, y + h * 0.72), (x + w * 0.92, y + h * 0.42)],
           fill=(90, 220, 120), width=5)


def ill_basra(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 178, 178))
    for ex, ey, er in [(0.2, 0.2, 13), (0.55, 0.14, 10), (0.85, 0.22, 12)]:
        d.ellipse([x + w * ex - er, y + h * ey - er * 0.7, x + w * ex + er, y + h * ey + er * 0.7],
                  fill=(110, 110, 110))
    d.polygon([(x + w * 0.12, y + h), (x + w * 0.18, y + h * 0.3), (x + w * 0.3, y + h * 0.3),
               (x + w * 0.36, y + h)], fill=(120, 120, 120))
    d.polygon([(x + w * 0.5, y + h), (x + w * 0.56, y + h * 0.38), (x + w * 0.68, y + h * 0.38),
               (x + w * 0.74, y + h)], fill=(100, 100, 100))
    burst(d, x + w * 0.24, y + h * 0.78, 12, (255, 140, 40))
    burst(d, x + w * 0.24, y + h * 0.78, 7, (255, 220, 90))
    burst(d, x + w * 0.62, y + h * 0.82, 10, (255, 140, 40))
    burst(d, x + w * 0.62, y + h * 0.82, 6, (255, 220, 90))


def ill_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(15, 20, 45))
    for sx, sy in [(0.15, 0.2), (0.4, 0.12), (0.65, 0.25), (0.9, 0.15)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1],
                  fill=(255, 255, 255))
    for bx, bw, bh in [(0.05, 0.18, 0.35), (0.28, 0.14, 0.5), (0.5, 0.2, 0.4), (0.75, 0.16, 0.45)]:
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h], fill=(8, 12, 28))
        d.rectangle([x + w * bx + 4, y + h - h * bh + 5, x + w * bx + 8, y + h - h * bh + 9],
                    fill=(250, 210, 90))
    d.line([(x + w * 0.15, y + h * 0.75), (x + w * 0.45, y + h * 0.3)], fill=(255, 160, 60),
           width=3)
    d.line([(x + w * 0.3, y + h * 0.8), (x + w * 0.62, y + h * 0.35)], fill=(255, 160, 60),
           width=3)
    burst(d, x + w * 0.72, y + h * 0.3, 15, (255, 220, 90))
    burst(d, x + w * 0.72, y + h * 0.3, 8, (255, 255, 255))


def ill_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(170, 170, 170))
    for ex, ey, er in [(0.25, 0.25, 14), (0.6, 0.18, 11), (0.85, 0.3, 12)]:
        d.ellipse([x + w * ex - er, y + h * ey - er * 0.7, x + w * ex + er, y + h * ey + er * 0.7],
                  fill=(100, 100, 100))
    for bx, bw, bh in [(0.05, 0.2, 0.5), (0.3, 0.16, 0.62), (0.52, 0.22, 0.48),
                       (0.78, 0.16, 0.55)]:
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h], fill=(90, 90, 90))
        for wy in range(2):
            d.rectangle([x + w * bx + 4, y + h - h * bh + 5 + wy * 12,
                         x + w * bx + 9, y + h - h * bh + 10 + wy * 12], fill=(60, 60, 60))
    d.rounded_rectangle([x + w * 0.36, y + h * 0.68, x + w * 0.66, y + h * 0.88], radius=4,
                        fill=(200, 120, 50))
    d.ellipse([x + w * 0.42 - 5, y + h * 0.88 - 5, x + w * 0.42 + 5, y + h * 0.88 + 5],
              fill=(30, 30, 30))
    d.ellipse([x + w * 0.6 - 5, y + h * 0.88 - 5, x + w * 0.6 + 5, y + h * 0.88 + 5],
              fill=(30, 30, 30))


ILLS = {"kyiv": ill_kyiv, "kryvyi": ill_kryvyi, "cop31": ill_cop31, "mexico": ill_mexico,
        "peru": ill_peru, "gta": ill_gta, "mercury": ill_mercury, "riemann": ill_riemann,
        "basra": ill_basra, "riyadh": ill_riyadh, "gaza": ill_gaza}


# ---------------------------------------------------------------- cards
def card(d, x, y, w, h, num, color, cat, headline, summary, source, ill, ill_h,
         head_size):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=LINE, width=1)
    ILLS[ill](d, x + 1, y + 1, w - 2, ill_h)
    d.ellipse([x + 8, y + 8, x + 30, y + 30], fill=color, outline=WHITE, width=2)
    nf = sans_b(13)
    ntxt = str(num)
    d.text((x + 19, y + 19), ntxt, font=nf, fill=WHITE, anchor="mm")
    ty = y + ill_h + 7
    d.text((x + 9, ty), cat, font=sans_b(11), fill=color)
    ty += 14
    hf = serif_b(head_size)
    for ln in wrap(d, headline, hf, w - 18)[:2]:
        d.text((x + 9, ty), ln, font=hf, fill=INK)
        ty += head_size + 2
    ty += 1
    sf = serif(12)
    for ln in wrap(d, summary, sf, w - 18)[:2]:
        d.text((x + 9, ty), ln, font=sf, fill=(60, 60, 60))
        ty += 14
    d.text((x + 9, y + h - 15), source, font=sans(9), fill=GREY)


# ---------------------------------------------------------------- dotted map
LAND = [
    (0.16, 0.30, 0.13, 0.16), (0.31, 0.13, 0.035, 0.05), (0.27, 0.64, 0.075, 0.17),
    (0.50, 0.26, 0.055, 0.09), (0.52, 0.56, 0.085, 0.17), (0.72, 0.30, 0.17, 0.16),
    (0.79, 0.60, 0.05, 0.05), (0.86, 0.74, 0.06, 0.05),
]

PINS = [(1, 0.52, 0.24), (2, 0.55, 0.28), (3, 0.565, 0.33), (4, 0.10, 0.44),
        (5, 0.26, 0.62), (6, 0.235, 0.36), (9, 0.60, 0.40), (10, 0.585, 0.45),
        (11, 0.565, 0.375)]


def dotted_map(d, x, y, w, h):
    step = 7
    gy = y + 4
    while gy < y + h:
        gx = x + 4
        while gx < x + w:
            u = (gx - x) / w
            v = (gy - y) / h
            for (cu, cv, ru, rv) in LAND:
                if ((u - cu) / ru) ** 2 + ((v - cv) / rv) ** 2 <= 1.0:
                    d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=MAP_DOT)
                    break
            gx += step
        gy += step
    pf = sans_b(10)
    for (num, pu, pv) in PINS:
        px, py = x + w * pu, y + h * pv
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
        d.text((px, py), str(num), font=pf, fill=WHITE, anchor="mm")

# ---------------------------------------------------------------- data
CARDS = [
    (1, RED, "DRONE STRIKE", "Drones strike Kyiv overnight",
     "Two hurt, one in hospital; water cut in five districts.",
     "KYIV24 \u00b7 KLITSCHKO", "kyiv"),
    (2, (200, 100, 30), "MISSILE", "Double-tap strike kills 2",
     "Boy, 7, and a paramedic, 20, die; 60 wounded.", "AP", "kryvyi"),
    (3, (40, 140, 110), "CLIMATE", "Antalya talks run past deadline",
     "No deal yet; draft strips fossil fuels and $120bn aid.",
     "REUTERS \u00b7 AP", "cop31"),
    (4, (150, 100, 40), "CARTEL", "'El Chapo Isidro' captured",
     "FBI Top 10 fugitive seized in Sinaloa; 11 killed.",
     "REUTERS \u00b7 AP \u00b7 CNN \u00b7 WSJ", "mexico"),
    (5, (120, 70, 160), "QUAKE", "M6.7 quake hits Jun\u00edn",
     "Felt in Lima; no casualties reported. Depth 108 km.", "USGS", "peru"),
    (6, (160, 60, 160), "GAMES", "GTA VI: $3.79bn day one",
     "32.5m copies; biggest entertainment launch ever.", "TAKE-TWO", "gta"),
    (7, (40, 90, 180), "SPACE", "Into orbit after 8 years",
     "ESA-JAXA probe arrives after 8 years, 10bn km.", "ESA \u00b7 NATURE", "mercury"),
    (8, (40, 140, 80), "MATHS", "'The proof checks out'",
     "Lean community verifies the Riemann claim on Saturday.", "WSJ", "riemann"),
    (9, (200, 100, 30), "FIRE", "Power station fire kills 4",
     "Gas pipeline blaze halts Hartha plant; 30 injured.", "REUTERS", "basra"),
    (10, (40, 90, 180), "DEFENCE", "Houthis fire 3 missiles at Riyadh",
     "All intercepted; second attack in days.", "REUTERS", "riyadh"),
    (11, RED, "WAR", "Israeli strike kills 4 in Gaza City",
     "Three die in a food-aid van; one shot in Jabalia.", "REUTERS \u00b7 AFP", "gaza"),
]

BRIEFS = [
    (12, "Protests sweep 25+ nations", "Day of action continues; Italy strike.", "CNN"),
    (13, "Mosquitoes cut dengue 69%", "Wolbachia trial in Brazil, 5,700 kids.", "AP"),
    (14, "Trade deal after 10 years", "Brussels pact cuts tariffs; from 2027.", "REUTERS"),
    (15, "'Killer robot' talks stall", "No UN binding rules; talks go on.", "AP \u00b7 NPR"),
    (16, "New poll: PP 0.9 pts ahead", "Right leads before Nov 29 election.", "MORE IN COMMON"),
    (17, "No shift in US military ties", "Ottawa rejects rift after Hegseth memo.", "REUTERS"),
    (18, "M3.3 quake off San Pedro", "538 felt reports off San Pedro.", "USGS"),
    (19, "Russian cargo ship ablaze", "Sparta 2 hit by drones off Finland.", "NY POST \u00b7 REUTERS"),
]


def brief(d, x, y, w, num, headline, summary, source):
    d.text((x, y), str(num), font=sans_b(13), fill=RED)
    hf = serif_b(13)
    hx = x + 24
    ty = y
    for ln in wrap(d, headline, hf, w - 24)[:2]:
        d.text((hx, ty), ln, font=hf, fill=INK)
        ty += 16
    sf = serif(11)
    for ln in wrap(d, summary, sf, w)[:1]:
        d.text((x, ty + 1), ln, font=sf, fill=(60, 60, 60))
        ty += 14
    d.text((x, ty + 2), source, font=sans(9), fill=GREY)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([16, 16, 1008, 112], fill=NAVY)
    d.rectangle([16, 16, 88, 112], fill=RED)
    d.text((52, 32), "NOV", font=sans_b(17), fill=WHITE, anchor="ma")
    d.text((52, 62), "21", font=sans_b(34), fill=WHITE, anchor="ma")
    d.text((52, 96), "SAT", font=sans_b(15), fill=WHITE, anchor="ma")
    d.text((512, 28), "THE DAY IN WORLD NEWS", font=sans_b(15), fill=GOLD, anchor="ma")
    d.text((512, 52), "Saturday 21 November 2026", font=serif_b(42), fill=WHITE, anchor="ma")
    d.text((992, 30), "19 STORIES", font=sans_b(14), fill=WHITE, anchor="ra")
    d.text((992, 52), "4 CONTINENTS", font=sans_b(14), fill=WHITE, anchor="ra")
    d.text((992, 74), "ONE PAGE", font=sans_b(14), fill=GOLD, anchor="ra")
    d.text((512, 122), "Everything on this page happened, or was first reported, "
           "on Saturday 21 November 2026.", font=serif_i(15), fill=(80, 80, 80), anchor="ma")

    # card grid
    row1 = CARDS[0:3]
    row2 = CARDS[3:7]
    row3 = CARDS[7:11]
    xs3 = [16, 349, 683]
    ws3 = [325, 326, 325]
    for (c, cx, cw) in zip(row1, xs3, ws3):
        card(d, cx, 142, cw, 172, c[0], c[1], c[2], c[3], c[4], c[5], c[6], 64, 19)
    xs4 = [16, 266, 516, 766]
    for (c, cx) in zip(row2, xs4):
        card(d, cx, 322, 242, 154, c[0], c[1], c[2], c[3], c[4], c[5], c[6], 52, 16)
    for (c, cx) in zip(row3, xs4):
        card(d, cx, 484, 242, 154, c[0], c[1], c[2], c[3], c[4], c[5], c[6], 52, 16)

    # bottom: map + briefs
    d.text((16, 646), "WHERE IT HAPPENED", font=sans_b(15), fill=INK)
    dotted_map(d, 16, 666, 480, 210)
    lf = sans(11)
    d.text((16, 886), "1 KYIV \u00b7 2 KRYVYI RIH \u00b7 3 ANTALYA \u00b7 4 GUASAVE \u00b7 5 JUN\u00cdN",
           font=lf, fill=INK)
    d.text((16, 902), "6 NEW YORK \u00b7 9 BASRA \u00b7 10 RIYADH \u00b7 11 GAZA",
           font=lf, fill=INK)
    d.text((512, 646), "ALSO ON SATURDAY 21 NOVEMBER", font=sans_b(15), fill=INK)
    for i, b in enumerate(BRIEFS[:4]):
        brief(d, 512, 666 + i * 64, 240, b[0], b[1], b[2], b[3])
    for i, b in enumerate(BRIEFS[4:]):
        brief(d, 764, 666 + i * 64, 244, b[0], b[1], b[2], b[3])

    # date check strip
    d.rectangle([16, 928, 1008, 962], outline=RED, width=2)
    dc = ("DATE CHECK \u2014 NOT 21 NOVEMBER:  "
          "Friday's market crash (S&P \u22123.7%) \u00b7 Kyiv bridge barrage \u00b7 "
          "Bayer $7.25bn deal \u00b7 FBI/USDA hack \u00b7 Rinderknecht verdict \u00b7 "
          "Myanmar ICJ ruling (19 Nov) \u00b7 UK drones (19 Nov) \u2014 all 20 Nov or earlier.")
    lines = wrap(d, dc, serif(12), 960)
    ly = 934
    for ln in lines[:2]:
        d.text((28, ly), ln, font=serif(12), fill=INK)
        ly += 15

    # footer
    d.text((512, 970), "All 19 stories happened, or were first reported, on Saturday "
           "21 November 2026. Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 CNN \u00b7 USGS \u00b7 "
           "ESA \u00b7 Take-Two \u00b7 Kyiv24. Original drawings.",
           font=sans(10), fill=GREY, anchor="ma")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "entry.png")
    else:
        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out_path, "PNG")
    print("wrote", out_path)


if __name__ == "__main__":
    main()
