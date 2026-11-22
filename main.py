#!/usr/bin/env python3
"""news-image-20261121 v4: front page like the 19 Nov winner.
Draws Saturday 21 November 2026 world news in one 1024x1024 image.
Python + Pillow only, no network, deterministic."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (245, 240, 230)
NAVY = (20, 35, 70)
RED = (190, 30, 30)
GOLD = (212, 175, 55)
INK = (30, 30, 30)
GREY = (110, 110, 110)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SERIF_I = lambda s: font("DejaVuSerif.ttf", s)  # no Serif-Italic on system
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def draw_badge(draw, cx, cy, num, color):
    r = 11
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color,
                 outline=WHITE, width=2)
    text(draw, (cx, cy), str(num), F_SANS_B(13), WHITE, anchor="mm")


def draw_card(draw, x, y, w, h, num, cat, cat_color, headline, summary,
              source, ill):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=(200, 190, 175))
    ill_h = 52 if w > 300 else 44
    ill(draw, x, y, w, ill_h)
    draw_badge(draw, x + 16, y + ill_h + 12, num, cat_color)
    text(draw, (x + 32, y + ill_h + 4), cat, F_SANS_B(11), cat_color)
    hl = wrap(draw, headline, F_SERIF_B(17 if w > 300 else 15), w - 20)
    yy = y + ill_h + 22
    lh = 19 if w > 300 else 17
    for ln in hl[:2]:
        text(draw, (x + 10, yy), ln, F_SERIF_B(17 if w > 300 else 15))
        yy += lh
    sm = wrap(draw, summary, F_SERIF(12), w - 20)
    yy += 2
    if sm:
        text(draw, (x + 10, yy), sm[0], F_SERIF(12), (60, 60, 60))
    text(draw, (x + 10, y + h - 16), source, F_SANS(9), GREY)


# ---- illustrations (flat vector shapes) ----
def ill_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 60))
    for bx, bw, bh in [(8, 34, 30), (52, 26, 42), (88, 40, 26), (140, 30, 38),
                       (180, 36, 30), (226, 28, 44), (264, 34, 28)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(8, 12, 32))
        for wy in range(y + h - bh + 6, y + h - 4, 10):
            for wx in range(x + bx + 5, x + bx + bw - 4, 10):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 220, 90))
    for sx, sy in [(30, 12), (120, 8), (200, 14), (280, 10)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=WHITE)
    cx, cy = x + w - 46, y + 22
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 140, 30))
    for ang in range(0, 360, 45):
        import math
        ex = cx + 20 * math.cos(math.radians(ang))
        ey = cy + 20 * math.sin(math.radians(ang))
        d.line([cx, cy, ex, ey], fill=(255, 180, 60), width=3)
    d.ellipse([x + 60, y + 10, x + 76, y + 16], fill=(180, 180, 180))
    d.line([x + 68, y + 16, x + 68, y + 24], fill=(180, 180, 180), width=2)
    d.line([x + 60, y + 20, x + 76, y + 20], fill=(180, 180, 180), width=2)


def ill_kryvyi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 70, 40))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(60, 35, 20))
    for cx, cy, r in [(70, 30, 20), (230, 26, 24)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(255, 170, 40))
        d.ellipse([x + cx - r // 2, y + cy - r // 2, x + cx + r // 2,
                   y + cy + r // 2], fill=(255, 230, 120))
    for cx, cy, r in [(110, 16, 12), (190, 12, 14), (270, 18, 10)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(90, 90, 90))


def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(170, 210, 235))
    d.ellipse([x + 18, y + 8, x + 66, y + 56], fill=(60, 160, 90))
    d.ellipse([x + 30, y + 18, x + 44, y + 30], fill=(40, 120, 70))
    d.ellipse([x + 44, y + 34, x + 58, y + 48], fill=(40, 120, 70))
    d.rectangle([x + 150, y + 30, x + 280, y + h - 4], fill=(240, 240, 235))
    d.polygon([(x + 140, y + 32), (x + 215, y + 10), (x + 290, y + 32)],
              fill=(190, 40, 40))
    for wx in range(x + 162, x + 272, 18):
        d.rectangle([wx, y + 40, wx + 10, y + 52], fill=(40, 70, 110))
    d.ellipse([x + w - 34, y + 8, x + w - 8, y + 34], fill=(255, 220, 90))


def ill_mexico(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 200, 140))
    d.ellipse([x + w - 50, y + 8, x + w - 18, y + 40], fill=(255, 180, 60))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(200, 140, 70))
    d.rectangle([x + 30, y + 18, x + 40, y + h - 14], fill=(40, 130, 60))
    d.rectangle([x + 18, y + 30, x + 30, y + 38], fill=(40, 130, 60))
    d.rectangle([x + 40, y + 26, x + 54, y + 34], fill=(40, 130, 60))
    cx, cy = x + 150, y + 30
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(212, 175, 55),
              outline=(150, 110, 20), width=2)
    d.text((cx, cy), "*", font=F_SANS_B(20), fill=(150, 110, 20), anchor="mm")


def ill_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(180, 215, 240))
    d.polygon([(x + 10, y + h), (x + 80, y + 12), (x + 150, y + h)],
              fill=(120, 90, 70))
    d.polygon([(x + 70, y + 12), (x + 80, y + 12), (x + 88, y + 24),
               (x + 72, y + 24)], fill=WHITE)
    d.polygon([(x + 120, y + h), (x + 180, y + 22), (x + 235, y + h)],
              fill=(100, 75, 60))
    d.rectangle([x + 8, y + h - 26, x + w - 8, y + h - 8], fill=WHITE,
                outline=(150, 150, 150))
    pts = []
    for i, v in enumerate([0, -8, 6, -12, 10, -6, 4, 0]):
        pts.append((x + 14 + i * 28, y + h - 17 + v))
    d.line(pts, fill=(200, 30, 30), width=3)


def ill_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 150, 80))
    d.rectangle([x, y + 34, x + w, y + h], fill=(60, 30, 70))
    d.ellipse([x + w - 40, y + 6, x + w - 14, y + 32], fill=(255, 230, 140))
    for bx, bw, bh in [(10, 26, 26), (44, 20, 36), (72, 30, 22),
                       (110, 24, 32), (142, 28, 24), (178, 22, 30)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(25, 12, 35))
    d.rounded_rectangle([x + 88, y + h - 22, x + 150, y + h - 6], radius=6,
                        fill=(230, 230, 230))
    d.ellipse([x + 96, y + h - 18, x + 104, y + h - 10], fill=(40, 40, 40))
    d.ellipse([x + 134, y + h - 18, x + 142, y + h - 10], fill=(200, 40, 40))


def ill_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 12, 35))
    for sx, sy in [(20, 10), (60, 22), (180, 8), (220, 18)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=WHITE)
    d.ellipse([x + 30, y + 14, x + 210, y + h - 6], outline=(150, 150, 180),
              width=2)
    cx, cy, r = x + 120, y + h // 2 + 2, 22
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 140, 110))
    d.ellipse([cx - 8, cy - 6, cx + 2, cy + 4], fill=(140, 110, 85))
    d.ellipse([cx + 8, cy + 6, cx + 16, cy + 14], fill=(140, 110, 85))
    d.rectangle([x + 196, y + 12, x + 214, y + 20], fill=(200, 200, 210))
    d.polygon([(x + 214, y + 12), (x + 224, y + 16), (x + 214, y + 20)],
              fill=(255, 200, 60))


def ill_riemann(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 80, 50))
    d.rectangle([x + 6, y + 6, x + w - 6, y + h - 6], outline=(120, 100, 60),
                width=2)
    text(d, (x + 18, y + 5), "\u03b6(s) = 0", F_SERIF_B(18), WHITE)
    text(d, (x + 18, y + 25), "Re(s) = \u00bd", F_SERIF(13), (220, 220, 200))
    d.line([(x + w - 66, y + 14), (x + w - 46, y + 34), (x + w - 14, y + 6)],
           fill=(80, 220, 120), width=4)


def ill_basra(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(170, 170, 165))
    for tx in [30, 120]:
        d.polygon([(x + tx, y + h), (x + tx + 14, y + 14),
                   (x + tx + 46, y + 14), (x + tx + 60, y + h)],
                  fill=(120, 120, 115))
    for fx, fy in [(60, 30), (150, 26), (200, 34)]:
        d.ellipse([x + fx - 10, y + fy - 10, x + fx + 10, y + fy + 10],
                  fill=(255, 140, 30))
        d.ellipse([x + fx - 5, y + fy - 5, x + fx + 5, y + fy + 5],
                  fill=(255, 220, 100))
    d.ellipse([x + w - 40, y + 8, x + w - 16, y + 32], fill=(100, 100, 100))


def ill_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 45))
    for sx, sy in [(24, 12), (90, 8), (160, 14), (210, 10)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=WHITE)
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(5, 8, 25))
    for x0, y0, x1, y1 in [(30, 44, 90, 10), (90, 46, 150, 12),
                          (150, 44, 205, 10)]:
        d.line([x + x0, y + y0, x + x1, y + y1], fill=(255, 150, 50), width=3)
    cx, cy = x + 150, y + 14
    d.ellipse([cx - 10, cy - 8, cx + 10, cy + 8], fill=(255, 230, 120))
    for ang in range(0, 360, 45):
        import math
        ex = cx + 16 * math.cos(math.radians(ang))
        ey = cy + 16 * math.sin(math.radians(ang))
        d.line([cx, cy, ex, ey], fill=(255, 220, 100), width=2)


def ill_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(180, 175, 165))
    for bx, bw, bh in [(12, 40, 34), (60, 34, 44), (102, 44, 30),
                       (154, 36, 40), (198, 40, 32)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(110, 105, 100))
    for cx, cy, r in [(70, 14, 12), (150, 10, 14), (210, 16, 10)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(120, 120, 120))
    d.rounded_rectangle([x + 90, y + h - 18, x + 150, y + h - 6], radius=3,
                        fill=(255, 140, 40))
    d.rectangle([x + 118, y + h - 16, x + 132, y + h - 8], fill=(200, 230, 255))


def draw_map(d, x, y, w, h, pins):
    d.rectangle([x, y, x + w, y + h], fill=CREAM)
    # land as ellipses per continent (map coords relative to x,y)
    land = [
        (0.02, 0.05, 0.30, 0.45),   # N America
        (0.10, 0.55, 0.22, 0.40),   # S America
        (0.46, 0.05, 0.10, 0.22),   # Europe
        (0.47, 0.28, 0.14, 0.38),   # Africa
        (0.58, 0.05, 0.34, 0.42),   # Asia
        (0.82, 0.62, 0.12, 0.22),   # Australia
    ]
    dot_r = 2
    step = 8
    for gy in range(y + 4, y + h - 4, step):
        for gx in range(x + 4, x + w - 4, step):
            rx = (gx - x) / w
            ry = (gy - y) / h
            inside = False
            for (lx, ly, lw, lh) in land:
                cx, cy = lx + lw / 2, ly + lh / 2
                if ((rx - cx) / (lw / 2)) ** 2 + ((ry - cy) / (lh / 2)) ** 2 <= 1:
                    inside = True
                    break
            if inside:
                d.ellipse([gx - dot_r, gy - dot_r, gx + dot_r, gy + dot_r],
                          fill=(40, 60, 110))
    for (num, fx, fy) in pins:
        px, py = x + int(fx * w), y + int(fy * h)
        r = 9
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=WHITE, width=1)
        text(d, (px, py), str(num), F_SANS_B(11), WHITE, anchor="mm")


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(outdir, exist_ok=True)
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 100], fill=NAVY)
    d.rectangle([10, 10, 92, 90], fill=RED)
    text(d, (51, 22), "NOV", F_SANS_B(22), WHITE, anchor="ma")
    text(d, (51, 46), "21", F_SERIF_B(30), WHITE, anchor="ma")
    text(d, (51, 76), "SAT", F_SANS_B(14), WHITE, anchor="ma")
    text(d, (512, 14), "THE DAY IN WORLD NEWS", F_SANS_B(15), GOLD,
         anchor="ma")
    text(d, (512, 34), "Saturday 21 November 2026", F_SERIF_B(40), WHITE,
         anchor="ma")
    text(d, (1014, 20), "19 STORIES", F_SANS_B(14), WHITE, anchor="ra")
    text(d, (1014, 40), "4 CONTINENTS", F_SANS_B(14), WHITE, anchor="ra")
    text(d, (1014, 60), "ONE PAGE", F_SANS_B(14), GOLD, anchor="ra")
    text(d, (512, 108),
         "Everything on this page happened, or was first reported, on "
         "Saturday 21 November 2026.", F_SERIF_I(15), (70, 70, 70),
         anchor="ma")

    cards = [
        # num, cat, color, headline, summary, source, ill, row, col, span
        (1, "DRONE STRIKE", RED, "Drones strike Kyiv overnight",
         "Two hurt; water cut in five districts.",
         "KYIV24 \u00b7 KLITSCHKO", ill_kyiv, 0, 0, 1),
        (2, "MISSILE", (200, 110, 20), "Double-tap strike kills 2",
         "Boy, 7, and a paramedic, 20, die; 60 wounded.", "AP",
         ill_kryvyi, 0, 1, 1),
        (3, "CLIMATE", (40, 130, 90), "Antalya talks run past deadline",
         "No deal yet; draft strips fossil fuels, $120bn aid.",
         "REUTERS \u00b7 AP", ill_cop31, 0, 2, 1),
        (4, "CARTEL", (150, 100, 30), "'El Chapo Isidro' captured",
         "Seized in Sinaloa; 11 killed.",
         "REUTERS \u00b7 AP \u00b7 CNN \u00b7 WSJ", ill_mexico, 1, 0, 1),
        (5, "QUAKE", (120, 60, 160), "M6.7 quake hits Jun\u00edn",
         "Felt in Lima; depth 108 km.", "USGS",
         ill_peru, 1, 1, 1),
        (6, "GAMES", (140, 40, 140), "GTA VI: $3.79bn day one",
         "32.5m copies; biggest launch ever.", "TAKE-TWO",
         ill_gta, 1, 2, 1),
        (7, "SPACE", (30, 60, 140), "Into orbit after 8 years",
         "Probe arrives after 8 years.", "ESA \u00b7 NATURE",
         ill_mercury, 1, 3, 1),
        (8, "MATHS", (30, 120, 70), "'The proof checks out'",
         "Lean verifies the Riemann claim.", "WSJ",
         ill_riemann, 2, 0, 1),
        (9, "FIRE", (200, 90, 20), "Power station fire kills 4",
         "Hartha plant blaze; 30 hurt.", "REUTERS",
         ill_basra, 2, 1, 1),
        (10, "DEFENCE", (30, 70, 150), "Houthis fire 3 missiles at Riyadh",
         "All intercepted; second attack.", "REUTERS", ill_riyadh,
         2, 2, 1),
        (11, "WAR", RED, "Israeli strike kills 4 in Gaza City",
         "Three die in a food-aid van.",
         "REUTERS \u00b7 AFP", ill_gaza, 2, 3, 1),
    ]
    # row geometry: row1 y=135 h=150 (3 cols), rows 2-3 y=295/455 h=150 (4 cols)
    rows = [(135, 150, 3), (295, 150, 4), (455, 150, 4)]
    for (num, cat, col, hl, sm, src, ill, row, cidx, span) in cards:
        ry, rh, ncols = rows[row]
        gap = 10
        cw = (W - 20 - gap * (ncols - 1)) // ncols
        cx = 10 + cidx * (cw + gap)
        draw_card(d, cx, ry, cw, rh, num, cat, col, hl, sm, src, ill)

    # bottom: map left, briefs right
    by = 620
    text(d, (10, by), "WHERE IT HAPPENED", F_SANS_B(15), INK)
    pins = [(1, 0.48, 0.10), (2, 0.52, 0.20), (3, 0.55, 0.32),
            (4, 0.08, 0.38), (5, 0.18, 0.68), (6, 0.24, 0.26),
            (9, 0.64, 0.28), (10, 0.60, 0.48), (11, 0.52, 0.44)]
    draw_map(d, 10, by + 22, 480, 170, pins)
    text(d, (10, by + 196),
         "1 KYIV \u00b7 2 KRYVYI RIH \u00b7 3 ANTALYA \u00b7 4 GUASAVE \u00b7 "
         "5 JUN\u00cdN", F_SANS(10), GREY)
    text(d, (10, by + 210),
         "6 NEW YORK \u00b7 9 BASRA \u00b7 10 RIYADH \u00b7 11 GAZA",
         F_SANS(10), GREY)

    bx = 510
    text(d, (bx, by), "ALSO ON SATURDAY 21 NOVEMBER", F_SANS_B(15), INK)
    briefs = [
        (12, "Protests sweep 25+ nations", "Day of action continues; Italy strike.", "CNN"),
        (13, "Mosquitoes cut dengue 69%", "Wolbachia trial in Brazil, 5,700 kids.", "AP"),
        (14, "Trade deal after 10 years", "Brussels pact cuts tariffs; from 2027.", "REUTERS"),
        (15, "'Killer robot' talks stall", "No UN binding rules; talks go on.", "AP \u00b7 NPR"),
        (16, "New poll: PP 0.9 pts ahead", "Right leads before Nov 29 election.", "MORE IN COMMON"),
        (17, "No shift in US military ties", "Ottawa rejects rift after Hegseth memo.", "REUTERS"),
        (18, "M3.3 quake off San Pedro", "538 felt reports off San Pedro.", "USGS"),
        (19, "Russian cargo ship ablaze", "Sparta 2 hit by drones off Finland.", "NY POST \u00b7 REUTERS"),
    ]
    # two columns of briefs
    col_w = 245
    for i, (num, hl, sm, src) in enumerate(briefs):
        col = i % 2
        row = i // 2
        x = bx + col * (col_w + 10)
        y = by + 24 + row * 48
        text(d, (x, y), str(num), F_SANS_B(13), RED)
        bhl = wrap(d, hl, F_SERIF_B(13), col_w - 24)
        yy = y
        for ln in bhl[:1]:
            text(d, (x + 22, yy), ln, F_SERIF_B(13))
            yy += 16
        text(d, (x + 22, yy), sm, F_SERIF(11), (60, 60, 60))
        text(d, (x + 22, yy + 14), src, F_SANS(9), GREY)

    # date check strip
    sy = 852
    d.rectangle([10, sy, W - 10, sy + 44], outline=RED, width=2)
    dc = ("DATE CHECK \u2014 NOT 21 NOVEMBER:  Friday's market crash "
          "(S&P \u22123.7%) \u00b7 Kyiv bridge barrage \u00b7 Bayer $7.25bn "
          "deal \u00b7 FBI/USDA hack \u00b7 Rinderknecht verdict \u00b7 "
          "Myanmar ICJ ruling (19 Nov) \u00b7 UK drones (19 Nov) \u2014 all "
          "20 Nov or earlier.")
    dcl = wrap(d, dc, F_SANS(12), W - 40)
    yy = sy + 6
    for ln in dcl[:2]:
        text(d, (20, yy), ln, F_SANS(12))
        yy += 16

    # footer
    text(d, (512, 908),
         "All 19 stories happened, or were first reported, on Saturday "
         "21 November 2026. Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 CNN "
         "\u00b7 USGS \u00b7 ESA \u00b7 Take-Two \u00b7 Kyiv24. Original "
         "drawings.", F_SANS(10), GREY, anchor="ma")
    text(d, (512, 924),
         "SATURDAY 21 NOVEMBER 2026 \u00b7 THE DAY IN WORLD NEWS",
         F_SANS_B(10), GREY, anchor="ma")

    img.save(os.path.join(outdir, "entry.png"), "PNG")
    print("wrote", os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    main()
