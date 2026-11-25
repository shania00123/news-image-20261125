#!/usr/bin/env python3
"""news-image-20261125 — THE WEDNESDAY LEDGER, morning edition.

Draws one 1024x1024 front page summing up the world's news of Wednesday
25 November 2026. Morning edition: every story verified against reporting
published on that day before ~09:30 WIB (02:30 UTC). Stories first
reported on Tuesday live only in the DATE CHECK box, never in the count.

Drawn entirely with PIL (stdlib + Pillow), no network at run time;
two runs write identical bytes.

Usage:  python3 render.py            # writes poster.png next to this file
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poster.png")

# ---- palette ------------------------------------------------------------
PAPER   = (247, 243, 232)   # newsprint cream
INK     = (26, 26, 26)
MUTED   = (96, 90, 78)
RULE    = (180, 172, 152)
RED     = (176, 32, 32)
NAVY    = (31, 58, 95)
NAVY_D  = (22, 42, 70)
GOLD    = (176, 132, 32)
GREEN   = (28, 110, 60)
SKY     = (168, 205, 228)
SEA     = (58, 110, 150)
CARD    = (255, 255, 255)
CARD_BG = (250, 247, 238)
GREY_BG = (232, 228, 216)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def f_serif(s):
    return font("DejaVuSerif-Bold.ttf", s)


def f_sans(s):
    return font("DejaVuSans.ttf", s)


def f_sans_b(s):
    return font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
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


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text, truncate to max_lines with an ellipsis if needed."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "…", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "…"
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines; returns y just below the last line."""
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# ---- the day's news (verified Wed 25 Nov 2026, before 02:30 UTC) ------
# kind: icon key for the small drawn thumb. pin: (lon, lat) for the map.

HEROES = [
    dict(num=1, place="JIUQUAN", kind="rocket",
         head="Pakistan's first astronaut rides to Tiangong",
         deck=("Zeeshan Ali, 40, joins Tang Hongbo and Wu Yi; "
               "5–10 days aboard the station."),
         pin=(100.3, 40.9)),
    dict(num=2, place="HONIARA", kind="pact",
         head="Canberra becomes the Solomons' defence partner of choice",
         deck=("Treaty signed Wednesday; a shift from the 2022 "
               "security deal with China."),
         pin=(159.97, -9.65)),
    dict(num=3, place="SAN FRANCISCO", kind="tide",
         head="Bay braces for near-record king tides",
         deck=("Wednesday's high tide may hit 8.5 ft, near the 1983 "
               "record; flood warning to Thursday."),
         pin=(-122.4, 37.8)),
]

GRID = [
    dict(num=4, place="SHANGHAI", kind="gavel",
         head="Shanghai party pledges loyalty to Beijing",
         deck="After the Chen Jining probe.",
         pin=(121.5, 31.2)),
    dict(num=5, place="WASHINGTON", kind="money",
         head="US weighs new duties on 16 partners",
         deck="Section 301 probe on excess capacity.",
         pin=(-77.0, 38.9)),
    dict(num=6, place="SEOUL", kind="chart",
         head="Kospi sinks 4.6%, breaker trips",
         deck="Samsung −6.7%, SK hynix −6.6%.",
         pin=(127.0, 37.5)),
    dict(num=7, place="TOKYO", kind="chart",
         head="Nikkei slides 2.4% in early trade",
         deck="Follows Wall Street's Tuesday retreat.",
         pin=(139.7, 35.7)),
    dict(num=8, place="BRUSSELS", kind="flag",
         head="EU Parliament debates €1.58tn budget plan",
         deck="MEPs may reject it; summit Thu.",
         pin=(4.35, 50.85)),
    dict(num=9, place="WASHINGTON", kind="capitol",
         head="Trump pardons the Thanksgiving turkeys",
         deck="White House ceremony, eve of holiday.",
         pin=(-77.0, 38.9)),
    dict(num=10, place="NEW YORK", kind="money",
         head="Shein to pay $100m to settle FTC claims",
         deck="FTC alleged deceptive practices.",
         pin=(-74.0, 40.7)),
    dict(num=11, place="WASHINGTON", kind="capitol",
         head="CDC director draws doubts from staff, lawmakers",
         deck="Staff and lawmakers question the chief.",
         pin=(-77.0, 38.9)),
    dict(num=12, place="WASHINGTON", kind="shield",
         head="Soldier admits selling secrets to China",
         deck="Pleads guilty over military data.",
         pin=(-77.0, 38.9)),
    dict(num=13, place="WASHINGTON", kind="gavel",
         head="Fort Hood survivors lose execution bid",
         deck="Court bars them from the execution.",
         pin=(-77.0, 38.9)),
    dict(num=14, place="LONDON", kind="shield",
         head="Two held over burglary at William's home",
         deck="Arrests after a suspected break-in.",
         pin=(-0.13, 51.5)),
    dict(num=15, place="KUALA LUMPUR", kind="flag",
         head="Malaysia to repatriate Myanmar migrants",
         deck="More returns announced on Wednesday.",
         pin=(101.7, 3.1)),
    dict(num=16, place="WASHINGTON", kind="ballot",
         head="Democrats turn sights to 2028",
         deck="After the midterm triumph.",
         pin=(-77.0, 38.9)),
    dict(num=17, place="MUMBAI", kind="chart",
         head="India markets reopen; GIFT Nifty points up",
         deck="Sensex resumes after the holiday.",
         pin=(72.9, 19.1)),
    dict(num=18, place="GENEVA", kind="chess",
         head="Gukesh takes White in chess game 2 today",
         deck="Game 1 drawn in 38 moves on Tuesday.",
         pin=(6.14, 46.2)),
    dict(num=19, place="NEW YORK", kind="chart",
         head="Gold slips as traders await US inflation",
         deck="$3,544.54; data due 13:30 GMT.",
         pin=(-74.0, 40.7)),
    dict(num=20, place="LONDON", kind="oil",
         head="Oil steadies on Wednesday morning",
         deck="Brent $91.16, WTI $81.81.",
         pin=(-0.13, 51.5)),
    dict(num=21, place="NEW YORK", kind="money",
         head="Bitcoin $59,702, down 2.6%",
         deck="Crypto slides with the tech retreat.",
         pin=(-74.0, 40.7)),
    dict(num=22, place="WASHINGTON", kind="chart",
         head="PCE inflation + Q3 GDP due 13:30 GMT",
         deck="Dec rate hike priced at 96.4%.",
         pin=(-77.0, 38.9)),
]

ALSO = [
    (23, "CANBERRA", "Australia October inflation due today"),
    (24, "LONDON", "BoE's Bailey faces MPs today"),
    (25, "BERLIN", "German Q3 GDP detail due 07:00 GMT"),
    (26, "WASHINGTON", "Treasury sells $44bn of 7-year notes"),
    (27, "WASHINGTON", "New home sales (Oct) due 15:00 GMT"),
    (28, "WASHINGTON", "Jobless claims (w/e 21 Nov) due 13:30 GMT"),
    (29, "NEW YORK", "Dow +0.9% Tue; S&P −0.5%; Nasdaq −1.5%"),
    (30, "SEOUL", "Kosdaq −2.8% in early trade (Wed)"),
    (31, "MUMBAI", "Sensex shut Tue for Guru Nanak Jayanti; reopens today"),
    (32, "LONDON", "FTSE −0.13% Tue; CAC flat; DAX −1.3%"),
    (33, "HONG KONG", "Hang Seng −0.73% Tue after US blacklists Alibaba unit"),
    (34, "SHANGHAI", "Shanghai +0.27% Tue to 3,548.37"),
    (35, "TAIPEI", "Taiex +9.1% Tue; TSMC, MediaTek hit daily limits"),
    (36, "NEW YORK", "Oracle bonds slump; CDS widen sharply (Tue)"),
    (37, "WASHINGTON", "10-year Treasury yield 4.94%; 2-year 4.69% (Tue)"),
    (38, "TOKYO", "Nikkei +3.9% Tue to 58,644.63"),
]

DATE_CHECK = [
    ("Nvidia board reinstates Huang as CEO", "MON 23 NOV", "Tue: the welcome + market fade"),
    ("Nvidia slides 6% as the Huang rally fades", "TUE 24 NOV", ""),
    ("Huawei convicted on 10 of 12 counts", "TUE 24 NOV", "Sentence due 14 Sep 2027"),
    ("Katz: Iran developing chemical weapons", "TUE 24 NOV", ""),
    ("Putin: retaliation 'inevitable' over refinery strikes", "TUE 24 NOV", ""),
    ("Russian missiles hit Poland", "TUE 24 NOV", "2 missiles + a drone"),
    ("25 held hostage in Cartagena supermarket", "TUE 24 NOV", "5 elderly women freed"),
    ("Hanoi blast kills 6, injures 10+", "TUE 24 NOV", ""),
    ("UN: 5 women killed each hour by relatives", "TUE 24 NOV", "47,000 in 2025"),
    ("World chess game 1: Gukesh–Sindarov draw", "TUE 24 NOV", "38 moves, 0.5–0.5"),
]

NUMBERS = [
    ("3", "CREW ABOARD SHENZHOU-24"),
    ("40", "ALI, 1ST PAKISTANI IN ORBIT"),
    ("−4.6%", "KOSPI, WEDNESDAY MORNING"),
    ("8.5 FT", "SF BAY TIDE, NEAR 1983 RECORD"),
    ("$100M", "SHEIN'S FTC SETTLEMENT"),
    ("96.4%", "DEC FED HIKE ODDS PRICED"),
]

TIMELINE = [
    ("00:09 GMT", "Kospi breaker trips as index sinks 4.6%"),
    ("00:18 GMT", "Shenzhou-24 lifts off from Jiuquan"),
    ("00:51 GMT", "Nikkei −2.4% in early Tokyo trade"),
    ("07:00 GMT", "German Q3 GDP detail due"),
    ("13:30 GMT", "US PCE inflation + Q3 GDP due"),
    ("14:00 GMT", "Gukesh has White in chess game 2"),
]

MARKETS = [
    ("KOSPI", "−4.6%", "4,777.46", "WED AM"),
    ("NIKKEI", "−2.4%", "57,265.26", "WED AM"),
    ("GOLD", "−0.3%", "$3,544.54", "WED"),
    ("BITCOIN", "−2.6%", "$59,702", "WED"),
    ("S&P 500", "−0.5%", "7,201.68", "TUE"),
    ("NASDAQ", "−1.5%", "23,733.54", "TUE"),
]

REGIONS = [
    ("ASIA-PACIFIC", 14),
    ("AMERICAS", 15),
    ("EUROPE", 7),
]


# ---- drawn art ----------------------------------------------------------
# All scenes are simple PIL geometry: no photos, no external images.

def hero_rocket(d, x, y, w, h):
    """Jiuquan: night launch, Long March-2F climbing past the stars."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 14, 32))
    for sx, sy, sr in [(24, 18, 2), (70, 36, 1), (120, 14, 2), (170, 40, 1),
                        (220, 20, 2), (270, 46, 1), (300, 16, 1), (48, 62, 1),
                        (150, 66, 1), (250, 70, 1)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(255, 255, 255))
    # launch pad and tower
    d.rectangle([x + 18, y + h - 30, x + w - 18, y + h], fill=(40, 44, 54))
    d.rectangle([x + w * 0.62, y + 26, x + w * 0.62 + 6, y + h - 30],
                fill=(90, 96, 110))
    d.line([x + w * 0.62 + 3, y + 26, x + w * 0.62 + 3, y + h - 30],
           fill=(150, 150, 160), width=1)
    # rocket body, nose and fins
    cx = x + w * 0.42
    top = y + 8
    d.polygon([(cx, top), (cx - 11, top + 16), (cx + 11, top + 16)],
              fill=RED)
    d.rectangle([cx - 11, top + 16, cx + 11, top + 62], fill=(240, 240, 235))
    d.rectangle([cx - 11, top + 34, cx + 11, top + 42], fill=RED)
    d.polygon([(cx - 11, top + 52), (cx - 20, top + 66), (cx - 11, top + 62)],
              fill=RED)
    d.polygon([(cx + 11, top + 52), (cx + 20, top + 66), (cx + 11, top + 62)],
              fill=RED)
    # flame and smoke
    d.polygon([(cx - 8, top + 66), (cx + 8, top + 66), (cx, top + 96)],
              fill=(255, 170, 40))
    d.polygon([(cx - 4, top + 66), (cx + 4, top + 66), (cx, top + 84)],
              fill=(255, 230, 120))
    for i, r in enumerate((14, 19, 24)):
        d.ellipse([cx - r, top + 86 - i * 2, cx + r, top + 86 + 9 - i * 2],
                  fill=(200, 200, 200))
    tag = "00:18 GMT · LONG MARCH-2F"
    tw = d.textlength(tag, font=f_sans_b(12))
    d.rectangle([x + w - tw - 22, y + h - 26, x + w - 8, y + h - 4],
                fill=(10, 14, 32))
    d.text((x + w - tw - 14, y + h - 23), tag, font=f_sans_b(12),
           fill=(255, 220, 120))


def hero_pact(d, x, y, w, h):
    """Honiara: two flags over a signed treaty, seal and pen."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    # sky band
    d.rectangle([x, y, x + w, y + 44], fill=NAVY_D)
    # Australian flag, stylised: blue field, stars
    fx, fy = x + 24, y + 58
    d.rectangle([fx, fy, fx + 74, fy + 46], fill=(0, 40, 104))
    d.polygon([(fx, fy), (fx + 34, fy + 23), (fx, fy + 46)], fill=(200, 30, 40))
    for sx, sy in [(52, 12), (60, 28), (44, 34), (64, 40), (52, 22)]:
        d.ellipse([fx + sx - 2, fy + sy - 2, fx + sx + 2, fy + sy + 2],
                  fill=(255, 255, 255))
    # Solomon Islands flag, stylised: blue over green, stars
    gx, gy = x + w - 98, y + 58
    d.polygon([(gx, gy), (gx + 74, gy), (gx + 74, gy + 46)], fill=(0, 40, 104))
    d.polygon([(gx, gy), (gx, gy + 46), (gx + 74, gy + 46)], fill=(0, 110, 60))
    for sx, sy in [(56, 10), (62, 20), (50, 22), (64, 32), (54, 36)]:
        d.ellipse([gx + sx - 2, gy + sy - 2, gx + sx + 2, gy + sy + 2],
                  fill=(255, 220, 60))
    # treaty document with seal
    dx, dy = x + w // 2 - 52, y + 52
    d.rectangle([dx, dy, dx + 104, dy + 52], fill=(255, 255, 255),
                outline=INK, width=2)
    for i in range(3):
        d.line([dx + 10, dy + 12 + i * 9, dx + 94, dy + 12 + i * 9],
               fill=(120, 120, 120), width=1)
    d.ellipse([dx + 74, dy + 30, dx + 96, dy + 50], fill=RED,
              outline=GOLD, width=2)
    d.text((dx + 10, dy + 36), "SIGNED", font=f_sans_b(10), fill=NAVY)
    d.text((x + 12, y + 12), "DEFENCE PARTNER OF CHOICE",
           font=f_sans_b(13), fill=(255, 255, 255))


def hero_tide(d, x, y, w, h):
    """San Francisco Bay: king tide waves under a bridge tower."""
    d.rectangle([x, y, x + w, y + h], fill=(206, 224, 238))
    # grey sky, full moon
    d.ellipse([x + w - 64, y + 12, x + w - 24, y + 52], fill=(240, 238, 220))
    d.ellipse([x + w - 58, y + 18, x + w - 30, y + 46], fill=(225, 222, 200))
    # bridge tower
    bx = x + w * 0.68
    d.rectangle([bx - 5, y + 18, bx + 5, y + h * 0.55], fill=(176, 60, 40))
    d.rectangle([bx - 34, y + 30, bx + 34, y + 38], fill=(176, 60, 40))
    d.line([bx - 5, y + 18, x + 10, y + h * 0.55], fill=(176, 60, 40), width=2)
    d.line([bx + 5, y + 18, x + w - 10, y + h * 0.55], fill=(176, 60, 40),
           width=2)
    # rising water, three wave crests
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=SEA)
    for k, yy in enumerate((0.60, 0.72, 0.85)):
        y0 = y + h * yy
        pts = []
        for i in range(0, w + 1, 8):
            pts.append((x + i, y0 + 5 * math.sin(i / 22.0 + k * 1.7)))
        d.line(pts, fill=(200, 225, 240), width=3)
    d.rectangle([x + 10, y + 10, x + 92, y + 32], fill=RED)
    d.text((x + 16, y + 14), "8.5 FT TIDE", font=f_sans_b(12),
           fill=(255, 255, 255))


HERO_SCENES = {"rocket": hero_rocket, "pact": hero_pact, "tide": hero_tide}


def thumb(d, x, y, w, h, kind):
    """A small drawn icon for a grid card, on a tinted tile."""
    tints = {"rocket": (12, 16, 34), "pact": (226, 232, 240),
             "tide": (206, 224, 238), "chart": (222, 236, 222),
             "gavel": (232, 228, 216), "money": (222, 238, 222),
             "flag": (238, 226, 226), "capitol": (226, 230, 240),
             "shield": (226, 230, 240), "ballot": (232, 228, 240),
             "chess": (236, 232, 222), "oil": (240, 232, 214)}
    d.rectangle([x, y, x + w, y + h], fill=tints.get(kind, GREY_BG))
    cx, cy = x + w // 2, y + h // 2
    if kind == "chart":
        d.line([(x + 6, y + h - 10), (x + 16, y + h - 22), (x + 26, y + 16),
                (x + 38, y + 10)], fill=GREEN, width=3, joint="curve")
        d.polygon([(x + 32, y + 8), (x + 40, y + 8), (x + 36, y + 16)],
                  fill=GREEN)
    elif kind == "gavel":
        d.rectangle([cx - 14, cy - 8, cx + 14, cy - 2], fill=(120, 84, 40))
        d.rectangle([cx - 3, cy - 2, cx + 3, cy + 12], fill=(120, 84, 40))
        d.rectangle([cx - 12, cy + 12, cx + 12, cy + 16], fill=(90, 64, 30))
    elif kind == "money":
        d.rectangle([cx - 15, cy - 9, cx + 15, cy + 9], fill=(120, 180, 120),
                    outline=GREEN, width=2)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(240, 240, 220))
        d.text((cx - 3, cy - 7), "$", font=f_sans_b(11), fill=GREEN)
    elif kind == "flag":
        d.rectangle([cx - 10, cy - 14, cx - 8, cy + 14], fill=INK)
        d.polygon([(cx - 8, cy - 14), (cx + 12, cy - 9), (cx - 8, cy - 4)],
                  fill=RED)
    elif kind == "capitol":
        d.polygon([(cx - 12, cy + 12), (cx, cy - 12), (cx + 12, cy + 12)],
                  fill=(200, 200, 200), outline=INK, width=1)
        d.rectangle([cx - 14, cy + 12, cx + 14, cy + 16], fill=INK)
        d.ellipse([cx - 6, cy - 12, cx + 6, cy - 4], fill=(200, 200, 200),
                  outline=INK, width=1)
    elif kind == "shield":
        d.polygon([(cx, cy - 13), (cx + 11, cy - 8), (cx + 11, cy + 2),
                   (cx, cy + 14), (cx - 11, cy + 2), (cx - 11, cy - 8)],
                  fill=NAVY)
        d.text((cx - 4, cy - 6), "!", font=f_sans_b(13), fill=(255, 255, 255))
    elif kind == "ballot":
        d.rectangle([cx - 12, cy - 10, cx + 12, cy + 12], fill=(250, 250, 250),
                    outline=INK, width=2)
        d.line([cx - 8, cy + 2, cx - 2, cy + 8], fill=RED, width=3)
        d.line([cx - 2, cy + 8, cx + 9, cy - 6], fill=RED, width=3)
    elif kind == "chess":
        d.rectangle([cx - 12, cy - 12, cx + 12, cy + 12], fill=(250, 250, 250),
                    outline=INK, width=2)
        d.line([cx, cy - 12, cx, cy + 12], fill=INK, width=1)
        d.line([cx - 12, cy, cx + 12, cy], fill=INK, width=1)
        d.ellipse([cx - 9, cy - 9, cx - 3, cy - 3], fill=INK)
        d.ellipse([cx + 3, cy + 3, cx + 9, cy + 9], fill=INK)
    elif kind == "oil":
        d.polygon([(cx, cy - 14), (cx + 9, cy + 2), (cx + 6, cy + 12),
                   (cx - 6, cy + 12), (cx - 9, cy + 2)], fill=(40, 40, 40))
        d.ellipse([cx - 4, cy + 2, cx + 4, cy + 10], fill=(240, 240, 220))
    elif kind == "rocket":
        d.polygon([(cx, cy - 14), (cx - 6, cy - 4), (cx + 6, cy - 4)],
                  fill=RED)
        d.rectangle([cx - 6, cy - 4, cx + 6, cy + 10], fill=(240, 240, 235),
                    outline=INK, width=1)
        d.polygon([(cx - 5, cy + 10), (cx, cy + 17), (cx + 5, cy + 10)],
                  fill=(255, 170, 40))
    elif kind == "pact":
        d.rectangle([cx - 13, cy - 10, cx + 13, cy + 10], fill=(255, 255, 255),
                    outline=INK, width=2)
        for i in range(3):
            d.line([cx - 9, cy - 5 + i * 6, cx + 9, cy - 5 + i * 6],
                   fill=(120, 120, 120), width=1)
        d.ellipse([cx + 3, cy + 1, cx + 11, cy + 9], fill=RED)
    elif kind == "tide":
        for k, yy in enumerate((-6, 0, 6)):
            pts = [(x + 4 + i * 4, cy + yy + 3 * math.sin(i / 1.6 + k))
                   for i in range(10)]
            d.line(pts, fill=SEA, width=2)


# ---- simplified world map ----------------------------------------------
# Rough continent polygons (lon, lat) — recognisable, not precise.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-75, 58), (-70, 45), (-75, 35), (-80, 26), (-85, 29),
     (-90, 21), (-97, 16), (-105, 20), (-115, 29), (-125, 40), (-125, 49),
     (-140, 60), (-155, 58), (-165, 60)],
    # South America
    [(-80, 10), (-75, 5), (-60, 5), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-70, -55), (-73, -40),
     (-72, -20), (-80, -5)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (2, 51), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 59), (28, 60), (30, 65), (32, 70),
     (40, 68), (45, 60), (40, 52), (35, 46), (30, 46), (28, 44), (23, 40),
     (19, 42), (12, 44), (8, 44), (3, 42), (0, 39)],
    # Africa
    [(-6, 35), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12), (51, 11),
     (48, 0), (40, -10), (35, -20), (32, -29), (26, -34), (19, -35),
     (15, -27), (12, -18), (9, -1), (-8, 4), (-16, 12), (-17, 20), (-15, 30)],
    # Asia
    [(40, 68), (50, 70), (60, 72), (70, 73), (80, 73), (90, 75), (105, 77),
     (120, 73), (135, 72), (150, 70), (160, 66), (170, 66), (178, 65),
     (170, 60), (162, 56), (158, 52), (150, 59), (142, 50), (140, 40),
     (135, 35), (130, 33), (127, 40), (122, 38), (120, 30), (115, 22),
     (110, 20), (108, 12), (105, 9), (100, 7), (98, 10), (95, 16), (92, 21),
     (89, 22), (86, 20), (80, 13), (77, 8), (74, 20), (70, 23), (66, 25),
     (61, 25), (57, 26), (52, 28), (50, 30), (48, 29), (44, 30), (40, 36),
     (36, 36), (35, 42), (40, 46), (42, 52), (45, 60)],
    # Australia
    [(114, -22), (122, -14), (130, -12), (136, -12), (142, -11), (146, -19),
     (150, -23), (153, -27), (150, -37), (140, -38), (135, -35), (129, -32),
     (124, -33), (118, -35), (114, -32)],
]


def lonlat_to_xy(lon, lat, x0, y0, x1, y1):
    x = x0 + (lon + 170.0) / 360.0 * (x1 - x0)
    y = y0 + (85.0 - lat) / 140.0 * (y1 - y0)
    return x, y


def draw_map(d, x0, y0, x1, y1, pins):
    """Ocean, continents, numbered pins for heroes + grid stories."""
    d.rectangle([x0, y0, x1, y1], fill=(206, 224, 238))
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, x0, y0, x1, y1) for lon, lat in poly]
        d.polygon(pts, fill=(226, 216, 188), outline=(150, 140, 110))
    for lon in range(-150, 181, 30):
        gx, _ = lonlat_to_xy(lon, 0, x0, y0, x1, y1)
        d.line([gx, y0, gx, y1], fill=(190, 210, 228), width=1)
    # pins, with a declutter pass: try offsets in order, take the first
    # spot at least 17 px from every pin already placed.
    placed = []
    offsets = [(0, 0), (17, -9), (-17, -9), (17, 9), (-17, 9), (0, -18),
               (0, 18), (26, 0), (-26, 0), (26, -18), (-26, -18)]
    for num, lon, lat in pins:
        px, py = lonlat_to_xy(lon, lat, x0, y0, x1, y1)
        ox, oy = 0, 0
        for cand in offsets:
            cx, cy = px + cand[0], py + cand[1]
            if all((cx - qx) ** 2 + (cy - qy) ** 2 >= 17 ** 2
                   for (qx, qy) in placed):
                ox, oy = cand
                break
        else:
            ox, oy = offsets[-1]
        placed.append((px + ox, py + oy))
        if ox or oy:
            d.line([px, py, px + ox, py + oy], fill=RED, width=1)
        cx, cy = px + ox, py + oy
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=2)
        lbl = str(num)
        tw = d.textlength(lbl, font=f_sans_b(9))
        d.text((cx - tw / 2, cy - 6), lbl, font=f_sans_b(9), fill=(255, 255, 255))


# ---- layout -------------------------------------------------------------
MARGIN = 12


def draw_masthead(d):
    d.text((MARGIN, 8), "MORNING EDITION", font=f_sans_b(12), fill=RED)
    right = "WEDNESDAY 25 NOVEMBER 2026"
    tw = d.textlength(right, font=f_sans_b(12))
    d.text((W - MARGIN - tw, 8), right, font=f_sans_b(12), fill=INK)
    title = "THE WEDNESDAY LEDGER"
    tf = f_serif(46)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 24), title, font=tf, fill=INK)
    d.line([MARGIN, 86, W - MARGIN, 86], fill=INK, width=3)
    d.line([MARGIN, 90, W - MARGIN, 90], fill=INK, width=1)
    sub = "THE WORLD IN ONE DAY  —  38 STORIES, EVERY ONE VERIFIED AGAINST WEDNESDAY'S REPORTING"
    sf = f_sans_b(11)
    tw = d.textlength(sub, font=sf)
    d.text(((W - tw) / 2, 96), sub, font=sf, fill=NAVY)


def draw_numbers(d):
    y0, y1 = 112, 148
    d.rectangle([MARGIN, y0, W - MARGIN, y1], fill=CARD)
    d.rectangle([MARGIN, y0, W - MARGIN, y1], outline=RULE, width=1)
    cw = (W - 2 * MARGIN) / 6
    for i, (num, label) in enumerate(NUMBERS):
        x = MARGIN + i * cw
        nf = f_serif(21)
        tw = d.textlength(num, font=nf)
        d.text((x + (cw - tw) / 2, y0 + 3), num, font=nf, fill=RED)
        lf = f_sans_b(8)
        tw = d.textlength(label, font=lf)
        d.text((x + (cw - tw) / 2, y0 + 26), label, font=lf, fill=MUTED)
        if i:
            d.line([x, y0 + 5, x, y1 - 5], fill=RULE, width=1)


def draw_timeline(d):
    y0 = 152
    d.text((MARGIN, y0), "THE DAY IN UTC", font=f_sans_b(10), fill=RED)
    col_w = (W - 2 * MARGIN - 130) / 3
    x0 = MARGIN + 130
    for i, (t, txt) in enumerate(TIMELINE):
        col, row = i % 3, i // 3
        x = x0 + col * col_w
        y = y0 + row * 13
        d.text((x, y), t, font=f_sans_b(10), fill=NAVY)
        tw = d.textlength(t + " ", font=f_sans_b(10))
        lines = fit_lines(d, txt, f_sans(10), col_w - tw - 6, 1)
        d.text((x + tw, y), lines[0] if lines else "", font=f_sans(10), fill=INK)


def draw_hero(d, story, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD)
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    HERO_SCENES[story["kind"]](d, x + 1, y + 1, w - 2, 104)
    ty = y + 110
    d.text((x + 8, ty), "%d · %s" % (story["num"], story["place"]),
           font=f_sans_b(11), fill=RED)
    lines = fit_lines(d, story["head"], f_sans_b(16), w - 16, 2)
    ty = text_block(d, x + 8, ty + 16, lines, f_sans_b(16), leading=19)
    dlines = fit_lines(d, story["deck"], f_sans(11), w - 16, 2)
    text_block(d, x + 8, ty + 3, dlines, f_sans(11), fill=MUTED, leading=13)


def draw_grid_card(d, story, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG)
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    thumb(d, x + 4, y + 4, 44, h - 8, story["kind"])
    tx = x + 52
    tw = w - 56
    d.text((tx, y + 3), "%d · %s" % (story["num"], story["place"]),
           font=f_sans_b(9), fill=RED)
    lines = fit_lines(d, story["head"], f_sans_b(10), tw, 2)
    text_block(d, tx, y + 14, lines, f_sans_b(10), leading=11)
    dlines = fit_lines(d, story["deck"], f_sans(9), tw, 1)
    if dlines:
        d.text((tx, y + h - 13), dlines[0], font=f_sans(9), fill=MUTED)


def draw_legend_cell(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY_D)
    lines = ["HOW TO READ",
             "1–22 pinned on the map.",
             "ALSO lists 16 more.",
             "DATE CHECK holds stories",
             "from earlier days."]
    yy = y + 5
    for i, ln in enumerate(lines):
        f = f_sans_b(9) if i == 0 else f_sans(9)
        d.text((x + 8, yy), ln, font=f, fill=(255, 255, 255))
        yy += 9 if i else 11


def draw_map_section(d):
    y0 = 650
    d.text((MARGIN, y0), "THE WORLD ON WEDNESDAY — 22 STORIES PINNED",
           font=f_sans_b(12), fill=INK)
    map_x0, map_y0, map_x1, map_y1 = MARGIN, y0 + 16, 756, 782
    pins = [(s["num"], s["pin"][0], s["pin"][1]) for s in HEROES + GRID]
    draw_map(d, map_x0, map_y0, map_x1, map_y1, pins)
    px0, py0, px1, py1 = 768, y0 + 16, W - MARGIN, 782
    d.rectangle([px0, py0, px1, py1], fill=CARD)
    d.rectangle([px0, py0, px1, py1], outline=RULE, width=1)
    d.text((px0 + 10, py0 + 6), "WHERE THE NEWS WAS", font=f_sans_b(11), fill=INK)
    yy = py0 + 26
    for name, count in REGIONS:
        d.text((px0 + 10, yy), name, font=f_sans_b(10), fill=INK)
        bw = (px1 - px0 - 118 - 30) * count / 15.0
        d.rectangle([px0 + 118, yy + 2, px0 + 118 + bw, yy + 10], fill=NAVY)
        d.text((px1 - 24, yy), str(count), font=f_sans_b(11), fill=RED)
        yy += 17
    d.text((px0 + 10, py0 + 78),
           "No Middle East or Africa story was",
           font=f_sans(9), fill=MUTED)
    d.text((px0 + 10, py0 + 89),
           "verified for Wednesday by press",
           font=f_sans(9), fill=MUTED)
    d.text((px0 + 10, py0 + 100),
           "time — see DATE CHECK for Tuesday's.",
           font=f_sans(9), fill=MUTED)


def draw_also(d):
    y0 = 784
    d.text((MARGIN, y0), "ALSO ON WEDNESDAY", font=f_sans_b(12), fill=INK)
    d.line([MARGIN + 170, y0 + 8, W - MARGIN, y0 + 8], fill=RULE, width=1)
    col_w = (W - 2 * MARGIN) / 2
    for i, (num, place, txt) in enumerate(ALSO):
        col, row = i % 2, i // 2
        x = MARGIN + col * col_w
        y = y0 + 14 + row * 12
        head = "%d · %s — " % (num, place)
        hw = d.textlength(head, font=f_sans_b(10))
        d.text((x, y), head, font=f_sans_b(10), fill=NAVY)
        lines = fit_lines(d, txt, f_sans(10), col_w - hw - 4, 1)
        d.text((x + hw, y), lines[0] if lines else "", font=f_sans(10), fill=INK)


def draw_date_check(d):
    y0 = 894
    d.text((MARGIN, y0), "DATE CHECK — NOT WEDNESDAY, KEPT OUT OF THE COUNT",
           font=f_sans_b(11), fill=RED)
    col_w = (W - 2 * MARGIN) / 2
    for i, (txt, when, note) in enumerate(DATE_CHECK):
        col, row = i % 2, i // 2
        x = MARGIN + col * col_w
        y = y0 + 12 + row * 11
        s = "%s — %s" % (txt, when)
        if note:
            s += " · " + note
        lines = fit_lines(d, s, f_sans(8), col_w - 4, 1)
        d.text((x, y), lines[0] if lines else "", font=f_sans(8), fill=MUTED)


def draw_markets(d):
    y0 = 964
    d.rectangle([MARGIN, y0, W - MARGIN, H - 6], fill=NAVY_D)
    d.text((MARGIN + 8, y0 + 4),
           "MARKETS — WEDNESDAY MORNING IN ASIA, TUESDAY CLOSES IN NEW YORK",
           font=f_sans_b(10), fill=(255, 220, 120))
    cw = (W - 2 * MARGIN - 16) / 6
    for i, (name, chg, val, day) in enumerate(MARKETS):
        x = MARGIN + 8 + i * cw
        d.text((x, y0 + 18), "%s — %s" % (name, day), font=f_sans_b(9),
               fill=(200, 210, 230))
        d.text((x, y0 + 30), "%s  %s" % (chg, val), font=f_sans_b(11),
               fill=(255, 255, 255))
    foot = ("Dow +0.9% Tue to 50,021.91  ·  Brent $91.16  ·  WTI $81.81  ·  "
            "Sources: Reuters, AP, AFP, Yonhap, SCMP, Hindu BusinessLine")
    d.text((MARGIN + 8, y0 + 46), foot, font=f_sans(8), fill=(180, 190, 210))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_numbers(d)
    draw_timeline(d)
    # heroes: 3 panels, y 180–376
    hw = (W - 2 * MARGIN - 2 * 10) // 3
    for i, story in enumerate(HEROES):
        draw_hero(d, story, MARGIN + i * (hw + 10), 180, hw, 196)
    gw = (W - 2 * MARGIN - 3 * 8) // 4
    for i, story in enumerate(GRID):
        row, col = divmod(i, 4)
        draw_grid_card(d, story, MARGIN + col * (gw + 8), 380 + row * 54,
                       gw, 52)
    draw_legend_cell(d, MARGIN + 3 * (gw + 8), 380 + 4 * 54, gw, 52)
    draw_map_section(d)
    draw_also(d)
    draw_date_check(d)
    draw_markets(d)
    return img


def main():
    img = build()
    img.save(OUT, format="PNG", optimize=True)
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
