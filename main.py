#!/usr/bin/env python3
"""news-image-20261121 — 'The World in One Image: Saturday 21 November 2026'.

Draws a 1024x1024 PNG news summary following the winning 19 Nov formula:
dotted world map with numbered location pins, two-column brief list,
bold serif headlines, and a DATE CHECK strip excluding other days' stories.
Stdlib + Pillow only. No network. Deterministic output.
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---- colours ----
PAPER = (251, 249, 244)
NAVY = (15, 42, 68)
INK = (30, 41, 59)
GREY = (100, 116, 139)
RED = (200, 16, 46)
GOLD = (180, 130, 20)
DOT = (71, 85, 105)
MAP_BG = (255, 255, 255)
MAP_BORDER = (203, 213, 225)
AMBER_BG = (255, 247, 237)
AMBER_BORDER = (245, 158, 11)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels, returning list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---- dotted world map landmask ----
# Grid: 96 cols (lon -180..180, 3.75 deg each) x 36 rows (lat 75..-60, 3.75 deg).
# Each entry: row -> list of (col_start, col_end) inclusive land ranges.
LAND = {
    0: [(16, 27), (32, 42), (64, 95)],
    1: [(3, 41), (52, 95)],
    2: [(3, 35), (42, 44), (49, 95)],
    3: [(3, 35), (46, 95)],
    4: [(13, 33), (46, 95)],
    5: [(13, 33), (45, 95)],
    6: [(14, 33), (45, 95)],
    7: [(14, 30), (45, 86)],
    8: [(14, 30), (45, 86)],
    9: [(16, 29), (45, 85)],
    10: [(16, 28), (45, 85)],
    11: [(16, 28), (45, 80)],
    12: [(17, 26), (45, 80)],
    13: [(20, 24), (43, 76), (80, 80)],
    14: [(22, 25), (43, 76), (80, 80)],
    15: [(23, 25), (43, 60), (68, 69), (73, 76)],
    16: [(25, 26), (43, 61), (74, 76)],
    17: [(26, 32), (44, 59), (69, 69)],
    18: [(27, 34), (45, 59), (73, 80)],
    19: [(27, 36), (45, 59), (73, 85)],
    20: [(27, 38), (45, 58), (74, 80), (82, 85)],
    21: [(28, 38), (45, 58), (76, 80), (82, 85)],
    22: [(29, 38), (50, 61), (77, 85)],
    23: [(29, 38), (51, 61), (82, 85)],
    24: [(29, 37), (51, 57), (59, 61), (80, 88)],
    25: [(29, 37), (51, 56), (59, 60), (78, 88)],
    26: [(29, 36), (51, 56), (78, 88)],
    27: [(29, 35), (52, 56), (78, 88)],
    28: [(29, 34), (52, 56), (78, 88)],
    29: [(29, 33), (52, 55), (78, 88), (94, 95)],
    30: [(29, 32), (85, 88), (92, 95)],
    31: [(29, 31), (92, 94)],
    32: [(29, 30)],
    33: [(29, 30)],
    34: [(29, 30)],
    35: [(29, 30)],
}

# ---- map geometry ----
MAP_L, MAP_T, MAP_W, MAP_H = 20, 190, 984, 330
LAT_TOP, LAT_BOT = 75.0, -60.0


def lonlat_to_xy(lon, lat):
    x = MAP_L + (lon + 180.0) / 360.0 * MAP_W
    y = MAP_T + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
    return x, y


# ---- stories: (num, headline, summary, lon, lat, pin_dx, pin_dy) ----
# pin_dx/pin_dy shift the numbered pin away from the true spot (leader line drawn).
STORIES = [
    (1, "KYIV", "Drones strike Kyiv overnight",
     "Two hurt, one in hospital; water cut in five districts.",
     30.5, 50.5, 0, 0),
    (2, "KRYVYI RIH", "Double-tap strike kills 2",
     "Boy, 7, and a paramedic, 20, die; 60 wounded.",
     33.4, 47.9, 19, 14),
    (3, "COP31", "Antalya talks run past deadline",
     "No deal yet; draft strips fossil fuels and $120bn aid.",
     30.7, 36.9, 0, 0),
    (4, "MEXICO", "'El Chapo Isidro' captured",
     "FBI Top 10 fugitive seized in Sinaloa; 11 killed.",
     -108.5, 25.6, 0, 0),
    (5, "PERU", "M6.7 quake hits Junin",
     "Felt in Lima; no casualties reported. Depth 108 km.",
     -75.5, -11.2, 0, 0),
    (6, "GTA VI", "$3.79bn day one, 32.5m copies",
     "Biggest entertainment launch ever, says Take-Two.",
     -74.0, 40.7, 0, 0),
    (7, "MERCURY", "Into orbit after 8 years",
     "ESA-JAXA probe arrives after 8 years, 10bn km.",
     None, None, 0, 0),
    (8, "RIEMANN", "'The proof checks out'",
     "Lean community verifies the Riemann claim on Saturday.",
     -122.4, 37.8, -17, -13),
    (9, "BASRA", "Power station fire kills 4",
     "Gas pipeline blaze halts Hartha plant; 30 injured.",
     47.8, 30.5, 15, -13),
    (10, "RIYADH", "Houthis fire 3 missiles at Riyadh",
     "All intercepted; second attack in days.",
     46.7, 24.6, 0, 0),
    (11, "GAZA", "Israeli strike kills 4 in Gaza City",
     "Three die in a food-aid van; one shot in Jabalia.",
     34.5, 31.5, 16, 14),
    (12, "GEN Z", "Protests sweep 25+ nations",
     "Day of action continues; Italy transport strike.",
     2.3, 48.9, -18, 12),
    (13, "DENGUE", "Mosquitoes cut dengue 69%",
     "Wolbachia trial, 5,700 children in Brazil; chikungunya too.",
     -43.9, -19.9, 0, 0),
    (14, "EU-INDONESIA", "Trade deal after 10 years",
     "Brussels pact cuts almost all tariffs; in force 2027.",
     4.4, 50.8, -16, -13),
    (15, "GENEVA", "'Killer robot' talks stall",
     "UN ends with no binding rules; two more years of talks.",
     6.1, 46.2, 11, 16),
    (16, "SPAIN", "New poll: PP 0.9 pts ahead",
     "Right leads before the Nov 29 snap election.",
     -3.7, 40.4, -16, 15),
    (17, "CANADA", "No shift in US military ties",
     "Ottawa rejects rift after Hegseth memo.",
     -75.7, 45.4, 17, -16),
    (18, "LOS ANGELES", "M3.3 quake off San Pedro",
     "538 felt reports; centred off San Pedro.",
     -118.3, 33.7, 0, 0),
    (19, "BALTIC", "Russian cargo ship ablaze",
     "Sparta 2 hit by drones in the Gulf of Finland.",
     24.0, 59.5, 0, 0),
]


def draw_star(d, cx, cy, r, colour):
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=colour)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header band ----
    d.rectangle([0, 0, W, 60], fill=NAVY)
    d.text((20, 12), "THE WORLD IN ONE IMAGE", font=F_SERIF_B(34), fill=(255, 255, 255))
    date_txt = "SATURDAY  21 NOVEMBER 2026"
    dw = d.textlength(date_txt, font=F_SANS_B(18))
    d.text((W - 20 - dw, 20), date_txt, font=F_SANS_B(18), fill=(255, 255, 255))

    # ---- lead headline ----
    d.text((20, 72), "KYIV HIT, \u2018EL CHAPO ISIDRO\u2019 FALLS,", font=F_SERIF_B(38), fill=NAVY)
    d.text((20, 114), "AND COP31 TALKS RUN INTO OVERTIME", font=F_SERIF_B(38), fill=NAVY)

    # ---- deck ----
    d.text((20, 158),
           "19 verified stories from Saturday 21 November 2026 \u2014 a Mercury arrival, a $3.79bn game launch, and a Riemann proof.",
           font=F_SANS(16), fill=GREY)

    # ---- map label ----
    d.text((20, 182), "W H E R E   I T   H A P P E N E D", font=F_SANS_B(13), fill=GREY)

    # ---- map panel ----
    d.rounded_rectangle([MAP_L - 8, MAP_T - 8, MAP_L + MAP_W + 8, MAP_T + MAP_H + 8],
                        radius=10, fill=MAP_BG, outline=MAP_BORDER, width=1)
    # dots
    cell_w = MAP_W / 96.0
    cell_h = MAP_H / 36.0
    for r, ranges in LAND.items():
        cy = MAP_T + (r + 0.5) * cell_h
        for (c0, c1) in ranges:
            for c in range(c0, c1 + 1):
                cx = MAP_L + (c + 0.5) * cell_w
                d.ellipse([cx - 2.3, cy - 2.3, cx + 2.3, cy + 2.3], fill=DOT)

    # pins
    f_pin = F_SANS_B(13)
    for (num, _loc, _hl, _sm, lon, lat, dx, dy) in STORIES:
        if lon is None:
            continue
        tx, ty = lonlat_to_xy(lon, lat)
        px, py = tx + dx, ty + dy
        if dx or dy:
            d.line([tx, ty, px, py], fill=RED, width=1)
            d.ellipse([tx - 2.5, ty - 2.5, tx + 2.5, ty + 2.5], fill=RED)
        d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=RED,
                  outline=(255, 255, 255), width=2)
        label = str(num)
        tw = d.textlength(label, font=f_pin)
        d.text((px - tw / 2, py - 8), label, font=f_pin, fill=(255, 255, 255))

    # Mercury (space) — star label in the empty South Pacific
    draw_star(d, 52, 398, 11, GOLD)
    d.text((70, 388), "7  MERCURY", font=F_SANS_B(15), fill=INK)
    d.text((70, 408), "orbit after 8 years", font=F_SANS(13), fill=GREY)

    # ---- brief list ----
    d.text((20, 534), "T H E   D A Y   I N   B R I E F", font=F_SANS_B(13), fill=GREY)
    d.line([20, 556, W - 20, 556], fill=MAP_BORDER, width=1)

    f_head = F_SERIF_B(18)
    f_sum = F_SANS(14)
    f_num = F_SANS_B(18)
    col_w = 480
    col_x = [20, 524]
    row_y = 566
    row_h = 39
    for i, (num, loc, hl, sm, _lon, _lat, _dx, _dy) in enumerate(STORIES):
        col = 0 if i < 10 else 1
        idx = i if i < 10 else i - 10
        x = col_x[col]
        y = row_y + idx * row_h
        # number
        d.text((x, y), str(num), font=f_num, fill=RED)
        nx = x + (28 if num < 10 else 34)
        # headline: LOC — headline (must fit on ONE line)
        head = "%s \u2014 %s" % (loc, hl)
        lines = wrap(d, head, f_head, col_w - (nx - x))
        if len(lines) > 1:
            print("WARN headline wraps:", num, head)
        d.text((nx, y), lines[0], font=f_head, fill=INK)
        # summary (one line, wrapped to fit)
        slines = wrap(d, sm, f_sum, col_w - (nx - x))
        if len(slines) > 1:
            print("WARN summary wraps:", num, sm)
        d.text((nx, y + 21), slines[0], font=f_sum, fill=GREY)

    # ---- date check strip ----
    box_y0, box_y1 = 958, 1016
    d.rounded_rectangle([20, box_y0, W - 20, box_y1], radius=8,
                        fill=AMBER_BG, outline=AMBER_BORDER, width=1)
    d.text((34, box_y0 + 6), "DATE CHECK \u2014 SATURDAY 21 NOVEMBER ONLY",
           font=F_SANS_B(14), fill=RED)
    d.text((34, box_y0 + 25),
           "NOT INCLUDED: Friday\u2019s market crash (S&P \u22123.7%) \u00b7 Kyiv bridge barrage \u00b7 Bayer $7.25bn deal \u00b7 FBI/USDA hack",
           font=F_SANS(13), fill=INK)
    d.text((34, box_y0 + 41),
           "Zecler verdict \u00b7 Gupta sentence \u00b7 Myanmar ICJ ruling (19 Nov) \u00b7 UK drones (19 Nov) \u2014 all 20 Nov or earlier.",
           font=F_SANS(13), fill=INK)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
