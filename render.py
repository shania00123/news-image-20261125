#!/usr/bin/env python3
"""Draw the 25 November 2026 full-day news front page.

The renderer is deterministic: fixed story data, fixed drawing coordinates,
no clock, no randomness, no network. It writes poster.png beside this file.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W = H = 1024
OUT = Path(__file__).resolve().with_name("poster.png")

CREAM = (244, 239, 227)
PAPER = (251, 248, 240)
INK = (20, 33, 61)
NAVY = (16, 42, 78)
RED = (178, 43, 43)
TEAL = (18, 116, 118)
GOLD = (201, 154, 52)
SKY = (154, 197, 214)
SEA = (35, 102, 141)
LAND = (222, 205, 164)
MUTED = (91, 101, 117)
LIGHT_LINE = (205, 196, 178)
WHITE = (255, 255, 255)
BLACK = (12, 16, 24)

FONT_PATHS = {
    "serif_bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "sans_bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATHS[kind], size)


F = {
    "mast": font("serif_bold", 57),
    "sub": font("sans_bold", 19),
    "kicker": font("sans_bold", 12),
    "badge": font("sans_bold", 15),
    "num_value": font("sans_bold", 25),
    "num_label": font("sans_bold", 10),
    "region": font("sans_bold", 13),
    "hero_head": font("serif_bold", 29),
    "hero_sub": font("sans", 15),
    "card_head": font("serif_bold", 21),
    "card_sub": font("sans", 13),
    "panel_title": font("sans_bold", 15),
    "small": font("sans", 12),
    "tiny": font("sans", 11),
    "tiny_bold": font("sans_bold", 11),
    "market": font("sans_bold", 15),
    "footer": font("sans", 10),
}


def text_w(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def draw_center(draw, cx, y, text, fnt, fill):
    draw.text((cx - text_w(draw, text, fnt) / 2, y), text, font=fnt, fill=fill)


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if text_w(draw, trial, fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, x, y, text, fnt, fill, max_width, leading=4, max_lines=None):
    lines = wrap(draw, text, fnt, max_width)
    if max_lines is not None:
        lines = lines[:max_lines]
    line_h = fnt.size + leading
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def panel(draw, box, fill=PAPER, outline=INK, width=2):
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=width)


def chip(draw, x, y, text, fill=RED):
    w = text_w(draw, text, F["kicker"]) + 18
    draw.rounded_rectangle((x, y, x + w, y + 24), radius=6, fill=fill)
    draw.text((x + 9, y + 5), text, font=F["kicker"], fill=WHITE)
    return w


def dashed_line(draw, start, end, fill, width=3, dash=12, gap=8):
    x1, y1 = start
    x2, y2 = end
    length = max(abs(x2 - x1), abs(y2 - y1))
    if length == 0:
        return
    steps = int(length // (dash + gap)) + 1
    for i in range(steps + 1):
        t1 = min(1, (i * (dash + gap)) / length)
        t2 = min(1, (i * (dash + gap) + dash) / length)
        draw.line(
            (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1, x1 + (x2 - x1) * t2, y1 + (y2 - y1) * t2),
            fill=fill,
            width=width,
        )


def star(draw, cx, cy, r1, r2, fill):
    offsets = [
        (1, 0), (0.72, 0.28), (0.42, 0.72), (0.15, 0.98),
        (-0.15, 0.98), (-0.42, 0.72), (-0.72, 0.28), (-1, 0),
        (-0.72, -0.28), (-0.42, -0.72), (-0.15, -0.98), (0.15, -0.98),
        (0.42, -0.72), (0.72, -0.28),
    ]
    pts = []
    for i, (ox, oy) in enumerate(offsets):
        r = r1 if i % 2 == 0 else r2
        pts.append((cx + ox * r, cy + oy * r))
    draw.polygon(pts, fill=fill)


def mine(draw, cx, cy, r=13):
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=BLACK)
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0), (1, -1), (-1, 1), (1, 1), (-1, -1)]:
        draw.line((cx, cy, cx + dx * (r + 8), cy + dy * (r + 8)), fill=BLACK, width=4)
    draw.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=(210, 210, 210))


def tanker(draw, x, y, scale=1.0):
    hull = [(x, y), (x + 250 * scale, y), (x + 225 * scale, y + 38 * scale), (x + 28 * scale, y + 38 * scale)]
    draw.polygon(hull, fill=(28, 35, 48))
    draw.rectangle((x + 28 * scale, y - 28 * scale, x + 190 * scale, y), fill=(238, 238, 232), outline=BLACK, width=2)
    for i in range(5):
        cx = x + (48 + i * 28) * scale
        draw.rectangle((cx, y - 22 * scale, cx + 18 * scale, y - 6 * scale), fill=[RED, GOLD, TEAL, NAVY, (120, 120, 120)][i])
    draw.rectangle((x + 205 * scale, y - 58 * scale, x + 238 * scale, y), fill=(245, 245, 240), outline=BLACK, width=2)
    draw.rectangle((x + 212 * scale, y - 50 * scale, x + 231 * scale, y - 38 * scale), fill=SKY)
    draw.line((x + 20 * scale, y + 45 * scale, x + 255 * scale, y + 45 * scale), fill=WHITE, width=3)


def drone(draw, cx, cy, s=1.0, fill=BLACK):
    draw.ellipse((cx - 13 * s, cy - 5 * s, cx + 13 * s, cy + 5 * s), fill=fill)
    draw.line((cx - 24 * s, cy - 10 * s, cx + 24 * s, cy + 10 * s), fill=fill, width=max(2, int(3 * s)))
    draw.line((cx - 24 * s, cy + 10 * s, cx + 24 * s, cy - 10 * s), fill=fill, width=max(2, int(3 * s)))
    for dx, dy in [(-24, -10), (24, -10), (-24, 10), (24, 10)]:
        draw.ellipse((cx + (dx - 5) * s, cy + (dy - 3) * s, cx + (dx + 5) * s, cy + (dy + 3) * s), outline=fill, width=2)


def draw_header(draw):
    draw.rectangle((0, 0, W, H), fill=CREAM)
    draw.rectangle((14, 14, W - 14, H - 14), outline=INK, width=3)
    draw.line((28, 104, W - 28, 104), fill=RED, width=4)
    draw.text((30, 28), "WORLD NEWS - ONE DAY", font=F["kicker"], fill=RED)
    draw_center(draw, W / 2, 20, "THE DAY IN FULL", F["mast"], INK)
    draw_center(draw, W / 2, 78, "Wednesday 25 November 2026 - verified to 14:10 UTC", F["sub"], INK)
    draw.rounded_rectangle((856, 30, 994, 66), radius=8, fill=RED)
    draw_center(draw, 925, 39, "38 STORIES", F["badge"], WHITE)


def draw_number_strip(draw):
    box = (28, 114, 996, 168)
    draw.rounded_rectangle(box, radius=8, fill=NAVY)
    stats = [
        ("+4.3%", "US GDP Q3"),
        ("3.8%", "US PCE Y/Y"),
        ("189k", "US JOBLESS CLAIMS"),
        ("4.9%", "AUSTRALIA CPI"),
        ("145", "DRONES DOWNED (SAMARA)"),
        ("03:56", "TIANGONG DOCK UTC"),
    ]
    cell_w = (box[2] - box[0]) / len(stats)
    for i, (value, label) in enumerate(stats):
        x = box[0] + i * cell_w
        if i:
            draw.line((x, box[1] + 8, x, box[3] - 8), fill=(80, 105, 145), width=2)
        draw_center(draw, x + cell_w / 2, box[1] + 5, value, F["num_value"], WHITE)
        label_font = F["num_label"] if text_w(draw, label, F["num_label"]) <= cell_w - 8 else font("sans_bold", 8)
        draw_center(draw, x + cell_w / 2, box[1] + 36, label, label_font, (205, 220, 240))


def draw_region_bar(draw):
    regions = [
        ("AMERICAS 12", NAVY),
        ("EUROPE 11", TEAL),
        ("ASIA-PACIFIC 11", GOLD),
        ("MIDDLE EAST 3", RED),
        ("AFRICA 1", (96, 74, 140)),
    ]
    x = 28
    y = 176
    w = 968 / len(regions)
    for label, color in regions:
        draw.rectangle((x, y, x + w - 4, y + 28), fill=color)
        draw_center(draw, x + (w - 4) / 2, y + 6, label, F["region"], WHITE)
        x += w


def draw_hormuz(draw):
    box = (28, 212, 528, 500)
    panel(draw, box, fill=SEA)
    x1, y1, x2, y2 = box
    for i in range(7):
        yy = y1 + i * 28
        draw.rectangle((x1 + 2, yy, x2 - 2, yy + 14), fill=(45, 116, 154) if i % 2 else SEA)
    draw.polygon([(x1, y1), (x1 + 170, y1), (x1 + 120, y1 + 58), (x1, y1 + 82)], fill=LAND)
    draw.polygon([(x2, y1), (x2 - 150, y1), (x2 - 105, y1 + 64), (x2, y1 + 92)], fill=LAND)
    draw.polygon([(x1, y1 + 150), (x1 + 105, y1 + 132), (x1 + 150, y1 + 190), (x1, y1 + 205)], fill=(205, 188, 142))
    dashed_line(draw, (x1 + 55, y1 + 150), (x2 - 55, y1 + 105), WHITE, width=3)
    tanker(draw, x1 + 105, y1 + 112, 1.05)
    mine(draw, x1 + 405, y1 + 154, 14)
    mine(draw, x1 + 92, y1 + 176, 11)
    star(draw, x1 + 392, y1 + 132, 42, 18, (240, 140, 40))
    star(draw, x1 + 392, y1 + 132, 24, 10, (250, 205, 70))
    draw.line((x1 + 350, y1 + 160, x1 + 392, y1 + 132), fill=(250, 205, 70), width=5)
    chip(draw, x1 + 14, y1 + 14, "1  MIDDLE EAST")
    draw.rectangle((x1 + 2, y2 - 96, x2 - 2, y2 - 2), fill=PAPER)
    draw.text((x1 + 16, y2 - 88), "TANKERS HIT MINES IN HORMUZ", font=font("serif_bold", 24), fill=INK)
    draw_wrapped(
        draw,
        x1 + 16,
        y2 - 52,
        "Iran says two ships caught fire; Tehran warns vessels to coordinate passage.",
        F["hero_sub"],
        MUTED,
        468,
        leading=3,
        max_lines=2,
    )


def draw_shenzhou(draw):
    box = (544, 212, 996, 500)
    panel(draw, box, fill=(8, 18, 42))
    x1, y1, x2, y2 = box
    for i in range(46):
        sx = x1 + 18 + ((i * 83) % 410)
        sy = y1 + 14 + ((i * 47) % 150)
        r = 2 if i % 5 else 3
        draw.ellipse((sx - r, sy - r, sx + r, sy + r), fill=WHITE)
    draw.pieslice((x1 + 18, y1 + 118, x2 - 18, y1 + 262), start=180, end=360, fill=(34, 104, 160))
    draw.arc((x1 + 18, y1 + 118, x2 - 18, y1 + 262), start=180, end=360, fill=SKY, width=5)
    draw.arc((x1 + 35, y1 + 25, x2 - 35, y1 + 205), start=190, end=345, fill=GOLD, width=3)
    sx, sy = x1 + 205, y1 + 82
    draw.rectangle((sx - 105, sy - 12, sx + 105, sy + 12), fill=(225, 230, 235), outline=WHITE, width=2)
    draw.rectangle((sx - 165, sy - 34, sx - 112, sy + 34), fill=(42, 92, 150), outline=SKY, width=2)
    draw.rectangle((sx + 112, sy - 34, sx + 165, sy + 34), fill=(42, 92, 150), outline=SKY, width=2)
    draw.rectangle((sx - 28, sy - 34, sx + 28, sy + 34), fill=(240, 240, 235), outline=WHITE, width=2)
    draw.ellipse((sx - 12, sy - 12, sx + 12, sy + 12), fill=SKY)
    cx, cy = x1 + 92, y1 + 142
    draw.ellipse((cx - 34, cy - 18, cx + 34, cy + 18), fill=(245, 245, 240), outline=WHITE, width=2)
    draw.polygon([(cx + 28, cy - 12), (cx + 58, cy), (cx + 28, cy + 12)], fill=GOLD)
    dashed_line(draw, (cx + 58, cy), (sx - 32, sy + 20), GOLD, width=3)
    chip(draw, x1 + 14, y1 + 14, "2  SPACE", fill=TEAL)
    draw.rectangle((x1 + 2, y2 - 96, x2 - 2, y2 - 2), fill=PAPER)
    draw.text((x1 + 16, y2 - 88), "FIRST PAKISTANI AT TIANGONG", font=font("serif_bold", 21), fill=INK)
    draw_wrapped(
        draw,
        x1 + 16,
        y2 - 52,
        "Shenzhou-24 docked 03:56 UTC; crew Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali.",
        F["hero_sub"],
        MUTED,
        420,
        leading=3,
        max_lines=2,
    )


def draw_card_base(draw, box, label, color):
    panel(draw, box, fill=PAPER)
    chip(draw, box[0] + 10, box[1] + 10, label, fill=color)


def draw_ukraine_card(draw):
    box = (28, 512, 340, 654)
    draw_card_base(draw, box, "3-4  EUROPE", RED)
    x1, y1, x2, y2 = box
    base = y1 + 84
    for i, h in enumerate([24, 36, 20, 42, 28, 34]):
        xx = x1 + 18 + i * 46
        draw.rectangle((xx, base - h, xx + 28, base), fill=(70, 78, 92))
        draw.rectangle((xx + 10, base - h - 10, xx + 18, base - h), fill=(50, 56, 70))
    star(draw, x1 + 238, y1 + 52, 20, 8, (240, 140, 40))
    drone(draw, x1 + 142, y1 + 46, 0.8)
    drone(draw, x1 + 190, y1 + 34, 0.65)
    drone(draw, x1 + 282, y1 + 40, 0.7)
    draw.text((x1 + 14, y1 + 86), "DRONES BOTH WAYS", font=F["card_head"], fill=INK)
    draw_wrapped(
        draw,
        x1 + 14,
        y1 + 110,
        "Samara: 1 dead, 145 downed. 5 regions lose power; Bila: 1 dead.",
        F["card_sub"],
        MUTED,
        284,
        leading=2,
        max_lines=2,
    )


def draw_us_card(draw):
    box = (356, 512, 668, 654)
    draw_card_base(draw, box, "8-11  AMERICAS", NAVY)
    x1, y1, x2, y2 = box
    chart_x, chart_y = x1 + 28, y1 + 78
    draw.line((chart_x, chart_y, chart_x + 230, chart_y), fill=INK, width=2)
    values = [(4.3, RED), (3.8, GOLD), (2.4, TEAL), (1.2, NAVY)]
    for i, (v, color) in enumerate(values):
        h = int(v * 11)
        xx = chart_x + 18 + i * 52
        draw.rectangle((xx, chart_y - h, xx + 32, chart_y), fill=color)
    draw.text((x1 + 14, y1 + 86), "GROWTH UP, PRICES STICKY", font=font("serif_bold", 17), fill=INK)
    draw_wrapped(
        draw,
        x1 + 14,
        y1 + 110,
        "GDP +4.3%; PCE +3.8% y/y; claims 189k; core capex +1.2%.",
        F["card_sub"],
        MUTED,
        284,
        leading=2,
        max_lines=2,
    )


def draw_solomons_card(draw):
    box = (684, 512, 996, 654)
    draw_card_base(draw, box, "7  ASIA-PACIFIC", TEAL)
    x1, y1, x2, y2 = box
    draw.rectangle((x1 + 12, y1 + 38, x2 - 12, y1 + 84), fill=SKY)
    for cx, cy, rx, ry in [(x1 + 70, y1 + 62, 34, 10), (x1 + 145, y1 + 55, 42, 12), (x1 + 225, y1 + 66, 30, 9), (x1 + 275, y1 + 50, 22, 8)]:
        draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(72, 145, 92), outline=(45, 100, 66), width=2)
    sx, sy = x1 + 252, y1 + 40
    draw.polygon([(sx, sy), (sx + 32, sy + 9), (sx + 32, sy + 30), (sx, sy + 42), (sx - 32, sy + 30), (sx - 32, sy + 9)], fill=NAVY, outline=WHITE)
    draw.line((sx - 13, sy + 21, sx - 4, sy + 30, sx + 15, sy + 11), fill=WHITE, width=4)
    draw.text((x1 + 14, y1 + 86), "SOLOMONS PACT SIGNED", font=font("serif_bold", 19), fill=INK)
    draw_wrapped(
        draw,
        x1 + 14,
        y1 + 110,
        "Australia named primary security partner; no foreign military base.",
        F["card_sub"],
        MUTED,
        284,
        leading=2,
        max_lines=2,
    )


def draw_timeline(draw):
    box = (28, 664, 996, 728)
    panel(draw, box, fill=PAPER)
    x1, y1, x2, y2 = box
    draw.text((x1 + 14, y1 + 24), "UTC TIMELINE", font=F["panel_title"], fill=INK)
    line_y = y1 + 38
    start_x, end_x = x1 + 150, x2 - 45
    draw.line((start_x, line_y, end_x, line_y), fill=INK, width=3)
    events = [
        (0.3, "00:18 launch\n00:30 Aus CPI", True),
        (3.93, "03:56 docking", False),
        (13.5, "13:30 data", False),
        (14.0, "14:00 chess", True),
    ]
    for hour, label, above in events:
        x = start_x + (hour / 14.17) * (end_x - start_x)
        scheduled = hour >= 15.0
        if scheduled:
            draw.ellipse((x - 7, line_y - 7, x + 7, line_y + 7), outline=RED, width=3, fill=PAPER)
        else:
            draw.ellipse((x - 7, line_y - 7, x + 7, line_y + 7), fill=RED, outline=WHITE, width=2)
        lines = label.split("\n")
        label_w = max(text_w(draw, line, F["tiny_bold"]) for line in lines)
        lx = min(max(x - label_w / 2, x1 + 145), x2 - label_w - 8)
        ly = y1 + 8 if above else y1 + 48
        for line in lines:
            draw.text((lx, ly), line, font=F["tiny_bold"], fill=INK)
            ly += 13


def draw_markets(draw):
    box = (28, 736, 996, 784)
    draw.rounded_rectangle(box, radius=8, fill=INK)
    x1, y1, x2, y2 = box
    draw.text((x1 + 16, y1 + 13), "MARKETS", font=F["panel_title"], fill=GOLD)
    draw.text((x1 + 118, y1 + 7), "24 Nov close: Dow +0.85%  -  S&P 500 -0.50%  -  Nasdaq -1.48%", font=F["market"], fill=WHITE)
    draw.text((x1 + 118, y1 + 28), "25 Nov: Nikkei -2.8%  -  KOSPI -6.2%  -  Nvidia premarket about -5%", font=F["market"], fill=(205, 220, 240))


def pin(draw, x, y, number, color=RED):
    draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=color, outline=WHITE, width=2)
    label = str(number)
    fnt = font("sans_bold", 9 if len(label) > 1 else 10)
    draw.text((x - text_w(draw, label, fnt) / 2, y - 6), label, font=fnt, fill=WHITE)


def draw_map(draw):
    box = (28, 792, 328, 1000)
    panel(draw, box, fill=(231, 240, 243))
    x1, y1, x2, y2 = box
    draw.text((x1 + 14, y1 + 10), "MAP PINS", font=F["panel_title"], fill=INK)
    draw.polygon([(x1 + 28, y1 + 58), (x1 + 86, y1 + 42), (x1 + 112, y1 + 66), (x1 + 88, y1 + 96), (x1 + 48, y1 + 92)], fill=LAND, outline=MUTED)
    draw.polygon([(x1 + 82, y1 + 104), (x1 + 112, y1 + 108), (x1 + 102, y1 + 150), (x1 + 78, y1 + 138)], fill=LAND, outline=MUTED)
    draw.polygon([(x1 + 142, y1 + 52), (x1 + 176, y1 + 44), (x1 + 190, y1 + 66), (x1 + 160, y1 + 78), (x1 + 140, y1 + 68)], fill=LAND, outline=MUTED)
    draw.polygon([(x1 + 154, y1 + 86), (x1 + 190, y1 + 82), (x1 + 198, y1 + 126), (x1 + 172, y1 + 150), (x1 + 150, y1 + 120)], fill=LAND, outline=MUTED)
    draw.polygon([(x1 + 190, y1 + 48), (x1 + 268, y1 + 42), (x1 + 282, y1 + 76), (x1 + 238, y1 + 104), (x1 + 202, y1 + 82)], fill=LAND, outline=MUTED)
    draw.polygon([(x1 + 244, y1 + 132), (x1 + 282, y1 + 128), (x1 + 288, y1 + 152), (x1 + 250, y1 + 158)], fill=LAND, outline=MUTED)
    pin(draw, x1 + 72, y1 + 70, 8, NAVY)
    pin(draw, x1 + 158, y1 + 58, 17, TEAL)
    pin(draw, x1 + 196, y1 + 52, 3, RED)
    pin(draw, x1 + 208, y1 + 78, 1, RED)
    pin(draw, x1 + 178, y1 + 90, 5, RED)
    pin(draw, x1 + 182, y1 + 112, 6, (96, 74, 140))
    pin(draw, x1 + 238, y1 + 94, 24, GOLD)
    pin(draw, x1 + 260, y1 + 98, 36, GOLD)
    pin(draw, x1 + 252, y1 + 34, 2, TEAL)
    pin(draw, x1 + 286, y1 + 136, 7, TEAL)
    pin(draw, x1 + 260, y1 + 150, 12, GOLD)
    draw.text((x1 + 14, y2 - 24), "Pins keyed to story numbers.", font=F["tiny"], fill=MUTED)


def draw_also(draw):
    box = (344, 792, 734, 1000)
    panel(draw, box, fill=PAPER)
    x1, y1, x2, y2 = box
    draw.text((x1 + 14, y1 + 10), "ALSO TODAY - 24 MORE", font=F["panel_title"], fill=INK)
    left = [
        "5 Gaza strike kills family",
        "6 Sudan: 19 reported dead",
        "13 Germany GDP +0.1%",
        "16 US proposes tariffs on 14",
        "18 Houthis claim Ras Tanura",
        "19 Pope: COP31 troubling",
        "20 Merz: Russia wants more",
        "21 Cartagena hostages freed",
        "22 Bogor mine: 3 bodies found",
        "23 MEPs debate EU budget box",
        "24 Bangladesh pay +36%",
        "25 UK energy cap +26% in Jan",
    ]
    right = [
        "26 EU proposes Quantum Act",
        "27 Sydney: guilty verdicts",
        "28 N Korea expels Swiss envoy",
        "29 Beijing backs Huawei",
        "30 easyJet profit falls 89%",
        "31 Deere Q4 profit $1.051bn",
        "32 Anmer: two charged",
        "33 Delhi court lists Das plea",
        "34 Thanksgiving rain, waivers",
        "36 Hong Kong seeks answers",
        "37 Ambarella -37.5%",
        "38 Workday -9% premarket",
    ]
    y = y1 + 36
    for item in left:
        draw.text((x1 + 14, y), item, font=F["tiny"], fill=INK)
        y += 14
    y = y1 + 36
    for item in right:
        draw.text((x1 + 202, y), item, font=F["tiny"], fill=INK)
        y += 14
    draw.line((x1 + 192, y1 + 36, x1 + 192, y2 - 14), fill=LIGHT_LINE, width=2)


def draw_date_check(draw):
    box = (750, 792, 996, 1000)
    panel(draw, box, fill=(255, 248, 230), outline=RED)
    x1, y1, x2, y2 = box
    draw.text((x1 + 14, y1 + 10), "DATE CHECK", font=F["panel_title"], fill=RED)
    items = [
        "Bank of Korea decision: 26 Nov - not counted.",
        "US close: not yet at 14:10 UTC; markets use 24 Nov close.",
        "Chess Game 2: began 14:00 UTC; no result yet.",
        "Huawei verdict: 24 Nov; only 25 Nov reactions counted.",
        "Sudan strikes: night of 24 Nov, reported 25 Nov.",
        "UNAIDS report: launched 24 Nov - excluded.",
    ]
    y = y1 + 34
    for item in items:
        draw.ellipse((x1 + 14, y + 5, x1 + 20, y + 11), fill=RED)
        y = draw_wrapped(draw, x1 + 26, y, item, F["tiny"], INK, 204, leading=1, max_lines=2)
        y += 3


def main() -> None:
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_number_strip(draw)
    draw_region_bar(draw)
    draw_hormuz(draw)
    draw_shenzhou(draw)
    draw_ukraine_card(draw)
    draw_us_card(draw)
    draw_solomons_card(draw)
    draw_timeline(draw)
    draw_markets(draw)
    draw_map(draw)
    draw_also(draw)
    draw_date_check(draw)
    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
